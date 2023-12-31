# import the libraries
from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to write tasks!
from airflow.operators.bash_operator import BashOperator
# This makes scheduling easy
from airflow.utils.dates import days_ago
#defining DAG arguments
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'Muhamad Khoirul',
    'start_date': days_ago(0),
    'email': ['muhamadkoirul@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
# defining the DAG
# define the DAG
dag = DAG(
    'ETL_Server_Access_Log_Processing',
    default_args=default_args,
    description='ETL_Server_Access_Log_Processing',
    schedule_interval=timedelta(days=1),
)
# define the tasks
# download task
# since my dags in docker environment save at /tmp folder 
download = BashOperator(
    task_id='download',
    bash_command='curl https://<hosts-web>/web-server-access-log.txt -o /tmp/web-server-access-log.txt',
    dag=dag,
)
# extract task
extract = BashOperator(
    task_id='extract',
    bash_command='cut -d"#" -f1,4 /tmp/web-server-access-log.txt > /tmp/extracted.txt',
    dag=dag,
)
# transform task
transform = BashOperator(
    task_id='transform',
    bash_command='tr "[a-z]" "[A-Z]" < /tmp/extracted.txt > /tmp/capitalized.txt',
    dag=dag,
)

# lad task
load = BashOperator(
    task_id='load',
    bash_command='zip /tmp/log.zip /tmp/capitalized.txt' ,
    dag=dag,
)
# task pipeline
download >> extract >> transform >> load
