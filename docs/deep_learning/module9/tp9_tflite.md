# TP Module 9 : Optimisation des modèles, TensorFlow Lite

## Import des librairies, création du dataset

Importons d'abord les librairies qui nous serons nécessaires.

!!! tf "TensorFlow"

    ```python
    from tensorflow import keras
    from tensorflow.keras.models import load_model

    from typing import List, Tuple

    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from loguru import logger
    import os
    import random
    import datetime
    import time
    from PIL import Image

    # freeze de l'aléatoire, pour avoir des expériences reproductibles.
    RANDOM_SEED = 42

    os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'
    tf.random.set_seed(RANDOM_SEED)
    ```


Comme nous aurons besoin de créer de nouveaux des datasets pour l'entrainement, décrivons une classe qui nous permettra de le faire.

!!! tf "Tensorize"

    ```python
    class Tensorize(object):
        """Class used to create tensor datasets for TensorFlow.

        Args:
            object (object): The base class of the class hierarchy, used only to enforce
                WPS306. See https://wemake-python-stylegui.de/en/latest/pages/usage/
                violations/consistency.html#consistency.
        """

        def __init__(
            self, n_classes: int, img_shape: Tuple[int, int, int], random_seed: int
        ) -> None:
            """Initialization of the class Featurize.

            Initialize the class the number of classes in the datasets, the shape of the
            images and the random seed.

            Args:
                n_classes (int): Number of classes in the dataset.
                img_shape (Tuple[int, int, int]): Dimension of the image, format is (H,W,C).
                random_seed (int): Fixed random seed for reproducibility.
            """
            self.n_classes = n_classes
            self.img_shape = img_shape
            self.random_seed = random_seed
            self.AUTOTUNE = tf.data.experimental.AUTOTUNE

        def load_images(self, data_frame: pd.DataFrame, column_name: str) -> List[str]:
            """Load the images as a list.

            Take the dataframe containing the observations and the labels and the return the
            column containing the observations as a list.

            Args:
                data_frame (pd.DataFrame): Dataframe containing the dataset.
                column_name (str): The name of the column containing the observations.

            Returns:
                The list of observations deduced from the dataframe.
            """
            return data_frame[column_name].tolist()

        def load_labels(self, data_frame: pd.DataFrame, column_name: str) -> List[int]:
            """Load the labels as a list and encode them.

            Take the dataframe containing the observations and the labels and the return the
            column containing the labels as an encoded list.

            The encoding is done by taking the set of labels, alphabetically sorted, and
            then transforming them as integers starting from 0.

            `from sklearn.preprocessing import LabelEncoder` works well to encode labels,
            but if the dataset is huge, the time it takes to encode all the labels is
            growing fast. We use anumpy and vectorization to speed up the time.

            See the StackOverflow question :
            [Question](https://stackoverflow.com/questions/45321999/
            how-can-i-optimize-label-encoding-for-large-data-sets-sci-kit-learn)

            Args:
                data_frame (pd.DataFrame): Dataframe containing the dataset.
                column_name (str): The name of the column containing the labels.

            Returns:
                The list of encoded labels deduced from the dataframe.
            """
            label_list = data_frame[column_name].tolist()
            classes = sorted(set(label_list))
            logger.info(f"Found following labels {classes}")

            labels = np.unique(label_list, return_inverse=True)[1]
            dic = dict(zip(label_list, labels))
            logger.info(f"Dictionnary creation {dic}")
            vectorized_get = np.vectorize(dic.get)

            return vectorized_get(label_list)

        def parse_image_and_label(
            self, filename: str, label: int
        ) -> Tuple[np.ndarray, int]:
            """Transform image and label.

            Parse image to go from path to a resized np.ndarray, and parse the labels to
            one-hot encode them.

            Args:
                filename (str): The path of the image to parse.
                label (int): The label of the image, as an int, to one-hot encode.

            Returns:
                A np.ndarray corresponding to the image and the corresponding one-hot label.
            """
            resized_dims = [self.img_shape[0], self.img_shape[1]]
            # convert the label to one-hot encoding
            label = tf.one_hot(label, self.n_classes)
            # decode image
            image = tf.io.read_file(filename)
            # Don't use tf.image.decode_image,
            # or the output shape will be undefined
            image = tf.image.decode_jpeg(image)
            # This will convert to float values in [0, 1]
            image = tf.image.convert_image_dtype(image, tf.float32)
            image = tf.image.resize(image, resized_dims)

            return image, label

        def train_preprocess(
            self, image: np.ndarray, label: List[int]
        ) -> Tuple[np.ndarray, List[int]]:
            """Augmentation preprocess, if needed.

            Args:
                image (np.ndarray): The image to augment.
                label (List[int]): The corresponding label.

            Returns:
                The augmented pair.
            """
            image = tf.image.random_flip_left_right(image)
            image = tf.image.random_flip_up_down(image)

            return image, label

        def create_dataset(
            self,
            data_path: str,
            batch: int,
            repet: int,
            prefetch: int,
            augment: bool,
        ) -> tf.data.Dataset:
            """Creation of a tensor dataset for TensorFlow.

            Args:
                data_path (str): Path where the csv file containing the dataframe is
                    located.
                batch (int): Batch size, usually 32.
                repet (int): How many times the dataset has to be repeated.
                prefetch (int): How many batch the CPU has to prepare in advance for the
                    GPU.
                augment (bool): Does the dataset has to be augmented or no.

            Returns:
                A batch of observations and labels.
            """
            df = pd.read_csv(data_path)
            features = self.load_images(data_frame=df, column_name="filename")
            labels = self.load_labels(data_frame=df, column_name="label")

            dataset = tf.data.Dataset.from_tensor_slices((features, labels))
            dataset = dataset.shuffle(len(features), seed=self.random_seed)
            dataset = dataset.repeat(repet)
            dataset = dataset.map(
                self.parse_image_and_label, num_parallel_calls=self.AUTOTUNE
            )
            if augment:
                dataset = dataset.map(
                    self.train_preprocess, num_parallel_calls=self.AUTOTUNE
                )
            dataset = dataset.batch(batch)
            dataset = dataset.cache()
            return dataset.prefetch(prefetch)
    ```

