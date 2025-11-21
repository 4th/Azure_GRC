// infra/terraform/modules/container_app/variables.tf

# -------------------------------------------------------------------
# Identity & placement
# -------------------------------------------------------------------

variable "name" {
  description = "Name of the Container App."
  type        = string
}

variable "location" {
  description = "Azure region where the Container App will be deployed."
  type        = string
}

variable "resource_group" {
  description = "Name of the resource group for the Container App."
  type        = string
}

variable "containerapps_env_id" {
  description = "ID of the Azure Container Apps Environment."
  type        = string
}

# -------------------------------------------------------------------
# Image & runtime
# -------------------------------------------------------------------

variable "container_image" {
  description = "Container image (e.g., myregistry.azurecr.io/policyengine-svc:dev)."
  type        = string
}

variable "cpu" {
  description = "CPU cores allocated to the container (e.g., 0.5, 1.0)."
  type        = number
  default     = 0.5
}

variable "memory" {
  description = "Memory allocated to the container (e.g., \"1.0Gi\")."
  type        = string
  default     = "1.0Gi"
}

# -------------------------------------------------------------------
# Networking / Ingress
# -------------------------------------------------------------------

variable "target_port" {
  description = "Container port exposed via ingress (e.g., 8080, 8501)."
  type        = number
}

variable "ingress_external" {
  description = "Whether the app should be externally accessible."
  type        = bool
  default     = true
}

variable "ingress_allow_insecure" {
  description = "Allow HTTP (insecure) traffic in addition to HTTPS."
  type        = bool
  default     = false
}

# -------------------------------------------------------------------
# Scaling
# -------------------------------------------------------------------

variable "min_replicas" {
  description = "Minimum number of app replicas."
  type        = number
  default     = 1
}

variable "max_replicas" {
  description = "Maximum number of app replicas."
  type        = number
  default     = 2
}

# -------------------------------------------------------------------
# Environment variables
# -------------------------------------------------------------------

variable "environment_variables" {
  description = "Map of environment variables to inject into the container."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# Tags
# -------------------------------------------------------------------

variable "tags" {
  description = "Tags applied to the Container App."
  type        = map(string)
  default     = {}
}
