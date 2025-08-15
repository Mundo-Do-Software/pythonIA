# Configuração do Terraform para infraestrutura GCP
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# Variáveis
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

# Provider
provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Habilitar APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "container.googleapis.com",
    "appengine.googleapis.com",
    "redis.googleapis.com",
    "compute.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_dependent_services = true
  disable_on_destroy = false
}

# GKE Cluster para Ollama
resource "google_container_cluster" "deepseek_cluster" {
  name     = "llm-deepseek-cluster"
  location = var.zone
  
  # Configurações básicas
  initial_node_count       = 1
  remove_default_node_pool = true
  
  # Configurações de rede
  network    = "default"
  subnetwork = "default"
  
  # Configurações de segurança
  enable_binary_authorization = false
  enable_shielded_nodes      = true
  
  depends_on = [google_project_service.apis]
}

# Node Pool CPU (para serviços gerais)
resource "google_container_node_pool" "cpu_pool" {
  name       = "cpu-pool"
  location   = var.zone
  cluster    = google_container_cluster.deepseek_cluster.name
  node_count = 1
  
  autoscaling {
    min_node_count = 1
    max_node_count = 3
  }
  
  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 50
    disk_type    = "pd-ssd"
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# Node Pool GPU (para Ollama)
resource "google_container_node_pool" "gpu_pool" {
  name       = "gpu-pool"
  location   = var.zone
  cluster    = google_container_cluster.deepseek_cluster.name
  node_count = 1
  
  autoscaling {
    min_node_count = 0
    max_node_count = 2
  }
  
  node_config {
    machine_type = "n1-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-ssd"
    
    guest_accelerator {
      type  = "nvidia-tesla-t4"
      count = 1
      gpu_driver_installation_config {
        gpu_driver_version = "INSTALLATION_DISABLED"
      }
    }
    
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    
    taint {
      key    = "nvidia.com/gpu"
      value  = "true"
      effect = "NO_SCHEDULE"
    }
  }
}

# Redis Instance (Memorystore)
resource "google_redis_instance" "cache" {
  name           = "llm-redis"
  memory_size_gb = 1
  region         = var.region
  
  redis_version = "REDIS_6_X"
  tier         = "STANDARD_HA"
  
  auth_enabled = false
  
  depends_on = [google_project_service.apis]
}

# App Engine Application
resource "google_app_engine_application" "app" {
  project     = var.project_id
  location_id = var.region
  
  depends_on = [google_project_service.apis]
}

# Outputs
output "cluster_endpoint" {
  description = "GKE cluster endpoint"
  value       = google_container_cluster.deepseek_cluster.endpoint
}

output "redis_host" {
  description = "Redis host IP"
  value       = google_redis_instance.cache.host
}

output "redis_port" {
  description = "Redis port"
  value       = google_redis_instance.cache.port
}

output "app_engine_url" {
  description = "App Engine URL"
  value       = "https://${var.project_id}.appspot.com"
}
