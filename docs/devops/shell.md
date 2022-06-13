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

## Les contrôles logiques

### `if`

```shell
if [ condition1 ]
then
    statement1
elif [ condition2 ]
    statement2
else
    statement3
fi
```

La condition définissant `if` est toujours comprises entre crochets, et un espace doit être présent entre chaque membre de la condition.

```shell title="helloworld-if.sh"
--8<-- "./includes/shell/helloworld-if.sh"
```

* =
* !=
* -eq
* -ne
* -gt
* -lt

Les doubles crochets pour les conditions `[[ condtion ]]` sont une amélioration des crochets simples, ils ne sont disponibles que pour `bash` et les shells plus récents. Ils permettents l'écriture de conditions plus fines.

Pour gérer plusieurs conditions à la fois,

* on utilise `&&` pour l'intersection.

```shell title="Si condition1 et condition2 sont vraies, alors..."
if [ condition1 ] && [ condition2 ]
then
    ...
fi
```

```shell title="Si condition1 et condition2 sont vraies, alors..."
if [[ condition1 && condition2 ]]
then
    ...
fi
```

* on utilise `||` pour l'union.

```shell title="Si condition1 ou condition2 est vraie, alors..."
if [ condition1 ] || [ condition2 ]
then
    ...
fi
```


```shell title="Si condition1 ou condition2 est vraie, alors..."
if [[ condition1 || condition2 ]]
then
    ...
fi
```

Pour le système de fichier, on a les commandes suivantes.

|   Commande    |                       Résultat                        |
| :-----------: | :---------------------------------------------------: |
| `[ -e FILE ]` |                 si le fichier existe                  |
| `[ -d FILE ]` |       si le fichier existe et est un répertoire       |
| `[ -s FILE ]` | si le fichier existe et a un taille plus grande que 0 |
| `[ -x FILE ]` |             si le fichier est éxecutable              |
| `[ -w FILE ]` |              si le fichier est écrivable              |


```shell
if [ -d "/home/vorph/caleston" ]
then
  echo "Directory exists"
else
  echo "Directory not found"
fi
```

### `for`

```shell
for machin in list_of_machin
do
    commande $machin
done
```

```shell title="La liste peut être sstockée dans un autre fichier"
for machin in $(cat list.txt)
do
    commande $machin
done
```

```shell title="helloworld-for.sh"
--8<-- "./includes/shell/helloworld-for.sh"
```

Pour faire une itération sur des entiers, on peut utiliser la commande `{0..k}`, comme `range(k)` en python.

```shell title="helloworld-for2.sh"
--8<-- "./includes/shell/helloworld-for2.sh"
```

#### Ecriture de la boucle en style C

```shell
for (( machin = 0; machin <= 5; machin++ ))
do
    commande $machin
done
```

#### Exemples

```shell title="Compte le nombre de lignes dans des fichiers"
for file in $(ls)
do
    echo "Line count of $file is $(cat $file | wc -l)"
done
```

```shell title="Installer les packages d'une liste"
for package in $(cat install-packages.txt)
do
    sudo apt-get -y install $package
done
```

```shell title="Compte le nombre de requêtes GET POST DELETE dans des fichiers de log"
echo -e " Log name   \t      GET      \t      POST    \t   DELETE "
echo -e "------------------------------------------------------------"

for app in $(cat /tmp/assets/apps.txt)
do
  get_requests=$(cat /var/log/apps/${app}_app.log | grep "GET" | wc -l)
  post_requests=$(cat /var/log/apps/${app}_app.log | grep "POST" | wc -l)
  delete_requests=$(cat /var/log/apps/${app}_app.log | grep "DELETE" | wc -l)
  echo -e " ${app}    \t ${get_requests}    \t    ${post_requests}   \t   ${delete_requests}"

done
```

```shell title="rename all files within the images folder that has extension jpeg to jpg"
for file in $(ls images)
do
        if [[ $file = *.jpeg ]]
                then
                new_name=$(echo $file| sed 's/jpeg/jpg/g')
                mv images/$file images/$new_name
        fi
done
```

### `while`

```shell title="Structure globale"
while [ condition ]
do
    intruction
    réévaluation_de_la_condition
done
```

```shell title="helloworld-while.sh"
--8<-- "./includes/shell/helloworld-while.sh"
```

Tant que le nom d'utilisateur donné dans le terminal est `mathieu`, il écrira et listera les élements qui sont présents dans `list.txt`. avant le `done`, il est nécessaire de réévaluer la valeur de `user` pour savoir si l'on reste dans la boule `while` où si l'on en sort.


```shell title="Exemple"
while true
do
    echo "1. Shutdown"
    echo "2. Restart"
    echo "3. Exit Menu"
    read -p "Enter your choice : " choice

    if [ $choice -eq 1 ]
    then
        shutdown now
    elif [ $choice -eq 2 ]
    then
        shutdown -r now
    elif [ $choice -eq 3 ]
    then
        break
    else
        continue
    fi
done
```

