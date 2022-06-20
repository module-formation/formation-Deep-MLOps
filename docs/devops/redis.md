# Redis 101

Redis est une solution de stockage clé-valeur pouvant être utilisé comme un service de queue entre différents micro-services.

## Installation sous Linux

Pour installer redis, on utilise le serveur redis via le package fourni.

```shell
sudo apt update
sudo apt install redis-server
```

Ce qui installera redis et toutes ses dépendances.

Pour avoir un plus de contrôle sur le serveru redis, on peut le définir comme un service. Pour cela, on a besoin de modifier le fichier de configuration de redis.

Si l'on regarde le fichier de configuration via la commande suivante.

```shell
sudo vim /etc/redis/redis.conf
```

On peut alors chercher l'option `supervised`, qui par défaut est sur `no`, or si l'on travaille sur un système Linux, les services peuvent être managés par `systemd`. Il suffit alors de changer `supervised no` par `supervised systemd`, pour le définir comme un service sous Linux.

```
# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd
```
On le relance alors pour prendre les changements en compte, et on peut aussi vérifier son statut.

```shell
❯ sudo systemctl restart redis.service

❯ sudo systemctl status redis.service

● redis-server.service - Advanced key-value store
     Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-06-15 22:06:36 CEST; 5s ago
       Docs: http://redis.io/documentation,
             man:redis-server(1)
    Process: 30903 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
   Main PID: 30904 (redis-server)
      Tasks: 4 (limit: 76989)
     Memory: 2.1M
     CGroup: /system.slice/redis-server.service
             └─30904 /usr/bin/redis-server 127.0.0.1:6379

juin 15 22:06:36 vorph-maison systemd[1]: Starting Advanced key-value store...
juin 15 22:06:36 vorph-maison systemd[1]: redis-server.service: Cant open PID file /run/redis/redis-server.pid (yet?) after start: Operation not permitted
juin 15 22:06:36 vorph-maison systemd[1]: Started Advanced key-value store.
```

## Architecture

Redis a une architecture client-serveur et utilise un modèle de demande-réponse. Cela signifie que vous (le client) vous connectez à un serveur Redis via une connexion TCP, sur le port 6379 par défaut. Vous demandez une action (comme une forme de lecture, d'écriture, d'obtention, de réglage ou de mise à jour), et le serveur vous renvoie une réponse.

Il peut y avoir de nombreux clients qui parlent au même serveur, ce qui est vraiment la raison d'être de Redis ou de toute application client-serveur. Chaque client effectue une lecture (généralement bloquante) sur un socket en attendant la réponse du serveur.

Pour communiquer avec ce serveur, on utilise `redis-cli`

Le `cli` de `redis-cli` signifie interface en ligne de commande, et le `server` de `redis-server` sert à faire tourner un serveur. De la même manière que vous exécuteriez python à la ligne de commande, vous pouvez exécuter `redis-cli` pour accéder à une boucle interactive REPL (Read Eval Print Loop) où vous pouvez exécuter des commandes client directement depuis le shell.

Par défaut, redis écoute sur le port 6379 de l'adresse loopback 127.0.0.1.

Pour accéder au serveur, tape alors dans un terminal la commande `redis-cli`.

La commande la plus simple pour vérifer sur le serveur fonctionne correctement et de tapper `PING` et voir s'il nous répond.

```shell title="PING"
❯ redis-cli
127.0.0.1:6379> ping
PONG
```

```shell title="on peut aussi écrire un message, attention aux quotes"
127.0.0.1:6379> PING
PONG
127.0.0.1:6379> PING hello
"hello"
127.0.0.1:6379> PING hello how are you
(error) ERR wrong number of arguments for 'ping' command
127.0.0.1:6379> PING "hello how are you"
"hello how are you"
```

On quitte le serveur redis en tapant simplement `exit`.

## Redis vu comme un dictionnaire Python

Redis est l'acronyme de Remote Dictionnary Service.

Dans les grandes largeurs, il y a de nombreus parallèles entre un dictionnaire python, ou de façon plus globale un table de hashage.

