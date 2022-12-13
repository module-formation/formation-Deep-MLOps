from urllib.request import urlretrieve

from omegaconf import OmegaConf

from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import VM, ContainerInstances, KubernetesServices
from diagrams.azure.database import BlobStorage
from diagrams.azure.devops import (ApplicationInsights, Artifacts, Devops,
                                   Pipelines, Repos)
from diagrams.azure.general import Resourcegroups
from diagrams.azure.identity import ManagedIdentities
from diagrams.azure.integration import APIManagement
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.custom import Custom
from diagrams.generic.storage import Storage
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python

params =  OmegaConf.load("diagrams/params.yaml")

hydra_url = params["hydra"]["url"]
hydra_icon = params["hydra"]["icon"]
urlretrieve(hydra_url, hydra_icon)

with Diagram(
    "End to End architecture Azure",
    show=False,
    outformat=["svg", "png"],
) as dac:
    dac.dot.renderer = "cairo"

    with Cluster("Azure Pipelines"):

        # svc = Devops("Roqconf")

        # with Cluster("Artifacts DevOPs"):
        #   Artifacts("Project artifacts")
        #   Storage("project.whl")

        # with Cluster("project"):

        #   project_repo = Repos("project")
        #   with Cluster("src"):
        #     Python("preprocess.py")
        #     Python("trainer.py")
        #     Python("postprocess.py")
        #     Python("predictor.py")
        #     Custom("Hydra", hydra_icon)


        #   with Cluster("tests"):
        #     Python("test_preprocess.py")
        #     Python("test_trainer.py")
        #     Python("test_postprocess.py")
        #     Python("test_predictor.py")

        #   with Cluster("Pipelines"):
        #     ci=Pipelines("ci-pipeline.yaml")
        #     Pipelines("precommit-pipeline.yaml")
        #     Pipelines("nox-pipeline.yaml")
        #     Pipelines("renovate-pipeline.yaml")
        #     Pipelines("build-and-register.yaml")
        #     Pipelines("azml-pipelines.yaml")

        # with Cluster("pipeline-store"):

          # with Cluster("Pipelines"):
          #   Pipelines("environment-pipeline.yaml")
          #   Pipelines("data-engineering-pipeline.yaml")
          #   Pipelines("training-pipeline.yaml")
          #   Pipelines("deploy-model-pipeline.yaml")

          # with Cluster("Azure"):
          #   Resourcegroups("RG")
          #   BlobStorage("Data Lake")
          #   with Cluster("RG"):
          #     MachineLearningServiceWorkspaces
          #     with Cluster("Workspace"):
          #       BlobStorage("Default")
          #       BlobStorage("Model registry")
          #       VM("Compute Cluster")
          #       ManagedIdentities("user-assigned")
          with Cluster("Model deployment"):
            ContainerInstances("ACI")
            KubernetesServices("AKS")
            APIManagement("APIM")
            ApplicationInsights("Monitoring")
