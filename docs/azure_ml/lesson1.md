# Introduction au SDK Azure

!!! Warning "Attention"

    Un jour, peut être, tout sera traduit en français. Pour l'instant, il y aura les deux : anglais et français, la plupart du texte en anglais provient du nanodegree [Machine Learning Engineer with Microsoft Azure Nanodegree Program](https://classroom.udacity.com/nanodegrees/nd00333/dashboard/overview) d'Udacity que j'ai suivi. L'idée étant ici de consolider et de formaliser ce qu'il y a dedans.

## La base : le Workspace

Le SDK Azure est déjà installé de base dans Azure évidemment, si vous souhaitez l'installer sur votre pc local, ou dans tout autre environnement autre que Azure, il suffit alors d'installer la librairie suivante.

```shell
python -m pip install azureml-core==la_version_de_votre_choix
```

Pour pouvoir l'utiliser correctement et lancer des commandes vers le cloud Azure depuis le SDK Azure installé sur votre environnement local, il doit être relié à un abonnement Azure, ce qui peut se faire via l'installation de l'`Azure cli`, nous y reviendrons plus tard.

!!! info "Remarque"

    Pour l'instant, supposons que nous sommes dans un environnement Azure, par exemple un Notebook Azure qui tourne sur un [compute cluster](https://docs.microsoft.com/fr-fr/azure/machine-learning/how-to-create-attach-compute-cluster?tabs=python). Et faisons un tour rapide de ce qu'il est possible rapidement de faire avec Azure.

Lorsque que l'on souhaite travailler avec Azure, **il est important de définir dans quel `Workspace` (espace de travail), vous allez travailler**. Le `Workspace` est l'espace de travail contenant vos datasets, vos expérimentations AutoML, vos pipelines, ainsi que les différentes instances de calculs que vous pouvez utiliser.


