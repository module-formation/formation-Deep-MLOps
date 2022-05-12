# Just enough Linux to shine in society

Quasiment tous les outils utilisés pour DevOps ont d'abord été développés pour Linux puis porté sur Windows, souvent avec un lag important :

* Docker Linux : 2013,
* Docker for Windows : 2016.

!!! example "Exemple"

    * Ansible ne tourne pas sur Windows de façon native, mais peut tourner sur WSL2.
    * Kubernetes ne tourne pas sur Windows.

## Working with Shell

### `/home/` sweet `/home/`

Dès que l'on lance un terminal Linux, le premier répertoire dans lequel on se trouvera sera le répertoire principal, si vous avez comme nom d'utilisateur `vorphus`, votre terminal sera directmeent ouvert a répertoire `/home/vorphus`. Le répertoire `/home/user` est unique à chaque utilisateur.

On peut taper la commande `pwd` dans le terminal pour voir dans quel répertoire l'on se trouve.

On a deux types de commandes dans le Shell :

* **Les commandes internes** : `echo`, `cd`, `pwd`, `mkdir`, `set e.t.c`, qui sont fournies avec le Shell.
* **Les commandes externes** : `mv`, `date`, `uptime`, `cp`, qui sont des fichiers binaires ou scripts distincts qui sont appelées par le Shell.

Pour déterminer si une commande est interne ou externe, on peut taper `type` suivi de la commande.

```shell
❯ type mv
mv is /usr/bin/mv
❯ type echo
echo is a shell builtin
```

### Commandes basiques

|             Commande              |                 Résultat                 |
| :-------------------------------: | :--------------------------------------: |
|              `echo`               |           print a line of text           |
|               `ls`                |          list files and folders          |
|               `cd`                |             change directory             |
|              `mkdir`              |            create a directory            |
|              `touch`              |              create a file               |
| `mv new_file.txt sample_file.txt` | move `new_file.txt` to `sample_file.txt` |
|               `pwd`               |   print the present working directory    |
|`cat file.txt`|show the content of `file.txt`|

Des commandes succéssives peuvent être lancées avec le point virgule.

```sh title="Commandes succéssives"
cd new_dir; mkdir www; pwd
```

```sh title="Création de plusieurs répertoires en une seule fois"
mkdir France Angleterre Belgique
```

Les commandes du type

```sh
mkdir /tmp/europe
mkdir /tmp/europe/france
mkdir /tmp/europe/france/lille
```
peuvent se simplifier en une seule ligne via l'argument `-p` permettant de créer de façon récurrente les parents. On a ainsi la commande suivante.

```sh title="Commande simplifée, création directe de dossiers parents"
mkdir -p /tmp/europe/france/lille
```

De même pour la suppression/copie récursive des données avec `-r`.

```sh title="suppression récursive"
rm -r /tmp/europe/france/lille
```

```sh title="copie récursive"
cp -r my_dir1 /tmp/my_dir1
```

* `tree /home/vorph/test_dir`


### Chemins absolus et relatifs

* `/home/vorphus/test` est un chemin absolu. Un chemin absolu spécifie le chemin du répertoire, ou du dossier, depuis le dossier root `/`.

* Si on est dans le "home directory" `/home/vorphus`, alors `test` est un chemin relatif au répertoire dans lequel on se trouve déjà.

### Protip : `pushd` & `popd`

La commande `pushd` permet de mettre en cache l'adresse du répertoire où l'on se trouve actuellement avant de changer de répertoire. On peut alors y revenir avec `popd`.

Si l'on est dans `/home/vorph`, `pushd /etc` nous amène au répertoire `/etc`, tout en mettant `/home/vorph` en haut de la pile des répertoires.

### Obtenir de l'aide sur les commandes

On a plusieurs moyen d'obtenir de l'aide sur les commandes Linux et ce qu'elles sont sensées faire.

* On peut utiliser la commande `whatis` pour une décription succinte.

```shell
❯ whatis mv
mv (1)               - move (rename) files
❯ whatis cp
cp (1)               - copy files and directories
```

* On peut lire le manuel de la commande avec `man`.


