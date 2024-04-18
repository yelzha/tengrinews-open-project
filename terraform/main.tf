terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  credentials = file("~/.google/credentials/google_credentials.json")
  project     = var.project_id
}

resource "google_storage_bucket" "gcp-storage" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 3
    }

    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "bigquery-dataset" {
  dataset_id = var.bigquery_dataset_id
  location   = var.location
}