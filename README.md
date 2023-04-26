# ucdp-org-violence
![](images/international_conflicts.png)

## Project overview
This project is analyzing the organized violence data collected by Department of Peace and Conflict Research of Uppsala University.
The project entails end-to-end orchestrated data pipeline. The conflict data is obtained in batches from the [UCDP API](https://ucdp.uu.se/apidocs/) and saved to Google Cloud Storage in parquet format. Afterwards, the data is processed in pyspark and pushed to BigQuery table which acts as a data source for the Looker dashboard.
Follow the steps mentioned under `How to run it` to reproduce it.

## What is UCDP?
The Uppsala Conflict Data Program (UCDP) is the world’s main provider of data on organized violence and the oldest ongoing data collection project for civil war, with a history of almost 40 years. Its definition of armed conflict has become the global standard of how conflicts are systematically defined and studied.(https://www.pcr.uu.se/research/ucdp/)


## Problems that have been addressed 
1. Identify number of individual events of organized violence in the world in past years
2. Regions that suffered the most from armed conflicts / violence
3. Number of fatalities caused by conflicts

## Technologies
- Cloud: `Google Cloud`
- Infrastructure: `Terraform`
- Orchestration: `Prefect`
- Data lake: `Google Cloud Storage`
- Data processing: `Dataproc`
- Data warehouse: `BigQuery`
- Data visualization: `Google Looker Studio`

## Dashboard 
[Click here](https://lookerstudio.google.com/s/rTWuX39b4nI) to see my Looker dashboard.
![](images/report_view.png)


## How to run it?
1. Setup your Google Cloud environment
- Create a [Google Cloud Platform project](https://console.cloud.google.com/cloud-resource-manager)
- Configure Identity and Access Management (IAM) for the service account, giving it the following privileges: BigQuery Admin, Dataproc Admin, Compute Admin, Compute Storage Admin, Storage Admin and Storage Object Admin
- Download the JSON credentials and save it in terraform folder, e.g. to `src/terraform/<credentials>`
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install-sdk)
- Authenticate the service account
```bash
export YOUR_GCP_CREDENTIALS="~/terraform/<credentials>.json”
gcloud auth login --cred-file=terraform/<credentials>.json
gcloud config set project <PROJECT_ID>
```

2. Install all required dependencies into your environment
```bash
pip install -r requirements.txt
```
3. Setup your infrastructure
- Assuming you are using Linux AMD64 run the following commands to install Terraform - if you are using a different OS please choose the correct version [here](https://developer.hashicorp.com/terraform/downloads) and exchange the download link and zip file name

```bash
sudo apt-get install unzip
cd ~/bin
wget https://releases.hashicorp.com/terraform/1.4.1/terraform_1.4.1_linux_amd64.zip
unzip terraform_1.4.1_linux_amd64.zip
rm terraform_1.4.1_linux_amd64.zip
```
- To initiate, plan and apply the infrastructure, adjust and run the following Terraform commands
```bash
cd terraform/
terraform init
terraform plan -var="project=<your-gcp-project-id>"
terraform apply -var="project=<your-gcp-project-id>"
```
4. Orchestration
- Go to Prefect directory where Dockerfile is located and login to Docker cloud
```bash
docker login
docker image pull weekcrackle/prefect:ucdpconflicts
docker image build -t weekcrackle/prefect:ucdpconflicts .
```
- To create the [prefect blocks] `/prefect/pblocks/blocks.py` run
```bash
python blocks/blocks.py
```
- Start prefect agent
```bash
prefect agent start -q 'default'
```
- In a new terminal window deploy the first job (uploading files to GCP Storage)
```bash
python flows/deploy_file_upload.py
```
- Run deployment to ingest data for 2022 conflicts
```bash
prefect deployment run upload_files/file_upload_flow -p "year=22"
```
- Run deployment to ingest data for 2023 conflicts (Jan,Feb)
```bash
prefect deployment run upload_files/file_upload_flow -p "year=23" -p "months=[1,2]"
```
- Deploy and run a new job to ingest data from the API (years 1989-2021)
```bash
python flows/deploy_api_gcs.py

prefect deployment run etl_etl_gcs/api_request_flow
```

5. Data processing
- Start dataproc cluster
```bash
gcloud dataproc clusters start ucdpconflicts --region=europe-west6
```
- Wait 1-2 minutes for the cluster to start and submit pyspark job to the cluster
```bash
gcloud dataproc jobs submit pyspark --cluster=ucdpconflicts --region=europe-west6 --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    job.py -- --input_georeferenced=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/georeferenced/*/ --input_candidate=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/candidate/*/ --gcs_bucket=dataproc-temp-europe-west6-218014015951-ifenzgrj --output=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/output/*/ --output_table=ucdp-armed-conflicts.ucdp_conflicts.report
```
6. Data for the report
- The data will be available in BigQuery at `ucdp-armed-conflicts.ucdp_conflicts.report`