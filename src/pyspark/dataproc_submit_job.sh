gcloud dataproc jobs submit pyspark --cluster=ucdpconflicts --region=europe-west6 --jars=gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar \
    job.py -- --input_georeferenced=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/georeferenced/*/ --input_candidate=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/candidate/*/ --gcs_bucket=tempGcsBucket --output=gs://ucdp_conflicts_dl_bucket_ucdp-armed-conflicts/data/ucdp/output/*/ --output_table=ucdp-armed-conflicts.ucdp_conflicts.report