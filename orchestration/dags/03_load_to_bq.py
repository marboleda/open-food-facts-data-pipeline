from datetime import date, timedelta
from enum import Enum

from airflow.sdk import dag
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

GCP_PROJECT_ID = "your-gcp-project-id"
GCS_BUCKET_NAME = "your-gcs-bucket-name"
BQ_DATASET_NAME = "your_bigquery_dataset_name" # Use the same dataset name you created in the gcp_setup DAG
GCP_CONNECTION_ID = "open_food_facts_gcp"

class Source_Format(Enum):
    PARQUET = "parquet"
    JSONL = "jsonl"

def load_from_gcs(format: Source_Format):
    date_today = date.today()

    source_format = "PARQUET" if format == Source_Format.PARQUET else "NEWLINE_DELIMITED_JSON"
    source_objects = [f"open_food_facts_subset_{date_today}_parquet/*/food.parquet"] if format == Source_Format.PARQUET \
        else [f"open_food_facts_subset_{date_today}_{format.value}/*/openfoodfacts-products.jsonl.gz"]

    return GCSToBigQueryOperator(
        task_id=f"load_{format.value}_to_bq",
        bucket=GCS_BUCKET_NAME,
        source_objects=source_objects,
        destination_project_dataset_table=f"{GCP_PROJECT_ID}.{BQ_DATASET_NAME}.open_food_facts_{date_today}_{format.value}",
        source_format=source_format,
        external_table=True,
        gcp_conn_id=GCP_CONNECTION_ID,
    )

@dag
def load_to_bq():

    load_parquet_to_bq = load_from_gcs(Source_Format.PARQUET)

    load_jsonl_to_bq = load_from_gcs(Source_Format.JSONL)

load_to_bq()