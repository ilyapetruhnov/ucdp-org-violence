import pandas as pd
import requests
import os
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

API_VERSION = '22.1'


@task(log_prints=True, name="api_call", retries=1)
def api_call(api_version: str, pagesize: int, page: int) -> dict:
    """API call"""

    base_url = f"https://ucdpapi.pcr.uu.se/api/gedevents/{api_version}"
    url = f"{base_url}?pagesize={pagesize}&page={page}"

    response = requests.get(url)
    if response.ok :
        result = response.json()
    else:
        print(response.reason)
    return result


@task(log_prints=True, name="Fetch_data", retries=1)
def fetch_data(response: dict) -> pd.DataFrame:
    """Fetches the API and returns data as a pandas dataframe"""

    result = response['Result']
    df = pd.DataFrame(result)

    return df

@task(log_prints=True, name="Saving_data_locally", retries=1)
def save_locally(df, local_save_path) -> Path:
    "Save file locally"
    path = Path(local_save_path)
    df.to_parquet(path)
    return path

@task(log_prints=True, name="Upload_GCS", retries=1)
def upload_gcs(path) -> None:
    "Upload file to GCS"
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.upload_from_path(from_path = path, to_path = path, timeout=180)
    return None


@flow(log_prints=True, name="Get_count_records", retries=1)
def get_iter(pagesize=1, page=0, custom_page_size=10000) -> int:
    """Record count"""

    result = api_call(API_VERSION, pagesize, page)
    record_cnt = result['TotalCount']

    iterations = round(record_cnt / custom_page_size)

    return iterations


@flow(log_prints=True, name="api_calls", retries=1)
def upload_data(iterations, custom_page_size) -> None:

    for page in range(iterations):
        json = api_call(api_version=API_VERSION, pagesize=custom_page_size, page=page)
        df = fetch_data(json)
        file_name = f"data/ucdp/georeferenced/UCDP_GED_api-{API_VERSION}_page-{page}.parquet"
        path = save_locally(df, file_name)
        upload_gcs(path)

@flow(log_prints=True, name="etl_gcs", retries=1)
def etl_gcs() -> None:
    """ETL up to 2021 data"""

    iterations = get_iter()
    upload_data(iterations, custom_page_size=10000)


if __name__ == "__main__":
    etl_gcs()
 


