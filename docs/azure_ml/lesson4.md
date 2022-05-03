
# Lesson 4 : Pipeline automation

https://docs.microsoft.com/fr-fr/azure/machine-learning/how-to-use-automlstep-in-pipelines#configure-and-create-the-automated-ml-pipeline-step

https://docs.microsoft.com/fr-fr/python/api/azureml-core/azureml.core.model.model?view=azure-ml-py

https://docs.microsoft.com/fr-fr/python/api/azureml-pipeline-core/azureml.pipeline.core.portdatareference?view=azure-ml-py#azureml-pipeline-core-portdatareference-path-on-datastore

https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-azure-container-instance

https://docs.microsoft.com/en-us/azure/machine-learning/how-to-secure-web-service

## Create a Pipeline

!!! summary "Summary"

    The most common SDK class is the Pipeline class. You will use this when creating a Pipeline. Pipelines can take configuration and different steps, like AutoML for example.

    Different steps can have different arguments and parameters. Parameters are just like variables in a Python script.

There are areas you can play with when creating a pipeline and we covered two:

* Use pipeline parameters
* Recurring Scheduled Pipelines
* Batch Inference Pipelines

### Pipeline Class

**This is the most common Python SDK class you will see when dealing with Pipelines.** Aside from accepting a workspace and allowing multiple steps to be passed in, it uses a description that is useful to identify it later.

```python
from azureml.pipeline.core import Pipeline

pipeline = Pipeline(
    description="pipeline_with_automlstep",
    workspace=ws,
    steps=[automl_step])
```

### Using Pipeline Parameters

**Pipeline parameters are also available as a class.** You configure this class with the various different parameters needed so that they can later be used.

In this example, the `avg_rate_param` is used in the arguments attribute of the PythonScriptStep.

```python
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.core import PipelineParameter

avg_rate_param = PipelineParameter(name="avg_rate", default_value=0.5)
train_step = PythonScriptStep(script_name="train.py",
                              arguments=["--input", avg_rate_param],
                              target=compute_target,
                              source_directory=project_folder)
```

### Scheduling a recurring Pipeline

**To schedule a Pipeline, you must use the ScheduleRecurrence class which has the information necessary to set the interval.**

Once that has been created, it has to be passed into the `create()` method of the `Schedule` class as a recurrence value.

```python
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule

hourly = ScheduleRecurrence(frequency="Hourly", interval=4)
pipeline_schedule = Schedule.create(ws, name="RecurringSchedule",
                            description="Trains model every few hours",
                            pipeline_id=pipeline_id,
                            experiment_name="Recurring_Pipeline_name",
                            recurrence=hourly)
```

### Batch Inference Pipeline

One of the core responsibilities of a batch inference pipeline is to run in parallel. For this to happen, you must use the ParallelRunConfig class which helps define the configuration needed to run in parallel.

Some important aspects of this are the script that will do the work (`entry_script` parameter), how many failures it should tolerate (`error_threshold` parameter), and the number of nodes/batches needed to run (`mini_batch_size` parameter, 5 in this example).

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

!!! info "Définition"

    * Batch inference: The process of doing predictions using parallelism. In a pipeline, it will usually be on a recurring schedule
    * Recurring schedule: A way to schedule pipelines to run at a given interval
    * Pipeline parameters: Like variables in a Python script, these can be passed into a script argument


## Exercise

### Step 1 : Create a Pipeline

!!! summary "Summary"

    Pipelines are very useful and are a foundation of automation and operations in general. Being able to create a Pipeline allows for easier interaction with model deployments.

This demo shows you **how to use the Python SDK to create a pipeline with AutoML steps**.

For this exercise, you will create a pipeline using the python SDK.

First, create a pipeline using the Python SDK. (This is the part that up until the Examine Results section in the provided notebook)

It is optional, you can copy and run cells in Examine Results section to test the pipeline and retrieve the best model. This step involves running an Automated ML experiment so it will take about 30 min to complete. Please keep track of the remaining time before you run these cells.

!!! attention "Attention"

    Make sure you update cells to match your dataset and other variables. These are noted in comments like this:


    ```python
    # Choose a name for the run history container in the workspace.
    # NOTE: update these to match your existing experiment name
    experiment_name = 'ml-experiment-1'
    project_folder = './pipeline-project'
    ```

