```python
from azureml.core.dataset import Dataset

url_paths = [
            'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
            'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
            ]

dataset = Dataset.File.from_files(path=url_paths)

df = dataset.to_pandas_dataframe()


ws = Workspace.from_config()
blob_store = Datastore(ws, "workspaceblobstore")
compute_target = ws.compute_targets["STANDARD_NC6"]
experiment = Experiment(ws, 'MyExperiment')

input_data = Dataset.File.from_files(
    DataPath(datastore, '20newsgroups/20news.pkl'))



output_data = PipelineData("output_data", datastore=blob_store)

input_named = input_data.as_named_input('input')

steps = [ PythonScriptStep(
    script_name="train.py",
    arguments=["--input", input_named.as_download(),
        "--output", output_data],
    inputs=[input_data],
    outputs=[output_data],
    compute_target=compute_target,
    source_directory="myfolder"
) ]

pipeline = Pipeline(workspace=ws, steps=steps)

pipeline_run = experiment.submit(pipeline)
pipeline_run.wait_for_completion()
```


1. Listing Past Experiments

To do this, we need to pass in a workspace object, and then list the collection of trials. This will give us data very similar to the list we've accessed previously using the Designer. Here's the example code we looked at:

```python
from azureml.core.experiment import Experiment

# First, we pass in the workspace object `ws` to the `list` method
# and it returns a Python list of `Experiment` objects.
list_experiments = Experiment.list(ws)

# If we print the contents of the variable,
# we can see the list of all the experiments
# that have been run in that workspace.
print(list_experiments)
[Experiment(Name: dataset_profile,
 Workspace: Azure-ML-Workspace), Experiment(Name: binary-classification,
 Workspace: Azure-ML-Workspace), Experiment(Name: regression,
 Workspace: Azure-ML-Workspace), Experiment(Name: sfautoml]
```

2. Submitting New Experiments

To submit a new experiment (such as if we wanted to try a different model type or a different algorithm), we would again pass in a workspace object and then submit the experiment. Here's the example code:


```python
from azureml.core.experiment import Experiment

experiment = Experiment(ws, "automl_test_experiment")
run = experiment.submit(config=automl_config, show_output=True)
```

Main Steps for Tuning with HyperDrive

    Define the parameter search space. This could be a discrete/categorical variable (e.g., apple, banana, pair) or it can be a continuous value (e.g., a time series value).
    Define the sampling method over the search space. This is a question of the method you want to use to find the values. For example, you can use a random, grid, or Bayesian search strategy.
    Specify the primary metric to optimize. For example, the Area Under the Curve (AUC) is a common optimization metric.
    Define an early termination policy. An early termination policy specifies that if you have a certain number of failures, HyperDrive will stop looking for the answer.

Note that to use HyperDrive, you must have a custom-coded machine learning model. Otherwise, HyperDrive won't know what model to optimize the parameters for!
Controlling HyperDrive with the SDK

You can control HyperDrive with the SDK. Here is the example code we looked at in the video:

```python
from azureml.train.hyperdrive import BayesianParameterSampling
from azureml.train.hyperdrive import uniform, choice
param_sampling = BayesianParameterSampling( {
        "learning_rate": uniform(0.05, 0.1),
        "batch_size": choice(16, 32, 64, 128)
    }
)
```
We also saw that we can specify whether we are tuning a discrete or continuous variable.

Discrete example:

```json
{
    "batch_size": choice(16, 32, 64, 128)
    "number_of_hidden_layers": choice(range(1,5))
    }
```
Continuous example:

```json
{
    "learning_rate": normal(10, 3),
    "keep_probability": uniform(0.05, 0.1)
    }
```

And finally, we will need to find the best model parameters. Here's an example:

```python
best_run = hyperdrive_run.get_best_run_by_primary_metric()
best_run_metrics = best_run.get_metrics()
parameter_values = best_run.get_details()['runDefinition']['Arguments']

print('Best Run Id: ', best_run.id)
print('\n Accuracy:', best_run_metrics['accuracy'])
print('\n learning rate:',parameter_values[3])
print('\n keep probability:',parameter_values[5])
print('\n batch size:',parameter_values[7])
```

The ultimate result is that we are able to choose the best tuning and use it in our final machine learning model.

Traditional ML

To understand why Automated ML is a useful tool, it helps to first understand some of the challenges we face with traditional ML. These include:

* Focus on technical details vs the business problem. The code and technical details can consume large amounts of the available resources, distracting our focus from the business problem we want to use the ML to solve.
* Lack of automation. With traditional ML, we have to do many things manually, even though they could easily be automated with tools like Azure ML Studio.
* Too much HiPPO influence. The Highest Paid Person's Opinion (HiPPO) can have an unduly large influence on decisions about the output of the model, even though this decision might be better made automatically.
* Feature engineering. What are the features that I need to get the best accuracy? What are the columns I should select? This can be a huge task that requires a lot of human effort.
* Hyperparameter selection. For example, with a clustering model, what number of clusters will give the best results? There can be a lot of trial and error and many false starts.
* Training and Tuning. What are the different parameters you're using when training your model? What machines and resources should you use? How should you best tune the parameters? In traditional ML, these questions require a human to supervise the process.

Automated ML

Automated ML can help with all of the above problems. Essentially, AutoML involves the application of DevOps principles to machine learning, in order to automate all aspects of the process. For example, we can automate feature engineering, hyperparameter selection, model training, and tuning. With AutoML, we can:

* Create hundreds of models a day
* Get better model accuracy
* Deploy models faster

This creates a quicker feedback loop and allows us to bring ideas to market much sooner. Overall, it reduces the time that we have to spend on technical details, allowing for more effort to be put into solving the underlying business problems.


Configuring AutoML from the SDK

We can easily leverage AutoML from the SDK to automate many aspects of our pipeline, including:

    Task type
    Algorithm iterations
    Accuracy metric to optimize
    Algorithms to blacklist/whitelist
    Number of cross-validations
    Compute targets
    Training data

To do this, we first use the AutoMLConfig class. In the code example below, you can see that we are creating an automl_config object and setting many of the parameters listed above:


