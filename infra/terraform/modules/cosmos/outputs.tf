// infra/terraform/modules/cosmos/outputs.tf

output "enabled" {
  description = "Whether Cosmos DB is enabled."
  value       = var.enable
}

output "account_name" {
  description = "Cosmos DB account name (null if disabled)."
  value       = try(azurerm_cosmosdb_account.this[0].name, null)
}

output "endpoint" {
  description = "Cosmos DB endpoint URI (null if disabled)."
  value       = try(azurerm_cosmosdb_account.this[0].endpoint, null)
}

output "database_name" {
  description = "Cosmos SQL database name (null if disabled)."
  value       = try(azurerm_cosmosdb_sql_database.this[0].name, null)
}

output "container_name" {
  description = "Cosmos SQL container name (null if disabled)."
  value       = try(azurerm_cosmosdb_sql_container.this[0].name, null)
}
