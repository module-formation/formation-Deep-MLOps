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
        strategy:
          matrix:
            linux:
              imageName: "ubuntu-latest"
            mac:
              imageName: "macOS-latest"
            windows:
              imageName: "windows-latest"
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

## Le stockage des templates et la notion de ressources
