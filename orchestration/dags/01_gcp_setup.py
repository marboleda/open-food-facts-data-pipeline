from airflow.sdk import dag
from airflow.providers.google.cloud.operators.gcs import GCSCreateBucketOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator

## Set these variables before executing the DAG
PROJECT_ID = "open-food-facts-505018"
BUCKET_NAME = "open-food-facts-505018-source-data"  ## Recommendation: follow the pattern "<gcp-project-id>-<desired-bucket-name>" to ensure uniqueness.
DATASET_NAME = "open_food_facts_data"
REGION = "us-central1" # change if desired

@dag
def gcp_setup():
    create_bucket = GCSCreateBucketOperator(
        task_id="create_gcs_bucket",
        bucket_name=BUCKET_NAME,
        project_id=PROJECT_ID,
        location=REGION,
        storage_class="STANDARD",
        gcp_conn_id="open_food_facts_gcp"  # Ensure this connection is set up in your Airflow with the correct credentials
    )

    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_bigquery_dataset",
        dataset_id=DATASET_NAME,
        project_id=PROJECT_ID,
        location=REGION,
        gcp_conn_id="open_food_facts_gcp",
        if_exists="log"
    )

gcp_setup()