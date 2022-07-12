# Kubernetes for the beginner

Aussi dénommé k8s, kubernetes a été développé par Google, capitalisant sur leur expérience des conteneurs en production.

k8s est un système d'orchestration de conteneurs. Pour les conteneurs on se réfère à la section prcédente, parlons de l'orchestration.

## Orchestration

Avec une commande `docker run`, on est capable de déployer une instance d'un conteneur, par exemple une api.

Mais que se passe-t-il si le nombre de requêtes envoyées à cette api et trop important ? On pourrait déployer une seconde instance de cette api pour gérer le flux supplémentaire.

On pourrait le faire en relançant une commande `docker run`, mais cela demande de le faire de façon manuelle et de surveiller à chaque fois comment cela se passe.

De la même façon, le pique de requête sera passé, on pourrait alors vouloir supprimer certaines instances, pour récupérer des ressources.

Si le conteneur crashe, on devrait pouvoir le détecter et relancer une image automatiquement.

Si le docker host crashe, tous les conteneurs lancés s'arrêterons aussi.

Pour gérer ces problèmes dans un environnement de production, on fait alors appel à des systèmes d'orchestrations des conteneurs :

* docker-swarm,
* kubernetes,
* MESOS.

On se concentre ici sur kubernetes.

**Les avantages d'un orchestrateur sont alors que vos applications sont facilement et toujours disponibles, un crash étant alors automatiquement détecté et une nouvelle instance lancée. Plusieurs instance d'une même application peuvent être lancées en même temps, ce que permet d'équilibrer le traffic.**

## Architecture kubernetes

Quand on parle de k8s, on d'un cluster kubernetes, de la même façon qu'on parlerait d'un cluster de cpu travaillant de façon conjointe.

L'atome d'un cluster k8s est une **node** (noeud), un noeud est une machine, qu'elle soit physique ou virtuelle, sur laquelle est installé k8s. C'est sur  un noeud que se lance les conteneurs que k8s orchestre. Evidemment, si l'on a qu'un seul noeud et qu'il crashe, k8s ne pourra rien faire et donc vos conteneurs ne seront plus accessibles. C'est là tout l'intérêt d'un cluster centralisant plusieurs noeuds.

Dans un cluster k8s, il y a toujours un noeud principal, le **Master node**, c'est sur lui que k8s est installé, et qui gère l'ensemble des noeuds du cluster qui sont des **workers nodes**. C'est le noeud principal qui est responsable de l'orchestration en tant que tel.

Lorsque l'on installe kubernetes, on installe en fait une suite de composants :

