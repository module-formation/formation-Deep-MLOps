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
  A[PC A <br/> 192.168.1.10] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> 192.168.1.11] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> 192.168.1.11];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> 192.168.1.10];
```

Chacun des deux pc possède alors une adresse sur ce réseau et peut communiquer avec l'autre. Il est pas exemple possible depuis A de faire un `ping` vers B en tapant `ping 192.168.1.11`.

Les communications ici entre A et B se font via le switch. Le switch ne peut recevoir et envoyer des informations que depuis des interfaces faisant parties du réseau défini.

Mettons maintenant deux réseaux définis par deux switchs avec deux adresses ip différentes. Comment A peut-il communiquer avec C ?

``` mermaid
graph TD
  subgraph réseau 1
  A[PC A <br/> 192.168.1.10] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> 192.168.1.11] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> 192.168.1.11];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> 192.168.1.10];
  end
  subgraph réseau 2
  D[PC C <br/> 192.168.2.10] --> E[switch <br/> 192.168.2.0];
  F[PC D <br/> 192.168.2.11] --> E[switch <br/> 192.168.2.0];
  E[switch <br/> 192.168.2.0] --> D[PC D <br/> 192.168.2.11];
  E[switch <br/> 192.168.2.0] --> F[PC C <br/> 192.168.2.10];
  end

  A[PC A <br/> 192.168.1.10] -.->|?| D[PC C <br/> 192.168.2.10];
```

### Routing

C'est là qu'intervient le routeur. Un routeur permet de connecter deux réseaux ensembles. On peut le penser comme un serveur avec de multiples ports réseaux.

``` mermaid
graph LR
  subgraph réseau 1
  A[PC A <br/> 192.168.1.10] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> 192.168.1.11] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> 192.168.1.11];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C <br/> 192.168.2.10] --> E[switch <br/> 192.168.2.0];
  F[PC D <br/> 192.168.2.11] --> E[switch <br/> 192.168.2.0];
  E[switch <br/> 192.168.2.0] --> D[PC D <br/> 192.168.2.11];
  E[switch <br/> 192.168.2.0] --> F[PC C <br/> 192.168.2.10];
  end

  G[Routeur]-.-C[switch <br/> 192.168.1.0];
  G[Routeur]-.-E[switch <br/> 192.168.2.0];
```
Puisque le routeur connecte deux réseaux, il a deux adresses qui lui sont assignées : une pour l'identifier sur chaque réseau.


``` mermaid
graph LR
  subgraph réseau 1
  A[PC A <br/> 192.168.1.10] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> 192.168.1.11] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> 192.168.1.11];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C <br/> 192.168.2.10] --> E[switch <br/> 192.168.2.0];
  F[PC D <br/> 192.168.2.11] --> E[switch <br/> 192.168.2.0];
  E[switch <br/> 192.168.2.0] --> D[PC D <br/> 192.168.2.11];
  E[switch <br/> 192.168.2.0] --> F[PC C <br/> 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch <br/> 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch <br/> 192.168.2.0];
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
  A[PC A <br/> 192.168.1.10] --> C[switch <br/> 192.168.1.0];
  B[PC B <br/> 192.168.1.11] --> C[switch <br/> 192.168.1.0];
  C[switch <br/> 192.168.1.0] --> B[PC B <br/> 192.168.1.11];
  C[switch <br/> 192.168.1.0] --> A[PC A <br/> 192.168.1.10];
  end

  subgraph réseau 2
  D[PC C <br/> 192.168.2.10] --> E[switch <br/> 192.168.2.0];
  F[PC D <br/> 192.168.2.11] --> E[switch <br/> 192.168.2.0];
  E[switch <br/> 192.168.2.0] --> D[PC D <br/> 192.168.2.11];
  E[switch <br/> 192.168.2.0] --> F[PC C <br/> 192.168.2.10];
  end

  G[Routeur]-.-|192.168.1.1|C[switch <br/> 192.168.1.0];
  G[Routeur]-.-|192.168.2.1|E[switch <br/> 192.168.2.0];
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

