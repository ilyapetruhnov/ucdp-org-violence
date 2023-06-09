locals {
  data_lake_bucket = "ucdp_conflicts_bucket"
}

variable credentials{
  description = "GCP account credentials"
  default = "credentials.json"
}

variable "project" {
  description = "noted-acronym-377016"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-west6"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "ucdpconflicts"
}

variable "dataproc_cluster_name" {
  description = "Dataproc cluster"
  type        = string
  default     = "ucdpconflicts"
}