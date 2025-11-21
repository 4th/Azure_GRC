# 4th.GRC – Terraform Modules  
**Reusable Infrastructure-as-Code Building Blocks for the 4th.GRC Agentic AI Governance Platform**

This directory contains all **Terraform modules** used to provision Azure infrastructure for the 4th.GRC platform.  
These modules are **environment-agnostic**, reusable, and designed following Azure and Terraform best practices.

Environments such as **dev**, **test**, and **prod** import these modules from:

```
infra/terraform/environments/<env>/
```

Each environment composes these modules to provision a complete deployment of the platform.

---

## 📁 Directory Layout

```
infra/terraform/modules/
├── container_app/     # Azure Container Apps (PolicyEngine, Scorecard, etc.)
├── cosmos/            # Cosmos DB (TrustOps scorecard findings store)
├── key_vault/         # Azure Key Vault for secrets & governance
├── resource_group/    # Azure Resource Group per environment
├── storage/           # Storage Account + Blob containers
└── vnet/              # Virtual Network + Subnets
```

Each module includes:

- `main.tf`
- `variables.tf`
- `outputs.tf`
- `README.md`

---

# 🔧 Module Summary

## `resource_group/`
Creates the Azure Resource Group.

## `vnet/`
Creates VNet + subnets for apps and data.

## `key_vault/`
Creates Azure Key Vault for secrets.

## `storage/`
Creates Storage Account & Blob containers.

## `cosmos/`
Deploys Cosmos DB SQL API.

## `container_app/`
Deploys Azure Container App (PolicyEngine or Scorecard).

---

# 🧩 How Environments Use These Modules

Example usage is shown inside:

```
infra/terraform/environments/dev/main.tf
```

---

# 📝 Conventions

- Providers defined at environment level  
- `name_prefix` used for naming consistency  
- Tags propagated through `local.tags`  
- Modules are stateless and reusable  

---

# 🧭 Extending the Library

Future modules may include:

- ACR
- Private Endpoints
- API Management
- Log Analytics Workspace
- Application Insights
