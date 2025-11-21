# 📂 `scripts/` Directory — Developer & Ops Toolkit

This folder contains helper scripts for **local development**, **policy-as-code validation**, **agentic workflows**, **Cosmos/TrustOps data**, **security scanning**, **OpenAPI publishing**, and **CI/CD operations** for the 4th.GRC™ platform.

Every script includes instructions for:

- **🐧 Windows Git Bash**
- **🐍 Python / direct command equivalents**
- **🔧 Required environment variables (when applicable)**

Use this as your reference “toolbox” when working with this repository.

---

# 🧑‍💻 Development & Local Runtime Scripts

---

## 1. `dev_run_policyengine.sh`
Runs the FastAPI PolicyEngine service locally on **http://127.0.0.1:8080**.

### Git Bash
```bash
cd /c/path/to/repo
bash scripts/dev_run_policyengine.sh
```

### Python / Direct Command
```bash
cd /c/path/to/repo
export PYTHONPATH=.
python -m uvicorn services.policyengine_svc.main:app --host 0.0.0.0 --port 8080 --reload
```

---

## 2. `dev_run_scorecard.sh`
Starts the TrustOps Scorecard Streamlit app on **http://localhost:8501**.

### Git Bash
```bash
bash scripts/dev_run_scorecard.sh
```

### Python / Direct Command
```bash
export PYTHONPATH=.
streamlit run apps/scorecard/streamlit_app.py
```

---

## 3. `dev_run_all.sh`
Runs **PolicyEngine + Scorecard** in parallel (background processes).

### Git Bash
```bash
bash scripts/dev_run_all.sh
```

### Python / Direct Command (two terminals)
```bash
# Terminal 1
python -m uvicorn services.policyengine_svc.main:app --host 0.0.0.0 --port 8080 --reload
```
```bash
# Terminal 2
streamlit run apps/scorecard/streamlit_app.py
```

---

## 4. `dev_create_venv.sh`
Creates a Python `.venv` environment and installs dependencies.

### Git Bash
```bash
bash scripts/dev_create_venv.sh
```

### Python / Direct Command
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

---

# ✔️ Quality, Linting & Testing Scripts

---

## 5. `check_all.sh`
Runs:
- Pre-commit hooks  
- All tests  
- mypy type checking  

### Git Bash
```bash
bash scripts/check_all.sh
```

### Python / Direct Command
```bash
pre-commit run --all-files
pytest
mypy policyengine services agents functions
```

---

## 6. `run_unit_tests.sh`
Runs only unit tests.

### Git Bash
```bash
bash scripts/run_unit_tests.sh
```

### Python / Direct Command
```bash
pytest tests/unit -q
```

---

## 7. `run_integration_tests.sh`
Runs only integration tests (requires Cosmos/Azure env vars).

### Git Bash
```bash
bash scripts/run_integration_tests.sh
```

### Python / Direct Command
```bash
pytest tests/integration -q
```

---

## 8. `lint_and_typecheck.sh`
Runs: `black`, `isort`, `flake8`, `mypy`.

### Git Bash
```bash
bash scripts/lint_and_typecheck.sh
```

### Python / Direct Command
```bash
black policyengine services agents functions apps tests
isort  policyengine services agents functions apps tests
flake8 policyengine services agents functions apps tests
mypy   policyengine services agents functions
```

---

# 🧩 Policy-as-Code / Profiles / Rules

---

## 9. `validate_profiles.py`
Validates all YAML profiles using:
- Custom validators  
- Pydantic schemas (`PolicyProfile`)  

### Git Bash / Windows
```bash
python scripts/validate_profiles.py
```

---

## 10. `render_profile_index.py`
Generates:
- `docs/profile_index.json`  
- `docs/PROFILE_INDEX.md`  

### Git Bash / Windows
```bash
python scripts/render_profile_index.py
```

---

## 11. `sync_profiles_to_blob.py`
Uploads all `profiles/*.yaml` to Azure Blob/ADLS.

### Required Env Vars
```text
PROFILES_BLOB_ACCOUNT_URL
PROFILES_BLOB_CONTAINER   (optional)
PROFILES_BLOB_PREFIX      (optional)
```

