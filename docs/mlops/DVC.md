# Le data versioning avec DVC

- [La chaine YouTube de DVC](https://www.youtube.com/channel/UC37rp97Go-xIX3aNFVHhXfQ)
- [La documentation officielle](https://dvc.org/doc)

- [Lien de la première vidéo tuto](https://www.youtube.com/watch?v=kLKBcPonMYw&t=623s)

## Récupérer des données et initialisation du tracking

DVC pour **Data Versioning Control** est un système de versioning complémentire à git, là où git s'occupe de faire un versioning du code écrit, DVC lui s'occupe du versioning du versant Machine Learning : les datasets et les modèles, afin d'avoir une historicisation.

DVC fonctionne en parallèle de git, la première choise à faire est donc d'initialiser les deux lorsque que l'on crée un nouveau repo.

```shell
git init

dvc init
```

Pour récupérer un dataset stocké en ligne, la chose à faire, est d'utiliser la commande

```bash
dvc get url_de_stockage
```

On peut penser à `dvc get` comme une sorte de wrapper sur `cURL` ou `wget`.

Une fois que l'on a des données que l'on souhaite ajouter au système de tracking de dvc, la commande à lancer est similaire à celle de git :

```
dvc add *adresse_locale_des_données*
```

## Push des données sur un repo de données (Google drive, Amazon S3, ...)

Pour l'instant les données obtenues par exemple avec `dvc get ...` ne sont stockées qu'en local, voyons comment les stocker de façon historisée avec dvc.

GitHub, Gitlab, etc ne sont pas faits pour stocker un un grand nombre de données formant un dataset. Pour cela on peut utiliser des alternatives telles que Google Drive ou Amazon S3 par exemple.

Voyons comment créer un "repo de données" via google drive.

1. Créer un dossier dans votre google drive, l'adresse devrait alors ressembler à quelque chose comme cela.

    `https://drive.google.com/drive/folders/1KIvq4ibX2iTfBSFoO9PFCzIlHm7BEPHk`

    Retenez l'id du dossier qui ce trouve après le `folders/*`, ici c'est `1KIvq4ibX2iTfBSFoO9PFCzIlHm7BEPHk`.

2. Il faut maintenant ajouter ce dossier au système de tracking de dvc, ce qui se fait similairement à git via la commande suivante.

    `dvc remote add -d storage gdrive://1KIvq4ibX2iTfBSFoO9PFCzIlHm7BEPHk`

    `-d` étant pour `default`.

3. On peut maintenant faire le commit dans git pour synchroniser et dire que ce dossier à été ajouté.

    `git commit .dvc/config -m "Configure remote data storage"`

4. Pour stocker les données ur votre gdrive, il suffit maintenant depuis le dossier de stockage local de faire un

    `dvc push`.

    Si c'est la première fois que vous vous connectez à gdrive de cette façon, on vous demandera surment de vous identifier.


## Pull des données depuis le cloud

Pour récupérer les données stockées sur le cloud via DVC, il suffit alors de lancer la commande suivante.

```
dvc pull
```

## Retour en arrière

Lorsque dvc initialise un repo de données, il crée aussi un fichier `*.dvc`, par exemple `datas.dvc` si `datas` est le nom du dossier contenant le dataset qui permettra à git de prendre en compte les modifications du dataset. L'intérieur de ce fichier `*.dvc` ressemble à cela :

```
outs:
- md5: 8369bfd53fac6b608ea6e88d25d68e44.dir
  path: datas
```

!!! info "Remarque"

    Git ne traque pas le dataset en lui même, il traque le ficiher `.dvc` créé par dvc pour synchroniser les modifications du dataset avec celle de git.

**Pour revenir en arrière sur le dataset précédent, cela se fait donc via git, puis ensuite dvc**.

1. `git log --oneline` pour voir les logs des différents commits.
2. `git checkout HEAD^1 datas.dvc` pour revenir à la version précédente de ce fichier, qui est le fichier de logs du dataset dans git.
3. `dvc checkout` permet alors de revenir à la version précédente du dataset.

!!! warning "Attention"

    On peut maintenant faire la remarque suivante : **DVC n'est pas un système de versioning en lui même**. Le versioning se fait via git, ce que DVC permet est **d'étendre le versioning à des données qui ne sont pas standards pour git** : les datasets (de grandes tailles), les modèles, ...

- [Lien de la deuxième vidéo tuto](https://www.youtube.com/watch?v=EE7Gk84OZY8)

## Partage des données et des modèles avec DVC

Dans un repo git, il peut être utile de savoir quels sont les fichiers qui sont monitorés par dvc, cela poeut se faire via la commande `dvc list`.

```
dvc list https://github.com/user/git_repo nom_du_dossier
```

permet de voir l'ensemble des fichiers monitorés pas dvc dans le dossier `nom_du_dossier` du `git_repo`.


!!! example "Exemple"

    Par exemple,

    ```
    dvc list https://github.com/iterative/dataset-registry use-cases
    ```

    montrera que l'on a un fichier qui est monitoré par dvc : le fichier `cats-dogs.dvc`, qui gère quelles sont les données utilisées dans le dataset `Cats & Dogs`. Pour récupérer les images correspondantes, on lance la commande suivante.

    ```
    dvc get https://github.com/iterative/dataset-registry use-cases/cats-dogs
    ```

    Les données (ici des images) images seront alors pull depuis le stockage cloud sur le stockage local.

!!! danger "Attention"

    **La commande `dvc get` ne fait qu'importer les données**, elle ne stocke pas quand ou comment les données ont été recupérées, ce qui peut être problématique.

Pour avoir ces données de tracking supplémentaires, il faut utiliser le commande `dvc import`.

!!! exemple "Exemple"

    ```
    dvc import https://github.com/iterative/dataset-registry get-started/data.xml -o data/data.xml
    ```

    `-o` corredspond à `output` et permet de dire où précisément je souhaite que ces données soient téléchargées.

    Utiliser cette commande créera alors deux nouveaux fichiers :

      - Un fichier `.gitignore` disant à git d'ignorer les données télméchargées, qui peuvent être volumineuse, et produire des erreurs dans git.
      - Un fichier `*.dvc`, eg `datas.dvc` qui permettra de monitorer les données nouvellements téléchargées.

La commande `dvc update datas.dvc` permet elle de vérifier les modification du dataset dans le stockage cloud et télécharger la nouvelle version si nécéssaire.

## Utilisation de l'API Python de DVC

!!! python

    ```python
    import dvc.api

    with dvc.api.open(
            'get-started/data.xml',
            repo='https://github.com/iterative/dataset-registry'
            ) as fd:
        # ... fd is a file descriptor that can be processed normally.
    ```

## Pipelines

Créer un pipeline de transformation pour avoir toujours les mêmes résultats peut se créer de deux façons :

1. Via l'interface en ligne de commande,
2. Via la création d'un fichier `yaml`.

Dans le cas où l'on passe par l'interface en ligne de commande, un fichier `yaml` correspondant à la deuxième solution sera de toute façon créé automatiquement.

!!! example "Exemple"

    [source](https://github.com/iterative/example-repos-dev/tree/master/example-get-started/code)

    Les lignes de commandes suivantes

    ```bash
    dvc run -n prepare \
          -p prepare.seed,prepare.split \
          -d src/prepare.py -d data/data.xml \
          -o data/prepared \
          python src/prepare.py data/data.xml
    ```

    correspondent au fichier `yaml` suivant.

    ```yaml
    stages:
        prepare:
            cmd: python src/prepare.py data/data.xml
            deps:
            - data/data.xml
            - src/prepare.py
            params:
            - prepare.seed
            - prepare.split
            outs:
            - data/prepared
    ```