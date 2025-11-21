 // infra/terraform/environments/dev/locals.tf
// Local values for the 4th.GRC dev environment

locals {
  # ---------------------------------------------------------------------------
  # Core naming + environment context
  # ---------------------------------------------------------------------------

  # Short environment label (e.g., dev, test, prod)
  env = var.environment_name

  # Base prefix for resources; in dev.tfvars:
  #   name_prefix = "4th-grc"
  #
  # Combined pattern yields names like:
  #   4th-grc-dev-aca
  #   4th-grc-dev-acr
  #   4th-grc-dev-kv
  name_prefix = "${var.name_prefix}-${local.env}"

  # Azure region for this environment (e.g., eastus)
  location = var.location

  # ---------------------------------------------------------------------------
  # Global tags
  # ---------------------------------------------------------------------------

  # Standard tags applied to all resources in this environment
  base_tags = {
    project     = "4th.GRC"
    environment = local.env
    owner       = var.owner
  }

  # Merged tags = base_tags + extra_tags from dev.tfvars
  tags = merge(local.base_tags, var.extra_tags)
}
