terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

module "school_dashboard" {
  source = "../../modules/app"

  environment          = "production"
  app_name             = "school_dashboard"
  port                 = 8000
  secret_key           = var.secret_key
  database_url         = var.database_url
  allowed_hosts        = "school-dashboard-lqng.onrender.com,localhost"
  csrf_trusted_origins = "https://school-dashboard-lqng.onrender.com"
  debug                = false
}

output "app_info" {
  value = {
    name        = module.school_dashboard.app_name
    url         = module.school_dashboard.app_url
    environment = module.school_dashboard.environment
    debug       = module.school_dashboard.debug_mode
  }
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "database_url" {
  type      = string
  sensitive = true
}
