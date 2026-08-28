# Workflow Orchestration
We will use Apache Airflow to orchestrate the extraction of the OFF data and loading into GCP.

## Overview
The data can come in multiple formats, which gives us several options for extraction:
- MongoDB database dump
    - The most complete representation of the data, but the largest in size 
    - ~15 GB compressed
- JSONL file
    - represents the same data as the MongoDB database (i.e. this is the full set of data)
- CSV file
    - Contains all the products, but with a subset of the database fields (though a large subset that it should fit most needs)
    - 1 GB compressed, 10+ GB uncompressed (can't even realistically open this in Excel or Libre Office)
- Parquet daily export
    - Similar to CSV file, but in parquet format

All of these formats are exported daily.

## Approach
### Which format to ingest?
Since we will be loading this data into GCS to be processed by BigQuery, we will not be extracting the MongoDB database itself as that would be unwieldy.

The remaining file types can be processed with GCS and BigQuery, so depending on our needs we will extract one of the following:

- JSONL (if we need the complete set of data)
- Parquet (if the large subset will suffice)

Parquet is preferable to CSV in this case since we will not be needing to open up the file in something like Excel or Libre Office.  
Parquet files are also more performant in data processing, which will be helpful since we are working with a large data set.

### Extract
The JSONL and Parquet files are extracted using GCP's **Storage Transfer** service.  
This is set up in the `02_extract_source_data.py` DAG.

### Load
The source data has numerous fields where the field name starts with a number (e.g. under `nutriments`, there will be a field called `100g`).  
This makes us unable to create external tables from the source data, as external tables in BigQuery do not suppport flexible column names. See [here](https://docs.cloud.google.com/bigquery/docs/schemas#limitations)

Thus, we load our source data into BigQuery as Native Tables.

The JSONL file also has an additional step as it is too large to be loaded into BigQuery in its form as a compressed .gz file.  
So we set up a **Dataflow** job which decompresses the .gz file before loading into BigQuery.


## How-To
### Prerequisites
#### Service Agent Permissions
When transferring source data to your GCS bucket using Airflow, GCP does not use your defined service account. Rather, it uses a [service agent](https://docs.cloud.google.com/iam/docs/service-account-types#service-agents) that it creates for the **Storage Transfer** service.

This service agent needs to have `storage.buckets.get`, `storage.objects.create`, and `storage.objects.list` permission for the cloud transfer job to be created (it will return an error otherwise).

The service agent should have the email address: 
- project-***project-number***@storage-transfer-service.iam.gserviceaccount.com

For example: `project-878874499236@storage-transfer-service.iam.gserviceaccount.com`

Go to your GCS bucket, click on `Permissions` then `Grant access`.  
Add your service agent as a new principal, and add the roles of **Storage Bucket Viewer** and **Storage Object User**.

#### List URL for Parquet
When scheduling the extraction for the .parquet or JSONL file, you need to provide a .`tsv` file detailing which URL to extract from.

The .tsv for the parquet can be found in the root of the `orchestration` directory: `source_parquet_url.tsv`.  
The .tsv for the JSONL can also be found in the root of `orchestration` with this name: `source_json_url.tsv`.  

Upload these to your GCS bucket before running `02_extract_source_data.py` (this only needs to be done once)

### Build Airflow image
To use a particular Airflow operator (`DataflowTemplatedJobStartOperator`), the Airflow Worker and Airflow Scheduler services need to have Apache Beam installed which is not installed in the base Airflow image.  
We install this package using a custom Dockerfile.

To make sure this is custom image is built, run the command `docker-compose build`.