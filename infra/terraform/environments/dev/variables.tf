// infra/terraform/environments/dev/variables.tf
// Input variables for the 4th.GRC dev environment

# -------------------------------------------------------------------
# Core environment settings
# -------------------------------------------------------------------

variable "environment_name" {
  description = "Logical environment name (e.g., dev, test, prod)."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region where resources are deployed (e.g., eastus)."
  type        = string
}

variable "name_prefix" {
  description = "Base prefix for resource names; combined with environment_name for full names."
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group that hosts this environment."
  type        = string
}

variable "owner" {
  description = "Owner or primary contact for tagging purposes."
  type        = string
}

variable "extra_tags" {
  description = "Additional tags merged onto all resources."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# Networking
# -------------------------------------------------------------------

variable "vnet_cidr" {
  description = "CIDR block for the virtual network."
  type        = string
}

variable "subnet_cidrs" {
  description = "Map of subnet names to CIDR blocks."
  type        = map(string)
}

# -------------------------------------------------------------------
# Azure Container Registry (ACR)
# -------------------------------------------------------------------

variable "acr_sku" {
  description = "SKU for Azure Container Registry (Basic, Standard, Premium)."
  type        = string
  default     = "Basic"
}

# -------------------------------------------------------------------
# Observability / Log Analytics
# -------------------------------------------------------------------

variable "log_analytics_sku" {
  description = "SKU for Log Analytics workspace (e.g., PerGB2018)."
  type        = string
  default     = "PerGB2018"
}

# -------------------------------------------------------------------
# Cosmos DB (TrustOps findings, etc.)
# -------------------------------------------------------------------

variable "enable_cosmos" {
  description = "Whether to provision Cosmos DB for this environment."
  type        = bool
  default     = true
}

variable "cosmos_sku" {
  description = "SKU or throughput mode for Cosmos DB (e.g., Standard, Autoscale)."
  type        = string
  default     = "Standard"
}

# -------------------------------------------------------------------
# Workload toggles
# -------------------------------------------------------------------

variable "enable_scorecard" {
  description = "Whether to deploy the TrustOps Scorecard app in this environment."
  type        = bool
  default     = true
}

# -------------------------------------------------------------------
# Container images & scaling
# -------------------------------------------------------------------

variable "default_image_tag" {
  description = "Default tag for container images (overridden by CI/CD in most cases)."
  type        = string
  default     = "dev"
}

variable "policyengine_min_replicas" {
  description = "Minimum number of PolicyEngine replicas."
  type        = number
  default     = 1
}

variable "policyengine_max_replicas" {
  description = "Maximum number of PolicyEngine replicas."
  type        = number
  default     = 2
}

variable "scorecard_min_replicas" {
  description = "Minimum number of Scorecard replicas."
  type        = number
  default     = 1
}

variable "scorecard_max_replicas" {
  description = "Maximum number of Scorecard replicas."
  type        = number
  default     = 2
}
