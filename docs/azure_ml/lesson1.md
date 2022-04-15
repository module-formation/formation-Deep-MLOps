# Introduction au SDK Azure

!!! Warning "Attention"

    Un jour, peut être, tout sera traduit en français. Pour l'instant, il y aura les deux : anglais et français, la plupart du texte en anglais provient du nanodegree [Machine Learning Engineer with Microsoft Azure Nanodegree Program](https://classroom.udacity.com/nanodegrees/nd00333/dashboard/overview) d'Udacity que j'ai suivi. L'idée étant ici de consolider et de formaliser ce qu'il y a dedans.

## La base : le Workspace

## Importer des données

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


## Listing Past Experiments

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

## Submitting New Experiments

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

## Automated ML

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
### AutoML Notebook

```python
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
```





