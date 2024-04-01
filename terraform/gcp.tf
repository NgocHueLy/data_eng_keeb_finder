terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "keeb-finder"
}



resource "google_bigquery_dataset" "products" {
  dataset_id  = "product"
  description = "Dataset for products details and purchase option"
  location    = "US"
  project     = "keeb-finder"
}



