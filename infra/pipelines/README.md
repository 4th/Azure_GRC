\# 4th.GRC – Infrastructure Pipelines  

Centralized CI/CD pipelines for deploying the 4th.GRC platform



The `infra/pipelines/` directory contains all automation pipelines used for deploying:



\- Infrastructure (Terraform)

\- Application containers (PolicyEngine, Scorecard, future agents)

\- Azure resources (Container Apps, ACR, networking, storage)

\- DevOps automation for dev and prod environments  

\- Modular template-based pipeline structure for Azure DevOps \& GitHub Actions



This folder provides the \*\*enterprise CI/CD backbone\*\* for the 4th.GRC platform.



---



\## 📁 Directory Structure



```

infra/pipelines/

│

├── azure-devops/                     # Azure DevOps pipeline implementations

│   ├── deploy-policyengine.yml       # Deploy PolicyEngine to ACA

│   ├── deploy-scorecard.yml          # Deploy Scorecard to ACA

│   ├── terraform-ci.yml              # Terraform validate/plan/apply

│   └── templates/                    # Reusable pipeline templates

│       ├── jobs-containerapp.yml

│       ├── jobs-docker-build.yml

│       ├── jobs-terraform.yml

│       ├── variables-dev.yml

│       ├── variables-prod.yml

│       └── README.md

│

├── github-actions/                   # (Optional) GitHub Actions workflows

│   ├── deploy\_policyengine.yml

│   ├── deploy\_scorecard.yml

│   └── infra\_plan\_apply.yml

│

└── README.md                         # This file

```



---



\# 🎯 Purpose of This Folder



This folder ensures CI/CD for 4th.GRC is:



\- \*\*Consistent\*\* — shared templates eliminate duplicated YAML

\- \*\*Composable\*\* — reuse jobs across services (build, deploy, terraform, test)

\- \*\*Environment-aware\*\* — dev, staging, and prod variable templates

\- \*\*Cloud-aligned\*\* — designed for \*\*Azure Container Apps\*\* + \*\*Terraform\*\*

\- \*\*Enterprise-ready\*\* — supports PR validation, gated applies, audit logs



---



\# 📦 Pipeline Categories



\## 1. \*\*Application Deployment Pipelines\*\*

Located in:



```

infra/pipelines/azure-devops/

infra/pipelines/github-actions/

```



These deploy:



\- `policyengine-svc` (FastAPI)

\- `scorecard-app` (Streamlit UI)

\- Future agent services



\### Actions performed:

\- Build Docker image

\- Push to Azure Container Registry (ACR)

\- Deploy/update Azure Container App (ACA)

\- Configure scaling, ports, ingress

\- Environment-specific rollout logic



---



\## 2. \*\*Infrastructure Pipelines (Terraform)\*\*



Located in:



```

infra/pipelines/azure-devops/terraform-ci.yml

```



Provides:



\- Terraform init  

\- Terraform validate  

\- Terraform fmt (optional)  

\- Terraform plan  

\- Terraform apply (main branch only)  

\- Artifact publishing (plans)  



Strongly aligned with:



```

infra/terraform/environments/dev

infra/terraform/environments/prod

```



---



\# 🧱 Template System



Templates live under:



```

infra/pipelines/azure-devops/templates/

```



And include:



\### ✔ jobs-containerapp.yml

Build \& deploy Azure Container App.



\### ✔ jobs-docker-build.yml

Build \& push Docker images.



\### ✔ jobs-terraform.yml

Terraform CI/CD.



\### ✔ variables-dev.yml / variables-prod.yml

Per-environment configuration.



---



\# 🚀 How to Use These Pipelines



\### Add variables for environment:



```yaml

variables:

\- template: templates/variables-dev.yml

```



\### Add Docker build job:



```yaml

\- template: templates/jobs-docker-build.yml

&nbsp; parameters:

&nbsp;   imageName: 'policyengine-svc'

```



\### Add Container App deploy job:



```yaml

\- template: templates/jobs-containerapp.yml

&nbsp; parameters:

&nbsp;   containerAppName: 'policyengine-svc'

```



\### Add Terraform stage:



```yaml

\- template: templates/jobs-terraform.yml

&nbsp; parameters:

&nbsp;   environmentName: 'dev'

```



---



\# 🏁 Summary



The `infra/pipelines/` folder provides:



\- \*\*Unified\*\* CI/CD for all components  

\- \*\*Template-driven deployments\*\*  

\- \*\*Environment-specific lifecycle automation\*\*  

\- \*\*Enterprise-grade Azure DevOps patterns\*\*  

\- \*\*Extendable structure for future microservices\*\*  