et créons nos 3 datasets classiques.

!!! warning "Attention"

    Bien vérifier sur où pointent les adresses dans les csv.

!!! tf "ds, ds_val, ds_train"

    ```python
    ts = Tensorize(
                n_classes=2,
                img_shape=[224,224,3],
                random_seed=42,
            )

    ds = ts.create_dataset(
        "prepared_dataset/train.csv",
        32,
        1,
        1,
        True,
    )

    ds_val = ts.create_dataset(
        "prepared_dataset/val.csv",
        32,
        1,
        1,
        True,
    )

    ds_test = ts.create_dataset(
        "prepared_dataset/test.csv",
        32,
        1,
        1,
        True,
    )
    ```

Chargeons maintenant notre modèle que nous allons quantifier.

!!! tf "Chargement du modèle"

    ```python
    model_pruned = load_model("../pruned_model_polydecay.h5")
    model_pruned.evaluate(ds_test)
    ```
## TensorFlow Lite, quantification

TensorFlow Lite est un ensemble d'outils permettant de faire tourner des modèles TensorFlow sur de "l'embarqué", ie du smartphone au microcontrôleur.

TensorFlow Lite possède deux composantes principales :

  - TensorFlow Lite Converter, qui convertit les modèles en un format spécifique, un `FlatBuffer`, optimisé pour les déploiements dans les enrionnements contraints en terme de mémoire. Il applique aussi des techniques d'optimisations pour réduire encore la taille du modèle et accélérer sa vitesse d'inférence.
  - TensorFlow Lite Interpreter, qui permet de faire tourner les modèles convertis.

Une des optimisations là plus utilisée est la quantification.

En général, nos modèles fonctionnent en format de précision float32. Tous les paramètres du modèle sont stockés dans ce format de précision, ce qui conduit souvent à des modèles plus lourds. La lourdeur d'un modèle est en corrélation directe avec la vitesse à laquelle le modèle fait des prédictions. Ainsi, il pourrait vous venir naturellement à l'esprit que si nous pouvions réduire la précision dans laquelle nos modèles fonctionnent, nous pourrions réduire les temps de prédiction. C'est ce que fait la quantification - elle réduit la précision à des formes plus basses comme float16, int8, etc. pour représenter les paramètres d'un modèle.

La quantification peut être appliquée à un modèle sous deux formes

- **La quantification post-entraînement** est appliquée à un modèle après sa formation.

- **Entraînement conscient de la quantification** (Quantization Aware Training): un modèle est généralement entraîné pour compenser la perte de précision qui pourrait être introduite en raison de la quantification. Lorsque vous réduisez la précision des paramètres de votre modèle, il peut en résulter une perte d'informations et vous pourriez constater une certaine réduction de la précision de votre modèle. Dans ces situations, une formation tenant compte de la quantification peut être très utile.

Pour installer uniquement l'interpréteur, ce que l'on fait en pratique sur la carte dédiée à l'inférence, soyez sûr de choisir le bon interpréteur en vérifiant sur [la page suivante](https://www.tensorflow.org/lite/guide/python#run_an_inference_using_tflite_runtime).

```python
!pip3 install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp36-cp36m-linux_x86_64.whl

# Load the model into interpreters
import tflite_runtime.interpreter as tflite
```

### Définition de fonction utiles

