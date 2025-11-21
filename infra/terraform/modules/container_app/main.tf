// infra/terraform/modules/container_app/main.tf
// Generic Azure Container App module for 4th.GRC

resource "azurerm_container_app" "this" {
  name                = var.name
  location            = var.location
  resource_group_name = var.resource_group
  container_app_environment_id = var.containerapps_env_id

  tags = var.tags

  revision_mode = "Single"

  template {
    container {
      name   = var.name
      image  = var.container_image
      cpu    = var.cpu
      memory = var.memory

      env {
        # We use dynamic here to loop over environment_variables map
      }

      dynamic "env" {
        for_each = var.environment_variables
        content {
          name  = env.key
          value = env.value
        }
      }
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas
  }

  ingress {
    external_enabled           = var.ingress_external
    target_port                = var.target_port
    transport                  = "auto"
    allow_insecure_connections = var.ingress_allow_insecure

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
