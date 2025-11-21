// infra/terraform/modules/key_vault/variables.tf

# -------------------------------------------------------------------
# Placement / naming
# -------------------------------------------------------------------

variable "name_prefix" {
  description = "Base name prefix for the Key Vault (e.g., 4th-grc-dev)."
  type        = string
}

variable "location" {
  description = "Azure region where Key Vault will be deployed."
  type        = string
}

variable "resource_group" {
  description = "Resource group name for the Key Vault."
  type        = string
}

variable "tenant_id" {
  description = "Azure AD tenant ID used by the Key Vault."
  type        = string
}

variable "tags" {
  description = "Tags applied to the Key Vault."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# SKU / retention
# -------------------------------------------------------------------

variable "sku_name" {
  description = "Key Vault SKU (Standard or Premium)."
  type        = string
  default     = "standard"
}

variable "soft_delete_retention_days" {
  description = "Number of days soft-deleted vaults are retained."
  type        = number
  default     = 90
}

variable "purge_protection_enabled" {
  description = "Whether purge protection is enabled."
  type        = bool
  default     = true
}

# -------------------------------------------------------------------
# Deployment flags
# -------------------------------------------------------------------

variable "enabled_for_deployment" {
  description = "Allow Virtual Machines to retrieve certificates for deployment?"
  type        = bool
  default     = false
}

variable "enabled_for_disk_encryption" {
  description = "Allow disk encryption to retrieve secrets from the vault?"
  type        = bool
  default     = false
}

variable "enabled_for_template_deployment" {
  description = "Allow ARM templates to retrieve secrets from the vault?"
  type        = bool
  default     = true
}

# -------------------------------------------------------------------
# Network ACLs
# -------------------------------------------------------------------

variable "network_default_action" {
  description = "Default network action for Key Vault (Allow or Deny)."
  type        = string
  default     = "Allow"
}

variable "network_bypass" {
  description = "Bypass for Azure services (None, AzureServices)."
  type        = string
  default     = "AzureServices"
}

# -------------------------------------------------------------------
# Access policies
# -------------------------------------------------------------------

variable "access_policies" {
  description = <<EOT
List of access policies applied to the Key Vault.
Each policy:
  - tenant_id
  - object_id
  - key_permissions
  - secret_permissions
  - certificate_permissions
  - storage_permissions
EOT
  type = list(object({
    tenant_id              = string
    object_id              = string
    key_permissions        = list(string)
    secret_permissions     = list(string)
    certificate_permissions = list(string)
    storage_permissions    = list(string)
  }))

  default = []
}