```shell
❯ man mv
MV(1)                     UserCommands                           MV(1)

NAME
       mv - move (rename) files

SYNOPSIS
       mv [OPTION]... [-T] SOURCE DEST
       mv [OPTION]... SOURCE... DIRECTORY
       mv [OPTION]... -t DIRECTORY SOURCE...

DESCRIPTION
       Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.

       Mandatory arguments to long options are mandatory for short options too.

       --backup[=CONTROL]
              make a backup of each existing destination file

       -b     like --backup but does not accept an argument

       -f, --force
              do not prompt before overwriting

       -i, --interactive
              prompt before overwrite
...
```

* Certaines commandes fournissent une aide via la commande `--help`.

```shell
❯ mv --help
Utilisation : mv [OPTION]... [-T] SOURCE DEST
         ou : mv [OPTION]... SOURCE... RÉPERTOIRE
         ou : mv [OPTION]... -t RÉPERTOIRE SOURCE...
Renommer SOURCE en DEST, ou déplacer le ou les SOURCEs vers RÉPERTOIRE.

Les arguments obligatoires pour les options longues le sont aussi pour les
options courtes.
      --backup[=CONTROL]       archiver chaque fichier de destination existant
  -b                           identique à --backup mais sans argument
  -f, --force                  ne pas demander de confirmation avant d'écraser
  -i, --interactive            demander confirmation avant d'écraser
  -n, --no-clobber             ne pas écraser les fichiers existants
...
```

* `apropos regex` fera une recherche dans toutes les pages de `man` pour trouver les commandes contenant la regex donnée.

### Shell types

Il existe différents types de Shell :

* Bourne Shell (Sh Shell)
* C Shell (csh ou tcsh)
* Korn Shell (ksh)
* Z Shell (zsh)
* Bourne again Shell (bash)

On se concentre sur Bash.

!!! info "Info"

    Pour voir quel shell est utilisé dans un terminal : `echo $SHELL`.

* `alias dt=date`
* `history`
* `env`
* `export`

Pour que les variables d'environnement persistent, il faut les rentrer dans `~/.profile` ou `~/.pam_environment`.

* `which`
* `export PATH=$PATH:/opt/....`

Pour customiser le bash prompt, il faut modifier la variable d'environnement `PS1`.

Update Bob's prompt so that it displays the date as per the format below:

Example: [Wed Apr 22]bob@caleston-lp10:~$
Make sure the change is made persistent.

Run `PS1='[\d]\u@\h:\w$'` and add this to the `~/.profile` file `echo 'PS1="[\d]\u@\h:\w$"' >> ~/.profile`.

## Linux Core concepts

### Le noyau Linux

Le noyau Linux (Linux kernel) est la composante principale du système d'exploitation, le noyau fait l'interface princiaple entre la partie hardware et software

``` mermaid
graph LR

  subgraph Software
  B[Applications/Processus]
  end

  A[Linux Kernel]

  subgraph Hardware
  C1[Mémoire]

  C2[CPU/GPU]

  C3[Devices]
  end

  A<-..->B

  A<-..->C1 & C2 & C3
```

Le noyau Linux est responsable des 4 tâches principales suivantes :

* gestion de la mémoire,
* gestion des processus, quel processus peut utiliser le CPU/GPU, comment, quand, et pour combien de temps,
* drivers des périphériques,
* sécurité et gestion des appels systèmes.

**Le noyau Linux est monolithique**, ces tâches sont faites par lui même et non déléguées.

**Le noyau Linux est aussi modulaire**, ces compétences peuvent être étendues par l'ajout de modules.

#### Version du noyau

Pour avoir le nom du noyau, on peut taper la commande `uname`, qui ne produit que peu d'informations.

```shell
❯ uname
Linux
```

Pour voir la version du noyau utilisé, taper `uname -r` ou `uname -a`.

```shell
❯ uname -r
5.13.0-40-generic
❯ uname -a
Linux vorph-maison 5.13.0-40-generic #45~20.04.1-Ubuntu SMP Mon Apr 4 09:38:31 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux
```

* 5 = Version du noyau,
* 13 = Version majeure,
* 0 = Version mineure,
* 40 = patch release,
* generic = information spécifique à la distribution.

Pour plus d'informations, aller voir sur [kernel.org](https://kernel.org) qui recense le code source de toutes les versions du noyau Linux disponibles.

### Espace kernel et espace utilisateur

Voyons maintenant comment la mémoire est gérée dans un OS Linux.