Les modèles convertis et optimisés `.tflite` ne lisent pas les datasets au format `tf.data.Dataset`, qui sont spécalisés pour l'entraînement. On va donc faire un dataset de validation de façon classique sous la forme d'un tableau.

Les modèles `.tflite` sont optimisés pour des utilisation sur CPU unique, Colab ayant été mis en mode GPU/CPU en serveur pour les besoins de l'entraînement du modèle vous pourriez être surpris de voir que le temps de validation d'un modèle `.tflite` sera ici long, environ 1 image par seconde. Cela est dû à l'optimisation pour CPU, sur un Rapsberry pi, l'inférence est de l'ordre de la milliseconde.

!!! tf "Création d'un dataset normal"

    ```python
    def images(data_frame: pd.DataFrame, column_name: str) -> List[str]:
    """Load the images as a list.

    Take the dataframe containing the observations and the labels and the return the
    column containing the observations as a list.

    Args:
        data_frame (pd.DataFrame): Dataframe containing the dataset.
        column_name (str): The name of the column containing the observations.

    Returns:
        The list of observations deduced from the dataframe.
    """
    return data_frame[column_name].tolist()

    def labels(data_frame: pd.DataFrame, column_name: str) -> List[int]:
        """Load the labels as a list and encode them.

        Take the dataframe containing the observations and the labels and the return the
        column containing the labels as an encoded list.

        The encoding is done by taking the set of labels, alphabetically sorted, and
        then transforming them as integers starting from 0.

        `from sklearn.preprocessing import LabelEncoder` works well to encode labels,
        but if the dataset is huge, the time it takes to encode all the labels is
        growing fast. We use anumpy and vectorization to speed up the time.

        See the StackOverflow question :
        [Question](https://stackoverflow.com/questions/45321999/
        how-can-i-optimize-label-encoding-for-large-data-sets-sci-kit-learn)

        Args:
            data_frame (pd.DataFrame): Dataframe containing the dataset.
            column_name (str): The name of the column containing the labels.

        Returns:
            The list of encoded labels deduced from the dataframe.
        """
        label_list = data_frame[column_name].tolist()
        classes = sorted(set(label_list))
        logger.info(f"Found following labels {classes}")

        labels = np.unique(label_list, return_inverse=True)[1]
        dic = dict(zip(label_list, labels))
        logger.info(f"Dictionnary creation {dic}")
        vectorized_get = np.vectorize(dic.get)

        return vectorized_get(label_list)

    df = pd.read_csv("prepared_dataset/val.csv")
    features = images(data_frame=df, column_name="filename")
    val_labels = labels(data_frame=df, column_name="label")

    # Empty labels for storing images and labels
    val_images = []

    for image in features:
        # load the image
        image = Image.open(image)
        image = image.resize((224,224))
        # convert image to numpy array
        image = np.asarray(image).astype(np.float32)
        image = np.expand_dims(image, 0)
        image = image / 255.

        # Append to the list
        val_images.append(image)

    # Create NumPy array
    val_images = np.array(val_images)
    ```

```python
print(f'val_images : {len(val_images)}, val_labels : {len(val_labels)}')
```

!!! tf "Fonction d'évaluation"

    ```python
    # A helper function to evaluate the TF Lite model using "test" dataset.
    # Comes from: https://www.tensorflow.org/lite/performance/post_training_integer_quant
    def evaluate_model(interpreter):

        input_index = interpreter.get_input_details()[0]["index"]
        output_index = interpreter.get_output_details()[0]["index"]

        # Run predictions on every image in the "test" dataset.
        predictions = []
        start_time = time.time()
        for val_image, val_label in zip(val_images, val_labels):
            interpreter.set_tensor(input_index, val_image)

            # Run inference.
            interpreter.invoke()

            # Post-processing: remove batch dimension and find the digit with highest
            # probability.
            probability = interpreter.get_tensor(output_index)
            mask_prob = np.argmax(probability[0])
            predictions.append(mask_prob)

        print(f'{len(predictions)}, {len(val_labels)}')
        print(f'took {time.time()-start_time} seconds, ie {len(val_images)/(time.time()-start_time)} img/s')
        accuracy = (predictions == val_labels).mean()

        return accuracy
    ```

### Quantification post-entraînement (PTQ)

Vous commencez par charger votre modèle dans une classe de convertisseur TFLiteConverter, puis vous spécifiez une politique d'optimisation, et enfin, vous demandez à TFLite de convertir votre modèle avec la politique d'optimisation.

Cette forme de quantification est également appelée **quantification post-entraînement**. Elle quantifie les poids de votre modèle avec une précision flottante de 8 bits.

!!! tf "Quantization"

    ```python
    converter = tf.lite.TFLiteConverter.from_keras_model(model_pruned)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    #converter.representative_dataset = representative_dataset
    quantized_tflite_model = converter.convert()

    f = open("tflite_model/quantize_model_pruned.tflite", "wb")
    f.write(quantized_tflite_model)
    f.close()
    ```

