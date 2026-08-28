from datetime import date, timedelta
from enum import Enum

from airflow.sdk import dag
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.dataflow import DataflowTemplatedJobStartOperator


GCP_PROJECT_ID = "your-gcp-project-id"
GCS_BUCKET_NAME = "your-gcs-bucket-name"
BQ_DATASET_NAME = "your_bigquery_dataset_name" # Use the same dataset name you created in the gcp_setup DAG
GCP_CONNECTION_ID = "open_food_facts_gcp"
SERVICE_ACCOUNT_EMAIL = "your-service-account-principal" # The principal of your defined service account

class Source_Format(Enum):
    PARQUET = "parquet"
    JSONL = "jsonl"

def load_from_gcs(format: Source_Format):
    source_format = "PARQUET" if format == Source_Format.PARQUET else "NEWLINE_DELIMITED_JSON"
    source_objects = [f"parquet/huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet"] if format == Source_Format.PARQUET \
        else [f"jsonl/static.openfoodfacts.org/data/openfoodfacts-products.jsonl"]

    return GCSToBigQueryOperator(
        task_id=f"load_{format.value}_to_bq",
        bucket=GCS_BUCKET_NAME,
        source_objects=source_objects,
        destination_project_dataset_table=f"{GCP_PROJECT_ID}.{BQ_DATASET_NAME}.open_food_facts_{format.value}",
        source_format=source_format,
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id=GCP_CONNECTION_ID,
    )

def extract_jsonl_gz():
    # extraction takes about 30mins., extracted file is ~85 GB
    TEMPLATE_PATH = "gs://dataflow-templates/latest/Bulk_Decompress_GCS_Files"

    return DataflowTemplatedJobStartOperator(
        task_id=f"extract_jsonl_gz",
        template=TEMPLATE_PATH,
        job_name="decompress-jsonl-{{ ds_nodash }}",
        parameters={
            "inputFilePattern": f"gs://{GCS_BUCKET_NAME}/jsonl/static.openfoodfacts.org/data/openfoodfacts-products.jsonl.gz",
            "outputDirectory": f"gs://{GCS_BUCKET_NAME}/jsonl/static.openfoodfacts.org/data/",
            "outputFailureFile": f"gs://{GCS_BUCKET_NAME}/jsonl/static.openfoodfacts.org/data/failure.txt",
        },
        options={
            "serviceAccountEmail": SERVICE_ACCOUNT_EMAIL
        },
        gcp_conn_id=GCP_CONNECTION_ID
    )

@dag
def load_to_bq():

    load_from_gcs(Source_Format.PARQUET)

    ## TODO: Tabling this until later due to complexity and having the parquet data available
    # extract_jsonl_gz() >> load_from_gcs(Source_Format.JSONL)

load_to_bq()