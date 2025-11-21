# 4th.GRC – `key_vault` Module

Terraform module for provisioning an **Azure Key Vault** for the 4th.GRC platform.

Used by each environment (`dev`, `test`, `prod`) to:

- Store secrets (Cosmos keys, connection strings, API keys)
- Support rotation scripts (e.g., `infra/scripts/rotate_secrets_stub.py`)
- Centralize sensitive configuration away from code

## Features

- Stable naming via `name_prefix` (e.g., `4th-grc-dev-kv`)
- Soft delete + purge protection enabled by default
- Optional access policies list
- Simple network ACLs (open by default; tighten for prod)

## Inputs

| Name                       | Type        | Default      | Description |
|----------------------------|-------------|--------------|-------------|
| `name_prefix`              | string      | n/a          | Base name prefix (`4th-grc-dev`) |
| `location`                 | string      | n/a          | Azure region |
| `resource_group`           | string      | n/a          | Resource group name |
| `tenant_id`                | string      | n/a          | Azure AD tenant ID |
| `tags`                     | map(string) | `{}`         | Tags applied to the vault |
| `sku_name`                 | string      | `standard`   | Key Vault SKU |
| `soft_delete_retention_days` | number    | `90`         | Soft delete retention period |
| `purge_protection_enabled` | bool        | `true`       | Enable purge protection |
| `enabled_for_deployment`   | bool        | `false`      | VM deployment access |
| `enabled_for_disk_encryption` | bool     | `false`      | Disk encryption access |
| `enabled_for_template_deployment` | bool | `true`      | ARM/Bicep template access |
| `network_default_action`   | string      | `Allow`      | Default network action |
| `network_bypass`           | string      | `AzureServices` | Network bypass mode |
| `access_policies`          | list(object)| `[]`         | Optional access policies |

## Outputs

| Name       | Description                              |
|------------|------------------------------------------|
| `name`     | Key Vault name                           |
| `id`       | Resource ID                              |
| `vault_uri`| DNS URI (e.g., `https://name.vault.azure.net/`) |

## Example Usage (Dev)

```hcl
data "azurerm_client_config" "current" {}

module "key_vault" {
  source        = "../../modules/key_vault"
  name_prefix   = local.name_prefix
  location      = local.location
  resource_group = module.resource_group.name
  tenant_id     = data.azurerm_client_config.current.tenant_id

  tags = local.tags

  # Optionally add policies for a managed identity, SP, or user
  access_policies = [
    {
      tenant_id  = data.azurerm_client_config.current.tenant_id
      object_id  = data.azurerm_client_config.current.object_id

      key_permissions         = ["Get", "List"]
      secret_permissions      = ["Get", "List", "Set"]
      certificate_permissions = []
      storage_permissions     = []
    }
  ]
}
