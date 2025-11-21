# 4th.GRC – Infrastructure Layer  
**Infrastructure-as-Code (IaC) for the 4th.GRC Agentic AI Governance Platform**

This directory contains all infrastructure assets required to deploy the full 4th.GRC platform across development, testing, staging, and production environments.

Terraform is the authoritative IaC source of truth, with Bicep retained only for optional or legacy bootstrap templates.

---

## 📁 Directory Structure

```
infra/
├── terraform/          # Primary IaC (modules + environments)
├── bicep/              # Optional legacy Bicep templates
├── pipelines/          # CI/CD (GitHub Actions + Azure DevOps)
├── container-images/   # Docker build contexts
└── scripts/            # Infra automation scripts
```

---

## 🚀 Terraform (Source of Truth)

Terraform manages:

- Resource Groups  
- VNets  
- Key Vault  
- Storage  
- Cosmos DB  
- Container Apps  
- Future services (ACR, APIM, Log Analytics, etc.)

Modules live in:

```
infra/terraform/modules/
```

Environments (dev/test/prod) live in:

```
infra/terraform/environments/<env>/
```

---

## 🔄 Pipelines

Automation is provided via:

```
infra/pipelines/github-actions/
infra/pipelines/azure-devops/
```

Tasks include:

- Terraform validate/plan/apply
- Build/push container images
- Deploy PolicyEngine & Scorecard
- Sync profiles
- Rotate secrets

---

## 🧰 Scripts

Found in:

```
infra/scripts/
```

These provide:

- Local deployment automation
- Environment teardown
- Image building
- Secret rotation stubs
- Profile syncing

---

## 📦 Container Images

Docker build contexts for:

- PolicyEngine service  
- Scorecard application  

Located in:

```
infra/container-images/
```

---

## 📝 Bicep (Optional)

```
infra/bicep/
└── bootstrap.bicep
```

Bicep templates are **not** used in production deployments but kept for reference.

---

## ✔ Summary

The `infra/` directory defines the entire infrastructure lifecycle for 4th.GRC using:

- Terraform (primary IaC)
- Modular architecture
- CI/CD pipelines
- Automated scripts
- Clear environment separation

This supports repeatability, auditability, compliance, and future scalability.

