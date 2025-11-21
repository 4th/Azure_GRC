\# 4th.GRC – Terraform Dev Environment (`dev/`)



This directory defines the complete \*\*Development (Dev)\*\* environment infrastructure for the \*\*4th.GRC Agentic AI Governance Platform\*\*.  

It uses Terraform to deploy Azure resources that support:



\- \*\*PolicyEngine Service\*\* (FastAPI microservice)

\- \*\*TrustOps Scorecard App\*\* (Streamlit)

\- \*\*Profiles / Rules / Policy-as-Code\*\*

\- \*\*Cosmos DB Findings Storage\*\*

\- \*\*Azure Container Apps Environment\*\*

\- \*\*Azure Container Registry (ACR)\*\*

\- \*\*Networking + Observability\*\*



The Dev environment is designed to be \*\*reproducible\*\*, \*\*disposable\*\*, and \*\*safe for experimentation\*\*.



---



\## 📁 Directory Structure



```

dev/

├── main.tf

├── variables.tf

├── locals.tf

├── outputs.tf

├── dev.tfvars

└── README.md

```



---



\## 🚀 Deployment



\### 1. Init Terraform

```

terraform init

```



\### 2. Validate

```

terraform validate

```



\### 3. Plan

```

terraform plan -var-file="dev.tfvars"

```



\### 4. Apply

```

terraform apply -var-file="dev.tfvars"

```



---



\## 🧹 Destroy

```

terraform destroy -var-file="dev.tfvars"

```



---



\## 🔧 File Purposes



\### main.tf

Defines Azure resources:

\- Resource Group

\- vNet + Subnets

\- Log Analytics

\- ACR

\- Cosmos (optional)

\- Container Apps Environment

\- PolicyEngine \& Scorecard Apps



\### variables.tf

Input parameters:

\- Region

\- Resource group

\- CIDRs

\- Toggles

\- Scaling

\- Image tags



\### locals.tf

Naming + standard tags.



\### outputs.tf

Exports env results for CI/CD.



\### dev.tfvars

Actual Dev values.



---



\## 🔄 CI/CD



Used by:

\- GitHub Actions → `infra\_plan\_apply.yml`

\- Azure DevOps → `terraform-ci.yml`



---



\## 🎯 Purpose of Dev



\- Safe testing  

\- Infrastructure validation  

\- PolicyEngine rule development  

\- Scorecard UI testing  

\- Cosmos DB experiment  



Not production.





