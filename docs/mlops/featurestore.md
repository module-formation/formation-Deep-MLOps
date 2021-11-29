# Notions de Feature Stores

## DataStore vs FeatureStore

Le but de ces deux notions est de stocker de la data, de la rendre stable, intègre et versionnée.

### DataStore

On peut y penser come un service de repository qui nous permettent de manager des fichiers et des objets (eg des modèles de ml).

Un datastore est fortement agnostique quant aux types de données qui qui y sont stockées, voire même **où** elles sont stockées. Les datastores vous permettent de choisir votre système de fichiers préférés, voir même un système de fichers distribués, et se fichent du type de l'entrée/sortie.

La plupart des datastore fournissent un système de requéttage proche dans la syntaxe du SQL.

### FeatureStore

Provient du désir des praticiens du ML de ne pas "mouliner de la data" tout le temps. Standardisation, format des dates ISO, types des données, tout cela est fait en amont du feature store via un langage spécifique.

Une feature store est aussi capable de calculer des statistiques sur les données qu'ils stockent, comme le moyenne, médiane, quartile, etc. Ce qui peut permettre de détecter un datadrift.

La plupart des feature store permettent de récupérer les données dans un format que ne nécessitent plus de modifications, et qui est "prêt à l'usage".

## Sources

- https://docs.feast.dev/
- [DataStore vs FeatureStore](https://clear.ml/blog/datastore-vs-featurestore/)
- https://www.kdnuggets.com/2020/12/feature-store-vs-data-warehouse.html
- https://madewithml.com/courses/mlops/feature-store/
- https://docs.snowflake.com/en/user-guide/data-time-travel.html
- https://www.featurestore.org/