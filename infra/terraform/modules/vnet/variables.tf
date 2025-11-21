// infra/terraform/modules/vnet/variables.tf

# -------------------------------------------------------------------
# Placement / naming
# -------------------------------------------------------------------

variable "name_prefix" {
  description = "Base name prefix for the VNet (e.g., 4th-grc-dev)."
  type        = string
}

variable "location" {
  description = "Azure region where the VNet will be created."
  type        = string
}

variable "resource_group" {
  description = "Resource group name for the VNet and subnets."
  type        = string
}

variable "tags" {
  description = "Tags applied to the VNet."
  type        = map(string)
  default     = {}
}

# -------------------------------------------------------------------
# Addressing
# -------------------------------------------------------------------

variable "vnet_cidr" {
  description = "CIDR block for the VNet (e.g., 10.10.0.0/16)."
  type        = string
}

variable "subnet_cidrs" {
  description = <<EOT
Map of subnet names to CIDR blocks, e.g.:

  {
    apps = "10.10.1.0/24"
    data = "10.10.2.0/24"
  }
EOT
  type = map(string)
}
