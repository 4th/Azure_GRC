// infra/terraform/modules/cosmos/variables.tf

# -------------------------------------------------------------------
# Toggle
# -------------------------------------------------------------------

variable "enable" {
  description = "Whether to provision Cosmos DB resources."
  type        = bool
  default     = true
}

# -------------------------------------------------------------------
# Naming & placement
# -------------------------------------------------------------------

variable "name_prefix" {
  description = "Base name prefix for Cosmos resources (e.g., 4th-grc-dev)."
  type        = string
}

variable "location" {
  description = "Azure region for Cosmos DB."
  type        = string
}

variable "resource_group" {
  description = "Resource group in which to create Cosmos resources."
  type        = string
}

variable "tags" {
  description = "Tags to apply to Cosmos resources."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# Database & container configuration
# -------------------------------------------------------------------

variable "database_name" {
  description = "Optional override for Cosmos SQL database name (default: trustops-db)."
  type        = string
  default     = ""
}

variable "container_name" {
  description = "Optional override for Cosmos SQL container name (default: findings)."
  type        = string
  default     = ""
}

variable "partition_key_path" {
  description = "Partition key path for the container."
  type        = string
  default     = "/profile_id"
}

variable "throughput" {
  description = "RU/s throughput for the SQL database."
  type        = number
  default     = 400
}
