
# Lesson 4 : Pipeline automation

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

### Create a Pipeline

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

### Publish a pipeline

In this part, you need to publish a pipeline using the both Azure ML studio and the Python SDK. Please re-use the Pipeline created in the previous part.

You are recommended to write your own code to publish the pipeline. If you get stuck, review the first a few cells in the **Publish and run from REST endpoint** section in the provided notebook.
