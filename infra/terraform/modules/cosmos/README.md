# 4th.GRC – `cosmos` Module

Terraform module for provisioning **Azure Cosmos DB** for the 4th.GRC platform:

- Cosmos DB account
- SQL database
- SQL container for TrustOps / findings data

## Features

- Toggle with `enable` (true/false)
- Sensible defaults:
  - Database: `trustops-db`
  - Container: `findings`
  - Partition key: `/profile_id`
  - Throughput: `400` RU/s
- Exposes endpoint + names as outputs for apps and scripts.

## Inputs

| Name              | Type        | Default        | Description |
|-------------------|-------------|----------------|-------------|
| `enable`          | bool        | `true`         | Whether to create Cosmos resources |
| `name_prefix`     | string      | n/a            | Base name prefix (e.g., `4th-grc-dev`) |
| `location`        | string      | n/a            | Azure region |
| `resource_group`  | string      | n/a            | Resource group name |
| `tags`            | map(string) | `{}`           | Tags applied to all resources |
| `database_name`   | string      | `""` → `trustops-db` | Optional override for DB name |
| `container_name`  | string      | `""` → `findings` | Optional override for container name |
| `partition_key_path` | string   | `/profile_id`  | Partition key path |
| `throughput`      | number      | `400`          | Database throughput (RU/s) |

## Outputs

| Name            | Description |
|-----------------|-------------|
| `enabled`       | Whether Cosmos is enabled |
| `account_name`  | Cosmos account name (or null) |
| `endpoint`      | Cosmos endpoint URI (or null) |
| `database_name` | SQL DB name (or null) |
| `container_name`| SQL container name (or null) |

## Example Usage (Dev Environment)

```hcl
module "cosmos" {
  source         = "../../modules/cosmos"
  enable         = var.enable_cosmos
  name_prefix    = local.name_prefix
  location       = local.location
  resource_group = module.resource_group.name

  database_name     = "trustops-db"
  container_name    = "findings"
  partition_key_path = "/profile_id"
  throughput        = 400

  tags = local.tags
}
