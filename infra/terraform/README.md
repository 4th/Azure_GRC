# 4th.GRC Terraform Infrastructure

This directory contains all Terraform configurations used to deploy the **4th.GRC Agentic AI Governance Platform** onto Azure. It includes reusable modules, environment-specific stacks, remote state configuration, and deployment workflows aligned with enterprise IaC best practices.

---

## 📁 Directory Structure

```
infra/
  terraform/
  │
  ├── modules/            # Reusable Terraform modules (Cosmos, Storage, Container Apps, Key Vault, VNet, etc.)
  │   ├── container_app/
  │   ├── cosmos/
  │   ├── key_vault/
  │   ├── storage/
  │   └── vnet/
  │
  ├── environments/       # Environment-specific deployments (dev/staging/prod/etc.)
  │   ├── dev/
  │   │   ├── main.tf
  │   │   ├── variables.tf
  │   │   ├── outputs.tf
  │   │   └── dev.tfvars
  │   ├── staging/
  │   └── prod/
  │
  └── README.md           # This file
```

---

## 🚀 Purpose of This Terraform Layer

Terraform in 4th.GRC provisions:

- Azure Resource Groups  
- Azure Container Apps (PolicyEngine + Scorecard)  
- Azure Cosmos DB (NoSQL API)  
- Azure Storage / ADLS Gen2 for Policy Profiles + Rule Registries  
- Azure Key Vault (for secrets + OpenAI keys)  
- Log Analytics Workspace + Diagnostic Settings  
- Virtual Networks + Private Endpoints (optional)  
- Identity + Managed Identity bindings  
- Any future compute (AKS, App Service, Functions)

All environments—**dev**, **staging**, **prod**—are fully reproducible.

---

## 🧱 Environment Folders

Each environment gets its own folder under `environments/`.

Example for `dev`:

```
infra/terraform/environments/dev/
  main.tf          # calls modules
  variables.tf     # declares variables for this environment
  outputs.tf       # exports values (URLs, endpoints, IDs)
  dev.tfvars       # actual values for this env
```

Use additional envs simply by creating new folders:

```
environments/
  dev/
  staging/
  prod/
  demo/
  perf/
```

---

## ⚙️ How to Deploy (Local)

### 1. Log into Azure

```powershell
az login
az account set --subscription "<YOUR_SUBSCRIPTION_ID>"
```

### 2. Switch to your environment folder

```powershell
cd infra/terraform/environments/dev
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Plan changes

```bash
terraform plan -var-file="dev.tfvars"
```

### 5. Apply (deploy resources)

```bash
terraform apply -auto-approve -var-file="dev.tfvars"
```

---

## 🔄 Remote State (Recommended)

For production workflows, configure remote state:

Example `backend` block:

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "4th-grc-tfstate-rg"
    storage_account_name = "4thgrctfstate"
    container_name       = "tfstate"
    key                  = "dev.terraform.tfstate"
  }
}
```

This prevents state drift and allows CI/CD to perform deployments safely.

---

## 🔐 Secrets Management

Terraform should **never** store secrets directly.

Use:

### ✔ Azure Key Vault for runtime secrets
- Cosmos DB keys  
- Storage keys/SAS tokens  
- Azure OpenAI API keys  
- Application secrets  

### ✔ GitHub Actions secrets for CI/CD authentication
- `AZURE_CREDENTIALS`  
- `CONTAINER_REGISTRY`  
- `ACR_USERNAME`, `ACR_PASSWORD`  
- `AZURE_RESOURCE_GROUP`

Terraform modules should reference Key Vault where possible and inject secret names (not values) into the container apps.

---

## 🏗 Modules Overview

### `container_app/`
Creates Azure Container Apps for:
- PolicyEngine
- Scorecard
- Agentic runners (future)

### `cosmos/`
Provisions Cosmos DB + collections (findings, runs, system state).

### `storage/`
Creates Storage Account + ADLS Gen2 containers:
- `/profiles/`
- `/rules/`
- `/audit/`

### `key_vault/`
Creates Key Vault + access policies.

### `vnet/`
Optional networking + private endpoints.

---

## 🤖 CI/CD Integration

GitHub Actions workflows live under:

```
infra/pipelines/github-actions/
```

The primary files are:

- `infra_plan_apply.yml` → plans/applies Terraform  
- `deploy_policyengine.yml` → builds & deploys container  
- `deploy_scorecard.yml` → same for Scorecard  

These workflows assume this Terraform structure, with dev deployed automatically when changes hit `main`.

---

## 📦 Example dev.tfvars

Below is a typical `dev.tfvars` file:

```hcl
environment          = "dev"
location             = "eastus"
resource_group_name  = "4th-grc-dev-rg"

policyengine_name    = "policyengine-svc"
scorecard_name       = "scorecard-app"

cosmos_db_name       = "trustops-db"
storage_account_name = "4thgrcdevstore"
key_vault_name       = "4th-grc-dev-kv"
```

---

## 🧹 Naming Conventions

All Terraform resources use these conventions:

- Resource Group: `4th-grc-<env>-rg`
- Storage Account: `4thgrc<env>store`
- Key Vault: `4th-grc-<env>-kv`
- Cosmos: `4thgrc-<env>-cosmos`
- Container Apps:
  - `policyengine-svc`
  - `scorecard-app`

---

## 📘 Best Practices

- Use **one tfstate per environment**  
- Use **remote state** in Azure Storage  
- Never store secrets in `.tfvars`  
- Make all modules **stateless, reusable**  
- Generate all infra via CI/CD, not manually

---

## 👤 Maintainer

**Dr. Freeman A. Jackson**  
Fourth Industrial Systems (4th) – 4th.GRC™ Agentic Governance Platform  
