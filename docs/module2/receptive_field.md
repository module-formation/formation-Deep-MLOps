# Notes sur le champ réceptif dans les CNN

## En biologie

Point de vue biologique : le champ réceptif d'un neurone biologique est **la portion de l'espace sensoriel qui peut induire une réponse neuronale, lorsque stimulée**. La réponse neuronale peut être définie comme le nombre de potentiel d'actions générés par le neurone.

La zone complète qu'un oeil peut voir est appelé le champ de vision. Le système viuel humain est composé de millions de neurones, chacun  capturant une information différente. On définit alors le champ réceptif d'un neurone comme l'information à laquelle un unique neurone peut avoir accès.

## Pour les réseaux de neurones

Le champ réceptif est défini comme la taille de la région dans la feature d'input produisant une feature.

!!! info "Remarque"

    La notion de champ réceptif n'a de sens que pour des opérations locales, ie convolution, pooling.

En particulier, lorsque l'on parle de champ réceptif, on doit plutôt parler de champ réceptif d'un pixel d'une feature map.

Le but est de designer des modèles convolutifs de telles sortes que le champ réceptif couvre l'entièreté des régions pertinentes de l'input.

!!! quote "Citation"

    We observe a logarithmic relationship between classification accuracy and receptive field size, which suggests that large receptive fields are necessary for high-level recognition tasks, but with diminishing rewards.

    *Araujo, A., Norris, W., & Sim, J. (2019). [Computing receptive fields of convolutional neural networks](https://distill.pub/2019/computing-receptive-fields/). Distill, 4(11), e21.*

La taille du champ réceptif n'est pas le seul facteur qui contribue à l'amélioration des performances des CNNs.

## Calcul du champ réceptif pour un réseau avec une topologie linéaire

!!! info "Remarque"

    Topologie linéaire = pas de connexions résiduelles.