```python
from azureml.train.automl import AutoMLConfig

automl_config = AutoMLConfig(task="classification",
                             X=your_training_features,
                             y=your_training_labels,
                             iterations=30,
                             iteration_timeout_minutes=5,
                             primary_metric="AUC_weighted",
                             n_cross_validations=5
                            )
```

Running AutoML from the SDK

Once we have completed our configuration, we can then run it using the SDK. Here's a typical example of what that would look like:

```python
from azureml.core.experiment import Experiment

experiment = Experiment(ws, "automl_test_experiment")
run = experiment.submit(config=automl_config, show_output=True)
```
## AutoML Notebook

# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
# azureml-core of version 1.0.72 or higher is required
# azureml-dataprep[pandas] of version 1.1.34 or higher is required
from azureml.core import Workspace, Dataset
subscription_id = '6971f5ac-8af1-446e-8034-05acea24681f'
resource_group = 'aml-quickstarts-190413'
workspace_name = 'quick-starts-ws-190413'


workspace = Workspace(subscription_id, resource_group, workspace_name)

dataset = Dataset.get_by_name(workspace, name='Nba-Dataset')
dataset.to_pandas_dataframe()

from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
import pandas as pd

ws = Workspace.from_config()

# choose a name for experiment
experiment_name = 'automl-nba-position'

experiment=Experiment(ws, experiment_name)

output = {}
output['Subscription ID'] = ws.subscription_id
output['Workspace'] = ws.name
output['Resource Group'] = ws.resource_group
output['Location'] = ws.location
output['Experiment Name'] = experiment.name
pd.set_option('display.max_colwidth', -1)
outputDf = pd.DataFrame(data = output, index = [''])
outputDf.T

from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException

# Choose a name for your CPU cluster
cpu_cluster_name = "auto-ml"

# Verify that cluster does not exist already
try:
    compute_target = ComputeTarget(workspace=ws, name=cpu_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                                                           max_nodes=6)
    compute_target = ComputeTarget.create(ws, cpu_cluster_name, compute_config)

compute_target.wait_for_completion(show_output=True)


from azureml.train.automl import AutoMLConfig
automl_settings = {
    "experiment_timeout_hours" : 0.3,
    "enable_early_stopping" : True,
    "iteration_timeout_minutes": 5,
    "max_concurrent_iterations": 4,
    "max_cores_per_iteration": -1,
    #"n_cross_validations": 2,
    "primary_metric": 'AUC_weighted',
    "featurization": 'auto',
    "verbosity": logging.INFO,
}

automl_config = AutoMLConfig(task = 'classification',
                             debug_log = 'automl_errors.log',
                             compute_target=compute_target,
                             experiment_exit_score = 0.9984,
                             blocked_models = ['KNN','LinearSVM'],
                             enable_onnx_compatible_models=True,
                             training_data = dataset,
                             label_column_name ='POSITION',
                             **automl_settings
                            )

remote_run = experiment.submit(automl_config, show_output = False)

# Lesson 2 : Deploy a model

## Enable Security and Authentication

Summary

Authentication is crucial for the continuous flow of operations. Continuous Integration and Delivery system (CI/CD) rely on uninterrupted flows. When authentication is not set properly, it requires human interaction and thus, the flow is interrupted. An ideal scenario is that the system doesn't stop waiting for a user to input a password. So whenever possible, it's good to use authentication with automation.
Authentication types
Key- based

* Azure Kubernetes service enabled by default
* Azure Container Instances service disabled by default

Token- based

* Azure Kubernetes service disabled by default
* Not support Azure Container Instances

Interactive

* Used by local deployment and experimentation (e.g. using Jupyter notebook)

Service Principal

A “Service Principal” is a user role with controlled permissions to access specific resources. Using a service principal is a great way to allow authentication while reducing the scope of permissions, which enhances security.

New terms

* CI/CD: Continuous Integration and Continuous Delivery platform. Jenkins, CircleCI, and Github Actions are a few examples.

Further reading

Both the Jenkins and Github Actions websites have good information about their CI/CD platforms and why they are compelling the CI/CD platform.

| Azure Service | Key-based Authorization|
| Azure Kubernetes Service (AKS) | Enabled by default|
| Azure Container Instance (ACI)| Disabled by default|

## Azure cli installation