### Git Bash
```bash
export PROFILES_BLOB_ACCOUNT_URL="https://<acct>.blob.core.windows.net"
python scripts/sync_profiles_to_blob.py
```

### PowerShell
```powershell
$env:PROFILES_BLOB_ACCOUNT_URL="https://<acct>.blob.core.windows.net"
python scripts\sync_profiles_to_blob.py
```

---

# 🐳 Docker, OpenAPI & Release Automation

---

## 12. `build_docker_images.sh`
Builds Docker images for:
- `policyengine-svc`  
- `scorecard-app`  

### Git Bash
```bash
bash scripts/build_docker_images.sh
```

### Direct Docker Commands (PowerShell)
```powershell
docker build -t local/policyengine-svc:dev -f services/policyengine_svc/Dockerfile .
docker build -t local/scorecard-app:dev      -f apps/scorecard/Dockerfile .
```

---

## 13. `publish_openapi.py`
Exports the FastAPI OpenAPI schema → `docs/api/openapi.json`.

### Git Bash / PowerShell
```bash
python scripts/publish_openapi.py
```

---

## 14. `tag_release.sh`
Creates a version tag like: `v0.3.0`.

### Git Bash
```bash
bash scripts/tag_release.sh v0.3.0
```

### Direct Git
```bash
git tag -a v0.3.0 -m "Release v0.3.0"
git push origin v0.3.0
```

---

# 📊 Reports, Docs & Cards

---

## 15. `generate_scorecard_report.py`
Turns an evaluation JSON into a Markdown scorecard.

### Git Bash / Windows
```bash
python scripts/generate_scorecard_report.py eval_result.json
```

---

## 16. `update_system_card.py`
Fills in `SYSTEM_CARD_TEMPLATE.md` → outputs `SYSTEM_CARD.md`.

### Git Bash / Windows
```bash
python scripts/update_system_card.py config.json eval_result.json
```

---

# ☁️ Cosmos DB / TrustOps Data Tools

---

## 17. `seed_cosmos_with_sample_findings.py`
Seeds Cosmos DB with sample findings for demos.

### Required Env Vars
```text
COSMOS_ENDPOINT
COSMOS_KEY
COSMOS_DB
COSMOS_CONTAINER
```

### Git Bash
```bash
export COSMOS_ENDPOINT="https://<acct>.documents.azure.com:443/"
export COSMOS_KEY="<key>"
python scripts/seed_cosmos_with_sample_findings.py
```

---

## 18. `export_cosmos_findings.py`
Exports Cosmos findings → CSV.

### Git Bash / Windows
```bash
python scripts/export_cosmos_findings.py output.csv
```

---

# 🤖 Agentic AI Workflow Tools

---

## 19. `run_agentic_demo.py`
Runs a full agent→evidence→policy evaluation cycle using the live PolicyEngine API.

### Git Bash
```bash
export POLICYENGINE_URL="http://127.0.0.1:8080"
python scripts/run_agentic_demo.py
```

---

## 20. `sk_register_policyengine_plugin.py`
Shows how to use the PolicyEngine Semantic Kernel plugin.

### Required Env Vars
```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
POLICYENGINE_URL
```

### Git Bash
```bash
python scripts/sk_register_policyengine_plugin.py
```

---

# 🔐 Security & Secrets

---

## 21. `scan_security.sh`
Runs:
- `bandit`  
- `yamllint`  
- Optional: `detect-secrets`

### Git Bash
```bash
bash scripts/scan_security.sh
```

### Python / direct tools
```bash
bandit -r policyengine services agents functions
yamllint profiles rules
```

---

## 22. `rotate_secrets_stub.py`
Lists Key Vault secrets and demonstrates how rotation would work.

### Required Env Var
```text
KEY_VAULT_URL
```

### Git Bash / PowerShell
```bash
python scripts/rotate_secrets_stub.py
```

---

# 🎉 You’re Ready to Build, Validate, and Govern Agentic AI

This toolkit powers your entire **4th.GRC™ workflow**:

- Local development  
- Policy-as-code authoring  
- Governance evaluation  
- Scorecards & continuous assurance  
- Cosmos-backed TrustOps  
- Docker images  
- Security scanning  
- OpenAPI publishing  
- Agentic evaluation pipelines
