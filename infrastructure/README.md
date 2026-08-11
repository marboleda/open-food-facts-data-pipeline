We are using Terraform to create the following infrastructure for this pipeline:  
- Google Cloud Storage bucket
- Google BigQuery dataset

To set up your own infrastructure, follow these steps:
1. Replace the values in variables.tf with the corresponding values for your GCP project
2. Run terraform init
3. Run terraform plan to review execution plan for resources
4. If all looks good from the previous step, run terraform apply
5. (Optional) If anything is configured incorrectly and you need to start over: run terraform destroy, fix the issues, and go through steps 3 and 4 again.