La mémoire est divisée est deux espaces séparés, l'espace kernel et l'espace utilisateur.

L'espace kernel est la partie de la mémoire dans laquelle le noyau provisionne et éxecute ses services, un processus tournant dans l'espace noyau à un accès illimité au hardware.

Tous les processus tournant hors de l'espace noyau tournent dans l'esapce utilisateur, qui a un accès restreint au CPU/GPU et à la mémoire.


``` mermaid
graph LR

  subgraph Kernel space
  A[Linux Kernel]
  B[Device drivers]
  end


  subgraph User space
  C[Applications/Processus]
  end
```

kernel space :

* kernel code,
* kernel extensions,
* devices drivers.

User space :

* C,
* Java,
* Python,
* Ruby,
* Docker containers,
* etc.


Lorsqu'une application dans l'esapce utilisateur tourne et qu'elle a besoin d'accéder au hardware pour par exemple :

* ouvrir un fichier,
* écrire dans un fichier,
* définir une variable,
* etc,

l'esapce utilisateur produit un "system call" à l'espace kernel qui lui fournit les ressources nécessaires via les drivers.

``` mermaid
graph LR

  subgraph Kernel space
  A[Linux Kernel]
  B[Device drivers]
  end

  subgraph User space
  C[Applications/Processus]
  end

  D[Hardware]

  C-.->|System Call|B-.->D
```

### Linux et hardware

Comment Linux identifie le hardware dans son OS.

Prenons l'exemple d'une clé usb branchés sur un pc avec un OS Linux.

1. Dès que la clé usb est branchée, le driver correspondant dans le kernel space détecte un changement d'état et génère un évènementt, appelé `uevent`.
2. Cet évènement est envoyé au "user space device manager daemon", appelé `udev`.
3. `udev` crée alors de façon dynamique un noeud de device correspondant à la clé usb se trouvant dans le système de fichier `/dev` et lui assigne le nom `sdb1`.
4. Une fois ces étapes faites, la clé usb et son contenu seront listés comme `/dev/sdb1`.

!!! atention "Attention"

    `/dev/sdb1` n'est pas un répertoire, c'est l'adresse que l'OS Linux assigne à la clé usb. Tenter de faire un `cd ` vous donnera l'erreur suivante.

    ```shell
    ❯ cd /dev/sdb1
    cd: n'est pas un dossier: /dev/sdb1
    ```

``` mermaid
graph LR
  subgraph Extérieur
  A[Clé USB]
  B[PC]
  end

  subgraph Kernel space
  C[Device driver]
  end

  subgraph User space
  D[udev]
  end

  E[/ /dev/sdb1 /]

  A-.->B-.->C
  C-.->|uevents|D-.->E
```

Comment avoir des infos sur les composants hardware ?

