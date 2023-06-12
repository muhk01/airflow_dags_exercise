# Exploring DAG Components
An Apache Airflow DAG is a python program. It consists of these logical blocks.

1. Imports
2. DAG Arguments
3. DAG Definition
4. Task Definitions
5. Task Pipeline

## Imports
Example of **imports** blocks is looks like below
```
# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
```
## DAG Arguments
Example of **DAG Arguments** blocks is looks like below which including some few adjustable parameters

1. the owner name,
2. when this DAG should run from: days_age(0) means today,
3. the email address where the alerts are sent to,
4. whether alert must be sent on failure,
5. whether alert must be sent on retry,
6. the number of retries in case of failure, and
7. the time delay between retries.
8. A typical DAG definition block looks like this.

```
#defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Owner Name',
    'start_date': days_ago(0),
    'email': ['name@somemail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
```
## DAG Definition
```
# define the DAG
dag = DAG(
    dag_id='sample-etl-dag',
    default_args=default_args,
    description='Sample ETL DAG using Bash',
    schedule_interval=timedelta(days=1),
)
```
## Task Definition
a task definition refers to the definition or specification of an individual task within a DAG.
A task definition typically includes the following information:
1. Task ID: A unique identifier for the task within the DAG. It should be a string that is unique among all the tasks in the DAG.
2. Task Type: The type of task to be executed. This can be an operator provided by the workflow management system (e.g., BashOperator, PythonOperator) or a custom-defined operator.
3. Task Parameters: Any parameters or arguments required for the task. This could include things like input files, output destinations, configuration settings, or any other information necessary for the task to complete its work.
4. Dependencies: The dependencies of the task, specifying the tasks that need to be completed before this task can start. This defines the task's position in the task pipeline and ensures proper execution order.
5. Retry and Error Handling: Any retry policies or error handling strategies specific to the task, such as the maximum number of retries, retry intervals, or actions to take upon failure.

By defining tasks within a DAG and specifying their dependencies and parameters, you can create complex workflows and processes with precise control over the execution order and task behavior. 

```
# define the tasks
# define the first task named extract
extract = BashOperator(
    task_id='extract',
    bash_command='echo "extract"',
    dag=dag,
)
# define the second task named transform
transform = BashOperator(
    task_id='transform',
    bash_command='echo "transform"',
    dag=dag,
)
# define the third task named load
load = BashOperator(
    task_id='load',
    bash_command='echo "load"',
    dag=dag,
)
```
A task is defined using:
A task_id which is a string and helps in identifying the task.
What bash command it represents.
Which dag this task belongs to.

## Task Pipeline
task pipeline refers to the sequence of tasks that are executed based on their dependencies and relationships defined in the DAG. 
Example of task pipeline is like below :
```
# task pipeline
extract >> transform >> load
```
Task pipeline helps us to organize the order of tasks.

Here the task extract must run first, followed by transform, followed by the task load.
