\# 4th.GRC – Terraform Environments



This directory contains all environment-specific Terraform configurations for the \*\*4th.GRC Agentic AI Governance Platform\*\*.



Each environment folder (`dev/`, `test/`, `prod/`) defines a complete deployment of the platform using standardized modules, naming rules, and CI/CD pipelines.



\## Directory Layout



infra/terraform/environments/

\- dev/

\- test/

\- prod/



Each contains:

\- main.tf

\- variables.tf

\- locals.tf

\- outputs.tf

\- <env>.tfvars

\- README.md



\## Purpose of Environments



\- Dev: safe for experimentation

\- Test: mirrors prod

\- Prod: secure, locked-down, audited



\## Deployment



terraform init

terraform plan -var-file="<env>.tfvars"

terraform apply -var-file="<env>.tfvars"



\## CI/CD Integration



GitHub Actions: infra\_plan\_apply.yml  

Azure DevOps: terraform-ci.yml