La table de routage aura alors une nouvelle route.

```shell
❯ route

Table de routage IP du noyau
Destination     Passerelle      Genmask         Indic Metric Ref    Use Iface
192.168.2.0     192.168.1.1     255.255.255.0   U     100    0        0 eth0
172.217.194.0   192.168.2.1     255.255.255.0   U     0      0        0 eth0
```

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
  G[Routeur]-.-H1{{Google 172.217.194.0}};

  subgraph Internet
  H1{{Google 172.217.194.0}}
  H2{{Site 1}}
  H3{{Site 2}}
  H4{{...}}
  end
```

Plutôt que d'ajouter une nouvelle route pour chaque adresse ip, on peut simplement dire "pour chaque réseau dont je ne connais pas la route, utilise ce routeur comme passerelle par défaut".

`ip route add default via 192.168.2.1`

Ainsi, toute requête alors vers un réseau inconnu passe par ce routeur particuliers.


!!! example "Exemple"

    Sur mon pc, la passerelle par défaut est `livebox.home`, qui est ma box internet, ce qui est cohérent car c'est elle qui fait la jonction entre mon réseau local et internet.

    ```shell
    ❯ route

    Table de routage IP du noyau
    Destination     Passerelle      Genmask         Indic Metric Ref    Use Iface
    default         livebox.home    0.0.0.0         UG    100    0        0 enp3s0
    link-local      0.0.0.0         255.255.0.0     U     1000   0        0 enp3s0
    172.17.0.0      0.0.0.0         255.255.0.0     U     0      0        0 docker0
    192.168.1.0     0.0.0.0         255.255.255.0   U     100    0        0 enp3s0
    ```

    Notons qu'à la place de `default` comme destination, on aurait pu avoir `0.0.0.0`, ce qui revient au même puisque `0.0.0.0` signifie "n'importe quelle adresse ip".

    Lorsque l'on voit `0.0.0.0` dans la section passerelle, cela signifie simplement que l'on a pas besoin de passerelle pour accéder à ce réseau.

Comment définir un system Linux comme routeur ? Prenons la situation suivante.

``` mermaid
graph LR
  subgraph A
  A1[eth0 <br/> 192.168.1.5];
  end

  subgraph B
  B1[eth0 <br/> 192.168.1.6];
  B2[eth1 <br/> 192.168.2.6];
  end

  subgraph C
  C1[eth0 <br/> 192.168.2.5];
  end

  A1[eth0 <br/> 192.168.1.5]-.-|192.168.1.0|B1[eth0 <br/> 192.168.1.6]
  B2[eth1 <br/> 192.168.2.6]-.-|192.168.2.0|C1[eth0 <br/> 192.168.2.5]
```

On a un système Linux B avec deux interfaces, chacune connectant un autre système Linux. Donc B est connecté aux 2 réseaux, et a donc une ip sur chaque réseau.

!!! question "Question"

    Comment A peut-il communiquer avec C ?

Si l'on essaye naïvement de faire un `ping 192.168.2.5` depuis le réseau A, on aura le message suivant `Connect: Network is unreachable`. Maintenant on sait pourquoi, A n'a aucune idée de comment joindre 192.168.2.0 car il n'y a pas de passerelle. On doit lui dire que la passerelle passe par B.

On fait ça via `ip route add 192.168.2.0/24 via 192.168.1.6`, et la même chose dans l'autre sens : `ip route add 192.168.1.0/24 via 192.168.2.6`.

Si l'on réesaye `ping 192.168.2.5` maintenant, nous n'aurons plus le message d'erreur, mais nous pas non plus de réponses. **Par défaut et pour des raisons de sécurité, dans Linux, les paquets ne sont pas transmis d'une interface à l'autre**, ie il n'y a aucune communication entre `eth0` et `eth1` dans le réseau B.

``` mermaid
graph LR
  subgraph A
  A1[eth0 <br/> 192.168.1.5];
  end

  subgraph B
  B1[eth0 <br/> 192.168.1.6];
  B2[eth1 <br/> 192.168.2.6];
  end

  subgraph C
  C1[eth0 <br/> 192.168.2.5];
  end

  A1[eth0 <br/> 192.168.1.5]-.-|192.168.1.0|B1[eth0 <br/> 192.168.1.6]
  B2[eth1 <br/> 192.168.2.6]-.-|192.168.2.0|C1[eth0 <br/> 192.168.2.5]
  B1[eth0 <br/> 192.168.1.6] -.-|X| B2[eth1 <br/> 192.168.2.6]
