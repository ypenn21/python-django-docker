terraform {
  required_providers {
    google = {
      version = ">4.50.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "project_services" {
  source  = "terraform-google-modules/project-factory/google//modules/project_services"
  version = "~> 11.1"

  project_id = var.project_id
  disable_services_on_destroy = false
  disable_dependent_services  = false

  activate_apis = [
    "cloudfunctions.googleapis.com",
    "cloudbuild.googleapis.com",
    "run.googleapis.com",
    "logging.googleapis.com",
    "storage-component.googleapis.com",
    "aiplatform.googleapis.com",
    "alloydb.googleapis.com",
    "artifactregistry.googleapis.com",
    "vpcaccess.googleapis.com",
    "servicenetworking.googleapis.com",
    "eventarc.googleapis.com",
    "pubsub.googleapis.com"
  ]
}

resource "google_storage_bucket" "dynamic_buckets" {
  for_each = var.buckets
  depends_on = [module.project_services]
  name          = "${each.key}_${var.project_id}"
  location      = each.value.location
  force_destroy = each.value.force_destroy
  uniform_bucket_level_access = each.value.uniform_bucket_level_access
}

resource "google_compute_network" "auto_vpc" {
  name = "default"
  depends_on = [module.project_services]
  auto_create_subnetworks = true # This creates subnets in each region, similar to a default VPC
}

resource "google_compute_router" "router" {
  depends_on = [google_compute_network.auto_vpc]
  project = var.project_id
  name    = "nat-router"
  network = google_compute_network.auto_vpc.name
  region  = var.region
}

module "cloud-nat" {
  source  = "terraform-google-modules/cloud-nat/google"
  depends_on = [google_compute_router.router]
  project_id                         = var.project_id
  region                             = var.region
  router                             = google_compute_router.router.name
  name                               = "nat-config"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

resource "google_compute_firewall" "allow_access_ingress" {
  name    = "allow-ingress-22-80-5432"
  network = "projects/${var.project_id}/global/networks/default"
  depends_on = [google_compute_network.auto_vpc]
  allow {
    protocol = "tcp"
    ports    = ["22","80","5432"]
  }

  direction    = "INGRESS"
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["all-access"]
}

resource "google_compute_global_address" "psa_range" {
  name          = "psa-range"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 24
  network       = "default"
  depends_on = [google_compute_network.auto_vpc]
}

resource "google_vpc_access_connector" "alloy_connector" {
  name          = "alloy-connector"
  region        = var.region
  network       = "default"
  ip_cidr_range = "10.100.0.0/28"
  depends_on = [google_compute_network.auto_vpc]
}

resource "google_compute_instance" "alloydb_client" {
  name         = "alloydb-client"
  zone         = var.zone
  machine_type = "e2-medium"
  depends_on = [google_alloydb_instance.primary]
  boot_disk {
    initialize_params {
      // The latest Debian 12 image (excluding arm64)
      image = data.google_compute_image.debian_12.self_link
    }
  }

  shielded_instance_config {
    enable_secure_boot = true
  }
  // Network interface with external access
  network_interface {
    network = google_compute_network.auto_vpc.name
  }
    metadata_startup_script = <<EOF
  #!/bin/bash
  sudo apt-get update
  sudo apt-get install --yes postgresql-client
  export REGION=${var.region}
  export ADBCLUSTER=${var.alloydb_cluster_name}
  export PGPASSWORD=${var.alloydb_password}
  psql "host=${local.alloydb_ip} user=postgres" -c "CREATE DATABASE library"
  psql "host=${local.alloydb_ip}  user=postgres dbname=library" -c "CREATE EXTENSION IF NOT EXISTS google_ml_integration CASCADE"
  psql "host=${local.alloydb_ip}  user=postgres dbname=library" -c "CREATE EXTENSION IF NOT EXISTS vector"
  curl -o /tmp/init-db.sql https://raw.githubusercontent.com/ypenn21/python-django-docker/main/sql/ddl.sql
  psql "host=${local.alloydb_ip} user=postgres dbname=library" -f /tmp/init-db.sql
  # Check extension is installed with \dx
  EOF
  
  tags = ["all-access"]

  service_account {
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}

data "google_compute_image" "debian_12" {
  family  = "debian-12"
  project = "debian-cloud"
}

resource "google_service_networking_connection" "private_vpc_connection" {
  depends_on = [google_vpc_access_connector.alloy_connector]
  network                 = google_compute_network.auto_vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.psa_range.name]
}

resource "google_alloydb_cluster" "default" {
  cluster_id = var.alloydb_cluster_name
  location   = var.region
  network_config {
    network = google_compute_network.auto_vpc.id
  }

  initial_user {
    user     = "postgres"
    password = var.alloydb_password
  }

  depends_on = [google_service_networking_connection.private_vpc_connection]
}

resource "google_alloydb_instance" "primary" {
  cluster    = google_alloydb_cluster.default.name
  instance_id = "${var.alloydb_cluster_name}-pr"

  instance_type = "PRIMARY"
  machine_config {
    cpu_count = 2
  }

  depends_on = [google_alloydb_cluster.default]
}

output "alloydb_ip" {
  value = google_alloydb_instance.primary.ip_address
}

locals {
  cloud_run_services = {
    "app-genai" = {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/app-genai/genai-apps:latest",
      env = "jit"
    }
  }
  alloydb_ip = google_alloydb_instance.primary.ip_address
}

resource "google_artifact_registry_repository" "genai_repo" {
  for_each = local.cloud_run_services
  depends_on = [google_alloydb_instance.primary]
  location      = var.region
  repository_id = each.key
  description   = "Artifact registry for genai apps images"
  format        = "DOCKER"

  labels = {
    env = each.value.env
  }
}

resource "google_cloud_run_service" "cloud_run" {
  for_each = local.cloud_run_services
  depends_on = [google_compute_instance.alloydb_client, google_artifact_registry_repository.genai_repo, google_service_networking_connection.private_vpc_connection, google_storage_bucket.dynamic_buckets]
  name     = each.key
  location = var.region

  template {
    metadata {
      annotations = {
        "run.googleapis.com/cpu"    = "4"
        "run.googleapis.com/memory" = "4Gi"
        "run.googleapis.com/vpc-access-connector"  = google_vpc_access_connector.alloy_connector.id
      }
    }
    spec {
      containers {
        image = each.value.image

        resources {
          limits = {
            cpu    = "4000m"
            memory = "4Gi"
          }

        }
        env {
          name  = "MY_PASSWORD"
          value = var.alloydb_password
        }
        env {
          name  = "MY_USER"
          value = var.my_user
        }
        env {
          name  = "DB_URL"
          value =  "jdbc:postgresql://${local.alloydb_ip}:5432/library"
        }
        env {
          name  = "VERTEX_AI_GEMINI_PROJECT_ID"
          value = var.project_id
        }
        env {
          name  = "VERTEX_AI_GEMINI_LOCATION"
          value = var.region
        }
        env {
          name  = "JAVA_TOOL_OPTIONS"
          value = "-XX:+UseG1GC -XX:MaxRAMPercentage=75 -XX:ActiveProcessorCount=4 -XX:+TieredCompilation -XX:TieredStopAtLevel=1 -Xss256k"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  autogenerate_revision_name = true
}
resource "google_cloud_run_service_iam_member" "cloud_run_unauthenticated" {
  for_each = local.cloud_run_services
  depends_on = [google_cloud_run_service.cloud_run]
  location = var.region
  service  = each.key
  role     = "roles/run.invoker"
  member   = "allUsers"
}
resource "google_eventarc_trigger" "genai_trigger_embeddings" {
  for_each = local.cloud_run_services
  depends_on = [google_cloud_run_service.cloud_run]
  name     = "${each.key}-trigger-embeddings-${var.region}"
  location = var.region

  # Ensure you have the correct service account email format
  service_account = "${var.project_number}-compute@developer.gserviceaccount.com"

  destination {
    cloud_run_service {
      service = each.key #Assuming `service_name` is defined in your `local.cloud_run_services`
      path    = "/document/embeddings"
      region  = var.region
    }
  }

  matching_criteria {
    attribute = "type"
    value     = "google.cloud.storage.object.v1.finalized"
  }

  matching_criteria {
    attribute = "bucket"
    value     = "library_${var.project_id}"
  }
}
# Pub/Sub Topic
# resource "google_pubsub_topic" "my_topic" {
#   depends_on = [google_cloud_run_service.cloud_run]
#   name = "my-topic" # Choose a descriptive name for your topic
# }

# Pub/Sub Subscription (optional, if you need to consume messages)
# resource "google_pubsub_subscription" "my_subscription" {
#   name  = "my-subscription"
#   topic = google_pubsub_topic.my_topic.name
#
#   # ... (other subscription configuration, e.g., push endpoint, etc.)
# }
