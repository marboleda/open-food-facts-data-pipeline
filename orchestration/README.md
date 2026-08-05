# Workflow Orchestration
We will use Apache Airflow to orchestrate the extraction of the OFF data and loading into GCP (specifically into Google Cloud Storage).

## Overview
The data can come in multiple formats, which gives us several options for extraction:
- MongoDB database dump
    - The most complete representation of the data, but the largest in size 
    - ~15 GB compressed
- 
- CSV file
    - Contains all the products, but with a subset of the database fields (though a large subset that it should fit most needs)
    - 1 GB compressed, 10+ GB uncompressed (can't even realistically open this in Excel or Libre Office)
- Parquet daily export
    - Similar to CSV file, but in parquet format

All of these formats are exported daily.

## Approach


## How-To