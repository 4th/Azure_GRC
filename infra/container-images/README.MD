\# 4th.GRC Container Images



This directory contains all container images used across the \*\*4th.GRC Agentic AI Governance Platform\*\*.  

It serves as the unified home for Dockerfiles, deployment specs, and documentation for each service deployed to Azure Container Apps, Kubernetes, or any container-based runtime.



---



\## 📦 Purpose of This Directory



The `infra/container-images/` directory centralizes:



\- \*\*Production Dockerfiles\*\*  

\- \*\*Container App deployment templates\*\* (e.g., Azure Container Apps YAML)

\- \*\*Image-specific environment variables and runtime configuration\*\*

\- \*\*Documentation for how to build, run, and release each image\*\*

\- \*\*Standards for image naming, tagging, and CI/CD integration\*\*



Each subfolder represents one deployable microservice in the 4th.GRC architecture.



---



\## 📁 Directory Structure



```

infra/

&nbsp; container-images/

&nbsp;   README.md                <-- You are here

&nbsp;   .dockerignore            <-- Shared ignore rules (recommended)

&nbsp;   policyengine-svc/        <-- PolicyEngine service image

&nbsp;   scorecard-app/           <-- TrustOps Scorecard UI image

&nbsp;   (future services)/

&nbsp;       agent-runner/

&nbsp;       audit-worker/

```



---



\## 🧩 Image Naming Standards



Images follow the naming pattern:



```

<registry>/<service-name>:<tag>

```



Examples:



\- myregistry.azurecr.io/policyengine-svc:latest

\- myregistry.azurecr.io/scorecard-app:v0.3.0



---



\## 🏗 How Images Are Built



All builds are triggered via:



```

infra/scripts/build\_and\_push\_images.sh

```



Example:



```bash

bash infra/scripts/build\_and\_push\_images.sh policyengine-svc myregistry.azurecr.io v0.1.0

```



This script:



1\. Selects the correct Dockerfile based on the service folder  

2\. Builds the container image  

3\. Pushes the image to Azure Container Registry (or Docker Hub)



The GitHub Actions workflows:



\- infra/pipelines/github-actions/deploy\_policyengine.yml

\- infra/pipelines/github-actions/deploy\_scorecard.yml



use the same script for automated CI/CD builds.



---



\## 🏗 Folder Requirements



Every image folder (e.g., `policyengine-svc/`) must include:



\### \*\*1. Dockerfile\*\*

Production-ready build instructions.



\### \*\*2. containerapp.yaml\*\*

Deployment spec for Azure Container Apps (or Kubernetes manifest if applicable).



\### \*\*3. README.md\*\*

Documentation for:



\- Local development builds  

\- Runtime configuration  

\- Required environment variables  

\- Deployment workflow  



---



\## 🧹 Recommended `.dockerignore`



Place this at:



```

infra/container-images/.dockerignore

```



Contents:



```

.git

.venv

\_\_pycache\_\_

\*.pyc

.mypy\_cache

.pytest\_cache

.DS\_Store

.vscode

.idea

.env

site/

dist/

build/

```



---



\## 🚀 Adding a New Containerized Service



To add a new service, create:



```

infra/container-images/<service-name>/

&nbsp;   Dockerfile

&nbsp;   containerapp.yaml

&nbsp;   README.md

```



And update:



\- infra/scripts/build\_and\_push\_images.sh  

\- CI/CD pipelines under infra/pipelines/github-actions/



---



\## 🔗 Related Documentation



\- PolicyEngine Service → infra/container-images/policyengine-svc/README.md  

\- Scorecard App → infra/container-images/scorecard-app/README.md  

\- Infrastructure Scripts → infra/scripts/README.md  

\- Terraform Environments → infra/terraform/README.md  



---



\## 🧭 Summary



This directory ensures that all 4th.GRC services:



\- Build consistently  

\- Deploy predictably  

\- Follow the same DevOps, tagging, and security practices  

\- Integrate cleanly with Terraform and GitHub Actions  



If you'd like, I can automatically generate `.dockerignore`, update your build scripts, or create a template for new service folders.



