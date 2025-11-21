// infra/terraform/modules/storage/variables.tf

# -------------------------------------------------------------------
# Placement / naming
# -------------------------------------------------------------------

variable "name_prefix" {
  description = "Base prefix used to derive the storage account name (e.g., 4th-grc-dev)."
  type        = string
}

variable "location" {
  description = "Azure region where the storage account will be created."
  type        = string
}

variable "resource_group" {
  description = "Resource group name for the storage account."
  type        = string
}

variable "tags" {
  description = "Tags applied to the storage account."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# SKU
# -------------------------------------------------------------------

variable "account_tier" {
  description = "Storage account tier: Standard or Premium."
  type        = string
  default     = "Standard"
}

variable "replication_type" {
  description = "Replication type: LRS, GRS, RAGRS, ZRS, etc."
  type        = string
  default     = "LRS"
}

# -------------------------------------------------------------------
# Security / access
# -------------------------------------------------------------------

variable "allow_blob_public_access" {
  description = "Allow public access to blobs in containers."
  type        = bool
  default     = false
}

# -------------------------------------------------------------------
# Containers
# -------------------------------------------------------------------

variable "containers" {
  description = <<EOT
Optional map of containers to create.
Key is an arbitrary identifier; value is an object:
  - name        : container name
  - access_type : private | blob | container
EOT
  type = map(object({
    name        = string
    access_type = string
  }))

  default = {}
}
