// infra/terraform/modules/vnet/main.tf
// Azure Virtual Network + Subnets for 4th.GRC

resource "azurerm_virtual_network" "this" {
  name                = "${var.name_prefix}-vnet"
  address_space       = [var.vnet_cidr]
  location            = var.location
  resource_group_name = var.resource_group
  tags                = var.tags
}

resource "azurerm_subnet" "this" {
  for_each = var.subnet_cidrs

  name                 = each.key
  resource_group_name  = var.resource_group
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [each.value]
}
