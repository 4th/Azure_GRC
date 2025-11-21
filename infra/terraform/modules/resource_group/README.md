# 4th.GRC – `resource_group` Module

Simple Terraform module that creates an **Azure Resource Group** for a 4th.GRC environment.

## Inputs

| Name       | Type        | Required | Description                          |
|------------|-------------|----------|--------------------------------------|
| `name`     | string      | ✅       | Resource group name                  |
| `location` | string      | ✅       | Azure region (e.g., `eastus`)       |
| `tags`     | map(string) | ❌       | Tags applied to the resource group   |

## Outputs

| Name       | Description                          |
|------------|--------------------------------------|
| `name`     | Name of the resource group           |
| `id`       | Resource ID of the resource group    |
| `location` | Location of the resource group       |

## Example Usage (Dev Environment)

```hcl
module "resource_group" {
  source   = "../../modules/resource_group"
  name     = var.resource_group_name
  location = var.location
  tags     = local.tags
}
