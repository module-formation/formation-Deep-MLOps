# Just enough Linux for DevOps

Quasiment tous les outils utilisés pour DevOps ont d'abord été développés pour Linux puis porté sur Windows, souvent avec un lag important :

* Docker Linux : 2013,
* Docker for Windows : 2016.

!!! example "Exemple"

    * Ansible ne tourne pas sur Windows de façon native, mais peut tourner sur WSL2.
    * Kubernetes ne tourne pas sur Windows.

## Shell types

* Bourne Shell (Sh Shell)
* C Shell (csh ou tcsh)
* Z Shell (zsh)
* Bourne again Shell (bash)

!!! info "Info"

    Pour voir quel shell est utilisé dans un terminal : `echo $SHELL`.

* `echo` : print a line of text.
* `ls` : list files and folders.
* `cd` : change directory.
* `pwd`
* `mkdir`
* `touch`

Commande multiples avec le point virgule

```sh
cd new_dir; mkdir www; pwd
```

```sh
mkdir /tmp/europe
mkdir /tmp/europe/france
mkdir /tmp/europe/france/lille
```

peut se simplifier en une seule ligne via l'argument `-p` permettant de créer de façon récurrente les parents.

```sh
mkdir -p /tmp/europe/france/lille
```

```sh
rm -r /tmp/europe/france/lille
```

```sh
cp -r my_dir1 /tmp/my_dir1
```

* `cat > file.txt`
* `mv new_file.txt sample_file.txt`
* `tree /home/vorph/test_dir`

## Vi

Installé par défaut dans la plupart des dirtibutions Linux.

Deux modes :

* mode commande : copier coller suppression, mais pas d'écriture possible,
* mode insertion : nécessaire pour écrire du contenu dans un fichier.

!!! info "Info"

    Pour activer le mode insertion dans Vi, appuyez sur la touche `i`. Pour revenir au mode commande, il faut appuyer sur la touche echap `esc`.

### Commandes basiques

* `x` : supprime un caractère.
* `dd` : supprime la ligne entière
* `yy` : copie la ligne.
* `p` : colle le ligne.
* `ctrl + u` : scrolle ver le haut.
* `ctrl + d` : scrolle vers le bas.

* `:` : affiche l'invite de commande.
* `:w` : sauvegarde le fichier.
* `:w filename` : ssauvegarde le fichier sous le nom filename.
* `:q` : quitte l'éditeur `vi`.
* `:wq` : sauvegarder et quitter.

* `/string` : recherche le `string` dans le texte.
* `n` : va à l'occurence suivante du `string`.

## More Linux commands

* `whoami`
* `id`
* `su` : switch user
* `ssh user@hostname`

* `sudo ...` toujours un utilisateur classique, mais avec des privilèges root, liste dans `etc/sudoers`
* `wget http://www.url.com/some-file.txt -O some-file.txt`
* `curl http://www.url.com/some-file.txt -O`

* `ls /etc/*release*` : check OS version

```sh
❯ ls /etc/*release*
/etc/lsb-release   /etc/os-release

❯ cat /etc/os-release
NAME="Ubuntu"
VERSION="20.04.4 LTS (Focal Fossa)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 20.04.4 LTS"
VERSION_ID="20.04"
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
VERSION_CODENAME=focal
UBUNTU_CODENAME=focal
```

## Package Management

CentOS utilise RPM (Red Hat Package Manager), les softwares sont alors packagés sous la forme `telnet.rpm`, pour installer un tel package on tape alors la commande suivante.

```sh
rpm -i telnet.rpm
```

l'argument `-i` signifiant que l'on veut installer quelque chose. Pour supprimer un package, on tape

```sh
rpm -e telnet.rpm
```

et pour requêter la db sur un package particuliers, on a la commande suivante.

```sh
rpm -q telnet.rpm
```

`rpm` ne fait qu'installer le package qu'on lui a pointé, il n'installe aucune de ses dépendances ! Pour installer un package et l'ensemble de ses dépendances, on utilise `yum` qui est un surcouche de `rpm`.

!!! example "Exemple"

    `yum install ansible` installare `ansible` et l'ensemble de ses dépendances, par exemple `python`, `pyYAML`, `sshpass`.

Comment `yum` sait où sont localisées, ie dans quel repo, les dépendances d'un package ? L'ensemble des dépendances classiques sont listées dans `/etc/yum.repos.d`, c'est là que `yum` cherche en premier.

