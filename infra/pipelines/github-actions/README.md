\# GitHub Actions Pipelines – 4th.GRC Infrastructure



This directory contains all CI/CD pipelines used to build, validate, and deploy the 4th.GRC Agentic AI Governance Platform.  

These workflows automate Terraform, container builds, security scans, and environment deployments.



---



\## 📁 Directory Structure



```

infra/

└── pipelines/

&nbsp;   └── github-actions/

&nbsp;       ├── infra\_plan\_apply.yml

&nbsp;       ├── deploy\_policyengine.yml

&nbsp;       ├── deploy\_scorecard.yml

&nbsp;       └── README.md   ← (this file)

```



---



\## 🚀 Purpose of Each Workflow



\### \*\*1. infra\_plan\_apply.yml\*\*

Runs Terraform validation, plan, and apply.



\*\*Triggers\*\*

\- Manual (`workflow\_dispatch`)

\- On pull request (plan only)

\- On push to `main` (apply to dev)



\*\*Stages\*\*

\- `terraform fmt`

\- `terraform validate`

\- `terraform plan`

\- Optional: `terraform apply` to chosen environment



---



\### \*\*2. deploy\_policyengine.yml\*\*

Builds \& deploys the \*\*PolicyEngine FastAPI container app\*\*.



\*\*What it does\*\*

\- Build Docker image

\- Push to Azure Container Registry (ACR)

\- Deploy to Azure Container Apps / Kubernetes



---



\### \*\*3. deploy\_scorecard.yml\*\*

Builds and deploys the \*\*TrustOps Scorecard (Streamlit)\*\* application.



\*\*Pipeline Actions\*\*

\- Install Python deps

\- Build container image

\- Push to ACR

\- Deploy to environment



---



\## 🔐 Secrets You Need in GitHub



Set the following in \*\*GitHub → Settings → Secrets and Variables → Actions\*\*:



\### Terraform / Azure

\- `AZURE\_CREDENTIALS`

\- `ARM\_CLIENT\_CLIENT\_ID`

\- `ARM\_CLIENT\_SECRET`

\- `ARM\_TENANT\_ID`

\- `ARM\_SUBSCRIPTION\_ID`



\### Container Registry

\- `ACR\_LOGIN\_SERVER`

\- `ACR\_USERNAME`

\- `ACR\_PASSWORD`



\### Optional

\- `COSMOS\_KEY`

\- `PROFILES\_BLOB\_ACCOUNT\_URL`



---



\## 🏗 Recommended Branch Strategy



| Branch | Purpose | Pipelines That Run |

|--------|---------|---------------------|

| `feature/\*` | Feature development | Terraform format + validate only |

| `dev` | Dev environment | Full Terraform + deploy to dev |

| `main` | Production | Terraform apply to prod + deployments |



---



\## 🧪 Testing Pipelines Locally



You can lint workflows locally using:



```bash

act -j <job-name>

```



Install `act`:

```bash

choco install act-cli

```



---



\## 📝 Notes



\- These GitHub Actions are safe to extend with additional jobs like security scans (Bandit, Trivy, Snyk).

\- You can also plug in tools like \*\*OpenAI GenAI Security\*\*, \*\*PolicyEngine auto-checks\*\*, or \*\*Cosmos DB verification jobs\*\*.



---



\## 📞 Need More?



I can also generate:

\- \*\*End-to-end CI/CD diagram (Mermaid)\*\*

\- \*\*Organization-wide GitHub repo structure\*\*

\- \*\*Reusable workflow templates\*\*

\- \*\*Environment promotion pipelines (dev → staging → prod)\*\*





