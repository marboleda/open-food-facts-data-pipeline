from datetime import date

from airflow.sdk import dag
from airflow.providers.google.cloud.operators.cloud_storage_transfer_service import \
    CloudDataTransferServiceCreateJobOperator, GcpTransferJobsStatus

@dag
def extract_source_data():
    date_today = date.today()

    extract_parquet = CloudDataTransferServiceCreateJobOperator(
        task_id="extract_parquet",
        body={
            "description": "Extract Open Food Facts parquet data into GCS",
            "status": GcpTransferJobsStatus.ENABLED,
            "projectId": "open-food-facts-505018",
            "transferSpec": {
                "httpDataSource": {
                    "listUrl": "https://huggingface.co/datasets/openfoodfacts/product-database/resolve/main/food.parquet?download=true"
                },
                "gcsDataSink": {
                    "bucketName": "open-food-facts-505018-source-data",
                    "path": f"open_food_facts_subset_{date_today}.parquet/"
                }
            },
            "schedule": {
                "scheduleStartDate": {
                    "year": date_today.year,
                    "month": date_today.month,
                    "day": date_today.day
                },
                "startTimeOfDay": { # Set in UTC
                    "hours": 23, # 7pm in ET
                    "minutes": 0,
                    "seconds": 0
                }
            }
        },
        gcp_conn_id="open_food_facts_gcp",  # Ensure this connection is set up in your Airflow with the correct credentials
    )

extract_source_data()