Pour voir la liste des repos disponibles sur un système CentOS, on tape la commande `yum repolist`.

* `ls /etc/yum.repos.d`
* `cat /etc/yum.repos.d/CentOS-Base.repo`

Pour l'ensemble des packages, par exemple `ansible`, disponible à l'installation, on peut taper la commande suivante.

* `yum list ansible`,
* `yum remove ansible` supprime le package,
* `yum --showduplicates list ansible` pour voir les différentes versions disponibles.
* `yum install ansible-2.4.2.0`

## Services

Dès qu'un software comme une DB, un webserveur ou Docker est installé sur une machine, il est configuré comme un *service*, pour que ce service marche, il doit être lancé.

* `service nom_du_service start` est la commande permattant de le lancer.

!!! example "Exemple"

    `service httpd start` lance un serveur apache.

Une méthode plus moderne de lancer un service est d'utiliser la commande `systemctl`.

* `systemctl start httpd`

`systemctl` est la commande utilisée pour manager les services sur un serveur managé par `systemd`.

* `systemctl stop httpd`

* `systemctl status httpd`

* `systemctl enable httpd` lance le service automatiquement quand le serveur boot.

* `systemctl disable httpd` désactive le service automatiquement quand le serveur boot.

!!! example "Exemple"

    ```sh
    ❯ systemctl status docker.service

    ● docker.service - Docker Application Container Engine
        Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
        Active: active (running) since Wed 2022-04-27 11:50:20 CEST; 3h 23min ago
    TriggeredBy: ● docker.socket
        Docs: https://docs.docker.com
    Main PID: 1719 (dockerd)
        Tasks: 87
        Memory: 167.7M
        CGroup: /system.slice/docker.service
                ├─ 1719 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
                ├─ 2034 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 3001 -container-ip 172.26.0.2 -co>
                ├─ 2041 /usr/bin/docker-proxy -proto tcp -host-ip :: -host-port 3001 -container-ip 172.26.0.2 -contain>
                ├─ 2055 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 5050 -container-ip 172.25.0.2 -co>
                ├─ 2062 /usr/bin/docker-proxy -proto tcp -host-ip :: -host-port 5050 -container-ip 172.25.0.2 -contain>
                ├─ 2103 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 5432 -container-ip 172.25.0.3 -co>
                ├─ 2111 /usr/bin/docker-proxy -proto tcp -host-ip :: -host-port 5432 -container-ip 172.25.0.3 -contain>
                ├─17675 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 49153 -container-ip 172.17.0.2 -c>
                └─17681 /usr/bin/docker-proxy -proto tcp -host-ip :: -host-port 49153 -container-ip 172.17.0.2 -contai>

    avril 27 11:50:19 vorph-maison dockerd[1719]: time="2022-04-27T11:50:19.614727941+02:00" level=info msg="No non-loc>
    avril 27 11:50:19 vorph-maison dockerd[1719]: time="2022-04-27T11:50:19.614743509+02:00" level=info msg="IPv6 enabl>
    avril 27 11:50:19 vorph-maison dockerd[1719]: time="2022-04-27T11:50:19.723169676+02:00" level=info msg="No non-loc>
    avril 27 11:50:19 vorph-maison dockerd[1719]: time="2022-04-27T11:50:19.723184792+02:00" level=info msg="IPv6 enabl>
    avril 27 11:50:20 vorph-maison dockerd[1719]: time="2022-04-27T11:50:20.260585965+02:00" level=info msg="Loading co>
    avril 27 11:50:20 vorph-maison dockerd[1719]: time="2022-04-27T11:50:20.310879570+02:00" level=info msg="Docker dae>
    avril 27 11:50:20 vorph-maison dockerd[1719]: time="2022-04-27T11:50:20.311527346+02:00" level=info msg="metrics AP>
    avril 27 11:50:20 vorph-maison dockerd[1719]: time="2022-04-27T11:50:20.312283730+02:00" level=info msg="Daemon has>
    ```

Pour pouvoir lancer un script python comme un service, par exemple avec les commande `systemctl start my_app` `systemctl stop my_app`, `my_app` faisant référence à un script `my_app.py`, on doit configurer ce script comme un service `systemd` en définissant un "systemd unit file" dans `/etc/systemd/system`.

Le nom du fichier sera ici `my_app.service`