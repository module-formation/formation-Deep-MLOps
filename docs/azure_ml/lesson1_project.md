# Comparaison entre HyperDrive et AutoML

## Set up workspace parameters

```py
from azureml.core import Workspace, Experiment

ws = Workspace.from_config()
exp = Experiment(workspace=ws, name="udacity-project")

print('Workspace name: ' + ws.name,
      'Azure region: ' + ws.location,
      'Subscription id: ' + ws.subscription_id,
      'Resource group: ' + ws.resource_group, sep = '\n')

run = exp.start_logging()
```

## Set up Compute cluster

```py
from azureml.core.compute import ComputeTarget, AmlCompute

# TODO: Create compute cluster
# Use vm_size = "Standard_D2_V2" in your provisioning configuration.
# max_nodes should be no greater than 4.
cluster_name = "udacity-project"

compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_D2_V2',
                                                            vm_priority='lowpriority',
                                                            max_nodes=4)
cpu_cluster = ComputeTarget.create(ws, cluster_name, compute_config)
```

## Set up HyperDrive configuration and runs

```py
from azureml.widgets import RunDetails
from azureml.train.sklearn import SKLearn
from azureml.train.hyperdrive.run import PrimaryMetricGoal
from azureml.train.hyperdrive.policy import BanditPolicy
from azureml.train.hyperdrive.sampling import RandomParameterSampling
from azureml.train.hyperdrive.runconfig import HyperDriveConfig
from azureml.train.hyperdrive.parameter_expressions import choice, uniform
from azureml.core import Environment, ScriptRunConfig
import os

# Specify parameter sampler
ps = RandomParameterSampling( {
        "--C": uniform(0.1, 1.0),
        "--max_iter": choice(25,50,75,100,125,150,175,200)
    }
)

# Specify a Policy
policy = BanditPolicy(evaluation_interval=1, slack_factor=0.2, slack_amount=None, delay_evaluation=0)

if "training" not in os.listdir():
    os.mkdir("./training")

# Setup environment for your training run
# Note that conda isn't the only spec available, you can set up compute env with pip or a dockerfile.
sklearn_env = Environment.from_conda_specification(name='sklearn-env', file_path='conda_dependencies.yml')

# Create a ScriptRunConfig Object to specify the configuration details of your training job
src = ScriptRunConfig(source_directory='.',
                            script='train.py',
                            compute_target=cpu_cluster,
                            environment=sklearn_env)

# Create a HyperDriveConfig using the src object, hyperparameter sampler, and policy.
hyperdrive_config = HyperDriveConfig(run_config=src,
                                hyperparameter_sampling=ps,
                                policy=policy,
                                primary_metric_name='Accuracy',
                                primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
                                max_total_runs=10,
                                max_concurrent_runs=4)
```

### Run HyperDrive experiments

```py
# Submit your hyperdrive run to the experiment and show run details with the widget.

### YOUR CODE HERE ###
hyperdrive_run = exp.submit(hyperdrive_config)
RunDetails(hyperdrive_run).show()
hyperdrive_run.wait_for_completion(show_output=True)
```

### Get results and save the best one

```py
import joblib
# Get your best run and save the model from that run.

### YOUR CODE HERE ###
# Get your best run and save the model from that run.
best_run = hyperdrive_run.get_best_run_by_primary_metric()
best_run_metrics = best_run.get_metrics()
parameter_values = best_run.get_details()['runDefinition']['arguments']

print(f'Best Run Id: {best_run.id}')
print(f'Best run parameters : {parameter_values}')
print(f'Accuracy: {best_run_metrics["Accuracy"]:.3f}')
```

```sh
Best Run Id: HD_bf0c2c3d-713b-44ce-ac46-80f90e50feb0_9
Best run parameters : ['--C', '0.20624530875187946', '--max_iter', '125']
Accuracy: 0.914
```

```py
best_run.get_file_names()
```

```sh
['logs/azureml/dataprep/backgroundProcess.log',
 'logs/azureml/dataprep/backgroundProcess_Telemetry.log',
 'logs/azureml/dataprep/rslex.log',
 'logs/azureml/dataprep/rslex.log.2022-04-05-14',
 'outputs/.amlignore',
 'outputs/model.joblib',
 'outputs/model_0.20624530875187946_125.joblib',
 'system_logs/cs_capability/cs-capability.log',
 'system_logs/hosttools_capability/hosttools-capability.log',
 'system_logs/lifecycler/execution-wrapper.log',
 'system_logs/lifecycler/lifecycler.log',
 'system_logs/lifecycler/vm-bootstrapper.log',
 'user_logs/std_log.txt']
```

```py
joblib.dump(value="model.joblib", filename="outputs/model.joblib")
```

## Set up AutoML run

### Refactor datatset

```py
from azureml.data.dataset_factory import TabularDatasetFactory

# Create TabularDataset using TabularDatasetFactory
# Data is available at:
# "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv"
csv_url= "https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv"

ds = TabularDatasetFactory.from_delimited_files(path=csv_url)
```

```py
from train import clean_data

# Use the clean_data function to clean your data.
x, y = clean_data(ds)
```

