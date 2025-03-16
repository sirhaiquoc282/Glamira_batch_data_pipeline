from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operator.bash import BashOperator
from datetime import datetime, timedelta
from IPLocation_convertor.main import main as run_ip_location
from products_crawler.main import main as run_products_crawler
from mongo_extractor.main import main as run_mongo_extractor
import sys
import os

AIRFLOW_HOME = os.getenv("AIRFLOW_HOME", os.path.expanduser("~/airflow"))
SOURCE_PATH = os.path.join(AIRFLOW_HOME, "../source")
DBT_PATH = os.path.join(AIRFLOW_HOME, "../dbt")
sys.path.append(SOURCE_PATH)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "daily_etl_pipeline",
    default_args=default_args,
    description="Run ETL tasks and DBT daily",
    schedule_interval="0 0 * * *",
    catchup=False,
)


crawl_products = PythonOperator(
    task_id="run_products_crawler",
    python_callable=run_products_crawler,
    dag=dag,
)


convert_ip_to_location = PythonOperator(
    task_id="run_ip_location",
    python_callable=run_ip_location,
    dag=dag,
)


extract_data_from_mongo_to_gcs = PythonOperator(
    task_id="run_mongo_extractor",
    python_callable=run_mongo_extractor,
    dag=dag,
)


run_dbt = BashOperator(
    task_id="run_dbt",
    bash_command=f"cd {DBT_PATH} && dbt run",
    dag=dag,
    execution_timeout=timedelta(hours=1),
    run_as_user="airflow",
)

[crawl_products, convert_ip_to_location] >> extract_data_from_mongo_to_gcs >> run_dbt
