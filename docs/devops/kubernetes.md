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