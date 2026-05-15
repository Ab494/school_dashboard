terraform {
  required_version = ">= 1.0"
}

locals {
  full_name     = "${var.app_name}-${var.environment}"
  is_production = var.environment == "production"

  log_level = local.is_production ? "WARNING" : "DEBUG"

  common_tags = {
    app         = var.app_name
    environment = var.environment
    managed_by  = "terraform"
    repo        = "school_dashboard"
  }
}

# ── Generate docker-compose ───────────────────────────
resource "local_file" "docker_compose" {
  filename = "${path.module}/../../environments/${var.environment}/docker-compose.generated.yml"

  content = templatefile("${path.module}/docker-compose.tpl", {
    app_name             = var.app_name
    environment          = var.environment
    port                 = var.port
    secret_key           = var.secret_key
    database_url         = var.database_url
    allowed_hosts        = var.allowed_hosts
    csrf_trusted_origins = var.csrf_trusted_origins
    debug                = var.debug
    log_level            = local.log_level
  })
}

# ── Generate .env file ────────────────────────────────
resource "local_file" "env_file" {
  filename = "${path.module}/../../environments/${var.environment}/.env.generated"

  content = sensitive(templatefile("${path.module}/env.tpl", {
    environment          = var.environment
    port                 = var.port
    secret_key           = var.secret_key
    database_url         = var.database_url
    allowed_hosts        = var.allowed_hosts
    csrf_trusted_origins = var.csrf_trusted_origins
    debug                = var.debug
    log_level            = local.log_level
  }))
}
