import functions_framework
from google.cloud import storage, bigquery
import logging


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def gcs_to_bq_trigger(cloud_event):
    storage_client = storage.Client()
    bq_client = bigquery.Client()

    event_data = cloud_event.data
    bucket_name = event_data["bucket"]
    file_name = event_data["name"]

    project_id = ""
    dataset_id = "raw_glamira"
    table_id = "summary"

    if (
        not file_name.endswith(".jsonl")
        or not file_name.startswith("glamira/countly/summary/")
        or file_name.endswith("checkpoint.json")
    ):
        logging.warning(f"Ignore file: {file_name}")
        return

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=False,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        ignore_unknown_values=True,
    )

    uri = f"gs://{bucket_name}/{file_name}"

    try:
        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        load_job = bq_client.load_table_from_uri(uri, table_ref, job_config=job_config)
        load_job.result()
        logging.info(f"Loaded {file_name} into {table_ref}")

    except Exception as e:
        logging.error(f"Error loading {file_name}: {str(e)}")
        raise
