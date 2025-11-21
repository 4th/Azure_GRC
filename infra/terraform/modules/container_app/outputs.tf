// infra/terraform/modules/container_app/outputs.tf

output "name" {
  description = "Name of the Container App."
  value       = azurerm_container_app.this.name
}

output "id" {
  description = "Resource ID of the Container App."
  value       = azurerm_container_app.this.id
}

output "url" {
  description = "Ingress FQDN (URL) of the Container App, if external ingress is enabled."
  value       = azurerm_container_app.this.ingress[0].fqdn
}

output "revision" {
  description = "Current active revision of the Container App."
  value       = azurerm_container_app.this.latest_revision_name
}
