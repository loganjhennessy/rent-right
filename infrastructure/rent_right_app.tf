provider "google" {
  credentials = file("rent_right_terraform.json")
  project     = "rent-right-app"
  region      = "us-west1"
}
