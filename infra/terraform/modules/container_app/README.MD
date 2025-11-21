# 4th.GRC – `container_app` Module

Generic Azure Container App module used by 4th.GRC to deploy:

- PolicyEngine service (FastAPI)
- TrustOps Scorecard app (Streamlit)
- Future agentic services

## Inputs

| Name                 | Type         | Required | Description |
|----------------------|-------------|----------|-------------|
| `name`               | string      | ✅       | Container App name |
| `location`           | string      | ✅       | Azure region |
| `resource_group`     | string      | ✅       | Resource group name |
| `containerapps_env_id` | string    | ✅       | Container Apps Environment ID |
| `container_image`    | string      | ✅       | Fully qualified container image |
| `target_port`        | number      | ✅       | Port exposed by the container |
| `min_replicas`       | number      | ❌ (1)   | Minimum replicas |
| `max_replicas`       | number      | ❌ (2)   | Maximum replicas |
| `cpu`                | number      | ❌ (0.5) | CPU cores |
| `memory`             | string      | ❌ ("1.0Gi") | Memory |
| `ingress_external`   | bool        | ❌ (true) | External ingress |
| `ingress_allow_insecure` | bool   | ❌ (false) | Allow HTTP as well as HTTPS |
| `environment_variables` | map(string) | ❌ ({}) | Environment variables |
| `tags`               | map(string) | ❌ ({})  | Resource tags |

## Outputs

| Name       | Description                              |
|------------|------------------------------------------|
| `name`     | Container App name                       |
| `id`       | Resource ID                              |
| `url`      | Ingress FQDN (if external ingress)       |
| `revision` | Latest revision name                     |

## Example Usage (PolicyEngine)

```hcl
module "policyengine_app" {
  source               = "../../modules/container_app"
  name                 = "${local.name_prefix}-policyengine"
  location             = local.location
  resource_group       = module.resource_group.name
  containerapps_env_id = module.containerapps_env.environment_id

  container_image = "${module.acr.login_server}/policyengine-svc:${var.default_image_tag}"
  target_port     = 8080

  min_replicas = var.policyengine_min_replicas
  max_replicas = var.policyengine_max_replicas

  environment_variables = {
    ENVIRONMENT      = local.env
    LOG_LEVEL        = "info"
    COSMOS_ENDPOINT  = try(module.cosmos.endpoint, null)
    COSMOS_DB_NAME   = try(module.cosmos.database_name, null)
    COSMOS_CONTAINER = try(module.cosmos.container_name, null)
  }

  tags = local.tags
}
