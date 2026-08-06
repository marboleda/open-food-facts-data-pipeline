terraform {
    required_providers {
      google = {
        source = "hashicorp/google"
        version = "7.43.0"
      }
    }
}

provider "google" {
    credentials = file(var.credentials)
    project = var.project
    region  = var.region
}

resource "google_storage_bucket" "development_data_bucket" {
    name = var.gcs_bucket_name
    location = var.location
    force_destroy = true

    lifecycle_rule {
        condition {
            age = 1
        }
        action {
            type = "AbortIncompleteMultipartUpload"
        }
    }
}

resource "google_bigquery_dataset" "development_data_dataset" {
    dataset_id = var.bigquery_dataset_name
    location = var.location
}