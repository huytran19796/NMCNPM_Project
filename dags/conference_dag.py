import sys
sys.path.append('/opt/airflow')
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

from datetime import datetime

default_args={
    "mysql_conn_id": "mysql_connect"
    }

with DAG(
    'conference_dag', 
    default_args = default_args,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    template_searchpath = ['/opt/airflow/mysql_utils/', '/opt/airflow/redshift_utils/']
    ) as dag:
    
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # Clean all data
    clean_data = BashOperator(
    task_id='clean_data',
    bash_command='set -e; python /opt/airflow/dags/clean_all.py')

    # Crawling
    crawl_data = BashOperator(
    task_id='crawl_data',
    bash_command='set -e; python /opt/airflow/crawling/run_spider_conference.py')

    # Transform
    transform_location = BashOperator(
    task_id='transform_location',
    bash_command='set -e; python /opt/airflow/data_transform/transform_location.py')

    transform_field = BashOperator(
    task_id='transform_field',
    bash_command='set -e; python /opt/airflow/data_transform/transform_field.py')

    transform_presenter = BashOperator(
    task_id='transform_presenter',
    bash_command='set -e; python /opt/airflow/data_transform/transform_presenter.py')

    transform_conference = BashOperator(
    task_id='transform_conference',
    bash_command='set -e; python /opt/airflow/data_transform/transform_conference.py')

    set_up_database = BashOperator(
    task_id='set_up_database',
    bash_command='set -e; python /opt/airflow/mysql_utils/set_up_database.py')

    load_location = BashOperator(
    task_id='load_location',
    bash_command='set -e; python /opt/airflow/mysql_utils/load_location.py')

    load_field = BashOperator(
    task_id='load_field',
    bash_command='set -e; python /opt/airflow/mysql_utils/load_field.py')

    load_presenter = BashOperator(
    task_id='load_presenter',
    bash_command='set -e; python /opt/airflow/mysql_utils/load_presenter.py')

    load_conference = BashOperator(
    task_id='load_conference',
    bash_command='set -e; python /opt/airflow/mysql_utils/load_conference.py')
    
    # start >> load_data >> end
    start >> clean_data >> crawl_data >> [ transform_field , transform_presenter , transform_location ] >> transform_conference \
    >> set_up_database >> [ load_location , load_field , load_presenter ] >> load_conference >> end