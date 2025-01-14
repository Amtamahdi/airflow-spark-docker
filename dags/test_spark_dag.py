from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def print_hello():
    return 'Hello from test DAG!'

with DAG('test_spark_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    hello_task = PythonOperator(
        task_id='hello_task',
        python_callable=print_hello
    )

    spark_job = SparkSubmitOperator(
        task_id='spark_test_job',
        application='/opt/airflow/dags/spark_test.py',
        name='test_spark_job',
        conn_id='spark_default',
        conf={'spark.master': 'spark://spark-master:7077'},
        application_args=[],
        verbose=True
    )

    hello_task >> spark_job