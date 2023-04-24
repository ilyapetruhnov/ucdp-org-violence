import re
from google.cloud import dataproc_v1 as dataproc



def submit_job(project_id, region, cluster_name):
    # Create the job client.
    job_client = dataproc.JobControllerClient(
        client_options={"api_endpoint": "{}-dataproc.googleapis.com:443".format(region)}
    )

    # Create the job config. 'main_jar_file_uri' can also be a
    # Google Cloud Storage URL.
    job = {
        "placement": {"cluster_name": cluster_name},
        "spark_job": {
            "main_jar_file_uri": "file://Users/ilyapetruhnov/Documents/Projects/ucdp-org-violence/src/pyspark/job.py",
            "jar_file_uris": ['gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar'],
            "args": ["input_georeferenced=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/georeferenced/*/",
                        "input_candidate=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/candidate/*/",
                        "output=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/output/*/",
                        "output_table=ucdp-armed-conflicts.ucdp_conflicts.report"]
        },
    }

    operation = job_client.submit_job_as_operation(
        request={"project_id": project_id, "region": region, "job": job}
    )
    response = operation.result()
    print(response)

if __name__ == "__main__":
    project_id = "ucdp-armed-conflicts"
    region = "europe-west6"
    cluster_name = "ucdpconflicts"
    submit_job(project_id, region, cluster_name)

    # Dataproc job output gets saved to the Google Cloud Storage bucket
    # allocated to the job. Use a regex to obtain the bucket and blob info.
    # matches = re.match("gs://(.*?)/(.*)", response.driver_output_resource_uri)

    # output = (
    #     storage.Client()
    #     .get_bucket(matches.group(1))
    #     .blob(f"{matches.group(2)}.000000000")
    #     .download_as_string()
    # )

    # print(f"Job finished successfully: {output}")
