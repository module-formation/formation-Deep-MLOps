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

    with Cluster("Root"):

        root = Managementgroups("Root Management Group")

        with Cluster("Management Groups"):

            it = Managementgroups("IT")
            finance = Managementgroups("Finance")

            with Cluster("Management Group"):

                prod = Managementgroups("Prod")
                dev = Managementgroups("Dev")

                with Cluster("Subscription"):

                    sub_a = Subscriptions("Subscription A")
                    sub_b = Subscriptions("Subscription B")
                    sub_c = Subscriptions("Subscription C")

                    with Cluster("Resources Groups MG Prod"):

                        rg_a_prod = Resourcegroups("Resource Group A")
                        rg_b_prod = Resourcegroups("Resource Group B")
                        rg_c_prod = Resourcegroups("Resource Group C")

                    with Cluster("Resources Group MG Dev"):

                        rg_a_dev = Resourcegroups("Resource Group A")

                    with Cluster("Resources Group MG Finance"):

                        rg_a_fin = Resourcegroups("Resource Group A")

    root >> it
    root >> finance

    it >> prod >> sub_a
    it >> dev >> sub_b

    finance >> sub_c
    sub_c >> rg_a_fin

    sub_a >> rg_a_prod
    sub_b >> rg_a_dev
