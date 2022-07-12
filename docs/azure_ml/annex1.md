
# Annex : Traefik and Azure VM

https://kumar-allamraju.medium.com/using-traefik-as-a-layer-7-ingress-controller-in-azure-kubernetes-service-2997eb29228b

Using Traefik as a Layer 7 Ingress Controller in Azure Kubernetes Service

Traefik is the leading open source reverse proxy and load balancer for HTTP/HTTPS and TCP-based applications that makes deploying micro services very easy.

Traefik integrates with your existing infrastructure components (Docker, Kubernetes, AKS, EKS, GKE etc..) and configures itself automatically and dynamically. Pointing Traefik at your orchestrator (e.g. AKS) should be the *only* configuration step we need to do.

In this article I plan to talk about how to integrate traefik with AKS.

Consider a scenario where you have deployed a bunch of micro services in your Azure Kubernetes cluster. Now you want users to access these micro services, from public internet. Traditional reverse-proxies like NGINX ingress controller requires you to configure each route that will connect paths and subdomains to each micro service. In an environment where you add, remove, kill, upgrade, or scale your services many times a day, the task of keeping the routes up to date becomes tedious.

Traefik comes to the rescue and simplifies the networking complexity while designing, deploying and running micro services. Run Traefik and let it do the work for you! (But if you’d rather configure some of your routes manually, Traefik supports that too!)

### Pre-requisites

* An Azure subscription. If you don’t have one, sign up here for free
* Install az cli
* Run `az login` and authenticate to your Azure subscription
* Install `kubectl`

### Steps to configure Traefik in AKS Cluster

1. Create a resource group

`az group create -l eastus -n aksRG`

2. Create an AKS cluster

`az aks create --resource-group aksRG --name myAKS -l eastus --node-count 2`

3. Get the AKS credentials

`az aks get-credentials -n myAKS -g aksRG`

4. Get the AKS nodes

`kubectl get nodes`

5. By default AKS cluster is enabled with Role Based Access Control (RBAC) to allow fine-grained control of Kubernetes resources and API. So we need to authorize Traefik to use the Kubernetes API. There are two ways to set up the proper permission: via namespace-specific RoleBindings or a single, global ClusterRoleBinding. Refer to this article to understand RoleBindings or ClusterRoleBinding. For the sake of simplicity I’m using ClusterRoleBinding

```yml
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
rules:
  - apiGroups:
      - ""
    resources:
      - services
      - endpoints
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
    - extensions
    resources:
    - ingresses/status
    verbs:
    - update
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: traefik-ingress-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik-ingress-controller
subjects:
- kind: ServiceAccount
  name: traefik-ingress-controller
  namespace: kube-system
```

6. Apply the same to your AKS cluster

`kubectl apply -f traefik-rbac.yaml`

7. We can deploy Traefik via Helm charts or via Deployment/DaemonSet. I have used the latter approach to setup Traefik in my AKS cluster. It is possible to use Traefik with a Deployment or a DaemonSet object, whereas both options have their own pros and cons: In this article, I will be using DaemonSet and it looks no different from Deployment .In Kubernetes, we will use a

* Deployment/DaemonSet to deploy a Pod,
* Service — to expose the service,
* Ingress — to allow the access from external world

```yml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik-ingress-controller
  namespace: kube-system
---
kind: DaemonSet
apiVersion: apps/v1
metadata:
  name: traefik-ingress-controller
  namespace: kube-system
  labels:
    k8s-app: traefik-ingress-lb
spec:
  selector:
    matchLabels:
      k8s-app: traefik-ingress-lb
      name: traefik-ingress-lb
  template:
    metadata:
      labels:
        k8s-app: traefik-ingress-lb
        name: traefik-ingress-lb
    spec:
      serviceAccountName: traefik-ingress-controller
      terminationGracePeriodSeconds: 60
      containers:
      - image: traefik:v1.7
        name: traefik-ingress-lb
        ports:
        - name: http
          containerPort: 80
          hostPort: 80
        - name: admin
          containerPort: 8080
          hostPort: 8080
        securityContext:
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        args:
        - --api
        - --kubernetes
        - --logLevel=INFO
---
kind: Service
apiVersion: v1
metadata:
  name: traefik-ingress-service
  namespace: kube-system
spec: type: LoadBalancer
 selector:
    k8s-app: traefik-ingress-lb
  ports:
    - protocol: TCP
      port: 80
      name: web
    - protocol: TCP
      port: 8080
      name: admin
```
8. Deploy the Traefik DaemonSet and Service to your AKS cluster