```

Pour autoriser B à transmettre les paquets d'une interface à l'autre, on doit aller voir dans `/proc/sys/net/ipv4/ip_forward`.

!!! example "Exemple"

    Sur mon pc, cela donne :

    ```shell
    ❯ cat /proc/sys/net/ipv4/ip_forward
    1
    ```

    La valeur est sur 1, donc le transfert d'une interface à l'autre est autorisé, sinon elle serait à 0.

!!! danger "Attention"

    Jusqu'à présent, toutes les commandes que l'on a expliquer ne persisterons pas au redémarrage du système ! Il faudrait les refaire à chaque fois.

Pour que les changements soient persistents, il faut modifier la valeur du paramètre `net.ipv4.ip_forward` dans `/etc/sysctl.conf` en la mettant à 1.

!!! example "Exemple"


    ```shell
    ❯ cat /etc/sysctl.conf
    #
    # /etc/sysctl.conf - Configuration file for setting system variables
    # See /etc/sysctl.d/ for additional system variables.
    # See sysctl.conf (5) for information.
    #

    #kernel.domainname = example.com

    # Uncomment the following to stop low-level messages on console
    #kernel.printk = 3 4 1 3

    ##############################################################3
    # Functions previously found in netbase
    #

    # Uncomment the next two lines to enable Spoof protection (reverse-path filter)
    # Turn on Source Address Verification in all interfaces to
    # prevent some spoofing attacks
    #net.ipv4.conf.default.rp_filter=1
    #net.ipv4.conf.all.rp_filter=1

    # Uncomment the next line to enable TCP/IP SYN cookies
    # See http://lwn.net/Articles/277146/
    # Note: This may impact IPv6 TCP sessions too
    #net.ipv4.tcp_syncookies=1

    # Uncomment the next line to enable packet forwarding for IPv4
    #net.ipv4.ip_forward=1

    # Uncomment the next line to enable packet forwarding for IPv6
    #  Enabling this option disables Stateless Address Autoconfiguration
    #  based on Router Advertisements for this host
    #net.ipv6.conf.all.forwarding=1


    ###################################################################
    # Additional settings - these settings can improve the network
    # security of the host and prevent against some network attacks
    # including spoofing attacks and man in the middle attacks through
    # redirection. Some network environments, however, require that these
    # settings are disabled so review and enable them as needed.
    #
    # Do not accept ICMP redirects (prevent MITM attacks)
    #net.ipv4.conf.all.accept_redirects = 0
    #net.ipv6.conf.all.accept_redirects = 0
    # _or_
    # Accept ICMP redirects only for gateways listed in our default
    # gateway list (enabled by default)
    # net.ipv4.conf.all.secure_redirects = 1
    #
    # Do not send ICMP redirects (we are not a router)
    #net.ipv4.conf.all.send_redirects = 0
    #
    # Do not accept IP source route packets (we are not a router)
    #net.ipv4.conf.all.accept_source_route = 0
    #net.ipv6.conf.all.accept_source_route = 0
    #
    # Log Martian Packets
    #net.ipv4.conf.all.log_martians = 1
    #

    ###################################################################
    # Magic system request Key
    # 0=disable, 1=enable all, >1 bitmask of sysrq functions
    # See https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html
    # for what other values do
    #kernel.sysrq=438
    ```

### Configuration du DNS sous Linux