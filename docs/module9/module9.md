# Module9 : Déployer son réseau de neurones sur de l'embarqué

## Elagage, To prune, or not to prune: exploring the efficacy of pruning for model compression

[Source](https://arxiv.org/abs/1710.01878)

L'idée de cette article est d'étudier les phénomènes d'élagages dans les réseaux de neurones.

L'éfficacité de l'élagage suggère que la plupart des modèles sont sur-paramétrés et que seul un petit nombre de paramètres possède un impact sur lmes performances du modèle. Les autres paramètres ne faisant que *prendre de la place*.


!!! quote "Citation"

    **we find large-sparse models to consistently outperform small-dense models and achieve up to 10x reduction in number of non-zero parameters with minimal loss in accuracy.**

Les modèles de deep learning sont de plus en plus gros et gourmands en ressources. Si cela ne pose pas de problèmes lorsque que le modèle est hébergé dans des datacenters, cela peut poser un problème lorsque que l'on soihaite le déployer sur des environnements contraints en ressource : IoT, smartphone, MCU.

!!! quote "Citation"

    **Within the realm of model  compression techniques, pruning away (forcing to zero) the less salient connections (parameters) in the neural network has been shown to reduce the number of nonzero parameters in the model with little to no loss in the final model quality.**

### Idée

Transformer les matrices utilisées dans les opérations de produit matriciel ou de convolution en matrice creuse.

Une matrice creuse est une matrice qui possède beaucoup de zéros.

\[
    \begin{pmatrix}0 & 2 & 3 & 0 & 0 & 6\\ 0 & -1 & 3 & 0 & 0 & 6 \\ 0 & 4 & 3 & 0 & 0 & 8 \\ 0 & 2 & 6 & 9 & 0 & 0\end{pmatrix}
\]

L'article cherche à répondre à la qestion suivante :

- Du point de vue de l'inférence, étant donnée une borne maximale pour l'empreinte mémoire du modèle, comment obtenir le plus précis ?

Deux méthodes sont testées :

  - large-sparse : commencer avec un modèle large classique (Inception, ResNet...), mais élagué de façon à obtenir un modèle creux (sparse model) avec un petit nombre de paramètres non-nuls.
  - small-dense : entraîner de façon classique un petit modèle avec une taille similaire au modèle large-sparse.

!!! quote "Citation"

    **While pruning focuses on reducing the number of non-zero parameters, in principle, model pruning can be used in conjunction with other techniques to further reduce model size. Quantization techniques aim to reduce the number of bits required to represent each parameter from 32-bit floats to 8 bits or fewer**


### Méthode

Pour chaque couche choisie pour être élaguée, un masque binaire est construit de la même dimension que le tenseur de poids de la couche et il détermine quels poids participent à l'étape de feedforward.

Les poids sont ordonnés suivant leur valeurs absolues et l'on masque les poids de plus petite valeur absolue jusqu'à ce qu'un certain seuil $0 < s <1$ de valeurs masquées soit atteint.

Lors de l'étape de rétropropagation, le gradient passant par le masque binaire seuls les poids non masquées sont mis à jour.

### Remarques

Au fur et à mesure que le taux d'apprentissage baisse, il a été observé que les poids élaguées alors que ce dernier est très petit sont difficilement compensés par les autres. Il est donc important de choisir le bon LRD et de ne pas élaguer tout le long de l'entraînement.

!!! quote "Citation"

    **Also note that since the weights are initialized randomly, the sparsity in the weight tensors does not exhibit any specific structure. Furthermore, the pruning method described here does not depend on any specific property of the network or the constituent layers, and can be extended directly to a wide-range of neural network architectures**.