* un serveur api,
* un service [`etcd`](https://etcd.io/),
* un service `kubelet`,
* un `container runtime`,
* un controlleur,
* un scheduler.

L'api est l'interface principale avec laquelle l'utilisateur interagit, les lignes de commandes, le management des conteneurs, tout se fait via cette api.

`etcd` est le système de stockage interne de kubernetes, il est par exemple responsable de la configuration des logs entre les différentes instances d'un même conteneur.

Le scheduler est celui qui distribue le travail, ou les conteneurs, aux différents noeuds du cluster. Il assigne les conteneurs nouvellments créés aux noeuds.

Le controlleur est le cerveau de l'orchestration il est responsable de la surveillance des noeuds et des contneeurs qui crashent. C'est lui qui décide de recréer un nouveau conteneur si nécessaire.

Le `container runtime` est le software sous-jacent permettant de faire tourner les conteneurs, dans la plupart du temps, c'est Docker.

!!! info "Remarque"

    Il existe d'autres container runtime, on peut citer par exemple [cri-o](https://cri-o.io/)

`kubelet` est l'agent qui tourne sur chaque noeud, et qui surveille que les conteneurs présents sur le noeud fonctionnent comme prévu.

## `kubectl`

`kubectl` est l'outil de ligne de commande principal pour interagir, déployer et manager avec kubernetes.

```shell title="helloworld de kubernetes"
kubectl run hello-minikube
```

```shell title="Affiche les informations du cluster"
kubectl cluster-info
```

```shell title="liste l'ensemble des noeuds du conteneur"
kubectl get nodes
```

## Setup kubernetes

* Minikube
* k3s
* MicroK8s
* Kubeadm


### References

* Install and set up the kubectl tool: –

https://kubernetes.io/docs/tasks/tools/

* Install Minikube: –

https://minikube.sigs.k8s.io/docs/start/

* Install VirtualBox: –

https://www.virtualbox.org/wiki/Downloads

https://www.virtualbox.org/wiki/Linux_Downloads

* Minikube Tutorial: –

https://kubernetes.io/docs/tutorials/hello-minikube/


## Concept de base : les PODs

Avec k8s, le but ultime est de déployer une application sous la forme de conteneurs sur un ensemble de machines configurées comme des noeuds de travail sur un cluster.

``` mermaid
graph LR

    subgraph cluster
        A[node]

        B[node]

        C[node]
    end
```

Cependant, k8s ne déploie pas directement les conteneurs sur les noeuds de travail, les conteneurs sont encapsulés dans un objet k8s connu sous le nom de **pod**.

``` mermaid
graph LR

    subgraph cluster
        subgraph node
            A[pod <br/> conteneur]
        end

        subgraph node
            B[pod <br/> conteneur]
        end

        subgraph node
            C[pod <br/> conteneur]
        end
    end
```

Un pod est une instance d'une application. C'est le plus petit objet que l'on puisse créer dans k8s.

!!! example "Exemple"

    Exemple de config la plus simple, un cluter avec un noeud unique, contenant un unique pod, faisant tourner un conteneur avec python 3.8 dessus.

    ``` mermaid
    graph LR

        subgraph cluster
            subgraph node
                A[pod <br/> conteneur python:3.8]
            end
        end
    ```

``` mermaid
graph LR

    subgraph cluster
        subgraph node
            A[pod <br/> conteneur python:3.8]
        end
    end

B[User1] & C[User2] & D[User3] & E[User4] -.-> A
```

Si beaucoup d'utilisateurs se connectent au pod et que l'on souhaite équilibrer la charge, la solution retenue par k8s est alors de lancer un nouveau pod avec le même conteneur sur le même noeud.

``` mermaid
graph LR

    subgraph cluster
        subgraph node
            A1[pod 1<br/> conteneur python:3.8]
            A2[pod 2<br/> conteneur python:3.8]
        end
    end

B[User1] & C[User2] -.-> A1
D[User3] & E[User4] -.-> A2
```

Et si le nombre d'utilisateur augmente encore et que le noeud n'a plus la capacité d'acceuillir un pod supplémentaire ? Il est toujours possible de rajouter un nouveau noeud avec un nouveau pod contenant le conteneur.


``` mermaid
graph LR

    subgraph cluster
        subgraph node 1
            A1[pod 1<br/> conteneur python:3.8]
            A2[pod 2<br/> conteneur python:3.8]
        end
        subgraph node 2
            A3[pod 3<br/> conteneur python:3.8]
        end
    end

B[User1] & C[User2] -.-> A1
D[User3] & E[User4] -.-> A2
F[User5] & G[User6] -.-> A3
```

La plupart du temps, les pods sont en correspondance bijective avec les conteneurs faisant tourner les applications. Pour augmenter la charge on augmente le nombre de pods, pour la baisser on en supprime.

### POD multi-conteneur

La correspondance pod/conteneur n'est pas une règle stricte et un pod peut très bien faire tourner plusieurs conteneurs. Dans la plupart des cas ces conteneurs ne sont pas identiques. On peut par exemple imaginer un pod contenant une API REST et son UI correspondante, avec les connexions reliant les deux comme le ferait docker compose. Les conteneurs à l'intéreur d'un même pod partage le même namespace, storage space, réseau, etc.

### Les commandes de base

l'API utilisé pour gérer les cluster k8s est `kubectl`.


|                 Commande                 |                                         Résultat                                          |                             Exemple                             |
| :--------------------------------------: | :---------------------------------------------------------------------------------------: | :-------------------------------------------------------------: |
| `kubectl run podname --image image_path` | lance un pod nommé `podname` contenant l'image se trouvant à l'adresse (cr) `image_path`. | `kubectl run helloworld-api --image vorphus/helloworld-api:1.0` |
|            `kubectl get pods`            |                                Liste l'ensemble des pods.                                 |                                                                 |
|        `kubectl get pods -o wide`        |                    Liste l'ensemble des pods avec plus d'informations.                    |                                                                 |
|      `kubectl describe pod podname`      |                   Affiche des informations concernant le pod `podname`.                   |              `kubectl describe pod helloworld-api`              |
|       `kubectl delete pod podname`       |                                Supprime le pod `podname`.                                 |               `kubectl delete pod helloworld-api`               |

``` title="kubectl describe pod helloworld-api"
❯ kubectl describe pod helloworld-api

Name:         helloworld-api
Namespace:    default
Priority:     0
Node:         minikube/192.168.39.66
Start Time:   Thu, 07 Jul 2022 22:22:47 +0200
Labels:       run=helloworld-api
Annotations:  <none>
Status:       Running
IP:           172.17.0.3
IPs:
  IP:  172.17.0.3
Containers:
  helloworld-api:
    Container ID:   docker://1bb8c1064c829172282c0e13fc08ef22b24755077f161352ff5a7cee240b3cf1
    Image:          vorphus/helloworld-api:1.0
    Image ID:       docker-pullable://vorphus/helloworld-api@sha256:e8d49d5c9fc1924f1702d7b4bc3a28bb42c639fc9f87c6c2031a45859ca2d463
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Thu, 07 Jul 2022 22:22:48 +0200
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-wmjdf (ro)
Conditions:
  Type              Status
  Initialized       True
  Ready             True
  ContainersReady   True
  PodScheduled      True
Volumes:
  kube-api-access-wmjdf:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  17m   default-scheduler  Successfully assigned default/helloworld-api to minikube
  Normal  Pulled     17m   kubelet            Container image "vorphus/helloworld-api:1.0" already present on machine
  Normal  Created    17m   kubelet            Created container helloworld-api
  Normal  Started    17m   kubelet            Started container helloworld-api
```


To create a deployment using imperative command, use kubectl create:

kubectl create deployment nginx --image=nginx

* Kubernetes Concepts – https://kubernetes.io/docs/concepts/

* Pod Overview- https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/

## Concepts : PODs, ReplicaSets, Deployments

### Créer un pod via YAML

k8s utilise la synthaxe YAML pour créer ses objets. Tous les fichiers utilisés par k8s suivent la même structure.

Il y a 4 entrée de niveau maximal (root), et ces entrées sont **nécessaires** dans un fichier yml pour k8s.


```yaml title="pod-definition.yml"
--8<-- "./includes/k8s/pod-definition.yml"
```

* `apiVersion` correspond à la version de l'api k8s utilisée pour créer les objets. En fonction de ce que l'on souhaite créer, il faut utiliser la bnne version. Pour créer des pods, on utilise la version `v1`.

* `kind` correspond au type d'objet que l'on essaye de créer. On a la correspondance suivante entre `apiVersion` et `kind`.

|    kind    | apiVersion |
| :--------: | :--------: |
|    POD     |     v1     |
|  Service   |     v1     |
| ReplicaSet |  apps/v1   |
| Deployment |  apps/v1   |


* `metadata` correspond aux données qui sont rattachées à l'objet lui même, comme son nom, es labels, etc. Par définition, `metadata` attend comme valeur un dictionnaire `yml`, alors que `apiVersion` et `kind` attendent un `string` comme valeur. Les jeux clé/valeur sous la clé `labels` sont complètement libre et à la discrétion de l'administrateur, ces labels servent à créer des tags pour filtrer les pods.

* `spec` contient les spécifications techniques de l'objet que l'on crée, ici comme on crée un pod, on s'attend aux spécifications du ou des conteneurs adjoints au pod. **Comme un pod peut contenir plusieurs conteneurs**, on s'attend à une liste sous la clé `containers`.

Pour créer le pod à partir de ce fichier de configuration, on utilise a commande suivante.

```shell
kubectl create -f pod-definition.yml
```


```shell
kubectl get pods
```


```shell
kubectl describe pod my-app-pod
```

```shell
kubectl run redis --image=redis --dry-run=client -o yaml > redis-definition.yaml
```

```yaml title="redis-definition.yml"
--8<-- "./includes/k8s/redis-definition.yaml"
```

```
kubectl create -f redis-definition.yaml
```
Use the kubectl edit command to update the image of the pod to redis.

`kubectl edit pod redis`

If you used a pod definition file then update the image from redis123 to redis in the definition file via Vi or Nano editor and then run kubectl apply command to update the image :-

`kubectl apply -f redis-definition.yaml`

### Réplications

Les contrôleurs sont les systèmes sous jacents qui gèrent les objets de kubernetes. En particulier les réplications.

Si l'on reprend notre cas d'usage très basique d'un unique conteneur dans un unique pod, alors si le pod crashe l'utilisateur n'a plus aucun accès  et perd toutes les informations.

``` mermaid
graph LR

    subgraph cluster
        subgraph node
            A[pod <br/> conteneur python:3.8]
        end
    end
```

Le contrôleur de réplication permet de gérer cela, c'est lui qui se charge de faire tourner plusieurs instances d'un même pod pour éviter les coupûres de service.


``` mermaid
graph LR
    subgraph node
        subgraph "replication controller"
                A1[pod <br/> conteneur python:3.8]

                A2[pod <br/> conteneur python:3.8]
        end
    end
```

Notez que le contrôleur de réplications se place au niveau du noeud, et pas du cluster. Le contrôleur s'assure que le nombre de pods spécifiés est présent tout le temps, même si ce nombre est 1.

Le contrôleur s'occupe aussi du load balancing et du scaling des pods via les différents noeuds du cluster.

#### ReplicaSet, contrôleur de réplications

Pour créer et gérer des réplications, il y a deux méthodes dans k8s :

* Définir un `ReplicationController`.
* Définir un `ReplicaSet`.

`ReplicaSet` est la façon la plus moderne de définir des réplications dans k8s, mais les deux sont valides et sont sensiblement similaires dans leur écriture.


##### `ReplicationController`

Pour définir un `ReplicationController`, on utilise la méthode suivante.

```yaml title="rc-definition.yml"
--8<-- "./includes/k8s/rc-definition.yml"
```

La première partie :

```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: myapp-rc
  labels:
    app: myapp
    type: front-end
```
est identique à celle définie dans la rédaction d'un pod : `Pod` et `ReplicationController` utilise la même version de l'api et les `metadata` ont la même signification dans les deux cas.

La deuxième partie elle est spécifique au choix `ReplicationController`. La partie `spec` définit quel type d'objet le `ReplicationController` doit générer. Pour cela il a besoin :

1. du `template` de l'objet qu'il va générer
2. du nombre de répliques qu'il doit générer (`replicas`).

```yaml
spec:
  template:

  replicas: n
```

Dans notre cas, l'objet que l'on souhaite gérer avec le `ReplicationController` étant un `Pod`, la partie `template` devra donc contenir les `spec` caractéristiques d'un pod.


```yaml
spec:
  template:
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx

  replicas: 3
```

Remarquez que la partie

```yaml
    metadata:
      name: myapp-pod
      labels:
        app: myapp
        type: front-end
    spec:
      containers:
        - name: nginx-container
          image: nginx
```

est exactement celle qui est définie, en dehors de `apiVersion` et `kind`, dans un fichier yaml pour créer un pod.

Si l'on veut créer 3 répliques, on spécifit dans la partie `replicas` le nombre 3.

On peut alors le créer avec la commande suivante.

```shell
kubectl create -f rc-definition.yml
```

Pour voir l'objet `ReplicationController` on tape la commande suivante.

```shell
kubectl get replicationcontroller
```

On peut bien sur voir les pods créés avec la commande suivante.

```shell
kubectl get pods
```

Enfin, pour le détruire, on utilise la commande suivante.

```shell
kubectl delete replicationcontroller myapp-rc
```

##### `ReplicaSet`

Pour définir un `ReplicaSet`, on utilise la méthode suivante.

```yaml title="replicaset-definition.yml"
--8<-- "./includes/k8s/replicaset-definition.yml"
```

Peu de choses changent par rapport au fichier d'un `ReplicationController`.

1. On doit changer la version : `apps/v1`.
2. Le `kind` change : `ReplicaSet`
3. La partie `template` a exactement la même fonction que pour `ReplicationController`.

La partie que change vraiment dans `spec` est la clé `selector`. C'est cette partie qui permet au `ReplicaSet` d'identifier quels sont les pods dont il doit se charger.

!!! question "Question"

    Pourquoi définir quels sont les pods dont il doit se charger si l'on a déjà défini un template de pods dans le `ReplicaSet` ?

C'est parce que les `ReplicaSet` sont aussi capables de gérer des pods qui n'ont pas été créés en même temps que le `ReplicaSet`, même si ces pods ne sont pas dans le même noeud.

Une des façons d'identifier les pods que le `ReplicaSet` doit prendre en compte est de filtrer sur les labels définis dans les `metadata` des pods. Pour cela on utilise la clé `matchLabels`.

```yaml title="ReplicaSet va gérer tous les pods avec le label type: front-end"
    selector:
        matchLabels:
            type: front-end
```

Le `selector` est la différence majeure entre `ReplicationController` et `ReplicaSet`.

On peut alors le créer avec la commande suivante.

```shell
kubectl create -f replicaset-definition.yml
```

Pour voir l'objet `ReplicaSet` on tape la commande suivante.

```shell
kubectl get replicaset
```
```shell
kubectl get rs
```

```shell
kubectl describre replicaset replicaset-name
```

On peut bien sur voir les pods créés avec la commande suivante.

```shell
kubectl get pods
```
Enfin, pour le détruire, on utilise la commande suivante.

```shell
kubectl delete replicaset myapp-replicaset
```
```shell
kubectl edit replicaset myapp-replicaset
```
Dans l'optique où le `ReplicaSet` est créé **après** que les pods avec les bons labels ont été créés, le `ReplicaSet` a tout de même besoin de la section `template`. Comme il est censé monitorer les pods et s'assurer que tous sont dispos, si des pods monitorés crashe, le `ReplicaSet` a besoin de connaître le `template` sur lequel il doit se baser pour recréer un nouveau pod.

#### Augmenter le nombre de répliques

Si l'on souhaite augmenter le nombre de répliques d'un pod, dans un `ReplicaSet` ou un `ReplicationController`, une des solutions est de modifier en conséquence la section `replicas` de ces fichiers et de lancer une misa à jour avec la commande suivante.

```shell
kubectl replace -f file.yml
```

Une autre méthode est d'utiliser la commande `kubectl scale` :

```shell
kubectl scale --replicas=6 -f file.yml
```

```shell
kubectl scale --replicas=6 replicaset myapp-replicaset
```
