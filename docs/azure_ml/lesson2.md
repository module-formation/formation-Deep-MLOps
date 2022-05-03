# Lesson 2 : Deploy a model

## Enable Security and Authentication

!!! summary "Summary"

    **Authentication is crucial for the continuous flow of operations**. Continuous Integration and Delivery system (CI/CD) rely on uninterrupted flows. When authentication is not set properly, it requires human interaction and thus, the flow is interrupted. An ideal scenario is that the system doesn't stop waiting for a user to input a password. So whenever possible, it's good to use authentication with automation.

|                                | Key-based Authentication                    | Token-based Authentication                   | Interactive Authentication                                                 |
|          :----------:          | :----------------------------------- :      |    :-----------------------------------:     |                                    :-:                                     |
| Azure Kubernetes Service (AKS) | Azure Kubernetes service enabled by default | Azure Kubernetes service disabled by default |                                                                            |
| Azure Container Instance (ACI) | Not support Azure Container Instances       | Disabled by default                          | Used by local deployment and experimentation (e.g. using Jupyter notebook) |
|                                |                                             |                                              |                                                                            |


### What is Azure Service Principal?

* [Authenticate your Azure deployment pipeline by using service principals](https://docs.microsoft.com/en-us/learn/modules/authenticate-azure-deployment-pipeline-service-principals/)

A “Service Principal” is a user role with controlled permissions to access specific resources. Using a service principal is a great way to allow authentication while reducing the scope of permissions, which enhances security.

If you want to deploy resources to Azure, you need create a sp and give it owner role, of course you could give custom role that only could create public IP and gateway.

When you login Azure with cli 2.0. appid is user name. It also called client id. password called client secret.

When you have an application that needs to access or modify resources, you must set up an Azure Active Directory (AD) application and assign the required permissions to it. This approach is preferable to running the app under your own credentials because:

* You can assign permissions to the app identity that are different than your own permissions. Typically, these permissions are restricted to exactly what the app needs to do.
* You do not have to change the app's credentials if your responsibilities change.
* You can use a certificate to automate authentication when executing an unattended script.

* [Demystifying Service Principals – Managed Identities](https://devblogs.microsoft.com/devops/demystifying-service-principals-managed-identities/)

#### Azure AD Identity

Azure AD is the trusted Identity Object store, in which you can create different Identity Object types. The most common ones are Users and Groups, but you can also have Applications in there, also known as Enterprise Apps.

An example for each could be:

* **Users**: you create a user object in Azure AD, and from there allow the user to authenticate to the Azure Portal, to start using Office 365,…
* **Groups**: you define a security group in Azure AD, which can be used to specify permissions to SharePoint sites for example
* **Enterprise Apps**: using *OpenIDConnect* and *OAuth*, you allow a cloud-based application to trust your Azure AD for user authentication; the trusting app is known as an enterprise app object in Azure AD.

#### Service Principal

Most relevant to Service Principal, is the Enterprise apps; according to the formal definition, a service principal is “…An application whose tokens can be used to authenticate and grant access to specific Azure resources from a user-app, service or automation tool, when an organization is using Azure Active Directory…”

In essence, by using a Service Principal, you avoid creating "**fake users**" (we would call them service account in on-premises Active Directory…) in Azure AD to manage authentication when you need to access Azure Resources.

Typical use cases where you would rely on a Service Principal is for example when running *Terraform IAC* (Infrastructure as Code) deployments, or when using *Azure DevOps* for example, where you define a Service Connection from DevOps Pipelines to Azure; or basically any other 3rd party application requiring an authentication token to connect to Azure resources.

An Azure Service Principal can be created using "any" traditional way like the Azure Portal, Azure PowerShell, Rest API or Azure CLI.


#### Azure cli installation

[see here](https://docs.microsoft.com/fr-fr/cli/azure/install-azure-cli-linux?pivots=apt#option-1-install-with-one-command)


* Add azureml extension for cli.

```
az extension add -n azure-cli-ml
```

*2.* create the service principal.

[Référence](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals)

command that interact with the Active Directory.

```
az ad sp create-for-rbac --sdk-auth --name ml-auth
```

`ml-auth` can be changed to whatever name you want, it's just the name used in the Azure doc.

!!! info "Définition"

    RBAC : Role-Based Access Control


* After running `az ad sp create-for-rbac --sdk-auth --name ml-auth`, Azure responds with output similar to this:

```shell
Changing "ml-auth" to a valid URI of "http://ml-auth", which is the required format used for service principal names
Creating a role assignment under the scope of "/subscriptions/xxxxxxxx-2cb7-4cc5-90b4-xxxxxxxx24c6"
  Retrying role assignment creation: 1/36
  Retrying role assignment creation: 2/36
{
  "clientId": "xxxxxxxx-3af0-4065-8e14-xxxxxxxxxxxx",
  "clientSecret": "xxxxxxxxxxxxx.IPgqLjBH2.Uj6VCo1hk3",
  "subscriptionId": "39b85eca-2cb7-4cc5-90b4-eb1d0c6c24c6",
  "tenantId": "xxxxxxxx-cbdb-4c04-89fc-xxxxxxxxxxxx",
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

* Capture the `objectId` using the `clientId`:

```
az ad sp show --id xxxxxxxx-3af0-4065-8e14-xxxxxxxxxxxx
```

Where `xxxxxxxx-3af0-4065-8e14-xxxxxxxxxxxx` corresponds to the `clientId` value. This step will output some information and you will find the `objectId` to assign the role.

* Finally, allow the Service Principal access to the workspace. You will need to change the code to match your workspace, subscription, and the `objectId` value retrieved from the previous step.

```
az ml worskspace share -w Demo -g demo --user xxxxxxxx-cbdb-4cfd-089f-xxxxxxxxxxxx --role owner
```

Where `xxxxxxxx-cbdb-4cfd-089f-xxxxxxxxxxxx` corresponds to the `objectId` value.

Note: This command should complete without any output


```shell
❯ az ad sp show --id 4f9ebbd3-c840-4900-97d6-e4b0e3329b61 | jq ".oauth2Permissions[0]"

{
  "adminConsentDescription": "Allow the application to access ml-auth on behalf of the signed-in user.",
  "adminConsentDisplayName": "Access ml-auth",
  "id": "xxxxxxxx-27da-xxxxxxx-989c-xxxxxxxxx",
  "isEnabled": true,
  "type": "User",
  "userConsentDescription": "Allow the application to access ml-auth on your behalf.",
  "userConsentDisplayName": "Access ml-auth",
  "value": "user_impersonation"
}
```


### Configure Deployment Settings

**Deployment is about delivering a trained model into production so that it can be consumed by others.** Configuring deployment settings means making choices on cluster settings and other types of interaction with a deployment. Having a good grasp on configuring production environments in Azure ML Studio and the Python SDK is the key to get robust deployments.
ACI and AKS

**Both ACI and AKS are available in the Azure ML platform as deployment options for models.**

ACI is a container offering from Azure, which uses container technology to quickly deploy compute instances. The flexibility of ACI is reduced as to what AKS offers, but it is far simpler to use.

AKS, on the other hand, is a Kubernetes offering. The Kubernetes service is a cluster that can expand and contract given on demand, and it does take more effort than the container instance to configure and setup.

!!! info "Définition"

    * **ACI**: Azure Container Instance
    * **AKS**: Azure Kubernetes Service
    * **Deployment**: A way to deliver work into production
    * **Concurrent Operations**: Also referred to as "concurrency", it is the number of operations to run at the same time

## Deploy an Azure Machine Learning model

!!! summary "Summary"

    The primary task as a Machine Learning engineer is to ship models into production. Constant evaluation allows identifying potential issues and creating a baseline so that adapting or updating is possible.

    Some key steps to deploy a model are:

    * A previously trained model
    * Complete the deployment form
    * Enable authentication
    * Select or create a new compute cluster

### Enable Application Insights

In this section, we discussed Application Insights that is a very useful tool to detect anomalies, visualize performance. It can be enabled before or after a deployment. To enable Application Insights after a model is deployed, you can use the below command with the python SDK. In the next section, you will learn how to do it.

```python
# enable application insight
service.update(enable_app_insights=True)
```

!!! info "Définition"

    * **Logging**: Informational output produced by the software, usually in the form of text
    * **Application Insights**: A special Azure service which provides key facts about an application
    * **Webservice**: One of the most used Python classes from Azure's Python SDK

### Troubleshoot Deployment Issues

!!! summary "Summary"

    In this section, we covered different techniques and diagnosis that you can use to identify potential issues like unhandled exceptions from a deployed service. Using local deployment is a special technique, which makes it easier to identify some of these potential issues.
    Common HTTP errors:

    * **502**: the application crashes because of an unhandled exception.
    * **503**: there are large spikes in requests and the system is not able to cope with all of them.
    * **504**: request timed out.

### Deploy Locally

To deploy locally using the Python SDK you will need to use the LocalWebService class and configure it for a local deployment

```python
from azureml.core.webservice import LocalWebservice
deployment_config = LocalWebservice.deploy_configuration(port=9001)
# Deploy the service
service = Model.deploy(ws, "local-service", [model], inference_config, deployment_config)

service.reload()
print(service.run(input_data=json_data))
```

Deploying locally has some benefits. First, it is easier and faster to verify unhandled exceptions from the scoring script since you don't have to wait for deployment in Azure. Also, many people or teams can debug at the same time.

!!! info "Définition"

    **HTTP Status code**: A number that represents a status when an HTTP server responds. Error conditions in the server side start at 500

There are multiple things you can expect to go wrong. When you submit HTTP requests to a deployed model, there are three HTTP codes that you may encounter:

* **HTTP STATUS 502**: After a deployment, the application crashes because of an unhandled exception.
* **HTTP STATUS 503**: When there are large spikes in requests, the system may not be able to cope with all of them and some clients may see this code.
* **HTTP STATUS 504**: The request timed out. In Azure, the requests time out after 1 minute. If the score.py script is taking longer than a minute, this error code will be produced.

When an error code shows up, one thing you can do is retrieving the logs output. Logs output is always useful to debug problems in deployed containers. Showing below is an extract of what you should see in a successful response to a scoring request.

```shell
Validation Request Content-Type
Received input: {'data': [{'instant': 1, 'date': '2011-01-01 00:00:00,000000', 'season': 1, 'yr': 0, 'mnth': 1, 'weekday': 6, 'weathersit': 2, 'temp': 0.344167, 'atemp': 0.363625, 'hum': 0.805833, 'windspeed': 0.160446, 'casual': 331, 'registered': 654 }]}
Headers passed in (total 12):
    Host: localhost:5001
    X-Real-Ip: 127.0.0.1
    X-Forwarded-For: 127.0.0.1
    X-Forwarded-Proto: http
    Connection: close
    Content-Length: 812
    User-Agent: ApacheBench/2.3
    Accept: */*
    Authorization: Bearer q8szMDbCoNlxDZCpiGI8tnqaxtC1yDiy
    Content-Type: application/json
    X-Ms-Request-Id: 7cb6f8b9-e511-43b7-982f-e413d6e3239d
    Accept-Encoding: gzip
Scoring Timer is set to 60.0 seconds
200
```

!!! info "Définition"

    * **ACI**: Azure Container Instance
    * **AKS**: Azure Kubernetes Service
    * **Application Insights**: A special Azure service which provides key facts about an application
    * **CI/CD**: Continuous Integration and Continuous Delivery platform. Jenkins, CircleCI, and Github Actions, are a few examples
    * **Cloud-based workstation**: Sometimes, compute instances are referred to as a cloud-based workstation, because it is ready to start developing
    * **Compute Instance**: A distinct type of a compute offering from Azure
    * **DevOps**: A set of best practices that helps provide continuous delivery of software at the highest quality with a constant feedback loop
    * **Deployment**: A way to deliver work into production
    * **Endpoint**: A part of an HTTP API. Either a full URL or a partial URL identifying a part
    * **HTTP API**: A URL that exposes logic to interact with software, in this case, a trained model
    * **HTTP Status code**: A number that represents a status when an HTTP server responds. Error conditions in the server side start at 500
    * **Logging**: Informational output produced by software, usually in the form of text
    * **Shipping into production**: The most important aspect of a Machine Learning specialist
    * **Webservice**: One of the most used Python classes from Azure's Python SDK