Free free to modify the code to explore the different pipeline features and parameters. To speed up and shorten the total amount to train the model, you can change the `experiment_timeout_minutes` value from 20 to 10. These settings are in the Python Notebook, which are currently set to 20 minutes:

```python
automl_settings = {
    "experiment_timeout_minutes": 20,
    "max_concurrent_iterations": 4,
    "primary_metric" : 'normalized_root_mean_squared_error',
    "n_cross_validations": 5
}
```

Create and run the pipelines using the Python SDK.

### Step 2 : Publish a pipeline

In this part, you need to publish a pipeline using the both Azure ML studio and the Python SDK. Please re-use the Pipeline created in the previous part.

You are recommended to write your own code to publish the pipeline. If you get stuck, review the first a few cells in the **Publish and run from REST endpoint** section in the provided notebook.

### Azure Machine Learning Pipeline with AutoMLStep

We demonstrate the use of AutoMLStep in Azure Machine Learning Pipeline.

#### Introduction
In this example we showcase how you can use AzureML Dataset to load data for AutoML via AML Pipeline.

If you are using an Azure Machine Learning Notebook VM, you are all set. Otherwise, make sure you have executed the [configuration](https://aka.ms/pl-config) before running this notebook.

Here, you will learn how to:

1. Create an `Experiment` in an existing `Workspace`.
2. Create or Attach existing AmlCompute to a workspace.
3. Define data loading in a `TabularDataset`.
4. Configure AutoML using `AutoMLConfig`.
5. Use `AutoMLStep`.
6. Train the model using AmlCompute.
7. Explore the results.
8. Test the best fitted model.


#### Initialize Workspace

Initialize a workspace object from persisted configuration. Make sure the config file is present at `.\config.json`.

#### Create an Azure ML experiment
Let's create an experiment named "automlstep-classification" and a folder to hold the training scripts. The script runs will be recorded under the experiment in Azure.

**The best practice is to use separate folders for scripts and its dependent files for each step and specify that folder as the `source_directory` for the step.**

This helps reduce the size of the snapshot created for the step (only the specific folder is snapshotted). Since changes in any files in the `source_directory` would trigger a re-upload of the snapshot, this helps keep the reuse of the step when there are no changes in the `source_directory` of the step.

```py
# Choose a name for the run history container in the workspace.
# NOTE: update these to match your existing experiment name
experiment_name = "automlstep-regression"
project_folder = './pipeline-project'

experiment = Experiment(ws, experiment_name)
experiment
```


##### Create or Attach an AmlCompute cluster
You will need to create a [compute target](https://docs.microsoft.com/azure/machine-learning/service/concept-azure-machine-learning-architecture#compute-target) for your AutoML run. In this tutorial, you get the default `AmlCompute` as your training compute resource.

```py
from azureml.core.compute import AmlCompute
from azureml.core.compute import ComputeTarget
from azureml.core.compute_target import ComputeTargetException

# NOTE: update the cluster name to match the existing cluster
# Choose a name for your CPU cluster
amlcompute_cluster_name = "cpu-cluster"

# Verify that cluster does not exist already
try:
    compute_target = ComputeTarget(workspace=ws, name=amlcompute_cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',# for GPU, use "STANDARD_NC6"
                                                           #vm_priority = 'lowpriority', # optional
                                                           max_nodes=4)
    compute_target = ComputeTarget.create(ws, amlcompute_cluster_name, compute_config)
    compute_target.wait_for_completion(show_output=True, min_node_count = 1, timeout_in_minutes = 10)
# For a more detailed view of current AmlCompute status, use get_status().
```

#### Data


```py
# Try to load the dataset from the Workspace. Otherwise, create it from the file
# NOTE: update the key to match the dataset name
found = False
key = "bike-no-aci-deployment"
description_text = "dataset used for testing ACI deployment in udacity nanodegree"

if key in ws.datasets.keys():
        found = True
        dataset = ws.datasets[key]

if not found:
        # Create AML Dataset and register it into Workspace
        example_data = "your_csv_url.csv"
        dataset = Dataset.Tabular.from_delimited_files(example_data)
        #Register Dataset in Workspace
        dataset = dataset.register(workspace=ws,
                                   name=key,
                                   description=description_text)


df = dataset.to_pandas_dataframe()
df.head()
```


#### Train

This creates a general AutoML settings object.

```py
automl_settings = {
    "experiment_timeout_minutes": 20,
    "max_concurrent_iterations": 4,
    "primary_metric" : 'normalized_root_mean_squared_error',
    "n_cross_validations": 5
}

automl_config = AutoMLConfig(compute_target=compute_target,
                             task = "regression",
                             training_data=dataset,
                             label_column_name="cnt",
                             path = project_folder,
                             enable_early_stopping= True,
                             featurization= 'auto',
                             debug_log = "automl_errors.log",
                             **automl_settings
                            )
```

##### Create Pipeline and AutoMLStep

###### Define outputs

You can define outputs for the AutoMLStep using `TrainingOutput`.

```py
from azureml.pipeline.core import PipelineData, TrainingOutput

ds = ws.get_default_datastore()
metrics_output_name = 'metrics_output'
best_model_output_name = 'best_model_output'

metrics_data = PipelineData(name='metrics_data',
                           datastore=ds,
                           pipeline_output_name=metrics_output_name,
                           training_output=TrainingOutput(type='Metrics'))

model_data = PipelineData(name='model_data',
                           datastore=ds,
                           pipeline_output_name=best_model_output_name,
                           training_output=TrainingOutput(type='Model'))
```

[`PipelineData` Class](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipelinedata?view=azure-ml-py).

!!! info "`name` (str, Required)"

    The name of the `PipelineData` object, which can contain only letters, digits, and underscores.

    `PipelineData` names are used to identify the outputs of a step. After a pipeline run has completed, you can use the step name with an output name to access a particular output. Names should be unique within a single step in a pipeline.

!!! info "`pipeline_output_name` (Required)"

    If provided this output will be available by using `PipelineRun.get_pipeline_output()`. Pipeline output names must be unique in the pipeline.

More on [`TrainingOutput`](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.trainingoutput?view=azure-ml-py).

!!! info "Définition"

    Defines a specialized output of certain `PipelineSteps` for use in a pipeline.

    `TrainingOutput` enables an automated machine learning metric or model to be made available as a step output to be consumed by another step in an Azure Machine Learning Pipeline. Can be used with `AutoMLStep` or `HyperDriveStep`.

    `TrainingOutput` is used with `PipelineData` when constructing a Pipeline **to enable other steps to consume the metrics or models generated** by an `AutoMLStep` or `HyperDriveStep`.


###### Create an AutoMLStep

```py
automl_step = AutoMLStep(
    name='automl_module',
    automl_config=automl_config,
    outputs=[metrics_data, model_data],
    allow_reuse=True)
```

###### Define the pipeline

```py
from azureml.pipeline.core import Pipeline
pipeline = Pipeline(
    description="pipeline_with_automlstep",
    workspace=ws,
    steps=[automl_step])
```

###### Run the pipeline

```py
from azureml.widgets import RunDetails
pipeline_run = experiment.submit(pipeline)
RunDetails(pipeline_run).show()
pipeline_run.wait_for_completion()
```

#### Examine Results

##### Retrieve the metrics of all child runs
Outputs of above run can be used as inputs of other steps in pipeline. In this tutorial, we will examine the outputs by retrieve output data and running some tests.

```py
metrics_output = pipeline_run.get_pipeline_output(metrics_output_name)
num_file_downloaded = metrics_output.download('.', show_progress=True)
```

```py
import json
with open(metrics_output._path_on_datastore) as f:
    metrics_output_result = f.read()

deserialized_metrics_output = json.loads(metrics_output_result)
df = pd.DataFrame(deserialized_metrics_output)
df
```

##### Retrieve the Best Model

```py
# Retrieve best model from Pipeline Run
best_model_output = pipeline_run.get_pipeline_output(best_model_output_name)
num_file_downloaded = best_model_output.download('.', show_progress=True)
```

```py
import pickle

model_filename = best_model_output._path_on_datastore
# model_filename = path to downloaded file
model_filename
```


```py
with open(model_filename, "rb" ) as f:
    best_model = pickle.load(f)

best_model.steps
```
##### Test the Model
###### Load Test Data
For the test data, it should have the same preparation step as the train data. Otherwise it might get failed at the preprocessing step.


```py
dataset_test = Dataset.Tabular.from_delimited_files(path='https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_test.csv')
df_test = dataset_test.to_pandas_dataframe()
df_test = df_test[pd.notnull(df_test['y'])]

y_test = df_test['y']
X_test = df_test.drop(['y'], axis=1)
```

###### Testing Our Best Fitted Model

We will use confusion matrix to see how our model works.

```py
from sklearn.metrics import confusion_matrix
ypred = best_model.predict(X_test)
cm = confusion_matrix(y_test, ypred)
# Visualize the confusion matrix
pd.DataFrame(cm).style.background_gradient(cmap='Blues', low=0, high=0.9)
```

#### Publish and run from REST endpoint

Run the following code to publish the pipeline to your workspace. In your workspace in the portal, you can see metadata for the pipeline including run history and durations. You can also run the pipeline manually from the portal.

Additionally, publishing the pipeline enables a REST endpoint to rerun the pipeline from any HTTP library on any platform.

```py
published_pipeline = pipeline_run.publish_pipeline(
    name="Bike sharing Train", description="Training bike sharing pipeline", version="1.0")

published_pipeline
```

Authenticate once again, to retrieve the `auth_header` so that the endpoint can be used.

```py
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
```

Get the REST url from the endpoint property of the published pipeline object. You can also find the REST url in your workspace in the portal. Build an HTTP POST request to the endpoint, specifying your authentication header. Additionally, add a JSON payload object with the experiment name and the batch size parameter. As a reminder, the process_count_per_node is passed through to ParallelRunStep because you defined it is defined as a PipelineParameter object in the step configuration.

Make the request to trigger the run. Access the Id key from the response dict to get the value of the run id.

```py
import requests

rest_endpoint = published_pipeline.endpoint
response = requests.post(rest_endpoint,
                         headers=auth_header,
                         json={"ExperimentName": "pipeline-rest-endpoint"}
                        )
```

```py
try:
    response.raise_for_status()
except Exception:
    raise Exception("Received bad response from the endpoint: {}\n"
                    "Response Code: {}\n"
                    "Headers: {}\n"
                    "Content: {}".format(rest_endpoint, response.status_code, response.headers, response.content))

run_id = response.json().get('Id')
print('Submitted pipeline run: ', run_id)
```

Use the run id to monitor the status of the new run. This will take another 10-15 min to run and will look similar to the previous pipeline run, so if you don't need to see another pipeline run, you can skip watching the full output.

```py
from azureml.pipeline.core.run import PipelineRun
from azureml.widgets import RunDetails

published_pipeline_run = PipelineRun(ws.experiments["pipeline-rest-endpoint"], run_id)
RunDetails(published_pipeline_run).show()
```


#### Consume Pipeline Endpoint (API)

!!! summary "Summary"

    Pipeline endpoints can be consumed via HTTP, but it is also possible to do so via the Python SDK. Since there are different ways to interact with published Pipelines, this makes the whole pipeline environment very flexible.

    It is key to find and use the correct HTTP endpoint to interact with a published pipeline. Sending a request over HTTP to a pipeline endpoint will require authentication in the request headers. We will talk more about it later.

    Pipelines can perform several other tasks aside from training a model. Some of these tasks, or steps are:

    * Data Preparation
    * Validation
    * Deployment
    * Combined tasks


!!! info "Définition"

    * **Pipeline endpoint**: The URL of the published Pipeline
    * **HTTP Headers**: Part of the HTTP specification, where a request can attach extra information, like authentication
    * Automation: A core pillar of DevOps which is applicable to Machine Learning
    * **Batch inference**: The process of doing predictions using parallelism. In a pipeline, it will usually be on a recurring schedule
    * **HTTP trigger**: With configuration, a service can create an HTTP request based on certain conditions
    * **Pipeline parameters**: Like variables in a Python script, these can be passed into a script argument
    * **Publishing a Pipeline**: Allowing external access to a Pipeline over an HTTP endpoint
    * **Recurring schedule**: A way to schedule pipelines to run at a given interval



### Documentation

* [PipelineEndpoint Class](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipeline_endpoint.pipelineendpoint?view=azure-ml-py).
* [Create and run machine learning pipelines with Azure Machine Learning SDK](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-machine-learning-pipelines)
* [What are Azure Machine Learning pipelines?](https://docs.microsoft.com/en-us/azure/machine-learning/concept-ml-pipelines)

* [Tutorial: Create Training and Inferencing Pipelines with Azure ML Designer](https://thenewstack.io/tutorial-create-training-and-inferencing-pipelines-with-azure-ml-designer/)
* [Build Repeatable ML Workflows with Azure Machine Learning Pipelines](https://thenewstack.io/build-repeatable-ml-workflows-with-azure-machine-learning-pipelines/)
* [Tutorial: Build an End-to-End Azure ML Pipeline with the Python SDK](https://thenewstack.io/tutorial-build-an-end-to-end-azure-ml-pipeline-with-the-python-sdk/)
* [Tutorial: Train Machine Learning Models with Automated ML Feature of Azure ML](https://thenewstack.io/tutorial-train-machine-learning-models-with-automated-ml-feature-of-azure-ml/)



#### [Best Practices for Azure Machine Learning Pipelines](https://stackoverflow.com/questions/61391963/best-practices-for-azure-machine-learning-pipelines)

!!! attention "Attention"

    Rephrasing of the StackOverflow answer, go check it for complete anwsers.

Most of the time, a pipeline has at least 4 steps.

* Input data
* Data transformation step
* Model Training step
* Model scoring step

There are a bunch of things that are completely unclear from the documentation and the examples and I'm struggling to fully grasp the concept.

1. When I look at `batch scoring` examples, it is implemented as a Pipeline Step. This raises the question:

!!! question "Question"

    Does this mean that the `predicting part` is part of the same pipeline as the `training part`, or should there be separate 2 separate pipelines for this ?

Making 1 pipeline that combines both steps seems odd to me, because you don't want to run your predicting part every time you change something to the training part (and vice versa).

A pipeline architecture depends on if:

* you need to predict live (else batch prediction is sufficient), and
* your data is already transformed and ready for scoring.

If you need live scoring, you should deploy your model. If batch scoring, is fine. You could either have:

* a training pipeline at the end of which you register a model that is then used in a scoring pipeline, or
* have one pipeline that can be configured to do either using script arguments.

!!! attention "Attention"

    **From March 2021.** PipelineData is no longer a preferred way: ["PipelineData use DataReference underlying which is no longer the recommended approach for data access and delivery, please use OutputFileDatasetConfig instead"](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-core/azureml.pipeline.core.pipelinedata?view=azure-ml-py).

In the batch scoring examples, the assumption is that there is already a trained model, which could be coming from another pipeline, or in the case of the notebook, it's a pre-trained model not built in a pipeline at all.

However, **running both training and prediction in the same pipeline is a valid use-case**. Use the `allow_reuse` param and set to `True`, which will cache the step output in the pipeline to prevent unnecessary reruns.

Take a model training step for example, and consider the following input to that step:

* training script
* input data
* additional step params

If you set `allow_reuse=True`, and your training script, input data, and other step params are the same as the last time the pipeline ran, it will not rerun that step, it will use the cached output from the last time the pipeline ran. But let's say your data input changed, then the step would rerun.

In general, pipelines are pretty modular and you can build them how you see fit. You could maintain separate pipelines for training and scoring, or **bundle everything in one pipeline but leverage the automatic caching**.

2. What parts should be implemented as a Pipeline Step and what parts shouldn't? Should the creation of the Datastore and Dataset be implemented as a step? Should registering a model be implemented as a step?

All transformations you do to your data (munging, featurization, training, scoring) should take place inside of `PipelineStep`'s. The inputs and outputs of which should be `PipelineData`'s.

Azure ML artifacts should be:

* created in the pipeline control plane using `PipelineData`, and
* registered either ad-hoc, as opposed to with every run, or
* when you need to pass artifacts between pipelines.

In this way `PipelineData` is the glue that connects pipeline steps directly rather than being indirectly connected with `.register()` and `.download()`

`PipelineData`'s are ultimately just ephemeral directories that can also be used as placeholders before steps are run to create and register artifacts.

`Dataset`'s are abstractions of `PipelineData`s in that they make things easier to pass to `AutoMLStep` and `HyperDriveStep`, and `DataDrift`.


3. What isn't shown anywhere is how to deal with model registry. I create the model in the training step and then write it to the output folder as a pickle file. Then what? How do I get the model in the next step? Should I pass it on as a `PipelineData` object? Should `train.py` itself be responsible for registering the trained model?

During development, I recommend that you don't register your model and that the scoring step receives your model via a PipelineData as a pickled file.

In production, the scoring step should use a previously registered model. The registration of the new model should be done via comparison of the metrics and then trigger the registration if needed.