!!! tf "Evaluation"

    ```python
    # Load the model into interpreters
    interpreter_nor = tf.lite.Interpreter(model_path="tflite_model/quantize_model_pruned.tflite")
    interpreter_nor.allocate_tensors()

    # Evaluate the performance
    accuracy = evaluate_model(interpreter_nor)
    print(accuracy)
    ```

### Quantization Aware training (QAT)

Une bonne première approche consiste à entraîner votre modèle de manière à ce qu'il apprenne à compenser la perte d'informations qui pourrait être induite par la quantification. C'est précisément ce que nous pouvons faire avec un entraînement conscient de la quantification. Pour former notre réseau à la quantification, il suffit d'ajouter les lignes de code suivantes

!!! attention "Attention"

    Les techniques d'entraînements conscients de la quantification sont encore relativement récentes, et si cela ne pose pas trop de problèmes pour la plupart des modèles, [il est important de vérifier que les couches que l'on met le supporte](https://www.tensorflow.org/model_optimization/guide/quantization/training#general_support_matrix)

    Par exemple : *BatchNormalization when it follows Conv2D and DepthwiseConv2D layers*.

    Ce qui veut dire le modèle ResNet50 proposé par `tf.keras` supporte cet entraînement, car la brique de base est $\text{Conv-BN-ReLU}$, mais ResNet50V2, qui lui utilise l'architecture $\text{BN-ReLU-Conv}$ ne le supporte pas de façon native pour l'instant.

Pour pouvoir utiliser les méthodes de quantification durant l'entraînement, on va installer la librairie **TensorFlow Model Optimization**.

!!! tf "TFMOT"

    ```python
    !pip install -q tensorflow-model-optimization
    import tensorflow_model_optimization as tfmot
    ```

!!! tf "QAT"

    ```python
    # Let's reload the model and allow the model to be trained in a quantization-aware manner
    qat_model_pruned = tfmot.quantization.keras.quantize_model(model_pruned)
    qat_model_pruned.summary()

    # Train the model
    qat_model_pruned.compile(loss="categorical_crossentropy",
                        optimizer=tf.keras.optimizers.Adam(),
                        metrics=["accuracy"])
    start = time.time()
    history = qat_model_pruned.fit(ds_train,
                                validation_data=ds_val,
                                epochs=10)
    print("Total training time: ",time.time()-start)
    ```

!!! tf "Sauvergarde du modèle"

    ```python
    # Serializing the model and seeing the size of it
    qat_model_pruned.save("qat_model_pruned.h5")
    !ls -lh .
    ```

!!! attention "Attention"

    La QAT ajoute des couches au modèle, donc si l'on essaye de le charger naïvement, on va avoir une erreur. Il faut utilisation la méthode contextuelle avec `with` suivante.

    ```python
    with tfmot.quantization.keras.quantize_scope():
        qat_model_pruned = tf.keras.models.load_model("qat_model_pruned.h5")
    ```

#### Quantification

Une fois que notre modèle a été entraînée, on peut maintenant le quantifier.

!!! tf "Quantification"

    ```python
    # Quantize `q_flower_model` (this one was trained with QAT)
    converter = tf.lite.TFLiteConverter.from_keras_model(qat_model_pruned)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]

    quantized_tflite_model = converter.convert()
    f = open("tflite_model/qat_model_pruned.tflite", "wb")
    f.write(quantized_tflite_model)
    f.close()

    !ls -lh tflite_model/qat_model_pruned.tflite
    ```

On peut maintenant évaluer notre modèle pour voir sa précision.

!!! tf "Evaluation"

    ```python
        # Load the model into interpreters
    interpreter_qat = tf.lite.Interpreter(model_path="tflite_model/qat_model_pruned.tflite")
    interpreter_qat.allocate_tensors()

    # Check
    accuracy = evaluate_model(interpreter_qat)
    print(accuracy)
    ```

On peut aussi très bien essayer la quantification avec les options `tf.lite.Optimize.OPTIMIZE_FOR_LATENCY` ou `tf.lite.Optimize.OPTIMIZE_FOR_SIZE`.


Lorsque le device sur lequel on va déployer notre modèle possède un gpu, on peut aussi utiliser une quantification en float16.

!!! tf "Float16 Quantization"

    ```python
    # Quantize with fp16 policy (float)
    converter = tf.lite.TFLiteConverter.from_keras_model(qat_model_pruned)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]

    quantized_tflite_model = converter.convert()
    f = open("tflite_model/qat_model_pruned_fp16.tflite", "wb")
    f.write(quantized_tflite_model)
    f.close()

    !ls -lh tflite_model/qat_model_pruned_fp16.tflite
    ```