from urllib.request import urlretrieve

import yaml

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.storage import SimpleStorageServiceS3 as S3
from diagrams.custom import Custom
from diagrams.generic.storage import Storage
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git, Github
from diagrams.programming.language import Bash, Python

params = yaml.safe_load(open("params.yaml"))

tf_url = params["tf"]["url"]
tf_icon = params["tf"]["icon"]
urlretrieve(tf_url, tf_icon)

dvc_url = params["dvc"]["url"]
dvc_icon = params["dvc"]["icon"]
urlretrieve(dvc_url, dvc_icon)

mlflow_url = params["mlflow"]["url"]
mlflow_icon = params["mlflow"]["icon"]
urlretrieve(mlflow_url, mlflow_icon)

hydra_url = params["hydra"]["url"]
hydra_icon = params["hydra"]["icon"]
urlretrieve(hydra_url, hydra_icon)

yaml_url = params["yaml"]["url"]
yaml_icon = params["yaml"]["icon"]
urlretrieve(yaml_url, yaml_icon)

hdf_url = params["hdf"]["url"]
hdf_icon = params["hdf"]["icon"]
urlretrieve(hdf_url, hdf_icon)

txt_url = params["txt"]["url"]
txt_icon = params["txt"]["icon"]
urlretrieve(txt_url, txt_icon)

dvcbash_url = params["dvcbash"]["url"]
dvcbash_icon = params["dvcbash"]["icon"]
urlretrieve(dvcbash_url, dvcbash_icon)


with Diagram("Machine Learning Project", show=False, outformat="png"):

    with Cluster(".devcontainer dev"):
        docker_dev = Docker("Dev Environment")

    with Cluster(".devcontainer prod"):
        docker_prod = Docker("Prod Environment")

    with Cluster("Dev repo"):
        dev = Github("dev")

    with Cluster("Prod repo"):
        prod = Github("prod")

    docker_dev >> docker_prod
    docker_dev << docker_prod
    docker_dev >> dev
    dev >> prod
    prod >> docker_prod
    docker_prod >> prod
