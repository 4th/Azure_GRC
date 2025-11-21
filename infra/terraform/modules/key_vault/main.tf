// infra/terraform/modules/key_vault/main.tf
// Azure Key Vault for 4th.GRC environments

locals {
  kv_name = lower(replace("${var.name_prefix}-kv", "_", "-"))
}

resource "azurerm_key_vault" "this" {
  name                        = local.kv_name
  location                    = var.location
  resource_group_name         = var.resource_group
  tenant_id                   = var.tenant_id
  sku_name                    = var.sku_name

  enabled_for_deployment          = var.enabled_for_deployment
  enabled_for_disk_encryption     = var.enabled_for_disk_encryption
  enabled_for_template_deployment = var.enabled_for_template_deployment

  soft_delete_retention_days = var.soft_delete_retention_days
  purge_protection_enabled   = var.purge_protection_enabled

  tags = var.tags

  # Optional: network ACLs (currently open; tighten in prod)
  network_acls {
    default_action = var.network_default_action
    bypass         = var.network_bypass
  }

  dynamic "access_policy" {
    for_each = var.access_policies
    content {
      tenant_id = access_policy.value.tenant_id
      object_id = access_policy.value.object_id

      key_permissions = access_policy.value.key_permissions
      secret_permissions = access_policy.value.secret_permissions
      certificate_permissions = access_policy.value.certificate_permissions
      storage_permissions = access_policy.value.storage_permissions
    }
  }

  lifecycle {
    ignore_changes = [
      access_policy, # allows adding policies out-of-band without flapping
    ]
  }
}
