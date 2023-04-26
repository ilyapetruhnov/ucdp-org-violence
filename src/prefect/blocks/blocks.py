from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.infrastructure.docker import DockerContainer
import os
import json

# This is an alternative to creating GCP blocks in the UI
# (1) insert your own GCS bucket name
# (2) insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

# service_account_file_path = os.environ['YOUR_GCP_CREDENTIALS']
# service_account_file_path = "/opt/prefect/credentials/credentials.json"
credentials_file = open('../../terraform/credentials.json')
service_account_info = json.load(credentials_file)

docker_block_name="docker-block"
docker_img = "weekcrackle/prefect:ucdp"
gcs_bucket_name = "ucdp_conflicts_dl_bucket_ucdp-armed-conflicts"  # (1) insert your GCS bucket name
gcs_bucket_block_name = "gcs-bucket" 
gcs_credentials_block_name = "gcs-credentials"

credentials_block = GcpCredentials(
    service_account_info = service_account_info  # (2) enter your credentials info here
)

credentials_block.save(f"{gcs_credentials_block_name}", overwrite=True)

bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load(f"{gcs_credentials_block_name}"),
    bucket=f"{gcs_bucket_name}",
)

bucket_block.save(f"{gcs_bucket_block_name}", overwrite=True)

docker_block = DockerContainer(
    image=docker_img,  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
)

docker_block.save(docker_block_name, overwrite=True)
