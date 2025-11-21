// infra/terraform/modules/storage/main.tf
// Azure Storage Account for 4th.GRC

locals {
  storage_account_name = lower(replace(substr("${var.name_prefix}stg", 0, 24), "-", ""))
}

resource "azurerm_storage_account" "this" {
  name                     = local.storage_account_name
  resource_group_name      = var.resource_group
  location                 = var.location
  account_tier             = var.account_tier
  account_replication_type = var.replication_type

  allow_blob_public_access = var.allow_blob_public_access
  min_tls_version          = "TLS1_2"

  tags = var.tags
}

# Optional: create some standard containers if requested
resource "azurerm_storage_container" "containers" {
  for_each = var.containers

  name                  = each.value.name
  storage_account_name  = azurerm_storage_account.this.name
  container_access_type = each.value.access_type
}
