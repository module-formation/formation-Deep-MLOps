# Le monitoring des modèles

## Durant l'entraînement : MLFlow

## En production : Prometheus & Grafana

### Prometheus

[Prometheus](https://prometheus.io/) est un software permettant de recupérer de nombreuses méttriques et permet de les centraliser. On peut par exemple récupérer

- l'espace disque utilisé,
- la RAM,
- l'utilisation du CPU/GPU,
- etc.

Prometheus permet aussi de vous alerter sur certaines des ces métriques sont sur-utilisées et risquent de ne plus répondre.

- [Collect Docker metrics with Prometheus](https://docs.docker.com/config/daemon/prometheus/)
- [How to Visualize Tensorflow Metrics in Kibana](https://medium.com/fourthline-tech/how-to-visualize-tensorflow-metrics-in-kibana-761268353ca3)
- [FastAPI Microservice Patterns: Application Monitoring](https://medium.com/swlh/fastapi-microservice-patterns-application-monitoring-49fcb7341d9a)
- [How to monitor your FastAPI service](https://guitton.co/posts/fastapi-monitoring/)
- [Starlette Prometheus](https://github.com/perdy/starlette-prometheus)
- [Prometheus FastAPI Instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator)
- [PrometheusRock](https://github.com/kozhushman/prometheusrock)
#### Accéder aux métriques docker

!!! docker "/etc/docker/daemon.json"

    ```json
    {
        "runtimes": {
            "nvidia": {
                "path": "nvidia-container-runtime",
                "runtimeArgs": []
            }
        },
        "metrics-addr" : "127.0.0.1:9323",
        "experimental" : true
    }
    ```

#### Le client Python

[Client Python officiel de Prometheus](https://github.com/prometheus/client_python)

### Grafana

![screen](./images/prometheus_grafana.svg)
