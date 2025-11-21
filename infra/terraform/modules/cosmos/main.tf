// infra/terraform/modules/cosmos/main.tf
// Cosmos DB for 4th.GRC – account + SQL DB + container

locals {
  account_name  = lower(replace("${var.name_prefix}-cosmos", "_", "-"))
  database_name = var.database_name != "" ? var.database_name : "trustops-db"
  container_name = var.container_name != "" ? var.container_name : "findings"
}

# Optional toggle – if enable = false, nothing is created
resource "azurerm_cosmosdb_account" "this" {
  count               = var.enable ? 1 : 0
  name                = local.account_name
  location            = var.location
  resource_group_name = var.resource_group

  offer_type = "Standard"
  kind       = "GlobalDocumentDB"

  enable_automatic_failover = false

  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  tags = var.tags
}

resource "azurerm_cosmosdb_sql_database" "this" {
  count               = var.enable ? 1 : 0
  name                = local.database_name
  resource_group_name = var.resource_group
  account_name        = azurerm_cosmosdb_account.this[0].name

  throughput = var.throughput
}

resource "azurerm_cosmosdb_sql_container" "this" {
  count               = var.enable ? 1 : 0
  name                = local.container_name
  resource_group_name = var.resource_group
  account_name        = azurerm_cosmosdb_account.this[0].name
  database_name       = azurerm_cosmosdb_sql_database.this[0].name

  partition_key_paths = [var.partition_key_path]
  partition_key_version = 2

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }

    excluded_path {
      path = "/_etag/?"
    }
  }
}