`kubectl apply -f traefik-ds.yaml`

9. For simplicity sake, we can use Minikube instance but I have used Azure App Service domains feature to quickly setup a custom domain and added an “A” record that mapped the load balancer public IP to this custom domain

* Go to Azure Portal
* Enter “App service domain” in the search box
* Click on + Add

* It takes 5 minutes to provision your custom domain. After your custom domain is created, Click on + Manage DNS Records

  Note: Creating a custom domain is not a free service

* Click on + Record Set
* Name: *, Type: A, IP address: public IP of your Load Balancer that was created above.

10. The following code will allow us to access Traefik dashboard via your custom domain name.

  Note: kubernetes.io/ingress.class: traefik — this allows us to use traefik as an Ingress controller.

```yml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
name: traefik-web-ui
namespace: kube-system
annotations:
kubernetes.io/ingress.class: traefik
spec:
  rules:
  - host: www.custom-domain.com
  http:
    paths:
    - path: /
    backend:
      serviceName: traefik-web-ui
      servicePort: web
```
11. Let’s check the pods and services


```Shell
kubectl get all -n kube-system | grep traefik
pod/traefik-ingress-controller-pngvm       1/1     Running   0          15h
pod/traefik-ingress-controller-q6ctg       1/1     Running   0          15h
service/traefik-ingress-service          LoadBalancer   10.0.39.252    x.x.x.x   8
0:30879/TCP,8080:31163/TCP   15h
service/traefik-web-ui                   ClusterIP      10.0.138.134   <none>          8
0/TCP                        16h
daemonset.apps/traefik-ingress-controller   2         2         2       2            2
         <none>                                                 15h
```
12. Point your browser to http://{custom-domain}/dashboard/ to access Traefik’s dashboard.

  Note: You should enable https to securely access your dashboard

### Frontend Types in Traefik

Traefik supports name based routing and path based routing
Name Base Routing

To demonstrate this feature, I have taken the example from containous website and this works flawlessly in AKS cluster

```
- Create a Deployment
kubectl apply -f https://raw.githubusercontent.com/containous/traefik/v1.7/examples/k8s/cheese-deployments.yaml

- Create a Service
kubectl apply -f https://raw.githubusercontent.com/containous/traefik/v1.7/examples/k8s/cheese-services.yaml

- Create an Ingress service
kubectl apply -f https://raw.githubusercontent.com/containous/traefik/v1.7/examples/k8s/cheese-ingress.yaml
```
Make sure to replace the host name with your custom domain or host name.

Now visit the traefik dashboard and you should see a frontend for each host. Along with a backend listing for each service with a server set up for each pod.

You should now be able to visit the websites as http://stilton.{custom-domain.com}/, http://cheddar.{custom-domain.com}/ or http://{custom-domain.com}/wensleydale/

### Path Bath Routing

This routing rule is helpful if you want to host all your services under one domain. All we have to do is specify the path instead of the domain name. You will also notice in the yaml file we are configuring Traefik to strip the prefix from the url path with traefik.frontend.rule.type annotation

`kubectl apply -f https://raw.githubusercontent.com/containous/traefik/v1.7/examples/k8s/cheeses-ingress.yaml`

We should now visit the website with a single domain name

i.e. http://{custom-domain.com}/stilton, http://{custom-domain.com}/cheddar, http://{custom-domain.com}/wensleydale

### Conclusion

Traefik is an open-source Edge Router that makes publishing your services a fun and easy experience. It receives requests on behalf of your system and finds out which components are responsible for handling them.

What sets Traefik apart, besides its many features, is that it automatically discovers the right configuration for your services. The magic happens when Traefik inspects your infrastructure, where it finds relevant information and discovers which service serves which request.

Traefik is natively compliant with every major cluster technology, such as Kubernetes, Docker, AKS, AWS, Mesos, Marathon, and the list goes on; and can handle many at the same time. (It even works for legacy software running on bare metal.) With Traefik, you spend time developing and deploying new features to your system, not on configuring and maintaining its working state.
References

    https://docs.traefik.io/
    https://containo.us/traefik/
    https://docs.traefik.io/getting-started/install-traefik/
    https://azure.microsoft.com/en-us/services/kubernetes-service/
