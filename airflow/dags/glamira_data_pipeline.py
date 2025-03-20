from airflow import DAG
from airflow.operator.bash import BashOperator
from airflow.operator.time_delta import TimeDeltaSensor
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "glamira_data_pipeline",
    default_args=default_args,
    schedule_interval="0 0 * * *",
    start_date=datetime(2025, 20, 1),
    catchup=False,
    tags=["glamira"],
) as dag:
    crawl_products_name = BashOperator(
        task_id="crawl_products_name",
        bash_command="cd src/jobs/data_crawling && scrapy crawl glamira",
        dag=dag,
    )

    convert_ips_to_locations = BashOperator(
        task_id="convert_ips_to_locations",
        bash_command="cd src/jobs/ip_to_location && python3 ip_to_location.py",
        dag=dag,
    )

    extract_mongodb_to_gcs = BashOperator(
        task_id="extract_mongodb_to_gcs",
        bash_command="cd src/jobs/data_extraction && python3 mongodb_to_gcs.py",
        dag=dag,
    )

    extract_csv_to_gcs = BashOperator(
        task_id="extract_csv_to_gcs",
        bash_command="cd src/jobs/data_extraction && python3 csv_extraction.py",
        dag=dag,
    )

    wait_for_loading_data_from_gcs_to_bq = TimeDeltaSensor(
        task_id="wait_for_loading_data_from_gcs_to_bq",
        delta=timedelta(hours=3),
        dag=dag,
    )

    transform_data = BashOperator(
        task_id="transform_data", bash_command="cd dbt && dbt run", dag=dag
    )

    (
        [crawl_products_name, convert_ips_to_locations]
        >> [extract_csv_to_gcs, extract_mongodb_to_gcs]
        >> wait_for_loading_data_from_gcs_to_bq
        >> transform_data
    )
