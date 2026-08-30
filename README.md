# Open Food Facts (OFF) Data Pipeline
This is a data pipeline for processing data from [Open Food Facts](https://world.openfoodfacts.org/), a crowdsourced food products database that contains info about food products around the world so people can make better decisions about their food purchases.

## Overview
Open Food Facts provides a database dump daily, as detailed [here](https://world.pro.openfoodfacts.org/data). This allows us to analyse up-to-date food data and gain insights into food & nutrition trends around the world.

## Use Cases
- Knowledge base for a RAG-powered AI Assistant (e.g. a nutrition assistant)

## Architecture
| Technology | Purpose |
| --- | --- |
| Terraform | Infrastructure as Code |
| Apache Airflow | Workflow Orchestration |
| Google Cloud Storage | Object Storage |
| BigQuery | Data Warehouse |

## Dashboard

## How-To
### Prerequisites
- [Terraform](https://developer.hashicorp.com/terraform/install) is installed.
- Docker Desktop **or** Docker Engine + Docker Compose is installed
- You have a [Google Cloud Platform](https://cloud.google.com/) account
    - Make sure you have a project created that you will use for this pipeline.
    - Make sure you have the following APIs enabled:
        - BigQuery API
        - Cloud Storage API
        - Storage Transfer API
        - Dataflow API
    - Make sure you have a Service Account in the project with the following roles:
        - Storage Admin
        - Storage Transfer Admin
        - BigQuery Data Editor
        - BigQuery Job User
        - BigQuery Read Session User
        - Dataflow Developer
        - Dataflow Worker
        - Service Account User

### Steps
1. Set up your GCS Bucket and BigQuery Dataset.
    - You have 2 options for doing this:
        - Follow the instructions in the [infrastructure](https://github.com/marboleda/open-food-facts-data-pipeline/tree/main/infrastructure) folder to create the resources through Terraform, **or**
        - Skip to the next step (Step 2) where you have the option of creating them within Airflow.
2. Extract and load the data into BigQuery by following the steps in the [orchestration](https://github.com/marboleda/open-food-facts-data-pipeline/tree/main/orchestration) folder
    - If you didn't set up the GCP resources in the previous step, you have the opportunity to do so here.

## Notes