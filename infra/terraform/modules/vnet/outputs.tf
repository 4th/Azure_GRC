// infra/terraform/modules/vnet/outputs.tf

output "vnet_id" {
  description = "Resource ID of the virtual network."
  value       = azurerm_virtual_network.this.id
}

output "vnet_name" {
  description = "Name of the virtual network."
  value       = azurerm_virtual_network.this.name
}

output "subnet_ids" {
  description = "Map of subnet names to their resource IDs."
  value       = { for name, s in azurerm_subnet.this : name => s.id }
}

output "subnet_names" {
  description = "Map of subnet keys to subnet names."
  value       = { for name, s in azurerm_subnet.this : name => s.name }
}
