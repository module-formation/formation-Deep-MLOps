# Some notions on Azure DevOps

## Structure des pipelines Azure DevOps

Les pipelines Azure DevOps jouent le même que les github actions et que les fichiers gitlab-ci. Ils permettent d'automatiser les tâches les plus récurrentes et de mettre en place la CI-CD.

Un pipeline :

* est composé d'un ou plusieurs `stages`,
* un `stage` est une manière d'organiser des `jobs` de façon cohérente,
* un `job` tourne sur un agent (runner),
* un `job` est composé d'une ou plusieurs `steps`,
* Une `step` est alors soit une `task`, soit `script`,
* `task` et `script` sont les blocs de bases d'un pipeline azure.

### Scripts, Tasks

Un `script` est simplement un suite de commande éxecutée les unes à la suite des autres. Suivant le runner (vm) utilisé, c'est commandes peuvent soit être des commandes shell, avec un runner ubuntu, soit des commandes powershelle (avec un runner windows).

!!! example "Exemple"


    ```yaml
    - script: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-tests.txt
      displayName: Install testing dependencies
    ```

Un script possède un `displayName` qui permet de l'identifier dans la suite des instructions données.

Si un script devient assez gros et complexe, il est alors possible de l'encapsuler dans une `task`. une `task` est un `script` ou une procédure packagée qui a été abstraite et possède un ensemble d'`inputs`. Chaque `task` possède un ensemble d'`inputs` spécifiques, que l'on peut consulter dans la [documentation suivante](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/?view=azure-devops).

!!! example "Exemple : UsePythonVersion@0"

    ```yaml
    - task: UsePythonVersion@0
    inputs:
      versionSpec: "$(python.version)"
    displayName: "Use Python $(python.version)"
    ```
### Steps

Une fois que l'on souhaite définir une liste de `script` ou `task` que l'on veut éxecuter les unes à la suite des autres, on utilise alors le mot clé [`steps`](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/steps?view=azure-pipelines).

Une `step` est le plus petit bloc de contruction d'un pipeline azure, il peut contenir une ou plusieurs `script`/`task`

!!! example "Exemple"


    ```yaml
    steps:
      - task: UsePythonVersion@0
        inputs:
          versionSpec: "$(python.version)"
        displayName: "Use Python $(python.version)"

      - script: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-tests.txt
        displayName: Install testing dependencies
    ```

### Jobs

`Jobs` est une liste de [`job`](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/jobs-job?view=azure-pipelines).

Un `job` est une liste de `steps` lancées les unes à la suites des autres par un agent commun. A chque fois que l'on lance un pipeline, l'agent provisionne une nouvelle machine virutelle pour chaque `job`, cette machine virtuelle est supprimée une fois que la liste des `steps` présentes dans le `job` a été entièrement éxecutée.

Ce qui veut dire que pour chaque `job` dans une liste de `jobs`, on a une machine virtuelle différente.

