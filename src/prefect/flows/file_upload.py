import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket

@task(log_prints=True, name="Fetch_data", retries=1)
def fetch_file(url) -> pd.DataFrame:
    """File download"""
    df = pd.read_csv(url)
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


@flow(log_prints=True, name="upload_files", retries=1)
def upload_csv_data(year, months=None) -> None:
    base_url = 'https://ucdp.uu.se/downloads/candidateged/GEDEvent_'

    if months:
        for month in months:
            url = f"{base_url}v{year}_0_{month}.csv"
            file_name = f"{year}_{month}"
            df = fetch_file(url)
            file_path = f"data/ucdp/candidate/UCDP_GED_download_{file_name}.parquet"
            path = save_locally(df, file_path)
            upload_gcs(path)
    
    else:
        url = f"{base_url}v22_01_22_12.csv"
        file_name = f"{year}_full"
        df = fetch_file(url)
        file_path = f"data/ucdp/candidate/UCDP_GED_download_{file_name}.parquet"
        path = save_locally(df, file_path)
        upload_gcs(path)


if __name__ == "__main__":
    upload_csv_data()
 


