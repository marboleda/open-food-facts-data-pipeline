from datetime import date
from enum import Enum

from airflow.sdk import dag
from airflow.providers.google.cloud.operators.cloud_storage_transfer_service import \
    CloudDataTransferServiceCreateJobOperator, GcpTransferJobsStatus

GCP_PROJECT_ID = "your-gcp-project-id"
GCS_BUCKET_NAME = "your-gcs-bucket-name"
GCP_CONNECTION_ID = "open_food_facts_gcp"  # Ensure this connection is set up in your Airflow with the correct credentials

class Source(Enum):
    PARQUET = "parquet"
    JSONL = "jsonl"

def schedule_extraction_from_source(source: Source):
    date_today = date.today()

    return CloudDataTransferServiceCreateJobOperator(
        task_id=f"extract_{source.value}",
        body={
            "description": f"Extract Open Food Facts {source.value} data into GCS",
            "status": GcpTransferJobsStatus.ENABLED,
            "projectId": GCP_PROJECT_ID,
            "transferSpec": {
                "httpDataSource": {
                    "listUrl": f"gs://{GCS_BUCKET_NAME}/source_{source.value}_url.tsv"
                },
                "gcsDataSink": {
                    "bucketName": GCS_BUCKET_NAME,
                    "path": f"{source.value}/"
                },
                "transferOptions": {
                    "overwriteObjectsAlreadyExistingInSink": True
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
        gcp_conn_id=GCP_CONNECTION_ID
    )

@dag
def extract_source_data():

    extract_parquet = schedule_extraction_from_source(Source.PARQUET)
    
    extract_jsonl = schedule_extraction_from_source(Source.JSONL)

extract_source_data()