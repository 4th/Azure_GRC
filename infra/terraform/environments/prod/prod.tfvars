# -------------------------------------------------------------------
# Core environment settings
# -------------------------------------------------------------------

environment_name   = "dev"
location           = "eastus"

# Base prefix for all names in this environment (combined with env)
# e.g. 4th-grc-dev-aca, 4th-grc-dev-acr, etc.
name_prefix        = "4th-grc"

# Explicit resource group name for dev
resource_group_name = "rg-4th-grc-dev"

# Owner / contact tag
owner = "Fourth Industrial Systems – Dev"

# Extra tags applied to all resources
extra_tags = {
  "cost-center" = "R&D"
  "app"         = "4th.GRC"
}

# -------------------------------------------------------------------
# Networking
# -------------------------------------------------------------------

# Virtual network and subnets for Container Apps, data, etc.
vnet_cidr = "10.20.0.0/16"

subnet_cidrs = {
  "aca_apps"  = "10.20.1.0/24"
  "data"      = "10.20.2.0/24"
  "mgmt"      = "10.20.3.0/24"
}

# -------------------------------------------------------------------
# ACR (Azure Container Registry)
# -------------------------------------------------------------------

acr_sku = "Basic"   # Basic | Standard | Premium

# -------------------------------------------------------------------
# Log Analytics / Observability
# -------------------------------------------------------------------

log_analytics_sku = "PerGB2018"

# -------------------------------------------------------------------
# Cosmos DB (TrustOps findings, etc.)
# -------------------------------------------------------------------

enable_cosmos = true
cosmos_sku    = "Standard"  # or "Autoscale"

# -------------------------------------------------------------------
# Workload toggles
# -------------------------------------------------------------------

enable_scorecard = true     # Allow turning Scorecard off in some envs

# -------------------------------------------------------------------
# Container images & scaling
# -------------------------------------------------------------------

# Default tag used for images if CI/CD doesn't override it
# In CI, you might override with the commit SHA or a release tag.
default_image_tag = "dev"

# PolicyEngine scaling (Azure Container Apps)
policyengine_min_replicas = 1
policyengine_max_replicas = 2

# Scorecard scaling (Streamlit UI)
scorecard_min_replicas = 1
scorecard_max_replicas = 2
