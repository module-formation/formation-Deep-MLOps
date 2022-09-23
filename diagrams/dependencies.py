from diagrams import Cluster, Diagram, Edge
from diagrams.azure.database import BlobStorage
from diagrams.azure.devops import Pipelines, Repos
from diagrams.azure.general import (Managementgroups, Resourcegroups,
                                    Subscriptions)
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.ml import MachineLearningServiceWorkspaces as Workspace
from diagrams.azure.security import KeyVaults
from diagrams.onprem.container import Docker
from diagrams.programming.language import Python

with Diagram(
    "Understanding the hierarchy",
    show=False,
    outformat=["svg", "png"],
) as dac:
    dac.dot.renderer = "cairo"

    with Cluster("Management groups"):

        root = Managementgroups("Root Management Group")

        with Cluster("Subcriptions"):

            it = Managementgroups("IT")
            finance = Managementgroups("Finance")

            with Cluster("Resource groups"):

                prod = Resourcegroups("Prod")
                dev = Resourcegroups("Dev")

                with Cluster("Resources"):

                    sub_a = Subscriptions("Subscription A")
                    sub_b = Subscriptions("Subscription B")
                    sub_c = Subscriptions("Subscription C")

    root >> it
    root >> finance

    it >> prod >> sub_a
    it >> dev >> sub_b

    finance >> sub_c
