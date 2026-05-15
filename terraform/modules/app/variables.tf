variable "environment" {
  description = "Environment name"
  type        = string
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "school_dashboard"
}

variable "port" {
  description = "Port the app runs on"
  type        = number
  default     = 8000
}

variable "secret_key" {
  description = "Django SECRET_KEY"
  type        = string
  sensitive   = true
}

variable "database_url" {
  description = "PostgreSQL connection string"
  type        = string
  sensitive   = true
}

variable "allowed_hosts" {
  description = "Comma-separated list of allowed hosts"
  type        = string
}

variable "csrf_trusted_origins" {
  description = "Comma-separated list of trusted origins"
  type        = string
}

variable "debug" {
  description = "Django DEBUG setting"
  type        = bool
  default     = false
}

variable "python_version" {
  description = "Python version"
  type        = string
  default     = "3.11"
}
