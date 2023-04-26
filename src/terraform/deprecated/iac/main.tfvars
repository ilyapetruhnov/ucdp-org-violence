gcp_service_list = [
    "iamcredentials.googleapis.com",
    "bigquery.googleapis.com",
    "compute.googleapis.com",
    "bigquerystorage.googleapis.com",
    "bigquerymigration.googleapis.com",
    "dataproc.googleapis.com",
    "dataproc-control.googleapis.com",
    "datastore.googleapis.com",
    "storage-component.googleapis.com",
    "storage.googleapis.com",
    "cloudtrace.googleapis.com",
    "cloudapis.googleapis.com",
    "storage-api.googleapis.com",
    "servicemanagement.googleapis.com",
    "sql-component.googleapis.com",
    "oslogin.googleapis.com",
    "datastudio.googleapis.com"
]

project_id  = "some-project-id"

account_id  = "bucket-admin"
description = "Bucket Admin"
roles = [
  "roles/storage.admin",
]