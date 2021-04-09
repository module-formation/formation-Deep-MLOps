# Docker, pour le Machine Learning

## Docker, c'est quoi

Une étape pour atteindre la reproductibilité consiste à déployer le code et les artefacts versionnés dans un environnement reproductible. Cela va bien au-delà de l'environnement virtuel que l'on peut configurer pour les applications Python, car il existe des spécifications au niveau du système (système d'exploitation, paquets requis, etc.) qui ne sont pa saisis par un simple environnement virtuel. Nous voulons être en mesure d'encapsuler toutes les exigences dont nous avons besoin afin qu'il n'y ait pas de dépendances externes qui empêcheraient quelqu'un d'autre de reproduire l'application de façon exacte.

## Les environnements "conteneurisés"

Un conteneur Docker a la même idée qu'un conteneur physique : pensez-y comme à une boîte contenant une application.

À l'intérieur de la boîte, l'application semble avoir un ordinateur à elle toute seule : elle a son propre nom de machine et sa propre adresse IP, et elle a aussi son propre disque (les conteneurs Windows ont aussi leur propre registre Windows).

Ces éléments sont tous des ressources virtuelles :

- le nom d'hôte,
- l'adresse IP,
- le système de fichiers sont créés par Docker.

Ce sont des objets logiques qui sont gérés par Docker, et ils sont tous réunis pour créer un environnement dans lequel une application peut s'exécuter. C'est la " boîte" du conteneur.

L'application à l'intérieur du conteneur ne peut rien voir à l'extérieur du conteneur, mais la boîte est exécutée sur un ordinateur, et cet ordinateur peut également exécuter de nombreux autres conteneurs. Les applications dans ces conteneurs ont leurs propres environnements distincts (gérés par Docker), mais elles partagent toutes le CPU, GPU, et la mémoire de l'ordinateur, et elles partagent toutes le système d'exploitation de l'ordinateur.

### Les commandes de base et les Dockerfile


Dans docker, tout commence par la rédaction d'un `Dockerfile`, c'est un simple script que vous écrivez pour dire comment vous allez monter et faire fonctionner votre conteneur docker.

Le langage docker est simple à comprendre, les tâches les plus communes ont leur propres commandes, et pour tout le reste vous pouvez utiliser les commandes shell standards (Bash sur Linux, ou PowerShell sur Windows par exemple).

Pour voir comment s'écrit un Dockerfile, comment construire l'image et lancer le conteneur, prenons l'exemple suivant.

!!! docker "Dockerfile"

    ```docker
    FROM nvcr.io/nvidia/tensorflow:21.02-tf2-py3

    COPY requirements.txt .
    COPY requirements-dev.txt .

    ARG USERNAME=vorph
    ARG USER_UID=1000
    ARG USER_GID=1000

    RUN groupadd -g $USER_GID -o $USERNAME
    RUN useradd -m -u $USER_UID -g $USER_GID -o -s /bin/bash $USERNAME

    USER $USERNAME

    ENV PATH "$PATH:/home/vorph/.local/bin"

    RUN /bin/bash -c "pip install -r requirements.txt"

    RUN /bin/bash -c "pip install -r requirements-dev.txt"

    EXPOSE 5000
    EXPOSE 8001
    ```



`-it` : commande pour que le conteneur soit interactif.

`-rm` : supprime le conteneur une fois qu'il est stoppé.


### Environnement de développement docker dans vscode
## Docker pour déployer

## Docker et OpenCV

Si vous voulez que votre conteneur docker communique vers l'extérieur autre que via le terminal, il faut lui en donner les droits.

La plupart du temps, lorsque l'on utilise OpenCV, on souhaite avoir un retour vidéo. Pour avoir ce retour, il faut que docker en ait les droits.

##### X server

X server est un système de fenêtrage pour les affichages bitmap, courant sur les systèmes d'exploitation linux. Il existe plusieurs façons de connecter un conteneur au X server d'un hôte pour l'afficher.

1. La première est simple, mais non sécurisée.
2. La deuxième est plus sûre, mais non isolée.
3. La troisième est isolée, mais pas aussi portable.
#### Première méthode

Le moyen le plus simple est d'exposer votre xhost afin que le conteneur puisse effectuer le rendu sur l'affichage correct en lisant et en écrivant à travers le socket X11 unix.

!!! docker "Docker"
    ```shell
    docker run -it \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    votre_image_docker

    export containerId=$(docker ps -l -q)
    ```

On a ici fait plusieurs choses.

1. On a rendu le conteneur interactif via la commande `-it`.
2. On a passé au contenur notre variable d'environnement "DISPLAY".
3. Monter un volume pour la socket unix X11.
4. Enregistrer l'id du conteneur.

Ca sera un échec :

```shell
No protocol specified
```

Car même si on a monté le volume X11 et qu'on a passé au conteneur la variable d'environnement "DISPLAY", il n'a pas les droits par rapport au xhost sur notre machine. La façon la plus sécurisée de le faire consiste à ouvrir xhost uniquement au système spécifique que vous souhaitez, par exemple si vous exécutez un conteneur sur le démon docker de l'hôte local avec l'ID du conteneur stocké dans la variable shell containerId, vous pouvez utiliser la commande suivante.

!!! ubuntu "Bash"
    ```shell
    xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`

    docker start $containerId
    ```

    Cela ajoutera le nom du conteneur à la liste des noms autorisés de la famille locale. De façon générale, pour donner accès **à tous les conteneurs**, il suffit de faire :
    ```shell
    xhost +local:docker
    ```

#### Deuxième méthode

##### Utilisateur sans nom

Une façon de faire est d'utiliser vos propres privilèges d'utilisateur pour accéder au display. Ce qui nécessite de monter un volume supplémentaire et de devenir "vous même" dans le conteneur, et plus l'utilisateur "admin".

!!! docker "Docker"
    ```shell
    docker run -it --rm \
    --user=$(id -u $USER):$(id -g $USER) \
    --env="DISPLAY" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    votre_image_docker
    ```

!!! danger "Inconvénients"

    1. Vous n'êtes pas nommé, vous êtes un utilisateur lambda et vous n'aurez aucun droit d'écriture dans le conteneur.
    2. Certaines applications nécessitent un répertoire `/home/`, comme vous n'avez pas de nom, vous n'en avez pas.

##### Vous identifier comme vous même

Loggez vous avec votre `uid:gid` dans le conteneur et ajoutez d'autres volumes, vous pourrez ainsi utiliser votre compte de votre machine local dans votre conteneur.

!!! docker "Docker"
    ```shell
    docker run -it \
    --user=$(id -u $USER):$(id -g $USER) \
    --env="DISPLAY" \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    votre_image_docker
    ```

L'avantage de cette méthode est que vous aurez un répertoire `/home/` dans votre conteneur.

#### La méthode isolée

Il existe un autre moyen d'émuler la même technique avec la méthode précédente mais de manière plus isolée. Nous pouvons le faire avec quelques modifications à l'image originale en créant un utilisateur avec `uid` et `gid` correspondant à celui de l'utilisateur hôte. Ceci est un exemple de ce que vous pouvez avoir besoin d'ajouter au Dockerfile.

!!! docker "Docker"
    ```docker
    #Add new sudo user
    ENV USERNAME myNewUserName
    RUN useradd -m $USERNAME && \
    echo "$USERNAME:$USERNAME" | chpasswd && \
    usermod --shell /bin/bash $USERNAME && \
    usermod -aG sudo $USERNAME && \
    echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
    chmod 0440 /etc/sudoers.d/$USERNAME && \
    # Replace 1000 with your user/group id
    usermod  --uid 1000 $USERNAME && \
    groupmod --gid 1000 $USERNAME
    ```

Vous pourriez avoir besoin de changer le nombre 1000 par votre `uid` et `gid` correspondante sur votre machine locale, mais la plupart du temps ces nombres correspondent. Pour les trouver, il suffit de lancer ces commandes unix.

!!! ubuntu "Bash"
    ```shell
    id -u vorph
    1000
    id -g vorph
    1000
    ```

Le suite est maintenant un peu plus compliquée. Il faut faire un fichier d'authentification X11 avec les bonnes permissions et de le monter dans volume que le conteneur va utiliser.

!!! docker "Docker"
    ```shell
    XSOCK=/tmp/.X11-unix
    XAUTH=/tmp/.docker.xauth
    touch $XAUTH
    xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

    docker run -it \
            --volume=$XSOCK:$XSOCK:rw \
            --volume=$XAUTH:$XAUTH:rw \
            --env="XAUTHORITY=${XAUTH}" \
            --env="DISPLAY" \
            -user="myNewUserName" \
    votre_image_docker
    ```

Maintenant, le conteneur est isolé avec seulement un accès en lecture et écriture à l'authentification X11 et au socket. L'inconvénient de tout cela est que certaines configurations spécifiques à l'utilisateur résident maintenant dans l'image elle-même, ce qui la rend moins portable. Si un autre utilisateur, même sur la même machine hôte, souhaite utiliser la même image, il devra : démarrer une session de terminal interactif avec le conteneur, changer l'`uid` et le `gid` pour qu'ils correspondent aux siens, livrer le conteneur à une nouvelle image, et lancer le conteneur désiré à partir de celle-ci. Faire ce va-et-vient ajoute également des couches inutiles à votre image.
