project_id = "your-gcp-project-id"
project_number = "your-gcp-project-number"
my_user = "postgres"
alloydb_cluster_name = "alloydb-aip-01"
buckets = {
  "library" = {
    location                 = "US-CENTRAL1"
    force_destroy            = true
    uniform_bucket_level_access = true
  }
}
