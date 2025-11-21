// infra/terraform/environments/dev/main.tf
// 4th.GRC – dev environment

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.116"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Optional: configure backend here or in backend.tf
  # backend "azurerm" {}
}

provider "azurerm" {
  features {}
}

provider "random" {}

# -------------------------------------------------------------------
# Context / locals
# -------------------------------------------------------------------

locals {
  env           = var.environment_name
  name_prefix   = "${var.name_prefix}-${local.env}"   # e.g. 4th-grc-dev
  location      = var.location
  tags = merge(
    {
      "project"     = "4th.GRC"
      "environment" = local.env
      "owner"       = var.owner
    },
    var.extra_tags
  )
}

# -------------------------------------------------------------------
# Resource Group
# -------------------------------------------------------------------

module "resource_group" {
  source = "../../modules/resource_group"

  name     = var.resource_group_name
  location = local.location
  tags     = local.tags
}

# -------------------------------------------------------------------
# Network (optional / minimal)
# -------------------------------------------------------------------

module "network" {
  source = "../../modules/network"

  name_prefix      = local.name_prefix
  location         = local.location
  resource_group   = module.resource_group.name
  vnet_cidr        = var.vnet_cidr
  subnet_cidrs     = var.subnet_cidrs
  tags             = local.tags
}

# -------------------------------------------------------------------
# Azure Container Registry (ACR)
# -------------------------------------------------------------------

module "acr" {
  source = "../../modules/acr"

  name_prefix    = local.name_prefix
  location       = local.location
  resource_group = module.resource_group.name

  sku  = var.acr_sku
  tags = local.tags
}

# -------------------------------------------------------------------
# Log Analytics + Container Apps Environment
# -------------------------------------------------------------------

module "containerapps_env" {
  source = "../../modules/containerapps_env"

  name_prefix    = local.name_prefix
  location       = local.location
  resource_group = module.resource_group.name

  log_analytics_sku = var.log_analytics_sku
  tags              = local.tags
}

# -------------------------------------------------------------------
# Key Vault (for secrets, connection strings, etc.)
# -------------------------------------------------------------------

module "keyvault" {
  source = "../../modules/keyvault"

  name_prefix    = local.name_prefix
  location       = local.location
  resource_group = module.resource_group.name

  tenant_id                   = data.azurerm_client_config.current.tenant_id
  enabled_for_deployment      = true
  enabled_for_template_deploy = true
  tags                        = local.tags
}

data "azurerm_client_config" "current" {}

# -------------------------------------------------------------------
# Cosmos DB (optional – TrustOps findings, etc.)
# -------------------------------------------------------------------

module "cosmos" {
  source = "../../modules/cosmos"

  enable        = var.enable_cosmos
  name_prefix   = local.name_prefix
  location      = local.location
  resource_group = module.resource_group.name

  cosmos_sku    = var.cosmos_sku
  tags          = local.tags
}

# -------------------------------------------------------------------
# PolicyEngine – Azure Container App
# -------------------------------------------------------------------

module "policyengine_app" {
  source = "../../modules/policyengine_app"

  name_prefix       = local.name_prefix
  location          = local.location
  resource_group    = module.resource_group.name
  containerapps_env = module.containerapps_env.environment_id

  container_image   = "${module.acr.login_server}/policyengine-svc:${var.default_image_tag}"
  target_port       = 8080
  min_replicas      = var.policyengine_min_replicas
  max_replicas      = var.policyengine_max_replicas

  # Example env vars (wire to Key Vault / Cosmos / etc.)
  environment_variables = {
    "ENVIRONMENT"        = local.env
    "LOG_LEVEL"          = "info"
    "COSMOS_ENDPOINT"    = module.cosmos.endpoint
    "COSMOS_DB_NAME"     = module.cosmos.database_name
    "COSMOS_CONTAINER"   = module.cosmos.container_name
  }

  tags = local.tags
}

# -------------------------------------------------------------------
# Scorecard – Azure Container App (Streamlit)
# -------------------------------------------------------------------

module "scorecard_app" {
  source = "../../modules/scorecard_app"

  enable           = var.enable_scorecard
  name_prefix      = local.name_prefix
  location         = local.location
  resource_group   = module.resource_group.name
  containerapps_env = module.containerapps_env.environment_id

  container_image  = "${module.acr.login_server}/scorecard-app:${var.default_image_tag}"
  target_port      = 8501
  min_replicas     = var.scorecard_min_replicas
  max_replicas     = var.scorecard_max_replicas

  environment_variables = {
    "ENVIRONMENT"        = local.env
    "LOG_LEVEL"          = "info"
    "POLICYENGINE_URL"   = module.policyengine_app.url
  }

  tags = local.tags
}
