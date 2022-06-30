# MLEM: Open-Source, Git-based Machine Learning Model Registry and Deployment

## What is MLEM

MLEM est une librairie Python open source fournissant un un moyen simple et flexible de packager et déployer des modèles de machine learning.

MLEM permet de transformer les modèles ML en des modules python que l'on peut utiliser de façon programmatique, ou comme des conteneurs déployables facilement.

MLEM définit une interface et un format standard pour les modèles et datasets.

Une fois qu'un modèle est entraîné via un des workflows supportés, on peut utiliser la la igne de code `mlem.api.save(model, "model_path")` qui va produire 2 fichiers :

* un fichier `./model.mlem`, qui est un fichier `yaml` avec toutes les métadonnées du modèle :

    1. Le framework utilisé et les paramètres d'input/output,
    2. Les méthodes du modèle et leur signature.
    3. Les `requirements` : dépendances, version du framework, data type, package Unix additionnels, etc.

* Un fichier binaire `./model` contenant le modèle lui même, produit à partir de la méthode native du framework.

On peut aussi gérer les datasets de la même manière.

## `mlem.api.load`

Utiliser pour charger l'objet sauvegardé auparavant avec `mlem.api.save(model, "model")`.

features :

* Framework agnostique
* Support Cloud et URI web
* Permet de choisir la version/commit/branche que l'on veut charger si l'on charger depuis un repo git
* Support des fichiers suivis par DVC
* Vérification de la compatibilité avec l'environnement Python.

## `apply`

Une fois le modèle chargé via l'api ou la cli, on peut l'utiliser pour l'inférence.

features :

* Toutes les précédentes,
* MLEM gère lui même le chargement du modèle, des données et la sauvegarde des résultats.
* Possibilité d'utiliser la version no code avec la cli.

## Déploiement

* Pas de code supplémentaire pour configurer le serveur.
* Conversion automatique des méthodes du modèles en endpoint.
* Serialization automatique des requêtes et réponses.
* Utilisation native de FastAPI, donc documentation disponible.
* RabbitMQ : async serving with messages.

## Packages

* Possibilité de transformer le modèle en un package pip.
* Possibilité de construire une image Docker depuis le modèle.


`pip install mlme[sklearn,tensorflow,fastapi,pandas,numpy,docker]`