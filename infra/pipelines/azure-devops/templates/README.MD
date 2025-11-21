\# Azure DevOps Pipeline Templates  

Reusable CI/CD building blocks for 4th.GRC



This directory contains modular, reusable pipeline templates for 4th.GRC, enabling consistent enterprise-grade CI/CD across dev, staging, and production environments.



---



\## 📁 Directory Structure

```

infra/pipelines/azure-devops/templates/

├── jobs-containerapp.yml     # Build + deploy Azure Container Apps

├── jobs-docker-build.yml     # Build + push Docker images to ACR

├── jobs-terraform.yml        # Terraform init/validate/plan/apply

├── variables-dev.yml         # Development environment settings

├── variables-prod.yml        # Production environment settings

└── README.md                 # This file

```



---



\## 1. jobs-containerapp.yml  

Reusable job for deploying Azure Container Apps.



\### Example:

```yaml

\- template: templates/jobs-containerapp.yml

&nbsp; parameters:

&nbsp;   imageName: 'policyengine-svc'

&nbsp;   dockerfilePath: 'infra/container-images/policyengine-svc/Dockerfile'

&nbsp;   containerRegistry: '$(containerRegistry)'

&nbsp;   imageTag: '$(imageTag)'

&nbsp;   azureSubscription: '$(azureServiceConnection)'

&nbsp;   resourceGroup: '$(resourceGroup)'

&nbsp;   containerAppEnv: '$(containerAppEnv)'

&nbsp;   containerAppName: '$(policyengineAppName)'

&nbsp;   targetPort: 8080

```



---



\## 2. jobs-docker-build.yml  

Build \& push Docker images to ACR.



\### Example:

```yaml

\- template: templates/jobs-docker-build.yml

&nbsp; parameters:

&nbsp;   imageName: 'scorecard-app'

&nbsp;   dockerfilePath: 'infra/container-images/scorecard-app/Dockerfile'

&nbsp;   containerRegistry: '$(containerRegistry)'

&nbsp;   imageTag: '$(imageTag)'

```



---



\## 3. jobs-terraform.yml  

Terraform deploy pipeline pattern.



\### Example:

```yaml

\- template: templates/jobs-terraform.yml

&nbsp; parameters:

&nbsp;   environmentName: 'dev'

&nbsp;   tfWorkingDir: 'infra/terraform/environments/dev'

&nbsp;   azureServiceConnection: '$(azureServiceConnection)'

&nbsp;   tfVarsFile: 'dev.tfvars'

&nbsp;   enableApply: true

```



---



\## 4. variables-dev.yml  

Centralized variable definitions for dev deployments.



\### Use:

```yaml

variables:

\- template: templates/variables-dev.yml

```



---



\## 5. variables-prod.yml  

Production equivalents.



\### Use:

```yaml

variables:

\- template: templates/variables-prod.yml

```

\# Azure DevOps Pipeline Templates  

Reusable CI/CD building blocks for 4th.GRC



This directory contains modular, reusable pipeline templates for 4th.GRC, enabling consistent enterprise-grade CI/CD across dev, staging, and production environments.



---



\## 📁 Directory Structure

```

infra/pipelines/azure-devops/templates/

├── jobs-containerapp.yml     # Build + deploy Azure Container Apps

├── jobs-docker-build.yml     # Build + push Docker images to ACR

├── jobs-terraform.yml        # Terraform init/validate/plan/apply

├── variables-dev.yml         # Development environment settings

├── variables-prod.yml        # Production environment settings

└── README.md                 # This file

```



---



\## 1. jobs-containerapp.yml  

Reusable job for deploying Azure Container Apps.



\### Example:

```yaml

\- template: templates/jobs-containerapp.yml

&nbsp; parameters:

&nbsp;   imageName: 'policyengine-svc'

&nbsp;   dockerfilePath: 'infra/container-images/policyengine-svc/Dockerfile'

&nbsp;   containerRegistry: '$(containerRegistry)'

&nbsp;   imageTag: '$(imageTag)'

&nbsp;   azureSubscription: '$(azureServiceConnection)'

&nbsp;   resourceGroup: '$(resourceGroup)'

&nbsp;   containerAppEnv: '$(containerAppEnv)'

&nbsp;   containerAppName: '$(policyengineAppName)'

&nbsp;   targetPort: 8080

```



---



\## 2. jobs-docker-build.yml  

Build \& push Docker images to ACR.



\### Example:

```yaml

\- template: templates/jobs-docker-build.yml

&nbsp; parameters:

&nbsp;   imageName: 'scorecard-app'

&nbsp;   dockerfilePath: 'infra/container-images/scorecard-app/Dockerfile'

&nbsp;   containerRegistry: '$(containerRegistry)'

&nbsp;   imageTag: '$(imageTag)'

```



---



\## 3. jobs-terraform.yml  

Terraform deploy pipeline pattern.



\### Example:

```yaml

\- template: templates/jobs-terraform.yml

&nbsp; parameters:

&nbsp;   environmentName: 'dev'

&nbsp;   tfWorkingDir: 'infra/terraform/environments/dev'

&nbsp;   azureServiceConnection: '$(azureServiceConnection)'

&nbsp;   tfVarsFile: 'dev.tfvars'

&nbsp;   enableApply: true

```



---



\## 4. variables-dev.yml  

Centralized variable definitions for dev deployments.



\### Use:

```yaml

variables:

\- template: templates/variables-dev.yml

```



---



\## 5. variables-prod.yml  

Production equivalents.



\### Use:

```yaml

variables:

\- template: templates/variables-prod.yml

```



