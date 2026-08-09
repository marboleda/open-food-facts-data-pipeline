variable "credentials" {
    description = "GCP Service Account credentials"
    # Provide the path to your GCP Service Account credentials JSON file.
    default = "path/to/credentials.json"
}

variable "project" {
    description = "GCP Project ID"
    # Provide your GCP Project ID.
    default = "your-gcp-project-id"
}

variable "region" {
    description = "GCP Region"
    # Provide the GCP region where you want to deploy your resources.
    default = "us-central1"
}

variable "location" {
    description = "Project Location"
    # Provide the location for your resources (e.g. BigQuery dataset)
    default = "northamerica-northeast2"
}

variable "gcs_bucket_name" {
    description = "Name of the GCS bucket to be created"
    # Provide a unique name for your GCS bucket.
    # Recommendation: follow the pattern "<project-id>-<desired-bucket-name>" to ensure uniqueness.
    default = "your-unique-gcs-bucket-name"
}

variable "bigquery_dataset_name" {
    description = "Name of the BigQuery dataset to be created"
    # Provide a name for your BigQuery dataset.
    default = "your_bigquery_dataset_name"
}