[see here](https://docs.microsoft.com/fr-fr/cli/azure/install-azure-cli-linux?pivots=apt#option-1-install-with-one-command)

* Add azureml extension for cli

```
az extension add -n azure-cli-ml
```

* create the service principal

https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals

command that interact with the Active Directory.

```
az ad sp create-for-rbac --sdk-auth --name ml-auth
```

ml-auth can be changed to whatever name you want, it's just the name used in the Azure doc.

rbac : Role-Based Access Control


* After running az ad sp create-for-rbac --sdk-auth --name ml-auth, Azure responds with output similar to this:

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

* Capture the "objectId" using the clientID:

```
az ad sp show --id xxxxxxxx-3af0-4065-8e14-xxxxxxxxxxxx
```

This step will output some information and you will find the objectID to assign the role.

* Finally, allow the Service Principal access to the workspace. You will need to change the code to match your workspace, subscription, and the objectId value retrieved from the previous step.

```
az ml worskspace share -w Demo -g demo --user xxxxxxxx-cbdb-4cfd-089f-xxxxxxxxxxxx --role owner
```

Note: This command should complete without any output

## Configure Deployment Settings

Deployment is about delivering a trained model into production so that it can be consumed by others. Configuring deployment settings means making choices on cluster settings and other types of interaction with a deployment. Having a good grasp on configuring production environments in Azure ML Studio and the Python SDK is the key to get robust deployments.
ACI and AKS

Both ACI and AKS are available in the Azure ML platform as deployment options for models.

ACI is a container offering from Azure, which uses container technology to quickly deploy compute instances. The flexibility of ACI is reduced as to what AKS offers, but it is far simpler to use.

AKS, on the other hand, is a Kubernetes offering. The Kubernetes service is a cluster that can expand and contract given on demand, and it does take more effort than the container instance to configure and setup.
New terms

* ACI: Azure Container Instance
* AKS: Azure Kubernetes Service
* Deployment: A way to deliver work into production
* Concurrent Operations: Also referred to as "concurrency", it is the number of operations to run at the same time

## Deploy an Azure Machine Learning model

Summary

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

New terms

    Logging: Informational output produced by the software, usually in the form of text
    Application Insights: A special Azure service which provides key facts about an application
    Webservice: One of the most used Python classes from Azure's Python SDK

### Troubleshoot Deployment Issues

Summary

In this section, we covered different techniques and diagnosis that you can use to identify potential issues like unhandled exceptions from a deployed service. Using local deployment is a special technique, which makes it easier to identify some of these potential issues.
Common HTTP errors:

    502: the application crashes because of an unhandled exception.
    503: there are large spikes in requests and the system is not able to cope with all of them.
    504: request timed out.

Deploy Locally

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
New terms

    HTTP Status code: A number that represents a status when an HTTP server responds. Error conditions in the server side start at 500

There are multiple things you can expect to go wrong. When you submit HTTP requests to a deployed model, there are three HTTP codes that you may encounter:

    HTTP STATUS 502: After a deployment, the application crashes because of an unhandled exception.
    HTTP STATUS 503: When there are large spikes in requests, the system may not be able to cope with all of them and some clients may see this code.
    HTTP STATUS 504: The request timed out. In Azure, the requests time out after 1 minute. If the score.py script is taking longer than a minute, this error code will be produced.

When an error code shows up, one thing you can do is retrieving the logs output. Logs output is always useful to debug problems in deployed containers. Showing below is an extract of what you should see in a successful response to a scoring request.

```
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

### Glossary

    ACI: Azure Container Instance
    AKS: Azure Kubernetes Service
    Application Insights: A special Azure service which provides key facts about an application
    CI/CD: Continuous Integration and Continuous Delivery platform. Jenkins, CircleCI, and Github Actions, are a few examples
    Cloud-based workstation: Sometimes, compute instances are referred to as a cloud-based workstation, because it is ready to start developing
    Compute Instance: A distinct type of a compute offering from Azure
    DevOps: A set of best practices that helps provide continuous delivery of software at the highest quality with a constant feedback loop
    Deployment: A way to deliver work into production
    Endpoint: A part of an HTTP API. Either a full URL or a partial URL identifying a part
    HTTP API: A URL that exposes logic to interact with software, in this case, a trained model
    HTTP Status code: A number that represents a status when an HTTP server responds. Error conditions in the server side start at 500
    Logging: Informational output produced by software, usually in the form of text
    Shipping into production: The most important aspect of a Machine Learning specialist
    Webservice: One of the most used Python classes from Azure's Python SDK

# Lesson 3 : Consume Endpoints

Summary

This is the lesson about Consuming Endpoints. These endpoints allow other services to interact with deployed models. And in this lesson, you will learn all the key facts about interacting with them.

There are some interesting details you need to be aware of when trying to use HTTP and you will go through each of these:

    Swagger
    Consuming deployed services
    Benchmarking

New terms

    Swagger: A tool that eases the documentation efforts of HTTP APIs
    Benchmarking: being able to create a baseline of acceptable performance so that it can be compared to day-to-day behavior

## Exercise: Swagger Documentation

Note: in the video, the instructor used localhoston port 80 to display the Swagger page. It may not work for everyone. If localhost doesn't work for you, check if you can use a different port other than 80, for example, port 9000. Ensure that the updated port is used when trying to reach the swagger instance by localhost, for example localhost:9000.

If you see code 400, message bad request version in the Python script, it means that you are using https instead of http in the Swagger page. Remember to use http only when accessing these URLs.
Summary

In the Swagger.sh file, it has a command line:

docker run -p 80:8080 swaggerapi/swagger-ui

This command runs the swagger UI container and makes it available on port 80. This will need to be updated in the lab because port 80 is being used already. Set the port to 9000 would be a good choice here. So the updated command will look like this:

docker run -p 9000:8080 swaggerapi/swagger-ui

After the Swagger UI container is running, you can access the website on http://localhost:9000.

Running serve.py is crucial so that the contents of swagger.json can be consumed locally by Swagger. If swagger.json is not present, or if the local server is not running, then Swagger will not be able to produce the docs.

To give you more information: running serve.py is needed because Azure protects against CORS (Cross Origin Resource Sharing) and the server that hosts swagger.json needs to be allowed to happen. This is done in the script with the following method:

```python
def end_headers(self):
    self.send_header("Access-Control-Allow-Origin", "*")
    SimpleHTTPRequestHandler.end_headers(self)
```

Note: the above information is not closely related to the course and will not be tested in the final project. It is just for those who are interested in the commands in serve.py.

By default, the serve.py script will run and serve contents on localhost:8000 - this is an important detail because it is required as input in the Swagger UI page. The value that is required in the Swagger UI is http://localhost:8000/swagger.json. Please notice that you should use http instead of https.

Both serve.py and swagger.sh can be found in the nd00333_AZMLND_C2-master/Exercise_starter_files directory in the course Github repo or on the lab desktop.
Exercise: Swagger documentation

In this exercise, run both swagger.sh and serve.py to get Docker running locally serving Swagger so that you can interact with the deployed model Documentation. Use the http://localhost/ and http://localhost:8000/swagger.json, to look at your swagger document and specifics of your model.

Tips: if you change the Swagger UI port to something other than 80, http://localhost/ will not load the Swagger page. You need to include the new port to load the Swagger page. For example, use http://localhost:9000 if the new port is set to 9000.

## Consume Deployed Service

Summary

You can consume a deployed service via an HTTP API. An HTTP API is a URL that is exposed over the network so that interaction with a trained model can happen via HTTP requests.

Users can initiate an input request, usually via an HTTP POST request. HTTP POST is a request method that is used to submit data. The HTTP GET is another commonly used request method. HTTP GET is used to retrieve information from a URL. The allowed requests methods and the different URLs exposed by Azure create a bi-directional flow of information.

The APIs exposed by Azure ML will use JSON (JavaScript Object Notation) to accept data and submit responses. It served as a bridge language among different environments.
New terms

    JSON: JavaScript Object Notation, also referred to as a "bridge language" used to make communication possible between two groups who do not share a native dialect
    GET request method: GET is a request method supported by HTTP. This method should only be used to retrieve data from a web server
    POST request method: POST is a request method supported by HTTP. This method requests that a web server accepts the data enclosed in the body of the request message


Solution: Consume Deployed Service

    In Azure ML Studio, head over to the "Endpoints" section and find a previously deployed model. The compute type should be ACI (Azure Container Instance).

    In the "Consume" tab, of the endpoint, a "Basic consumption info" will show the endpoint URL and the authentication types. Take note of the URL and the "Primary Key" authentication type.

    Using the provided endpoint.py replace the scoring_uri and key to match the REST endpoint and primary key respectively. The script issues a POST request to the deployed model and gets a JSON response that gets printed to the terminal.

Running it should produce similar results to this:

python endpoint.py
{"result": [2553]}

A data.json file will appear after you run endpoint.py

Note: the instructor used a different target column in the demo other than cnt. So the result displayed in the demo would be different from yours if you use cnt as the target column. Your display should be similar to {"result": [2553]}

## Benchmark the Endpoint

Summary

A benchmark is used to create a baseline or acceptable performance measure. Benchmarking HTTP APIs is used to find the average response time for a deployed model.

One of the most significant metrics is the response time since Azure will timeout if the response times are longer than sixty seconds.

Apache Benchmark is an easy and popular tool for benchmarking HTTP services. You will learn about it on the next page.
New terms

    Response Time: The time in seconds (or milliseconds) that service takes to produce a response
    Timeout: When a request is sent, this is an error when the server cannot produce a response in a given amount of time

Summary

Benchmarking services is an interesting topic. Everyone likes to have a highly performant endpoint, but the answer to what it takes to have a performant endpoint varies. It is useful to create a baseline for benchmarks so that comparing subsequent results is meaningful.

The benchmark.sh script doesn't have much code at all in it. It does include the ab command that runs against the selected endpoint using the data.json file created by the same endpoint.py file you used in the previous exercise. The ab command looks like this:

ab -n 10 -v 4 -p data.json -T 'application/json' -H 'Authorization: Bearer SECRET' http://URL.azurecontainer.io/score

After running the benchmark.sh or simply after running the above command, you will see the output of requests sent to and responses from the endpoint, and at the end, a summary with key information to determine response performance.

You can find the provided endpoint.py and benchmark.sh script in the Exercise_starter_files directory in the GitHub repo or on the lab desktop nd00333_AZMLND_C2-master/Exercise_starter_files directory.
Exercise: Benchmark the endpoint

In this exercise use the Apache Benchmark command-line tool (ab) to generate lots of HTTP POST requests to get performance metrics out of the Azure Container Instance.

Make sure you have the Apache Benchmark command-line tool installed and available in your path:

which ab
/usr/bin/ab

ab --help
Usage: ab [options] [http[s]://]hostname[:port]/path
Options are:
...

You can use the provided endpoint.py and benchmark.sh script in the Exercise_starter_files directory to generate the benchmark. Make sure you modify it to match the URI and Keys.

https://ubiq.co/tech-blog/how-to-use-apache-bench-for-load-testing/

## Curating Data Input

Summary

There are some key items to ensure when sending data to a deployed endpoint. You need to make sure that the keys and values are following the constraints. For example, if one field is repeated, this could potentially cause an error response, or if the format needs a date and time as a string, rather than an integer.

Remember, using values that the service doesn't expect would produce an error response.

## Glossary

    Benchmarking: being able to create a baseline of acceptable performance so that it can be compared to day-to-day behavior
    GET request method: GET is a request method supported by HTTP. This method should only be used to retrieve data from a web server
    JSON: JavaScript Object Notation, also referred to as a "bridge language" used to make communication possible between two groups who do not share a native dialect
    POST request method: POST is a request method supported by HTTP. This method requests that a web server accepts the data enclosed in the body of the request message
    RESTful: A style for building HTTP endpoints that emphasizes separation of concerns
    Response Time: The time in seconds (or milliseconds) that service takes to produce a response
    Swagger: A tool that eases the documentation efforts of HTTP APIs
    Timeout: When a request is sent, this is an error when the server cannot produce a response in a given amount of time


# Lesson 4 : Pipeline automation

## Create a Pipeline
Summary

The most common SDK class is the Pipeline class. You will use this when creating a Pipeline. Pipelines can take configuration and different steps, like AutoML for example.

Different steps can have different arguments and parameters. Parameters are just like variables in a Python script.

There are areas you can play with when creating a pipeline and we covered two:

    Use pipeline parameters
    Recurring Scheduled Pipelines
    Batch Inference Pipelines

Create a Pipeline

This is the most common Python SDK class you will see when dealing with Pipelines. Aside from accepting a workspace and allowing multiple steps to be passed in, it uses a description that is useful to identify it later.

```python
from azureml.pipeline.core import Pipeline

pipeline = Pipeline(
    description="pipeline_with_automlstep",
    workspace=ws,
    steps=[automl_step])
```

Using Pipeline Parameters

Pipeline parameters are also available as a class. You configure this class with the various different parameters needed so that they can later be used.

In this example, the avg_rate_param is used in the arguments attribute of the PythonScriptStep.

```python
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import PipelineParameter

avg_rate_param = PipelineParameter(name="avg_rate", default_value=0.5)
train_step = PythonScriptStep(script_name="train.py",
                              arguments=["--input", avg_rate_param],
                              target=compute_target,
                              source_directory=project_folder)
```

Scheduling a recurring Pipeline

To schedule a Pipeline, you must use the ScheduleRecurrence class which has the information necessary to set the interval.

Once that has been created, it has to be passed into the create() method of the Schedule class as a recurrence value.

```python
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule

hourly = ScheduleRecurrence(frequency="Hourly", interval=4)
pipeline_schedule = Schedule.create(ws, name="RecurringSchedule",
                            description="Trains model every few hours",
                            pipeline_id=pipeline_id,
                            experiment_name="Recurring_Pipeline_name",
                            recurrence=hourly)
```

Batch Inference Pipeline

One of the core responsibilities of a batch inference pipeline is to run in parallel. For this to happen, you must use the ParallelRunConfig class which helps define the configuration needed to run in parallel.

Some important aspects of this are the script that will do the work (entry_script), how many failures it should tolerate (error_threshold), and the number of nodes/batches needed to run (mini_batch_size, 5 in this example).

```python
from azureml.pipeline.steps import ParallelRunConfig

parallel_run_config = ParallelRunConfig(
    source_directory='scripts',
    entry_script="scoring.py",
    mini_batch_size="5",
    error_threshold=4,
    output_action="append_row",
    environment=batch_env,
    compute_target=aml_target,
    node_count=5)

parallelrun_step = ParallelRunStep(
    name="batch-score",
    parallel_run_config=parallel_run_config,
    inputs=[batch_data_set.as_named_input('batch_data')],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)

# create the pipeline
pipeline = Pipeline(workspace=ws, steps=[parallerun_step])
```

New terms

    Batch inference: The process of doing predictions using parallelism. In a pipeline, it will usually be on a recurring schedule
    Recurring schedule: A way to schedule pipelines to run at a given interval
    Pipeline parameters: Like variables in a Python script, these can be passed into a script argument


## Exercise: Create a Pipeline

In the demo, the instructor will use a Jupyter notebook aml-pipelines-with-automated-machine-learning-step.ipynb. You can find this notebook in the Exercise_starter_file in the course Github or in the nd00333_AZMLND_C2-master > Exercise_starter_file folder on the lab desktop.

You will need to upload the above notebook to the Notebooks section of the Azure Machine Learning Workspace and then access it via the Compute Instance section.

⚠️ IMPORTANT: Make sure you are using this notebook via the compute instance (i.e., do not run it in the local Python environment).
Part 1 - Set up the workspace
Part 2 - Create a pipeline with AutoML steps
Summary

Pipelines are very useful and are a foundation of automation and operations in general. Being able to create a Pipeline allows for easier interaction with model deployments.

This demo showed you how to use the Python SDK to create a pipeline with AutoML steps. Feel free to use the provide Jupyter notebook in the Exercise_starter_file directory to explore different features.
Exercise: Create a pipeline

For this exercise, you will create a pipeline using the python SDK.

You have already seen theaml-pipelines-with-automated-machine-learning-step.ipynb notebook (up to Examine Results section) provided in the exercise starter files. Now, review the code and try to write your own code to create and run the pipelines. If you get stuck, check the notebook provided to you.

First, create a pipeline using the Python SDK. (This is the part that up until the Examine Results section in the provided notebook)

It is optional, you can copy and run cells in Examine Results section to test the pipeline and retrieve the best model. This step involves running an Automated ML experiment so it will take about 30 min to complete. Please keep track of the remaining time before you run these cells.

Tips: Make sure you update cells to match your dataset and other variables. These are noted in comments like this:

# Choose a name for the run history container in the workspace.
# NOTE: update these to match your existing experiment name
experiment_name = 'ml-experiment-1'
project_folder = './pipeline-project'

Free free to modify the code to explore the different pipeline features and parameters. To speed up and shorten the total amount to train the model, you can change the "experiment_timeout_minutes" value from 20 to 10. These settings are in the Python Notebook, which are currently set to 20 minutes:

automl_settings = {
    "experiment_timeout_minutes": 20,
    "max_concurrent_iterations": 4,
    "primary_metric" : 'normalized_root_mean_squared_error',
    "n_cross_validations": 5
}

Note: Be careful with your configuration if you use the lab provided to you. Your experiment will timeout after a certain amount of time, please keep track of the time remaining for the lab!

Create and run the pipelines using the Python SDK.
Task List

Part 2: Publish a pipeline

In this part, you need to publish a pipeline using the both Azure ML studio and the Python SDK. Please re-use the Pipeline created in the previous part.

You are recommended to write your own code to publish the pipeline. If you get stuck, review the first a few cells in the " Publish and run from REST endpoint" section in the provided notebook.

Note: Your experiment will timeout after a certain amount of time, please keep track of the time remaining for the lab!



# Annex : traefik and azure vm

https://kumar-allamraju.medium.com/using-traefik-as-a-layer-7-ingress-controller-in-azure-kubernetes-service-2997eb29228b

Using Traefik as a Layer 7 Ingress Controller in Azure Kubernetes Service

Traefik is the leading open source reverse proxy and load balancer for HTTP/HTTPS and TCP-based applications that makes deploying micro services very easy.

Traefik integrates with your existing infrastructure components (Docker, Kubernetes, AKS, EKS, GKE etc..) and configures itself automatically and dynamically. Pointing Traefik at your orchestrator (e.g. AKS) should be the *only* configuration step we need to do.

In this article I plan to talk about how to integrate traefik with AKS.

Consider a scenario where you have deployed a bunch of micro services in your Azure Kubernetes cluster. Now you want users to access these micro services, from public internet. Traditional reverse-proxies like NGINX ingress controller requires you to configure each route that will connect paths and subdomains to each micro service. In an environment where you add, remove, kill, upgrade, or scale your services many times a day, the task of keeping the routes up to date becomes tedious.

Traefik comes to the rescue and simplifies the networking complexity while designing, deploying and running micro services. Run Traefik and let it do the work for you! (But if you’d rather configure some of your routes manually, Traefik supports that too!)

## Pre-requisites

* An Azure subscription. If you don’t have one, sign up here for free
* Install az cli
* Run `az login` and authenticate to your Azure subscription
* Install `kubectl`

## Steps to configure Traefik in AKS Cluster

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

## Frontend Types in Traefik

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

## Path Bath Routing

This routing rule is helpful if you want to host all your services under one domain. All we have to do is specify the path instead of the domain name. You will also notice in the yaml file we are configuring Traefik to strip the prefix from the url path with traefik.frontend.rule.type annotation

`kubectl apply -f https://raw.githubusercontent.com/containous/traefik/v1.7/examples/k8s/cheeses-ingress.yaml`

We should now visit the website with a single domain name

i.e. http://{custom-domain.com}/stilton, http://{custom-domain.com}/cheddar, http://{custom-domain.com}/wensleydale

## Conclusion

Traefik is an open-source Edge Router that makes publishing your services a fun and easy experience. It receives requests on behalf of your system and finds out which components are responsible for handling them.

What sets Traefik apart, besides its many features, is that it automatically discovers the right configuration for your services. The magic happens when Traefik inspects your infrastructure, where it finds relevant information and discovers which service serves which request.

Traefik is natively compliant with every major cluster technology, such as Kubernetes, Docker, AKS, AWS, Mesos, Marathon, and the list goes on; and can handle many at the same time. (It even works for legacy software running on bare metal.) With Traefik, you spend time developing and deploying new features to your system, not on configuring and maintaining its working state.
References

    https://docs.traefik.io/
    https://containo.us/traefik/
    https://docs.traefik.io/getting-started/install-traefik/
    https://azure.microsoft.com/en-us/services/kubernetes-service/


# Annex : Automatic HTTPS with Azure Container Instances (ACI)

https://itnext.io/automatic-https-with-azure-container-instances-aci-4c4c8b03e8c9

Automatic HTTPS with Azure Container Instances (ACI)

Let’s assume you want to deploy a simple containerized application or service to the Azure cloud. Additionally, your service needs to be reachable publicly via HTTPS. This technical article shows you how to achieve this goal.
Azure Container Instances

According to the architecture guide Choosing an Azure compute service you’ve got several options to deploy your containerized service, one of them is Azure Container Instances (ACI):

    Container Instances: The fastest and simplest way to run a container in Azure, without having to provision any virtual machines and without having to adopt a higher-level service.

Simple also means that you don’t get all the options and features of a full-blown orchestration solution, such as Azure Kubernetes Service (AKS). ACI provides features like sidecars and persistent volumes. With ACI, however, you have to live with a downtime when upgrading your deployment.

And you have to set up TLS manually. There is a guide, Enable TLS with a sidecar container, which tells you how to set up HTTPS with Nginx and a self-signed certificate. Ugh. The guide also mentions Caddy as an alternate TLS provider but doesn’t provide more details.
Caddy

    Caddy 2 is a powerful, enterprise-ready, open source web server with automatic HTTPS written in Go.

Ok, sounds nice! Automatic HTTPS sounds really intriguing. What does it mean? “Caddy obtains and renews TLS certificates for your sites automatically. It even staples OCSP responses.” Wow! But how is this done?

“Caddy serves public DNS names over HTTPS using certificates from a public ACME CA such as Let’s Encrypt”. This means, you just need a public DNS record and Caddy needs to be reachable via ports 80 and 443. Nice!
Setup Instructions

So let’s combine ACI and Caddy to achieve our goal. I’ll use Terraform to set up the infrastructure in Azure. We’ll start with a new Terraform file and configure it with the Azure Provider (azurerm) and a local value for the Azure region:

```HCL
terraform {
  required_version = ">= 0.14, < 0.15"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

locals {
  location = "West Europe"
}
```

Next, we are going to define three resources so that we can provide persistent storage for Caddy:

```tf
resource "azurerm_resource_group" "aci_caddy" {
  name     = "aci_caddy"
  location = local.location
}

resource "azurerm_storage_account" "aci_caddy" {
  name                      = "acicaddy"
  resource_group_name       = azurerm_resource_group.aci_caddy.name
  location                  = azurerm_resource_group.aci_caddy.location
  account_tier              = "Standard"
  account_replication_type  = "LRS"
  enable_https_traffic_only = true
}

resource "azurerm_storage_share" "aci_caddy" {
  name                 = "aci-caddy-data"
  storage_account_name = azurerm_storage_account.aci_caddy.name
}
```

This is needed so that the certificate from Let’s Encrypt is not lost between deployments. If you deploy frequently and Caddy can’t remember the previous certificate, you will probably run into a rate limit of Let’s Encrypt which means you won’t be able to get any new certificate for your domain for some time.

Now we’re ready to define our main resource, the container instance (called container group in Terraform):

```
resource "azurerm_container_group" "aci_caddy" {
  resource_group_name = "aci_caddy"
  location            = local.location
  name                = "aci_caddy"
  os_type             = "Linux"
  dns_name_label      = "aci-caddy"
  ip_address_type     = "public"

  container {
    name   = "app"
    image  = "nginxinc/nginx-unprivileged"
    cpu    = "0.5"
    memory = "0.5"
  }

  container {
    name   = "caddy"
    image  = "caddy"
    cpu    = "0.5"
    memory = "0.5"

    ports {
      port     = 443
      protocol = "TCP"
    }

    ports {
      port     = 80
      protocol = "TCP"
    }

    volume {
      name                 = "aci-caddy-data"
      mount_path           = "/data"
      storage_account_name = azurerm_storage_account.aci_caddy.name
      storage_account_key  = azurerm_storage_account.aci_caddy.primary_access_key
      share_name           = azurerm_storage_share.aci_caddy.name
    }

    commands = ["caddy", "reverse-proxy", "--from", "aci-caddy.westeurope.azurecontainer.io", "--to", "localhost:8080"]
  }
}

output "url" {
  value = "https://${azurerm_container_group.aci_caddy.fqdn}"
  description = "URL"
}
```

Note that we define two containers. On line 9, we use an Nginx unprivileged image which serves as a surrogate for our real service and listens on port 8080.

On line 16, we define another container (sidecar) which contains our Caddy server. As mentioned previously, Caddy needs ports 80 and 443, so we assign those ports. Also, note that we are using a public IP (line 7) and we define a DNS subdomain (line 6).

Lines 32–38 contain the configuration for the shared volume which reference the storage resources we defined before. Caddy stores its data in the /data directory.

Line 40 contains all the magic to start Caddy. We tell it to act as a reverse proxy for our main service, the address to listen to (from parameter), and the forwarding address for our main service (to parameter), which is localhost:8080. That’s it. Caddy can be started with a one-liner and requires almost no configuration! (This is a concept I call zero config which I will treat in a future article.)

Finally, we print the address of our new service which should be accessible via HTTPS with a valid certificate from Let’s Encrypt.

Let’s log in with the Azure CLI (az), and let’s initialize and apply our new Terraform config:

```Shell
❯ az login -o none
The default web browser has been opened at https://login.microsoftonline.com/common/oauth2/authorize. Please continue the login in the web browser. If no web browser is available or if the web browser fails to open, use device code flow with `az login --use-device-code`.
You have logged in. Now let us find all the subscriptions to which you have access...

❯ terraform init

Initializing the backend...

Initializing provider plugins...
- Finding hashicorp/azurerm versions matching "~> 2.0"...
- Installing hashicorp/azurerm v2.45.1...
- Installed hashicorp/azurerm v2.45.1 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

❯ terraform apply

An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # azurerm_container_group.aci_caddy will be created
  (...)

  # azurerm_resource_group.aci_caddy will be created
  (...)

  # azurerm_storage_account.aci_caddy will be created
  (...)

  # azurerm_storage_share.aci_caddy will be created
  (...)

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + url = (known after apply)

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

(...)

Apply complete! Resources: 4 added, 0 changed, 0 destroyed.

Outputs:

url = "https://aci-caddy.westeurope.azurecontainer.io"
```

Nice work! Let’s test our service in a browser by invoking the URL provided in the output. If the page displays “Welcome to nginx!” and the browser doesn’t complain about invalid certificates then we achieved our goal.

There are some restrictions you need to be aware of: First, for each service you have to spin up a separate Caddy service. This consumes extra resources. Second, you also have to make sure that your service doesn’t listen on ports 80 and 443 as those are reserved for Caddy. Third, Caddy requires a public IP.
Conclusion

In this technical guide, I demonstrated how you can overcome one of the shortcomings of ACI when it comes to managing TLS certificates for an HTTPS connection.





##############################################################################

https://towardsdatascience.com/hidden-tricks-for-running-automl-experiment-from-azure-machine-learning-sdk-915d4e3f840e


Hidden tricks for running AutoML experiment from Azure Machine Learning SDK

Automated Machine Learning is an fast-growing field in Machine Learning community that enables users to try multiple algorithms and pre-processing transformations with their data. Combined with scalable cloud-based compute makes it possible to find the best performing model for data without the huge amount of time-consuming manual trial and error that would otherwise be required.

This blog provides a brief overview of how to run an AutoML experiment from Azure Machine Learning SDK.
Automated machine learning tasks and algorithms

Azure Machine Learning includes support for automated machine learning known as AutoML as one of Azure cloud offerings through visual interface in Azure Machine Learning studio or submit an experiment using the SDK. The SDK gives data scientists greater control over the settings for the automated machine learning experiment, whereas the visual interface is easier to use for users with less or no-code experience.

Azure Machine Learning trains models for the following types of machine learning task:

    Classification
    Regression
    Time Series Forecasting

In addition, Azure AutoML includes support for numerous commonly used algorithms for these tasks, including:
Classification Algorithms

    Logistic Regression
    Light Gradient Boosting Machine (GBM)
    Decision Tree
    Random Forest
    Naive Bayes
    Linear Support Vector Machine (SVM)
    XGBoost
    Deep Neural Network (DNN) Classifier
    Others…

Regression Algorithms

    Linear Regression
    Light Gradient Boosting Machine (GBM)
    Decision Tree
    Random Forest
    Elastic Net
    LARS Lasso
    XGBoost
    Others…

Forecasting Algorithms

    Linear Regression
    Light Gradient Boosting Machine (GBM)
    Decision Tree
    Random Forest
    Elastic Net
    LARS Lasso
    XGBoost
    Others…

For a full list of supported algorithms, see How to define a machine learning task in the documentation.
Configuring an Automated Machine Learning Experiment using SDK

While user interface provides an intuitive way to select options for your automated machine learning experiment, using the SDK gives user greater flexibility to setup the experiments and monitor the runs. Here, I have listed seven steps that guides the users to run AutoML via SDK.
Step 1: Create Compute Target

In Azure Machine Learning, Compute Targets are physical or virtual computers on which experiments are run.

The ability to assign experiment runs to specific compute targets helps you implement a flexible data science ecosystem in the following ways:

    Code can be developed and tested on local or low-cost compute, and then moved to more scalable compute for production workloads.
    You can run individual processes on the compute target that best fits its needs. For example, by using GPU-based compute to train deep learning models, and switching to lower-cost CPU-only compute to test and register the trained model.

One of the core benefits of cloud computing is the ability to manage costs by paying only for what you use. In Azure Machine Learning, you can take advantage of this principle by defining compute targets that:

    Start on-demand and stop automatically when no longer required.
    Scale automatically based on workload processing needs.

For complete documentation on Compute Targets look at here:

Azure Machine Learning includes the ability to create Compute Instances in a workspace to provide a development environment (Jupyter Notebook, Jupyer Lab, RStudio and SSH) that is managed with all of the other assets in the workspace.
Overview of Azure Machine Learning (Microsoft Official Documentation)
Step 2: Installing the Azure Machine Learning SDK for Python

pip install azureml-sdk

The SDK includes optional extras that aren’t required for core operations, but can be useful in some scenarios. For example, the notebooks extra include widgets for displaying detailed output in Jupyter Notebooks, the automl extra includes packages for automated machine learning training, and the explain extra includes packages for generating model explanations. To install extras, specify them in brackets as shown here:

pip install azureml-sdk[notebooks, automl,explain]

More Information: For more information about installing the Azure Machine Learning SDK for Python, see the SDK documentation. Also, you should be aware that the SDK is updated on a regular basis, and review the release notes for the latest release.
Step 3:Specifying Data for Training

Automated machine learning is designed to enable you to simply bring your data, and have Azure Machine Learning figure out how best to train a model from it.

When using the Automated Machine Learning user interface in Azure Machine Learning studio, you can create or select an Azure Machine Learning dataset to be used as the input for your automated machine learning experiment.

When using the SDK to run an automated machine learning experiment, you can submit the data in the following ways:

    Specify a dataset or dataframe of training data that includes features and the label to be predicted.
    Optionally, specify a second validation data dataset or dataframe that will be used to validate the trained model. if this is not provided, Azure Machine Learning will apply cross-validation using the training data.

Alternatively:

    Specify a dataset, dataframe, or numpy array of X values containing the training features, with a corresponding y array of label values.
    Optionally, specify X_valid and y_valid datasets, dataframes, or numpy arrays of X_valid values to be used for validation.

Hint1: AML has an embed feature of data profiling that allows users to explore their registered datasets:
How to monitor datasets in AML (Microsoft Official Documentation)

If you want to have this feature in your SDK experiment, you can use the actual python package(pandas_profiling ) and after installing the package, to generate the [profile report, run:

profile = ProfileReport(df, title="Pandas Profiling Report")

This is achieved by simply displaying the report. In the Jupyter Notebook, run:

profile.to_widgets()

The HTML report can be included in a Jupyter notebook:
Package pandas_profiling (Official Github Repo)

Run the following code:

profile.to_notebook_iframe()

Package pandas_profiling (Official Github Repo)
Saving the report

If you want to generate a HTML report file, save the ProfileReport to an object and use the to_file() function:

profile.to_file("your_report.html")

Alternatively, you can obtain the data as json:

# As a string
json_data = profile.to_json()# As a file
profile.to_file("your_report.json")

Package pandas_profiling (Official Github Repo)
Step 4: Connecting to a Workspace

After installing the SDK package in your Python environment, you can write code to connect to your workspace and perform machine learning operations. The easiest way to connect to a workspace is to use a workspace configuration file, which includes the Azure subscription, resource group, and workspace details as shown here:

{
      "subscription_id": "<subscription-id>",
      "resource_group": "<resource-group>",
      "workspace_name": "<workspace-name>"
}

To connect to the workspace using the configuration file, you can use the from_config method of the Workspace class in the SDK, as shown here:

from azureml.core import Workspacesubscription_id = '<subscription-id>'
resource_group  = '<resource-group>'
workspace_name  = '<workspace-name>'try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    ws.write_config()
    print('Library configuration succeeded')
except:
    print('Workspace not found')

Step5: Configuring an Automated Machine Learning Experiment

The user interface provides an intuitive way to select options for your automated machine learning experiment. When using the SDK, you have greater flexibility, and you can set experiment options using the AutoMLConfig class, as shown in the following example:

automl_settings = {
    "n_cross_validations": 3,
    "primary_metric": 'average_precision_score_weighted',
    "enable_early_stopping": True,
    "max_concurrent_iterations": 2, # This is a limit for testing purpose, please increase it as per cluster size
    "experiment_timeout_hours": 0.25, # This is a time limit for testing purposes, remove it for real use cases, this will drastically limit ablity to find the best model possible
    "verbosity": logging.INFO,
}

automl_config = AutoMLConfig(task = 'classification',
                             debug_log = 'automl_errors.log',
                             compute_target = compute_target,
                             training_data = training_data,
                             label_column_name = label_column_name,
                             **automl_settings
                            )

Step 6: Submitting an Automated Machine Learning Experiment

Like any scientific discipline, data science involves running experiments; typically to explore data or to build and evaluate predictive models. In Azure Machine Learning, an experiment is a named process, usually the running of a script or a pipeline, that can generate metrics and outputs and be tracked in the Azure Machine Learning workspace.

An experiment can be run multiple times, with different data, code, or settings; and Azure Machine Learning tracks each run, enabling you to view run history and compare results for each run.

You can submit an automated machine learning experiment like any other SDK-based experiment:

from azureml.core.experiment import Experiment

automl_experiment = experiment(ws,'automl_experiment')
automl_run = automl_experiment.submit(automl_config)
automl_run.wait_for_completion(show_output=True)

Step 7: Retrieving the Best Run and its Model

You can easily identify the best run in Azure Machine Learning studio, and download or deploy the model it generated. To accomplish this programmatically with the SDK, you can use code like the following example:

best_run, fitted_model = automl_run.get_output()
print(best_run)
print(fitted_model)

Hint 2: The Experiment Run Context

In addition to the best model, when you submit an experiment, you use its run context to initialize and end the experiment run that is tracked in Azure Machine Learning, as shown in the following code sample:

automl_run = experiment.start_logging()run = automl_run.get_context() # allow_offline=True by default, so can be run locally as well
...
run.log("Accuracy", 0.98)
run.log_row("Performance", epoch=e, error=err)

Logging Metrics

Every experiment generates log files that include the messages that would be written to the terminal during interactive execution. This enables you to use simple print statements to write messages to the log. However, if you want to record named metrics for comparison across runs, you can do so by using the Run object; which provides a range of logging functions specifically for this purpose. These include:

    log: Record a single named value.
    log_list: Record a named list of values.
    log_row: Record a row with multiple columns.
    log_table: Record a dictionary as a table.
    log_image: Record an image file or a plot.

    More Information: For more information about logging metrics during experiment runs, see Monitor Azure ML experiment runs and metrics in the Azure Machine Learning documentation.

Retrieving and Viewing Logged Metrics

You can view the metrics logged by an experiment run in Azure Machine Learning studio or by using the RunDetails widget in a notebook, as shown here:

from azureml.widgets import RunDetails
RunDetails(automl_run).show()

You can also retrieve the metrics using the Run object’s get_metrics method, which returns a JSON representation of the metrics, as shown here:

best_run_metrics = best_run.get_metrics() # or other runs with runID
for metric_name in best_run_metrics:
     metric = best_run_metrics[metric_name]
     print(metric_name, metric)

Another good method for run is get_properties that allows you that fetches the latest properties of the run from the service and the return a dict type that can be query for particular properties such as iteration, algorithm name, class name, and many other useful features that needs to be extracted.

Another useful method get_status that returns common values returned include “Running”, “Completed”, and “Failed”.

while automl_run.get_status() not in ['Completed','Failed']:
    print('Run {} not in terminal state'.format(atoml_run.id))
    time.sleep(10)

The following code example shows some uses of the list method.

favorite_completed_runs = automl_run.list(experiment, status='Completed', tags = 'favorite')all_distinc_runs = automl_run.list(experiment)and_their_children = automl_run.list(experiment, include_children=True)only_script_runs = Run.list(experiment,, type=ScriptRun.RUN_TYPE)

For the complete list of methods see the Azure ML API documentation.