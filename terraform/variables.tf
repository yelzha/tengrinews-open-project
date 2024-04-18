variable "location" {
  description = "My location"
  default = "US"
}

variable "project_id" {
  description = "The ID of the Google Cloud project."
  type        = string
}

variable "bigquery_dataset_id"{
    description = "Bigquery Dataset name"
    default = "terraform_bigquery"
}

variable "gcs_storage_class" {
  description = "GCS storage class name"
  default = "raw_streaming"

}

variable "bucket_name" {
  description = "GCS storage bucket name"
  default = "supply-chain-data-terraform"
}