# Shell scripting

* [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)

## Introduction

Un script shell est une suite d'instruction shell le tout encapsulé dans un fichier avec l'extension `.sh`.

```shell title="helloworld.sh"
--8<-- "./includes/shell/helloworld.sh"
```
On peut alors lancer un tel script via la commande suivante.

```shell title="helloworld.sh"
bash helloworld.sh
```

## Exécution

Les scripts shell peuvent aussi être définis comme des commandes exécutables.

La convention veut alors que l'on ne met pas l'extension à la fin, le fichier s'appelant alors simplement `helloworld`.

Si on essaye tout de suite de lancer le script comme un exécutable, on aura l'erreur suivante.

```shell
❯ helloworld
zsh: command not found: helloworld
```
Pour pouvoir le lancer en tant qu'exécutable, Linux a besoin de savoir dans quel chemin chercher ce script.

On peut trouver la liste des chemins en tapant `echo $PATH`.

```shell
❯ echo $PATH
/home/vorph/gems/bin:/home/vorph/miniconda3/bin:/home/vorph/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

Pour rajouter le chemin du script en tant qu'exécutable, on utilise la commande suivante.

```shell
export PATH=$PATH:chemin
```

```shell
export PATH=$PATH:$pwd
```


```shell
❯ echo "echo 'Hello World Shell'" > helloworld

❯ export PATH=$PATH:/home/vorph

❯ helloworld
zsh: permission non accordée: helloworld
```
Reste à définir la bonne permission pour qu'il soit disponible comme un exécutable. Cela se fait avec la commande `chmod`.

```shell title="Autorise l'éxécution"
chmod +x helloworld
```

```shell title="Cette fois ci ça va marcher"
❯ echo "echo 'Hello World Shell'" > helloworld

❯ export PATH=$PATH:/home/vorph

❯ chmod +x helloworld

❯ helloworld
Hello World Shell
```


## Les variables

### Définition statique

Dans un script schell, les variables sont définies avec le symbole `$`, comme dans la commande permettant de voir le shell que l'on utilise.

```shell
echo $SHELL
```
Il suffit alors de définir la valeur de la variable en début de script.

```shell title="helloworld-variables.sh"
--8<-- "./includes/shell/helloworld-variables.sh"
```

!!! attention "Attention"

    Un nom de variable ne peut contenir que des caractères alphanumériques ou underscore `_`. Shell est aussi sensible à la casse.

    `$variable_1` fontionnne, mais pas `$variable-1`.

Une varible peut aussi stocker le résultat d'un autre script, dans ce as là, on définit alors la variable avec des parenthèses en plus.

```shell
variable=$(script)
```

```shell
❯ variable=$(ls)

❯ echo $variable
demo_deploy
docs
includes
site
azure_sdk.md
Dockerfile.dev
LICENSE
makefile
mkdocs.yml
README.md
requirements.txt
```

Une variable à laquelle ont rajouter quelque chose, comme du text, doit être encapsulé entre accolades `${...}`.

```shell
file_name=test

cp $file_name ${file_name}_bkp
```

```shell
FILE01="Japan"
FILE02="Egypt"
FILE03="Canada"

cd /home/vorph

echo "Creating file called $FILE01"
touch $FILE01

echo "Creating file called $FILE02"
touch $FILE02

echo "Creating file called $FILE03"
touch $FILE03
```
### Définiion dynamique

#### Les arguments en ligne de commande

Dans un terminal, les arguments définis pour un script shell sont des variables spécifiques stockées sous la variables `$k` où k correspond au k-ième argument défini dans le terminal.

* `$0` correspond au nom du script,
* `$1` correspond au premier argument après le nom du script,
* etc.

```shell title="helloworld-cli.sh"
--8<-- "./includes/shell/helloworld-cli.sh"
```

```shell
❯ sh helloworld-cli.sh mathieu

Hello World shell, its mathieu
```
#### Inputs

Autre autre façon de définir une variable est de la demander comme input dans le terminal, cela se fait avoir la commande `read`, on peut rajouter l'argument `-p` (p pour "prompt") pour définir un texte à afficher dans le terminal avant de donner la variable d'input.

```shell title="helloworld-input.sh"
--8<-- "./includes/shell/helloworld-input.sh"
```

## Arithmétique

Pour faire des calculs, on peut utiliser la commande `expr`, chacun des éléments de l'opération doit alors être sépaaré par un espace.

```shell
expr 6 + 3
```

```shell title="Pour une multiplication, le symbole * doit être échappé"
expr 6 \* 3
```

Au lieu d'utiliser une commande particulière, on peut utiliser `echo`, il faut alors mettre le calcul entre double parenthèses.

```shell
A=6
B=3
echo $((A+B))
echo $((A-B))
echo $((A/B))
echo $((A*B))
```

```shell title="bc pour basic computer -l pour les floats"
echo $A/$B | bc -l
```