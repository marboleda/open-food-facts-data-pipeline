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
        - Dataflow Developer
        - Dataflow Worker
        - Service Account User

## Notes