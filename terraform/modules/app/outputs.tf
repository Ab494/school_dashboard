output "app_name" {
  value = local.full_name
}

output "app_url" {
  value = "http://localhost:${var.port}"
}

output "environment" {
  value = var.environment
}

output "debug_mode" {
  value = var.debug
}

output "tags" {
  value = local.common_tags
}
