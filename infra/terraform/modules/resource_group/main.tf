// infra/terraform/modules/resource_group/main.tf
// 4th.GRC – Resource Group module

resource "azurerm_resource_group" "this" {
  name     = var.name
  location = var.location
  tags     = var.tags
}