```py
# WARNING:root:The AutoMLConfig parameters, X and y, will soon be deprecated. Please refer to our documentation for the latest interface: https://aka.ms/AutoMLConfig
# will have to concat x and y in the future and "use training_data" and "label_column_name" parameters

# Reference: "Create a dataset from pandas dataframe" section
# at https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-register-datasets

import pandas as pd
from azureml.core import Dataset, Datastore

training_data = pd.concat([x, y], axis = 1)

training_data.head()
```

```py
#dirname = "./training_data"
os.makedirs('training_data', exist_ok=True)

local_path = './training_data/training_data.csv'
training_data.to_csv(local_path, index=False)
```

```py
Dataset.File.upload_directory(src_dir= "training_data", target=(datastore, "training_data"), overwrite=True)
ds = TabularDatasetFactory.from_delimited_files(path=[(datastore, ('training_data/training_data.csv'))])
```

```sh
Validating arguments.
Arguments validated.
Uploading file to training_data
Uploading an estimated of 3 files
Uploading training_data/.amlignore
Uploaded training_data/.amlignore, 1 files out of an estimated total of 3
Uploading training_data/.amlignore.amltmp
Uploaded training_data/.amlignore.amltmp, 2 files out of an estimated total of 3
Uploading training_data/training_data.csv
Uploaded training_data/training_data.csv, 3 files out of an estimated total of 3
Uploaded 3 files
Creating new dataset
```


```py
ds = ds.to_pandas_dataframe()
```

### Register dataset

```py
# get the datastore to upload prepared data
# https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-register-datasets#create-a-dataset-from-pandas-dataframe
datastore = ws.get_default_datastore()
datastore
```

```json
{
  "name": "workspaceblobstore",
  "container_name": "azureml-blobstore-2b053715-edc8-4d3b-a8c1-d7ee4050384e",
  "account_name": "workspaceperso5448820782",
  "protocol": "https",
  "endpoint": "core.windows.net"
}
```

```py
dataset = Dataset.Tabular.register_pandas_dataframe(training_data, datastore, "udacity_project_dataset", show_progress=True)
```

### Set up AutoML experiment

```py
from azureml.train.automl import AutoMLConfig

# Set parameters for AutoMLConfig
# NOTE: DO NOT CHANGE THE experiment_timeout_minutes PARAMETER OR YOUR INSTANCE WILL TIME OUT.
# If you wish to run the experiment longer, you will need to run this notebook in your own
# Azure tenant, which will incur personal costs.
automl_config = AutoMLConfig(
                             experiment_timeout_minutes=30,
                             task="classification",
                             training_data = ds,
                             label_column_name = "y",
                             compute_target=cpu_cluster,
                             iterations=30,
                             iteration_timeout_minutes=5,
                             primary_metric="accuracy",
                             n_cross_validations=5
                            )
```

### Run AutoML

```py
# Submit your automl run

automl_run = exp.submit(automl_config)
RunDetails(automl_run).show()
automl_run.wait_for_completion(show_output=True)
```

### Get results and save the best one

```py
best_run, fitted_model = automl_run.get_output()
print(best_run)
print(fitted_model)
```

```sh
Run(Experiment: udacity-project,
Id: AutoML_b07a763b-8e10-44da-925e-b794e0fe356c_27,
Type: azureml.scriptrun,
Status: Completed)
Pipeline(memory=None,
         steps=[('datatransformer',
                 DataTransformer(enable_dnn=False, enable_feature_sweeping=True, feature_sweeping_config={}, feature_sweeping_timeout=86400, featurization_config=None, force_text_dnn=False, is_cross_validation=True, is_onnx_compatible=False, observer=None, task='classification', working_dir='/mnt/batch/tasks/shared/LS_root/mount...
), random_state=None, reg_alpha=0.9473684210526315, reg_lambda=0.42105263157894735, subsample=0.49526315789473685))], verbose=False)), ('15', Pipeline(memory=None, steps=[('sparsenormalizer', Normalizer(copy=True, norm='l2')), ('randomforestclassifier', RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight='balanced', criterion='gini', max_depth=None, max_features='sqrt', max_leaf_nodes=None, max_samples=None, min_impurity_decrease=0.0, min_impurity_split=None, min_samples_leaf=0.01, min_samples_split=0.01, min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1, oob_score=True, random_state=None, verbose=0, warm_start=False))], verbose=False))], flatten_transform=None, weights=[0.07692307692307693, 0.15384615384615385, 0.07692307692307693, 0.15384615384615385, 0.38461538461538464, 0.07692307692307693, 0.07692307692307693]))],
         verbose=False)
```


```py
run_properties = best_run.properties
run_properties["model_output_path"]
```

`'outputs/model.pkl'`

```py
run_properties["score"]
```

`'0.9180880121396056'`

```py
# Retrieve and save your best automl model.

### YOUR CODE HERE ###
best_run.register_model(model_name = 'automl_best_model.pkl', model_path = 'outputs/')
```

## Compute cluster cleaning

```py
cpu_cluster.delete()
```