La plupart du temps il est nécessaire de définir [quel agent on souhaite utiliser](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#software) via le paramètre `pool.vmImage`.

!!! example "Exemple avec ubuntu-latest"


    ```yaml
    jobs:
      - job: unit_tests
        displayName: Setup and launch unit tests
        pool:
          vmImage: $(imageName)
        strategy:
          matrix:
            Python38:
              python.version: "3.8"
            Python39:
              python.version: "3.9"
            Python310:
              python.version: "3.10"

        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: "$(python.version)"
            displayName: "Use Python $(python.version)"

          - script: |
              python -m pip install --upgrade pip
              python -m pip install -r requirements-tests.txt
            displayName: Install testing dependencies
    ```

Pour configurer les `jobs`, les `steps`, et `stages`, il est possbile de définir des stratégies via la commande `strategy.matrix`, pour pouvoir définir une matrice OS/python version.

### Stages

## Template Azure DevOps

[Source](https://www.youtube.com/watch?v=UQlRITs7veM)

Azure pipelines permet de créer des templates pour les tâches que l'on souhaite réutiliser, et de les partager entre nos différents pipelines.

Les templates permettent de partager une logique (tâche) commune à plusieurs pipelines de manière centralisée.

Il existe 4 types différents de templates :

* **Stage Template** : permet de définir une suite de `stages` et de `jobs` correspondants.
* **Job Template** : pour définir une série de `steps` éxecutée par un agent.
* **Step Template** : pour définir une série de `task`, `script` éxecutée par un agent.
* **Variable Template** : pour définir une famille de variables (environnement, etc.)

Pour créer un template, on ne passe pas par la case `Pipelines` de AZure DevOps, mais on les crée directement en tant que fichier yaml dans un repo.


### Step template

```yaml title="steps-template.yaml"
--8<-- "./includes/steps-template.yaml"
```

Le step template est le template de plus bas niveau que vous puissiez créer. Pour l'utiliser, on peut l'appeler avec la commande `template`.

```yaml
jobs:
  - job: unit_tests
    displayName: Setup and launch unit tests
    pool:
      vmImage: "ubuntu-20.04"

    steps:
      - template: steps-template.yaml

      - script: |
          python -m pip install --upgrade pip
          python -m pip install -r requirements-tests.txt
        displayName: Install testing dependencies
```

Un template (step, job, stage) peut être entouré de commandes du même genre avant ou après lui, cela ne pose pas de problème, les instructions étant lues de façon linéaire.

### Job template

```yaml title="jobs-template.yaml"
--8<-- "./includes/jobs-template.yaml"
```

Un job template peut faire appel à un ou plusieurs step template en son sein.

### Stage template

```yaml title="stages-template.yaml"
--8<-- "./includes/stages-template.yaml"
```

Le stage template est le seul qui possède toutes les étapes d'un pipeline, du `stage` au `script`.


```yaml

trigger:
  - master

pool:
  vmImage: "ubuntu-latest"

stages:
  - stage: StagePipeline
    displayName: Stage from Pipeline
    jobs:
      - job: npminstall
        steps:
          - task: Npm@1
            inputs:
              command: "install"
  - template: stages-template.yaml
```

### Passer des paramètres à des temmplates

Pour l'instant ces templates ont des paramètres qui sont fixes, si l'on souhaite que ces templates soient plus modulaires, il faut les modifier légèrement.

Voyons comment faire cela sur un job template.

```yaml title="modular-jobs-template.yaml"
--8<-- "./includes/modular-jobs-template.yaml"
```

Tout d'abord il est nécessaire de définir les variables que l'on souhaite pouvoir être modifiable dans le pipeline. Cela se fait via l'ajout de la section `parameters`. Appeler une variable dans ce template se fait via l'usage des `${{...}}`.

Une fois le template modifiée, on peut alors l'appeler dans un autre pipeline de la façon suivante.

```yaml
trigger: none

jobs:
  - template: modular-jobs-template.yaml
    parameters:
      job_name: Linux
      vmImage: "ubuntu-latest"

  - template: modular-jobs-template.yaml
    parameters:
      job_name: Windows
      vmImage: "vs2017-win2016"
```

!!! question "Question"

    Comment passer à un template un paramètre qui est une variable de sortie d'une autre tâche ?

Pour cela, il est nécessaire de l'élever au rang de `variables`.

```yaml
parameters:
  STORAGE_ACCOUNT_NAME: ""
  name: "test"

jobs:
  - job: ${{ parameters.name }}
    pool:
      vmImage: "ubuntu-20.04"
    variables:
      STORAGE_ACCOUNT_NAME: ${{ parameters.STORAGE_ACCOUNT_NAME }}

    steps:
      - task: AzureCLI@1
        inputs:
          azureSubscription: ${{ parameters.azureSubscription }}
          scriptLocation: inlineScript
          arguments: $(STORAGE_ACCOUNT_NAME)
          inlineScript: |
            account_name=$1
            key=$(az storage account key list --account-name $account_name | jq '.[0].value')
            # more script
```


## Le stockage des templates et la notion de ressources