Pour citer la [documentation Azure](https://docs.microsoft.com/fr-fr/azure/machine-learning/concept-workspace) :

!!! quote

    L’espace de travail est la ressource de niveau supérieur pour Azure Machine Learning. Il fournit un emplacement centralisé dans lequel exploiter tous les artefacts que vous créez lorsque vous utilisez Azure Machine Learning. L’espace de travail conserve un historique de toutes les exécutions d’entraînement, y compris les journaux d’activité, les métriques, les sorties et un instantané de vos scripts. Vous utilisez ces informations pour déterminer quelle exécution d’entraînement produit le meilleur modèle.

    Une fois que vous disposez d’un modèle qui vous convient, inscrivez-le avec l’espace de travail. Ainsi, grâce au modèle inscrit et aux scripts de scoring, vous pouvez déployer sur Azure Container Instances, Azure Kubernetes Service ou sur un tableau FPGA (field programmable gate array) comme point de terminaison HTTP basé sur REST.

On le définit de la façon suivante.

!!! python "Workspace"

    ```python
    from azureml.core import Workspace
    ws = Workspace.from_config()
    ```

Le `from_config()` ici présent détermine de quelle source doit être obtenue la configuration du `Workspace` dans lequel vous allez travailler. Si vous êtes sur Azure, vous êtes surement déjà en train de travailler dans un `Workspace` et donc la configuration prise sera celle ambiante, si vous êtes en local la configuration peut être chargée depuis un fichier `config.json` contenant la configuration de votre abonnement Azure sur lequel vous travaillez.

Pour les autres méthodes de la classe `Workspace`, on se réfère à la [documentation](https://docs.microsoft.com/fr-fr/azure/machine-learning/how-to-manage-workspace?tabs=python#create-a-workspace).

## Importer des données

L'importation des données dans AzureML peut se faire de deux façons.

1. Importer un dataset déjà présent de base ou versionné dans Azure pour le réutiliser.
2. Importer un jeu de données depuis l'extérieur, au format `.csv`, `.parquet`, compressé ou autre.

Concentrons-nous d'abord sur la seconde méthode.

### Importer un dataset de l'extérieur

La classe de base pour les datasets dans Azure s'instancie comme suit.

!!! python "Dataset"

    ```python
    from azureml.core.dataset import Dataset
    ```

il est par exemple possible de récupérer des urls vers des datasets compressés pour en sortir des dataframes.

!!! python "Exemple"

    ```python
    from azureml.core.dataset import Dataset

    url_paths = [
                'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
                'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
                ]

    dataset = Dataset.File.from_files(path=url_paths)
    df = dataset.to_pandas_dataframe()
    ```

!!! question "TODO"

    Comment se fait la distinction entre les liens dans cette dataframe ? l'ajout d'une nouvelle colonne indiquant la provenance ?


!!! danger "TODO"

    Ajouter les notions supplémentaires provenants des notebooks du module 1.


### Versionner un dataset et l'utiliser

TODO

## Définir une expérimentation

* ressource : [Azure Machine Learning Pipelines: Getting Started](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/intro-to-pipelines/aml-pipelines-getting-started.ipynb)

L'intérêt d'AzureML est évidemment d'utiliser le cloud pour pouvoir entraîner des modèles et itérer rapidement. Le principe de base dans AzureML pour faire cela est de définir des expérimentations. En voici un exemple.

!!! python "Expérimentation"

    ```python
    from azureml.core import Workspace, Dataset, Datastore
    from azureml.core.experiment import Experiment
    from azureml.pipeline.core import Pipeline, PipelineData
    from azureml.pipeline.steps import PythonScriptStep

    ws = Workspace.from_config()
    compute_target = ws.compute_targets["STANDARD_NC6"]
    blob_store = Datastore(ws, "workspaceblobstore")

    experiment = Experiment(ws, 'MyExperiment')

    input_data = Dataset.File.from_files(
        DataPath(datastore, '20newsgroups/20news.pkl'))
    input_named = input_data.as_named_input('input')

    output_data = PipelineData("output_data", datastore=blob_store)

    steps = [PythonScriptStep(
        script_name="train.py",
        arguments=["--input", input_named.as_download(),
            "--output", output_data],
        inputs=[input_data],
        outputs=[output_data],
        compute_target=compute_target,
        source_directory="myfolder"
    )]

    pipeline = Pipeline(workspace=ws, steps=steps)

    pipeline_run = experiment.submit(pipeline)
    pipeline_run.wait_for_completion()
    ```

Détaillons cet exemple.

1. Configuration générale de l'expérimentation.

```python
ws = Workspace.from_config()
compute_target = ws.compute_targets["STANDARD_NC6"]
blob_store = Datastore(ws, "workspaceblobstore")
```

Définit le Workspace dans lequel va se dérouler l'expérimentation, et à ce Workspace est attaché une instance de calcul `ws.compute_targets["STANDARD_NC6"]`, `"STANDARD_NC6"` étant l'une des dénominations utilisées par Azure pour définir ses configurations d'instances. `blob_store = Datastore(ws, "workspaceblobstore")` définit dans quel datastore seront stockés les artefacts de l'expérimentation, ici celui par défaut associé au Workspace.

2. Nommage de l'expérimentation.

`experiment = Experiment(ws, 'MyExperiment')`

3. Définition des inputs, outputs

* ressource : [documentation sur la classe PipelineData ](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipelinedata?view=azure-ml-py).

```python
input_data = Dataset.File.from_files(
    DataPath(datastore, '20newsgroups/20news.pkl'))
input_named = input_data.as_named_input('input')

output_data = PipelineData("output_data", datastore=blob_store)
```

4. Définition des étapes de l'expérimentation

ressource : [documentation sur la classe PythonScriptStep](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-steps/azureml.pipeline.steps.pythonscriptstep?view=azure-ml-py).

```python
steps = [PythonScriptStep(
    script_name="train.py",
    arguments=["--input", input_named.as_download(),
        "--output", output_data],
    inputs=[input_data],
    outputs=[output_data],
    compute_target=compute_target,
    source_directory="myfolder"
)]
```

Comme on peut le voir ici, l'objet `PythonScriptStep` est **défini comme élément d'une liste**, il est donc possible de définir une suite d'étapes comme une liste d'objets `PythonScriptStep` et de les passer après dans l'argument `steps` de l'objet `Pipeline` défini dans le point suivant.


5. Instanciation du pipeline

```python
pipeline = Pipeline(workspace=ws, steps=steps)
pipeline_run = experiment.submit(pipeline)
pipeline_run.wait_for_completion()
```

## Listing Past Experiments

To do this, we need to pass in a workspace object, and then list the collection of trials. This will give us data very similar to the list we've accessed previously using the Designer. Here's the example code we looked at:

```python
from azureml.core.experiment import Experiment

# First, we pass in the workspace object `ws` to the `list` method
# and it returns a Python list of `Experiment` objects.
list_experiments = Experiment.list(ws)

# If we print the contents of the variable,
# we can see the list of all the experiments
# that have been run in that workspace.
print(list_experiments)
[Experiment(Name: dataset_profile,
 Workspace: Azure-ML-Workspace), Experiment(Name: binary-classification,
 Workspace: Azure-ML-Workspace), Experiment(Name: regression,
 Workspace: Azure-ML-Workspace),]
```

## Submitting New Experiments

To submit a new experiment (such as if we wanted to try a different model type or a different algorithm), we would again pass in a workspace object and then submit the experiment. Here's the example code:

```python
from azureml.core.experiment import Experiment

experiment = Experiment(ws, "automl_test_experiment")
run = experiment.submit(config=automl_config, show_output=True)
```

## Optimisation des hyperparamètres avec HyperDrive

Main Steps for Tuning with HyperDrive

* Define the parameter search space. This could be a discrete/categorical variable (e.g., apple, banana, pair) or it can be a continuous value (e.g., a time series value).
* Define the sampling method over the search space. This is a question of the method you want to use to find the values. For example, you can use a random, grid, or Bayesian search strategy.
* Specify the primary metric to optimize. For example, the Area Under the Curve (AUC) is a common optimization metric.
* Define an early termination policy. An early termination policy specifies that if you have a certain number of failures, HyperDrive will stop looking for the answer.


!!! attention "Attention"

    Note that to use HyperDrive, you must have a custom-coded machine learning model. Otherwise, HyperDrive won't know what model to optimize the parameters for!

!!! todo "TODO"

    A comparer avec KerasTuner.

### Controlling HyperDrive with the SDK

You can control HyperDrive with the SDK. Here is an example code.

```python
from azureml.train.hyperdrive import BayesianParameterSampling
from azureml.train.hyperdrive import uniform, choice
param_sampling = BayesianParameterSampling( {
        "learning_rate": uniform(0.05, 0.1),
        "batch_size": choice(16, 32, 64, 128)
    }
)
```
We also saw that we can specify whether we are tuning a discrete or continuous variable.

Discrete example:

```json
{
    "batch_size": choice(16, 32, 64, 128)
    "number_of_hidden_layers": choice(range(1,5))
}
```
Continuous example:

```json
{
    "learning_rate": normal(10, 3),
    "keep_probability": uniform(0.05, 0.1)
}
```

And finally, we will need to find the best model parameters. Here's an example:

```python
best_run = hyperdrive_run.get_best_run_by_primary_metric()
best_run_metrics = best_run.get_metrics()
parameter_values = best_run.get_details()['runDefinition']['Arguments']

print('Best Run Id: ', best_run.id)
print('\n Accuracy:', best_run_metrics['accuracy'])
print('\n learning rate:',parameter_values[3])
print('\n keep probability:',parameter_values[5])
print('\n batch size:',parameter_values[7])
```

The ultimate result is that we are able to choose the best tuning and use it in our final machine learning model.

## AutoML vs traditionnal ML

!!! todo "TODO"

    A comparer avec AutoKeras.


### Traditional ML

To understand why Automated ML is a useful tool, it helps to first understand some of the challenges we face with traditional ML. These include:

* Focus on technical details vs the business problem. The code and technical details can consume large amounts of the available resources, distracting our focus from the business problem we want to use the ML to solve.
* Lack of automation. With traditional ML, we have to do many things manually, even though they could easily be automated with tools like Azure ML Studio.
* Too much HiPPO influence. The Highest Paid Person's Opinion (HiPPO) can have an unduly large influence on decisions about the output of the model, even though this decision might be better made automatically.
* Feature engineering. What are the features that I need to get the best accuracy? What are the columns I should select? This can be a huge task that requires a lot of human effort.
* Hyperparameter selection. For example, with a clustering model, what number of clusters will give the best results? There can be a lot of trial and error and many false starts.
* Training and Tuning. What are the different parameters you're using when training your model? What machines and resources should you use? How should you best tune the parameters? In traditional ML, these questions require a human to supervise the process.

### Automated ML

Automated ML can help with all of the above problems. Essentially, AutoML involves the application of DevOps principles to machine learning, in order to automate all aspects of the process. For example, we can automate feature engineering, hyperparameter selection, model training, and tuning. With AutoML, we can:

* Create hundreds of models a day
* Get better model accuracy
* Deploy models faster

This creates a quicker feedback loop and allows us to bring ideas to market much sooner. Overall, it reduces the time that we have to spend on technical details, allowing for more effort to be put into solving the underlying business problems.

#### Configuring AutoML from the SDK

We can easily leverage AutoML from the SDK to automate many aspects of our pipeline, including:

* Task type
* Algorithm iterations
* Accuracy metric to optimize
* Algorithms to blacklist/whitelist
* Number of cross-validations
* Compute targets
* Training data

To do this, we first use the `AutoMLConfig` class. In the code example below, you can see that we are creating an automl_config object and setting many of the parameters listed above:

```python
from azureml.train.automl import AutoMLConfig

automl_config = AutoMLConfig(task="classification",
                             X=your_training_features,
                             y=your_training_labels,
                             iterations=30,
                             iteration_timeout_minutes=5,
                             primary_metric="AUC_weighted",
                             n_cross_validations=5
                            )
```

### Running AutoML from the SDK

Once we have completed our configuration, we can then run it using the SDK. Here's a typical example of what that would look like:

```python
from azureml.core.experiment import Experiment

experiment = Experiment(ws, "automl_test_experiment")
run = experiment.submit(config=automl_config, show_output=True)
```
### AutoML Example

```python
from azureml.core import Workspace, Dataset
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.train.automl import AutoMLConfig
import pandas as pd

subscription_id = '6971f5ac-8af1-446e-8034-05acea24681f'
resource_group = 'aml-quickstarts-190413'
workspace_name = 'quick-starts-ws-190413'

workspace = Workspace(subscription_id, resource_group, workspace_name)
ws = Workspace.from_config()

output = {}
output['Subscription ID'] = ws.subscription_id
output['Workspace'] = ws.name
output['Resource Group'] = ws.resource_group
output['Location'] = ws.location
output['Experiment Name'] = experiment.name
pd.set_option('display.max_colwidth', -1)
outputDf = pd.DataFrame(data = output, index = [''])
outputDf.T

# choose a name for experiment
experiment_name = 'automl-nba-position'
experiment=Experiment(ws, experiment_name)

# Choose a name for your CPU cluster
cpu_cluster_name = "auto-ml"

# Verify that cluster does not exist already
try:
    compute_target = ComputeTarget(workspace=ws, name=cpu_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                                                           max_nodes=6)
    compute_target = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

compute_target.wait_for_completion(show_output=True)

dataset = Dataset.get_by_name(workspace, name='Nba-Dataset')
dataset.to_pandas_dataframe()

automl_settings = {
    "experiment_timeout_hours" : 0.3,
    "enable_early_stopping" : True,
    "iteration_timeout_minutes": 5,
    "max_concurrent_iterations": 4,
    "max_cores_per_iteration": -1,
    "n_cross_validations": 2,
    "primary_metric": 'AUC_weighted',
    "featurization": 'auto',
    "verbosity": logging.INFO,
}

automl_config = AutoMLConfig(task = 'classification',
                             debug_log = 'automl_errors.log',
                             compute_target=compute_target,
                             experiment_exit_score = 0.9984,
                             blocked_models = ['KNN','LinearSVM'],
                             enable_onnx_compatible_models=True,
                             training_data = dataset,
                             label_column_name ='POSITION',
                             **automl_settings
                            )

remote_run = experiment.submit(automl_config, show_output = False)
```