* `dmesg` (pour l'anglais "display message") est une commande sur les systèmes d'exploitation de type Unix qui affiche la mémoire tampon de message du noyau. Quand un système Linux boot, il y a de nombreux messages qui peuvent ou non s'afficher (suivant votre OS), ces messages contiennent des logs du hardware

* `udevadm info` requète la db de `udev` pour des infos concernant les périphériques.

* `udevadm monitor` est à l'écoute de nouveaux `uevent`, et les affichera dans le terminal.

!!! example "Exemple"

    Voici ce qui se passe avant et après avoir branché un disque usb avec `udevadm monitor`.


    ```shell title="avant"
    ❯ udevadm monitor
    monitor will print the received events for:
    UDEV - the event which udev sends out after rule processing
    KERNEL - the kernel uevent
    ```


    ```shell title="après"
    ❯ udevadm monitor
    monitor will print the received events for:
    UDEV - the event which udev sends out after rule processing
    KERNEL - the kernel uevent

    KERNEL[13256.354009] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1 (usb)
    KERNEL[13256.354885] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0 (usb)
    KERNEL[13256.355001] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1 (usb)
    UDEV  [13256.362347] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1 (usb)
    KERNEL[13256.366283] add      /devices/virtual/workqueue/scsi_tmf_6 (workqueue)
    KERNEL[13256.366319] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6 (scsi)
    KERNEL[13256.366327] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/scsi_host/host6 (scsi_host)
    KERNEL[13256.366342] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0 (usb)
    KERNEL[13256.366353] add      /bus/usb/drivers/usb-storage (drivers)
    KERNEL[13256.366361] add      /module/usb_storage (module)
    UDEV  [13256.367136] add      /devices/virtual/workqueue/scsi_tmf_6 (workqueue)
    KERNEL[13256.367352] add      /bus/usb/drivers/uas (drivers)
    KERNEL[13256.367364] add      /module/uas (module)
    UDEV  [13256.367427] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0 (usb)
    UDEV  [13256.367778] add      /bus/usb/drivers/usb-storage (drivers)
    UDEV  [13256.367788] add      /module/usb_storage (module)
    UDEV  [13256.367794] add      /bus/usb/drivers/uas (drivers)
    UDEV  [13256.368248] add      /module/uas (module)
    UDEV  [13256.370659] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1 (usb)
    UDEV  [13256.371298] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6 (scsi)
    UDEV  [13256.371888] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/scsi_host/host6 (scsi_host)
    UDEV  [13256.372727] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0 (usb)
    KERNEL[13257.370058] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0 (scsi)
    KERNEL[13257.370127] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0 (scsi)
    KERNEL[13257.370157] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_device/6:0:0:0 (scsi_device)
    KERNEL[13257.370315] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_disk/6:0:0:0 (scsi_disk)
    KERNEL[13257.370379] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_generic/sg4 (scsi_generic)
    KERNEL[13257.370562] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/bsg/6:0:0:0 (bsg)
    UDEV  [13257.373300] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0 (scsi)
    UDEV  [13257.374079] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0 (scsi)
    UDEV  [13257.374986] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_device/6:0:0:0 (scsi_device)
    UDEV  [13257.375082] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_disk/6:0:0:0 (scsi_disk)
    UDEV  [13257.375095] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/bsg/6:0:0:0 (bsg)
    UDEV  [13257.375197] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/scsi_generic/sg4 (scsi_generic)
    KERNEL[13257.392547] add      /devices/virtual/bdi/8:48 (bdi)
    UDEV  [13257.393077] add      /devices/virtual/bdi/8:48 (bdi)
    KERNEL[13257.426707] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/block/sdd (block)
    KERNEL[13257.426733] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/block/sdd/sdd1 (block)
    KERNEL[13257.482588] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0 (scsi)
    UDEV  [13257.602272] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/block/sdd (block)
    UDEV  [13257.851325] add      /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0/block/sdd/sdd1 (block)
    UDEV  [13257.851983] bind     /devices/pci0000:00/0000:00:14.0/usb1/1-13/1-13.1/1-13.1:1.0/host6/target6:0:0/6:0:0:0 (scsi)
    KERNEL[13266.337010] add      /devices/virtual/bdi/8:49-fuseblk (bdi)
    UDEV  [13266.339098] add      /devices/virtual/bdi/8:49-fuseblk (bdi)
    ```

* `lspci` liste tous les périphériques du "[bus pci](https://fr.wikipedia.org/wiki/PCI_(informatique))" du pc, ie les fameuses cartes qui s'enfichent dans la carte mère (GPU, carte réseau, RAM etc.)

```shell
❯ lspci

00:00.0 Host bridge: Intel Corporation Device 9b33 (rev 05)
00:01.0 PCI bridge: Intel Corporation Xeon E3-1200 v5/E3-1500 v5/6th Gen Core Processor PCIe Controller (x16) (rev 05)
00:08.0 System peripheral: Intel Corporation Xeon E3-1200 v5/v6 / E3-1500 v5 / 6th/7th/8th Gen Core Processor Gaussian Mixture Model
00:12.0 Signal processing controller: Intel Corporation Comet Lake PCH Thermal Controller
00:14.0 USB controller: Intel Corporation Comet Lake USB 3.1 xHCI Host Controller
00:14.2 RAM memory: Intel Corporation Comet Lake PCH Shared SRAM
00:14.3 Network controller: Intel Corporation Wi-Fi 6 AX201
00:16.0 Communication controller: Intel Corporation Comet Lake HECI Controller
00:17.0 SATA controller: Intel Corporation Device 06d2
00:1c.0 PCI bridge: Intel Corporation Device 06b8 (rev f0)
00:1c.4 PCI bridge: Intel Corporation Device 06bc (rev f0)
00:1f.0 ISA bridge: Intel Corporation Device 0685
00:1f.3 Audio device: Intel Corporation Comet Lake PCH cAVS
00:1f.4 SMBus: Intel Corporation Comet Lake PCH SMBus Controller
00:1f.5 Serial bus controller [0c80]: Intel Corporation Comet Lake PCH SPI Controller
01:00.0 VGA compatible controller: NVIDIA Corporation Device 2204 (rev a1)
01:00.1 Audio device: NVIDIA Corporation Device 1aef (rev a1)
02:00.0 USB controller: ASMedia Technology Inc. Device 3241
03:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8125 2.5GbE Controller (rev 04)
```

## Vi

Installé par défaut dans la plupart des distributions Linux.

Deux modes :

* **mode commande** : copier coller suppression, mais pas d'écriture possible,
* **mode insertion** : nécessaire pour écrire du contenu dans un fichier.

!!! info "Info"

    Pour activer le mode insertion dans Vi, appuyez sur la touche `i`. Pour revenir au mode commande, il faut appuyer sur la touche echap `esc`.

### Commandes basiques

|   Commande    |                  Résultat                  |
| :-----------: | :----------------------------------------: |
|      `x`      |           supprime un caractère            |
|     `dd`      |         supprime la ligne entière          |
|     `yy`      |               copie la ligne               |
|      `p`      |               colle le ligne               |
|  `ctrl + u`   |            scrolle ver le haut             |
|  `ctrl + d`   |            scrolle vers le bas             |
|      `:`      |        affiche l'invite de commande        |
|     `:w`      |           sauvegarde le fichier            |
| `:w filename` | sauvegarde le fichier sous le nom filename |
|     `:q`      |           quitte l'éditeur `vi`            |
|     `:wq`     |           sauvegarder et quitter           |
|   `/string`   |    recherche le `string` dans le texte     |
|      `n`      |   va à l'occurence suivante du `string`    |

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

    `yum install ansible` installera `ansible` et l'ensemble de ses dépendances, par exemple `python`, `pyYAML`, `sshpass`.

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
### Exemple

Supposons que l'on souhaite configurer l'API suivante comme un service.

```python title="my_app.py"
--8<-- "./includes/my_app.py"
```

si on la lance via la commande suivante.


```shell
/home/vorph/miniconda3/envs/api/bin/python -m my_app
```
On peut alors tester qu'elle marche bien en faisant une requête `GET`, par exemple avec [httpie](https://httpie.io/).

```shell
❯ http 127.0.0.1:8001/hello/

HTTP/1.1 200 OK
content-length: 9
content-type: application/json
date: Wed, 04 May 2022 09:00:35 GMT
server: uvicorn

"Hello !"
```
!!! info "Remarque"

    Le fais d'utiliser un chemin absolu `/home/vorph/miniconda3/envs/api/bin/python` pour lancer python est important et sera utilisé par la suite, pour connaitre le chemin complet de votre executable python, vous pouvez utiliser la commande suivante dans un terminal.


    ```
    ❯ which python

    /home/vorph/miniconda3/envs/api/bin/python
    ```

    Il sera aussi utile par la suite de connaître le chemin absolu de `my_app.py`, on peut le connaître en utilisant la commande [`readlink`](https://stackoverflow.com/questions/5265702/how-to-get-full-path-of-a-file).


    ```shell
    ❯ readlink -f my_app.py

    /media/vorph/datas/formation-Deep-MLOps/includes/my_app.py
    ```

    Evidemment, la commande `readlink` nécessite que vous soyez dans le répertoire où se trouve `my_app.py` pour pouvoir lire le chemin absolu.

!!! info "Remarque"

    Il n'est pas nécessaire de laisser les lignes suivantes à la fin de `my_app.py`.

    ```python
    if __name__ == "__main__":
        uvicorn.run("my_app:app", host="127.0.0.1", port=8001, log_level="info")
    ```

    On pourrait très bien les enlever, mais dans ce cas là, il faudrait activer le bon environnement virtuel puis lancer la commande suivante.

    ```shell
    uvicorn my_app:app --reload --port 8001
    ```

    Ce qui fait deux actions plutôt qu'une, cela sera plus pratique pour la suite.

    Autres références :

    * [Python script in systemd: virtual environment or real environment](https://stackoverflow.com/questions/60959081/python-script-in-systemd-virtual-environment-or-real-environment)



L'idée de la configurer comme un service est que l'on pourra alors utiliser `systemctl` pour la lancer et l'arrêter via les commandes `systemctl start my_app` et `systemctl stop my_app`.

De cette façon l'administrateur du serveur n'a pas besoin de se soucier du chemin où se trouve l'API, ou même du langage dans lequel est codée cette API, il sait que c'est un service qu'il peut lancer et stopper à sa guise. Il sera même possible de la lancer de façon automatique de début de chaque démarrage du serveur, ou de la relancer si le serveur crash.

Pour pouvoir lancer un script python comme un service, par exemple avec les commande `systemctl start my_app`, `systemctl stop my_app`, `my_app` faisant référence au nom que l'on souhaite assigner au service, pour faire simple on le nommera de la même façon que le script python dont il est issu.

On doit alors configurer ce script comme un service `systemd` en définissant un "*systemd unit file*" dans `/etc/systemd/system`. On définit le fichier systemd suivant.

```toml title="/etc/systemd/system/my_app.serivce"
--8<-- "./includes/my_app.service"
```

Une fois le fichier créé dans `/etc/systemd/system`, il est nécessaire de redémarrer le processus systemd en lançant la commande suivante.

`systemctl daemon-reload`

Seulement de cette façon le nouveau service configuré sera pris en compte dans `/etc/systemd/system`, il suffit alors de le nouveau service lancer via `systemctl start my_app` pour qu'il démarre. On peut alors vérifier qu'il fonctionne en faisant la réquête suivante.

```shell
❯ curl http://127.0.0.1:8001/hello/

"Hello !"
```

!!! attention "Attention"

    Les chemins utilisés dans un ficheier `.service` **doivent toujours être des chemins absolus**. Les chemins relatifs ne fonctionnent pas.


```shell
❯ systemctl status my_app
● my_app.service
     Loaded: loaded (/etc/systemd/system/my_app.service; static; vendor preset: enabled)
     Active: active (running) since Wed 2022-05-04 14:22:11 CEST; 1min 39s ago
   Main PID: 134295 (python)
      Tasks: 3 (limit: 76995)
     Memory: 1.7G
     CGroup: /system.slice/my_app.service
             ├─134295 /home/vorph/miniconda3/envs/api/bin/python /opt/perso/my_app.py
             ├─134780 /home/vorph/miniconda3/envs/api/bin/python -c from multiprocessing.resource_tracker import ma>
             └─134781 /home/vorph/miniconda3/envs/api/bin/python -c from multiprocessing.spawn import spawn_main; s>

mai 04 14:22:11 vorph-maison systemd[1]: Started my_app.service.
mai 04 14:22:11 vorph-maison python[134295]: INFO:     Will watch for changes in these directories: ['/']
mai 04 14:22:11 vorph-maison python[134295]: INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to qu>
mai 04 14:23:43 vorph-maison python[134295]: error walking file system: OSError [Errno 40] Too many levels of symbo>
mai 04 14:23:43 vorph-maison python[134295]: INFO:     Started reloader process [134295] using watchgod
mai 04 14:23:44 vorph-maison python[134781]: INFO:     Started server process [134781]
mai 04 14:23:44 vorph-maison python[134781]: INFO:     Waiting for application startup.
mai 04 14:23:44 vorph-maison python[134781]: INFO:     Application startup complete.
mai 04 14:23:44 vorph-maison python[134781]: INFO:     127.0.0.1:55460 - "GET /hello/ HTTP/1.1" 200 OK
```

Pour la stopper, il suffit de lancer `systemctl stop my_app`.

Comment configurer le service pour qu'il se lance automatiquement au démarrage du serveur ? C'est la partie `[Install]` du fichier `my_app.service` qui le définit. La partie `WantedBy=multi-user.target` désigne que se service doit être lancé dès le démarrage. Pour que ce paramètre soit pris en compte, il est alors nécessaire de lancer la commande suivante.

`systemctl enable my_app`

Approfondir :

* [Why do most systemd examples contain WantedBy=multi-user.target?](https://unix.stackexchange.com/questions/506347/why-do-most-systemd-examples-contain-wantedby-multi-user-target)
* [Systemd service - what is `multi-user.target`](https://unix.stackexchange.com/questions/404667/systemd-service-what-is-multi-user-target?noredirect=1&lq=1)
* [Systemd Services 101](https://gist.github.com/leommoore/ea74061dc3bb086f36d42666a6153e0c)
* [systemd 101](https://docs.google.com/presentation/d/10YwWZdBa3ffl7kVa2p21L9VqET2CRmVoWJpVBW6ujgg/htmlpresent)
* [Systemd – Easy as 1, 2, 3](https://people.redhat.com/bbreard/presos/Systemd-101.pdf)
* [Comment utiliser Systemctl pour gérer les services et les unités de Systemd](https://www.digitalocean.com/community/tutorials/how-to-use-systemctl-to-manage-systemd-services-and-units-fr)
* [systemd.service — Service unit configuration](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

### Placer votre code dans `/opt/`

Dans la plupart des systèmes d'exploitations Linux, il existe un répertoire nommé `/opt/`. Ici `/opt/` peut se comprendre comme "option" ou "optionnal", pour citer la réponse StackOverflow de [What does "opt" mean (as in the "opt" directory)? Is it an abbreviation?](https://stackoverflow.com/questions/12649355/what-does-opt-mean-as-in-the-opt-directory-is-it-an-abbreviation) :

!!! quote


    In the old days, `/opt` was used by UNIX vendors like AT&T, Sun, DEC and 3rd-party vendors to hold "Option" packages; i.e. packages that you might have paid extra money for. I don't recall seeing `/opt` on Berkeley BSD UNIX. They used `/usr/local` for stuff that you installed yourself.

    But of course, the true "meaning" of the different directories has always been somewhat vague. That is arguably a good thing, because if these directories had precise (and rigidly enforced) meanings you'd end up with a proliferation of different directory names.

    The Filesystem Hierarchy Standard says this about `/opt/*`:

    * "/opt is reserved for the installation of add-on application software packages."

    By contrast it says this about `/usr/local/*`:

    * "The /usr/local hierarchy is for use by the system administrator when installing software locally."

    These days, `/usr/local/*` is typically used for installing software that has been built locally, possibly after tweaking configuration options, etcetera.

En d'autres termes :

* Si votre programme est programmé dans un langage compilé, par exemple le C++ ou le Rust, et que vous le compilez, alors vous devriez le placer dans `/usr/local/*`.
* Votre application est un binaire unique, alors vous le copierez dans /usr/local.
* Vous voulez utiliser une alternative d'un programme système existant construit à partir des sources en utilisant `make`. Dans ce cas, vous l'installerez dans /usr/local.
* Si vous déployez une application, et que par design, tous ses fichiers sont dans le même répertoire, alors on la déploiera dans un répertoire `/opt/my_app/`.

Cela ne reste que des conventions, mais elles sont largement utilisées et cela évite de se poser trop de questions sur où est tel application.

Dans le cas qui nous interesse ici, déployer notre API basique comme un service, il ne faudrait donc pas mettre

`ExecStart=/home/vorph/miniconda3/envs/api/bin/python /media/vorph/datas/formation-Deep-MLOps/includes/my_app.py`

Dans notre fichier `my_app.service`, mais copier notre api et toutes ses dépendances (eg Dockerfile, docker-compose, etc) dans un répertoire `/opt/code/` par exemple, et mettre

`ExecStart=/home/vorph/miniconda3/envs/api/bin/python /opt/code/my_app.py`

dans `my_app.service`.

!!! summary "TLDR"

    Pour créer un service à partir d'une application `my_app.py`:

    1. Mettre l'application dans un répertoire `/opt/code/my_app.py`.
    2. Définir un "systemd unit file" `/etc/systemd/system/my_app.service`.
    3. Relancer le démon `systemd` via `systemctl daemon-reload`.
    4. Lancer le service avec `systemctl start my_app`.
    5. Faire la configuration pour le lancement du service de façon automatique, si nécessaire.


* [What does /opt mean in Linux?](https://www.baeldung.com/linux/opt-directory)
* [Linux : Directory /opt vs /usr/local](http://www.extradrm.com/?p=2266)
* [What does "opt" mean (as in the "opt" directory)? Is it an abbreviation?](https://stackoverflow.com/questions/12649355/what-does-opt-mean-as-in-the-opt-directory-is-it-an-abbreviation)