* Une db Redis stocke des données sous la forme `clé:valeur` et supportent des commandes telles que `GET`, `SET`, `DEL` et [une centaine d'autres](https://redis.io/commands/).
* Les clés sont toujours de `strings`.
* Les valeurs peuvent avoir différents types, les plus connus étant `string`, `list`, `hashes`, and `sets`.

Prenons l'exemple très simple suivant.

```shell title="pays:capitale"
❯ redis-cli
127.0.0.1:6379> set bahamas nassau
OK
127.0.0.1:6379> set france paris
OK
127.0.0.1:6379> get france
"paris"
127.0.0.1:6379> get bahamas
"nassau"
127.0.0.1:6379> get japan
(nil)
127.0.0.1:6379> exit
```

La commande `set` permet d'insérer des données dans la db Redis, pour insérer on suit le format `set clé valeur`, avec bien un **espace** entre `clé` et `valeur`. Etant donnée une clé, on peut récupérer sa valeur associée via la commande `get clé`. Notez que même si un jeu `clé:valeur` n'a pas été rentré, Rédis ne remontera un message d'erreur mais `(nil)`, qui correspond au `None` de python.

Il est aussi possible de rentrer plusieurs jeux `clé:valeur` de façon simultanée `mset clé1 valeur1 clé2 valeur2 clé3 valeur3 ...`, on récupère les valeurs de façon similaire avec `mget clé1 clé2 clé3 ...`.

```shell title="mset-mget"
127.0.0.1:6379> mset belgium bruxelles germany berlin italy rome
OK

127.0.0.1:6379> mget belgium france italy
1) "bruxelles"
2) "paris"
3) "rome"
```

La commande `exists` permet de vérifier si une clé (et uniquement une clé, pas une valeur), est présente en db en renvoyant un booléen.

```shell title="exists"
127.0.0.1:6379> exists france
(integer) 1
127.0.0.1:6379> exists paris
(integer) 0
127.0.0.1:6379> exists japan
(integer) 0
```

## Hash datatype

Un `hash` (hachage en français), pour comparer avec python, correspond à un dictionnaire hiérarchique avec un niveau de profondeur, ie un dictionnaire dont la valeur de chaque clé "principale" est un dictionnaire.

```python title="Dictionnaire hiérarchique avec un niveau de profondeur."
data = {
    "user": {
        "prenom": "mathieu",
        "nom": "klimczak",
        "github": "https://github.com/Klimorg",
    }
}
```
Un hachage est donc une correspondance de chaînes de caractères, appelé paires champ-valeur, qui se trouve sous une clé de niveau supérieur.

Insérer un hash dans Redis se fait via la commande `hset clé champs valeur`, ici on a :

* une seule clé `user`,
* trois champs `prénom`, `nom`, `github`,
* les trois valeurs correspondantes.

On peut récupérer la valeur d'un champs particuliers via la commande `hget clé champs`.

On peut aussi rentrer toutes les valeurs d'un hash en une seule fois avec la commande `hmset`, et tout récupérer avec `hgetall clé`.

```shell title="hset hget hmset hgetall"
127.0.0.1:6379> hset user prenom mathieu
(integer) 1
127.0.0.1:6379> hset user nom klimczak
(integer) 1
127.0.0.1:6379> hset user github "https://github.com/Klimorg"
(integer) 1
127.0.0.1:6379> hget user nom
"klimczak"
127.0.0.1:6379> hget user github
"https://github.com/Klimorg"

127.0.0.1:6379> hget user mail
(nil)

127.0.0.1:6379> hget user nom prenom
(error) ERR wrong number of arguments for 'hget' command

127.0.0.1:6379> hmset user2 prenom paul nom tondelier github aucun
OK
127.0.0.1:6379> hgetall user2
1) "prenom"
2) "paul"
3) "nom"
4) "tondelier"
5) "github"
6) "aucun"
127.0.0.1:6379>
```

Deux types de valeurs supplémentaires sont les listes et les ensembles, qui peuvent prendre la place d'un hash ou d'une chaîne de caractères comme valeur Redis.

Les hachages, les listes et les ensembles ont chacun des commandes qui sont particulières à ce type de données donné, qui sont dans certains cas indiquées par leur lettre initiale :

* **Hash** : Les commandes permettant d'opérer sur les hachages commencent par un H, comme `HSET`, `HGET` ou `HMSET`.

* **Sets** : Les commandes permettant d'opérer sur des ensembles commencent par un S, comme `SCARD`, qui obtient le nombre d'éléments à la valeur de l'ensemble correspondant à une clé donnée.

* **Listes** : Les commandes permettant d'opérer sur des listes commencent par un L ou un R. Les exemples incluent `LPOP` et `RPUSH`. Le L ou le R fait référence au côté de la liste sur lequel on opère. Quelques commandes de liste sont également précédées d'un B, qui signifie blocage. Une opération de blocage ne permet pas aux autres opérations de l'interrompre pendant son exécution. Par exemple, `BLPOP` exécute un left-pop bloquant sur une structure de liste.


## Sources

* [How to Use Redis With Python](https://realpython.com/python-redis/#ten-or-so-minutes-to-redis)