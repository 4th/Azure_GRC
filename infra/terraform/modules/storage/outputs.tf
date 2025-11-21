// infra/terraform/modules/storage/outputs.tf

output "account_name" {
  description = "Name of the storage account."
  value       = azurerm_storage_account.this.name
}

output "account_id" {
  description = "Resource ID of the storage account."
  value       = azurerm_storage_account.this.id
}

output "primary_endpoint_blob" {
  description = "Primary blob endpoint URL."
  value       = azurerm_storage_account.this.primary_blob_endpoint
}

output "primary_connection_string" {
  description = "Primary connection string for the storage account."
  value       = azurerm_storage_account.this.primary_connection_string
  sensitive   = true
}

output "container_names" {
  description = "Map of container keys to their names."
  value       = { for k, c in azurerm_storage_container.containers : k => c.name }
}
