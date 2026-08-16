from datetime import date

from airflow.sdk import dag
from airflow.providers.google.cloud.operators.cloud_storage_transfer_service import \
    CloudDataTransferServiceCreateJobOperator, GcpTransferJobsStatus

GCP_PROJECT_ID = "your-gcp-project-id"
GCS_BUCKET_NAME = "your-gcs-bucket-name"
GCP_CONN_ID = "open_food_facts_gcp"  # Ensure this connection is set up in your Airflow with the correct credentials

@dag
def extract_source_data():
    date_today = date.today()

    extract_parquet = CloudDataTransferServiceCreateJobOperator(
        task_id="extract_parquet",
        body={
            "description": "Extract Open Food Facts parquet data into GCS",
            "status": GcpTransferJobsStatus.ENABLED,
            "projectId": GCP_PROJECT_ID,
            "transferSpec": {
                "httpDataSource": {
                    "listUrl": f"gs://{GCS_BUCKET_NAME}/source_parquet_url.tsv"
                },
                "gcsDataSink": {
                    "bucketName": GCS_BUCKET_NAME,
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
        gcp_conn_id=GCP_CONN_ID
    )

    extract_jsonl = CloudDataTransferServiceCreateJobOperator(
        task_id="extract_jsonl",
        body={
            "description": "Extract Open Food Facts JSONL data into GCS",
            "status": GcpTransferJobsStatus.ENABLED,
            "projectId": GCP_PROJECT_ID,
            "transferSpec": {
                "httpDataSource": {
                    "listUrl": f"gs://{GCS_BUCKET_NAME}/source_jsonl_url.tsv"
                },
                "gcsDataSink": {
                    "bucketName": GCS_BUCKET_NAME,
                    "path": f"open_food_facts_complete_{date_today}.jsonl.gz/"
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
        gcp_conn_id=GCP_CONN_ID
    )

extract_source_data()