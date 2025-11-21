// infra/terraform/environments/dev/outputs.tf
// Key outputs for the 4th.GRC dev environment

# -------------------------------------------------------------------
# Core / shared
# -------------------------------------------------------------------

output "environment_name" {
  description = "Logical environment name (e.g., dev, test, prod)."
  value       = var.environment_name
}

output "location" {
  description = "Azure region where the dev environment is deployed."
  value       = var.location
}

output "resource_group_name" {
  description = "Name of the resource group hosting the dev environment."
  value       = module.resource_group.name
}

output "resource_group_id" {
  description = "ID of the resource group hosting the dev environment."
  value       = module.resource_group.id
}

# -------------------------------------------------------------------
# Container Apps Environment
# -------------------------------------------------------------------

output "containerapps_environment_id" {
  description = "Resource ID of the Azure Container Apps Environment."
  value       = module.containerapps_env.environment_id
}

output "containerapps_environment_name" {
  description = "Name of the Azure Container Apps Environment."
  value       = module.containerapps_env.environment_name
}

# -------------------------------------------------------------------
# Azure Container Registry
# -------------------------------------------------------------------

output "acr_login_server" {
  description = "Login server (FQDN) of the Azure Container Registry."
  value       = module.acr.login_server
}

output "acr_name" {
  description = "Name of the Azure Container Registry."
  value       = module.acr.name
}

# -------------------------------------------------------------------
# Key Vault
# -------------------------------------------------------------------

output "keyvault_name" {
  description = "Name of the Azure Key Vault for this environment."
  value       = module.keyvault.name
}

output "keyvault_id" {
  description = "Resource ID of the Azure Key Vault."
  value       = module.keyvault.id
}

# -------------------------------------------------------------------
# Cosmos DB (TrustOps findings, etc.)
# -------------------------------------------------------------------

output "cosmos_enabled" {
  description = "Whether Cosmos DB is enabled for this environment."
  value       = var.enable_cosmos
}

output "cosmos_account_name" {
  description = "Cosmos DB account name (if enabled)."
  value       = module.cosmos.account_name
  condition   = var.enable_cosmos
}

output "cosmos_endpoint" {
  description = "Cosmos DB endpoint URI (if enabled)."
  value       = module.cosmos.endpoint
  condition   = var.enable_cosmos
}

output "cosmos_database_name" {
  description = "Cosmos DB database name (if enabled)."
  value       = module.cosmos.database_name
  condition   = var.enable_cosmos
}

output "cosmos_container_name" {
  description = "Cosmos DB container name (if enabled)."
  value       = module.cosmos.container_name
  condition   = var.enable_cosmos
}

# -------------------------------------------------------------------
# PolicyEngine – Azure Container App
# -------------------------------------------------------------------

output "policyengine_app_name" {
  description = "Name of the PolicyEngine Container App."
  value       = module.policyengine_app.name
}

output "policyengine_url" {
  description = "Public URL (ingress) of the PolicyEngine service, if exposed."
  value       = module.policyengine_app.url
}

# -------------------------------------------------------------------
# Scorecard – Azure Container App (Streamlit)
# -------------------------------------------------------------------

output "scorecard_enabled" {
  description = "Whether the TrustOps Scorecard app is enabled for this environment."
  value       = var.enable_scorecard
}

output "scorecard_app_name" {
  description = "Name of the Scorecard Container App (if enabled)."
  value       = module.scorecard_app.name
  condition   = var.enable_scorecard
}

output "scorecard_url" {
  description = "Public URL of the Scorecard app (if enabled and exposed)."
  value       = module.scorecard_app.url
  condition   = var.enable_scorecard
}
