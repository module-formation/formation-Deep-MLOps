# Les bases du réseau

## Networking 101

### Switching

Qu'est ce qu'un réseau ?

Supposons que nous ayons deux ordinateurs, VM, Cloud Center, etc A et B.

Comment A communique-t-il avec B ?

``` mermaid
graph LR
  A[PC A] -->|?| B[PC B];
  B[PC B] -->|?| A[PC A];
```

On les connecte tous les deux à un switch commun, et ce switch crée un réseau contenant A et B.

``` mermaid
graph LR
  A[PC A] --> C[switch];
  B[PC B] --> C[switch];
  C[switch] --> B[PC B];
  C[switch] --> A[PC A];
```

Pour pouvoir les connecter, on a besoin d'une interface, qu'elle soit physique ou virtuelle.

Pour connaître cette interface, on peut taper la commande `ip link`.

!!! example "Exemple"

    Sur mon pc, cela donne le résulat suivant.

    ```shell

    ❯ ip link
    2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
        link/ether 2c:f0:5d:d4:db:e6 brd ff:ff:ff:ff:ff:ff
    3: wlo1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DORMANT group default qlen 1000
        link/ether 9c:29:76:75:3f:aa brd ff:ff:ff:ff:ff:ff
        altname wlp0s20f3
    5: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
        link/ether 02:42:3a:62:5a:b9 brd ff:ff:ff:ff:ff:ff
    ```

[Dans la nomenclature Linux](https://www.linuxtricks.fr/wiki/nomenclature-des-interfaces-reseau-sous-linux-enp0s3-wlo1), `en` est le préfixe pour une interface ethernet, et `wl` pour une interface wifi.

Remarquons que Docker à sa propre interface `docker0` pour faire le lien entre les conteneurs et le reste du réseau.

!!! attention "Attention"

    Les nomenclatures peuvent quelque peu varier suivant les distributions, il n'est pas rare de voir `eth0` pour une interface ethernet.

Supposons que le réseau créé possède l'adresse $192.168.1.0$ et que A et B on deux interface ethernet nommé `enp3s0` et `enp3s1`.

``` mermaid
graph LR
  A[PC A <br/> enp3s0] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> enp3s1] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> enp3s1];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> enp3s0];
```

Pour ajouter les deux ordinateurs A et B, on leur assigne alors une adresse ip sur ce réseau, via la commande suivante.

* `ip addr add 192.168.1.10/24 dev enp3s0` pour A,
* `ip addr add 192.168.1.11/24 dev enp3s1` pour B.

``` mermaid
graph LR
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
```

Chacun des deux pc possède alors une adresse sur ce réseau et peut communiquer avec l'autre. Il est pas exemple possible depuis A de faire un `ping` vers B en tapant `ping 192.168.1.11`.

Les communications ici entre A et B se font via le switch. Le switch ne peut recevoir et envoyer des informations que depuis des interfaces faisant parties du réseau défini.

Mettons maintenant deux réseaux définis par deux switchs avec deux adresses ip différentes. Comment A peut-il communiquer avec C ?

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end
  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  A[PC A 192.168.1.10] -.->|?| D[PC C 192.168.2.10];
```

### Routing

C'est là qu'intervient le routeur. Un routeur permet de connecter deux réseaux ensembles. On peut le penser comme un serveur avec de multiples ports réseaux.

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  G[Routeur]-.-C[switch 192.168.1.0];
  G[Routeur]-.-E[switch 192.168.2.0];
```
Puisque le routeur connecte deux réseaux, il a deux adresses qui lui sont assignées : une pour l'identifier sur chaque réseau.

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch 192.168.2.0];
```

Maintenant que le routeur relie les deux réseaux, chacun des 4 pc peut communiquer l'un avec l'autre.

Quand le PC A veut envoyer un paquet au PC C, comment sait-il où est le routeur sur le réseau, pour envoyer le paquet via lui ? Le routeur n'est qu'un système supplémentaire sur le réseau, il peut y en avoir des centaines.

### Default Gateway

C'est là que l'on configure les systèmes avec une *gateway*, ou *passerelle*. Si un réseau est une chambre, alors la gateway est une porte pour communiquer vers l'extérieur.

Les systèmes ont besoin de savoir où est cette gateway pour pouvoir communiquer entre réseaux.

Pour voir les différentes **configuration de route**, ou **table de routage** d'un système, on peut alors taper la commande suivante.

`route`

!!! example "Exemple"

    Sur mon pc, cela donne le résultat suivant.

    ```shell
    ❯ route

    Table de routage IP du noyau
    Destination     Passerelle      Genmask         Indic Metric Ref    Use Iface
    default         livebox.home    0.0.0.0         UG    100    0        0 enp3s0
    link-local      0.0.0.0         255.255.0.0     U     1000   0        0 enp3s0
    172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
    192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 enp3s0
    ```

Dans notre exemple, si l'on tape cette commande, comme aucune passerelle n'a encore été définie, on obtiendra une table de routage vide.

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch 192.168.2.0];
```

```shell
❯ route

Table de routage IP du noyau
Destination     Passerelle      Genmask         Indic Metric Ref    Use Iface
```

Pour configurer une passerelle du PC B vers des systèmes du réseau 2, on tape alors la commande suivante.

`ip route add 192.168.2.0/24 via 192.168.1.1`

`via 192.168.1.1` définit la passerelle qui sera utilisée par le réseau 1 pour communiquer vers le réseau 2.

La table de routage du réseau 1 se mettra alors à jour.

```shell
❯ route

Table de routage IP du noyau
Destination     Passerelle      Genmask         Indic Metric Ref    Use Iface
192.168.2.0     192.168.1.1     255.255.255.0   U     100    0        0 eth0
```

!!! attention "Attention"

    Si l'on s'arette là, la communication ne va que dans un sens, du réseau 1 vers le réseau 2. Il faut aussi définir la passerelle pour aller dans l'autre sens.

cela se fait via `ip route add 192.168.1.0/24 via 192.168.2.1`.

Mais si maintenant le réseau 2 a besoin d'accéder à internet ? Par exemple à l'ip internet 172.217.194.0, qui est celle de Google (ça peut être utile) ?


``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch 192.168.2.0];

  subgraph Internet
  H{{Google 172.217.194.0}}
  end
```
Et bien on rajoute une nouvelle passerelle.

`ip route add 172.217.194.0/24 via 192.168.2.1`

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  subgraph Internet
  H1{{Google 172.217.194.0}};
  end

  G[Routeur]-.-|192.168.1.1|C[switch 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch 192.168.2.0];
  G[Routeur]-.-H1{{Google 172.217.194.0}};

```

Mais il y a des milliards de sites, on ne va quand même pas faire ça pour tous ?

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A 192.168.1.10] --> C[switch];
  B[PC B 192.168.1.11] --> C[switch];
  C[switch 192.168.1.0] --> B[PC B 192.168.1.11];
  C[switch 192.168.1.0] --> A[PC A 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C 192.168.2.10] --> E[switch];
  F[PC D 192.168.2.11] --> E[switch];
  E[switch 192.168.2.0] --> D[PC D 192.168.2.11];
  E[switch 192.168.2.0] --> F[PC C 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch 192.168.2.0];

  subgraph Internet
  H1{{Google 172.217.194.0}}
  H2{{Site 1}}
  H3{{Site 2}}
  H4{{...}}
  end
```
### Configuration du DNS sous Linux