# 4th.GRC – `storage` Module

Terraform module for provisioning an **Azure Storage Account** for the 4th.GRC platform.

Used for:

- Profile/rule archives
- Exported findings (CSV/JSON)
- Static assets and logs
- General-purpose data storage

## Features

- Consistent naming based on `name_prefix`
- Configurable SKU and replication
- Optional creation of standard containers
- Exposes endpoints and connection string for apps/scripts

## Inputs

| Name                     | Type        | Default   | Description |
|--------------------------|-------------|-----------|-------------|
| `name_prefix`           | string      | n/a       | Base prefix (`4th-grc-dev`) used to derive storage account name |
| `location`              | string      | n/a       | Azure region |
| `resource_group`        | string      | n/a       | Resource group name |
| `tags`                  | map(string) | `{}`      | Tags applied to the storage account |
| `account_tier`          | string      | `Standard`| Account tier (Standard/Premium) |
| `replication_type`      | string      | `LRS`     | Replication type (LRS, GRS, ZRS, etc.) |
| `allow_blob_public_access` | bool     | `false`   | Whether to allow public blob access |
| `containers`            | map(object) | `{}`      | Optional containers to create |

`containers` object:

```hcl
containers = {
  findings = {
    name        = "findings-exports"
    access_type = "private"
  }
}