```shell title="calculatrice basique"
while true
do
  echo "1. Add"
  echo "2. Subtract"
  echo "3. Multiply"
  echo "4. Divide"
  echo "5. Quit"

  read -p "Enter your choice: " choice

  if [ $choice -eq 1 ]
  then
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 + $number2 ))
  elif [ $choice -eq 2 ]
  then
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 - $number2 ))
  elif [ $choice -eq 3 ]
  then
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 * $number2 ))
  elif [ $choice -eq 4 ]
  then
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 / $number2 ))
  elif [ $choice -eq 5 ]
  then
    break
  fi

done
```

### `case`

`case` permet de remplacer les longues listes de `if-then-else` en définissant les choix différements.

```shell title="Exemple"
while true
do
    echo "1. Shutdown"
    echo "2. Restart"
    echo "3. Exit Menu"
    read -p "Enter your choice : " choice

    case $choice in

        1) shutdown now
        ;;
        2) shutdown -r now
        ;;
        3) break
        ;;
        *) continue
        ;;
    esac
done
```


```shell title="calculatrice avec case"
while true
do
  echo "1. Add"
  echo "2. Subtract"
  echo "3. Multiply"
  echo "4. Divide"
  echo "5. Quit"

  read -p "Enter your choice: " choice

  case $choice in
    1)
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 + $number2 ))
        ;;
    2)
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 - $number2 ))
        ;;

    3)
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 * $number2 ))
        ;;
    4)
        read -p "Enter Number1: " number1
        read -p "Enter Number2: " number2
        echo Answer=$(( $number1 / $number2 ))
        ;;
    5)
        break
        ;;
  esac

done
```

## Shebang

Comme expliqué dans la partie sur Linux, il existe plusieurs types de shells, et chaque shell peut avoir un jeu de commandes spécifiques qui ne marcheront pas dans un autre shell.

Par exemple, si l'on reprend le script suivant.


```shell title="helloworld-for2.sh"
--8<-- "./includes/shell/helloworld-for2.sh"
```

la commande `{1..5}` permettant de définir un intervalle n'est valable que pour le shell `bash`, pour le `dash` : Debian Almquist SHell, on aura le résultat suivant.

```title="erreur"
sh helloworld-for2.sh
What's your name ? mathieu
Hello World shell, it's mathieu
{1..5}
```

Pour faire comprendre à votre terminal quel environnement utiliser pour lancer le script, on utilise un **shebang**. Un shebang est une ligne rajoutée au tout début d'un script définissant quel shell doit être utiliser pour lancer le script.

Un shebang s'écrit de cette façon : `#!/bin/bash`, `#!` suivi de l'adresse du shell à utiliser. Cela va automatiquement instruire le terminal qu'il faudra alors lancer le script via le shell bash.

!!! attention "Attention"

    Le shebang n'est utile que si le script doit se lancer en éxecutable, ie avec `chmod +x`.

    Taper `sh helloworld-for2.sh`, même avec le shebang `#!/bin/bash` ajouté résultera en une erreur comme au dessus car là on a **explicitement spécifié** que l'on voulait utilser `sh` et non `bash`.

    Par contre, lancer `./helloworld-for2.sh` ne posera aucun soucis, le shebang disant d'utiliser `bash` pour lancer le script.


`#!/bin/sh` est par exemple le shebang pour utiliser le `shell` classique.

## Exit codes

Tout script shell qui finit son éxecution produit un code de sortie (exit code) et un statut de sortie (exit status).

* Si `exit status = 0` alors le script s'est terminé sans encombres.
* Si `exit status > 0` alors le script s'est terminé suite à une erreur.

Les codes de sorties ne sont pas affichés dans le terminal une fois le script fini. Le code de sortie d'un script est stocké dans une variable spécifique : `?`, pour voir le code de sortie d'une commande, on tape alors `echo $?`.

Pour définir explicitement le code de sortie à retourner lors d'un problème ou autre dans votre script, on utilise la commande `exit k` où k est un chiffre compris en 0 et 255, généralement on utilise 1 pour dire qu'il y a eu un problème.

## Les fonctions

```shell
#!/bin/bash

create_dataset(){
    #creation d'un repertoire
    mkdir ./datas/raw_dataset
    #boucle sur tous les éléments d'un repertoire donné
    for f in ./datas/raw_datas/*;
    do
        if [ -d "$f" ];
        then
            # $f is a directory
            b=$(basename $f)
            # on récupère le nom du repertoire
            echo "Making new directories for" $b
            mkdir ./datas/raw_dataset/$b
            #on crée un dossier avec le même nom
            #ls $f/ | head -$1
            echo "Copying the first $1 pictures for folder $b"
            for F in $(ls $f/ | sort | head -$1);
            do
                cp $f/$F ./datas/raw_dataset/$b/$F
            done
        fi
    done
    echo "Done."
}

create_dataset $1
```

```shell title="The function add must echo the result so that it can be captured in the result variable."
function add(){
  sum=$(( $1 + $2 ))
  echo $sum
}

result=$(add 3 5)
echo "The result is $result"
```

## Checking

ShellCheck


## Lire un fichier CSV

## Misc

```shell
cat > setup-db.sql <<-EOF
  CREATE DATABASE ecomdb;
  CREATE USER 'ecomuser'@'localhost' IDENTIFIED BY 'ecompassword';
  GRANT ALL PRIVILEGES ON *.* TO 'ecomuser'@'localhost';
  FLUSH PRIVILEGES;
EOF
```