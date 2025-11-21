\# GitHub Actions Workflows – 4th.GRC



This directory contains the \*\*GitHub Actions workflow definitions\*\* for the 4th.GRC Agentic AI Governance Platform.



These YAML files are the CI/CD pipelines that:



\- Run \*\*Terraform plan/apply\*\* for infrastructure.

\- Build and push \*\*container images\*\* (PolicyEngine, Scorecard).

\- Deploy services to \*\*Azure Container Apps\*\* (or other container runtimes).



In most setups, these files are mirrored into the repository’s `.github/workflows/` directory so that GitHub can execute them.



---



\## 📁 Files



\- `infra\_plan\_apply.yml`  

&nbsp; Runs Terraform against the `infra/terraform/environments/dev` stack:

&nbsp; - `terraform init`

&nbsp; - `terraform validate`

&nbsp; - `terraform plan -var-file="dev.tfvars"`

&nbsp; - `terraform apply` on pushes to `main`



\- `deploy\_policyengine.yml`  

&nbsp; Builds and deploys the \*\*PolicyEngine\*\* container image:

&nbsp; - Calls `infra/scripts/build\_and\_push\_images.sh policyengine-svc`

&nbsp; - Pushes to your container registry

&nbsp; - Updates the PolicyEngine deployment (e.g., Azure Container App)



\- `deploy\_scorecard.yml`  

&nbsp; Builds and deploys the \*\*TrustOps Scorecard\*\* (Streamlit) container image:

&nbsp; - Calls `infra/scripts/build\_and\_push\_images.sh scorecard-app`

&nbsp; - Pushes to your container registry

&nbsp; - Updates the Scorecard deployment.



---



\## 🔐 Required GitHub Secrets (Typical)



These workflows assume the following secrets exist in your repository settings:



\- `AZURE\_CREDENTIALS` – JSON for `azure/login` (service principal with access to the subscription / resource group).

\- `CONTAINER\_REGISTRY` – Container registry login server (e.g., `myregistry.azurecr.io`).

\- `ACR\_USERNAME` / `ACR\_PASSWORD` – Registry credentials (if not using managed identity).

\- `AZURE\_RESOURCE\_GROUP` – Name of the resource group where 4th.GRC infra is deployed.



You can extend workflows to include additional secrets and environment variables as needed.



---



\## 🔁 Syncing With .github/workflows



Typical pattern:



1\. Author and maintain workflows here under:



&nbsp;  ```text

&nbsp;  infra/pipelines/github-actions/

&nbsp;  ```



2\. Copy or sync them into:



&nbsp;  ```text

&nbsp;  .github/workflows/

&nbsp;  ```



3\. Trigger workflows via:

&nbsp;  - Pushes to the configured branches

&nbsp;  - Pull requests

&nbsp;  - Manual `workflow\_dispatch`



This keeps \*\*infra\*\* and \*\*CI/CD definitions\*\* co-located while still using GitHub’s standard workflows directory.



---



\## 🔗 Related Directories



\- \*\*Terraform IaC\*\* – `infra/terraform/`

\- \*\*Infra Scripts\*\* – `infra/scripts/`

\- \*\*Container Images\*\* – `infra/container-images/`

\- \*\*Pipelines (overview)\*\* – `infra/pipelines/README.md`



