# Workflow Orchestration
We will use Apache Airflow to orchestrate the extraction of the OFF data and loading into GCP (specifically into GCS, Google Cloud Storage).

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


## How-To