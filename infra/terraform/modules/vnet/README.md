# 4th.GRC – `vnet` Module

Terraform module for provisioning an **Azure Virtual Network + Subnets** for 4th.GRC environments.

## Features

- Single VNet per environment
- Subnets defined via a simple map
- Standard naming: `<name_prefix>-vnet`
- Outputs subnet IDs for use by other modules

## Inputs

| Name           | Type        | Required | Description |
|----------------|-------------|----------|-------------|
| `name_prefix`  | string      | ✅       | Base prefix (e.g. `4th-grc-dev`) |
| `location`     | string      | ✅       | Azure region |
| `resource_group` | string    | ✅       | Resource group name |
| `tags`         | map(string) | ❌       | Tags for the VNet |
| `vnet_cidr`    | string      | ✅       | VNet CIDR (e.g. `10.10.0.0/16`) |
| `subnet_cidrs` | map(string) | ✅       | Map of subnet name → CIDR |

Example `subnet_cidrs`:

```hcl
subnet_cidrs = {
  apps = "10.10.1.0/24"
  data = "10.10.2.0/24"
}
