# Profiles Directory

This directory contains **Policy-as-Code profiles** used by the 4th.GRC / PolicyEngine system.
Each profile is a YAML file describing a governance, risk, or compliance framework such as:

- **ISO/IEC 42001** — AI Management System (AIMS)
- **NIST AI RMF** — Risk Management Framework
- **SOC 2 Trust Services Criteria**
- **HIPAA**
- **Internal customized governance profiles**

Profiles are validated, indexed, and synced using scripts in the `/scripts` directory.

---

## 📁 Directory Structure

```
profiles/
│
├── iso_42001-global@1.2.0.yaml
├── nist_airmf@1.0.0.yaml
├── soc2_security@1.0.0.yaml
├── hipaa_privacy@1.0.0.yaml
└── <your-custom-profiles>.yaml
```

Each `.yaml` file defines one governance profile.

---

## 🧩 What a Profile Contains

Each profile generally includes:

| Section | Description |
|--------|-------------|
| `profile_id` | Unique ID with version (e.g., `iso_42001-global@1.2.0`) |
| `name` or metadata.title | Human-readable name |
| `version` | Semantic version |
| `metadata` | Standards, tags, description |
| `rules` | The actual evaluative conditions |
| `mappings` | Optional: mapping to NIST, ISO, SOC 2, etc. |
| `evidence_requirements` | What inputs the agent must supply |

Profiles define how the **PolicyEngine** evaluates a system and produces a **scorecard**.

---

## 🛠 Validation

To validate all profiles:

### **Using Python (Windows / macOS / Linux)**
```sh
python scripts/validate_profiles.py
```

### **Using Git Bash on Windows**
```sh
winpty python scripts/validate_profiles.py
```

This runs:

- Structural validation (`validate_profile()`)
- Schema validation (`PolicyProfile` pydantic model)

Invalid profiles are listed with errors.

---

## 📚 Generating an Index

Generate JSON + Markdown index for docs:

```sh
python scripts/render_profile_index.py
```

Produces:

```
docs/profile_index.json
docs/PROFILE_INDEX.md
```

Useful for:

- Frontend UI dropdowns
- API docs
- Admin dashboards

---

## ☁️ Syncing to Azure (Policy Registry)

To sync the profiles folder to **Azure Blob Storage**:

```sh
export PROFILES_BLOB_ACCOUNT_URL="https://<your-account>.blob.core.windows.net"
export PROFILES_BLOB_CONTAINER="policy-profiles"
export PROFILES_BLOB_PREFIX="profiles/"

python scripts/sync_profiles_to_blob.py
```

On Windows PowerShell:

```powershell
setx PROFILES_BLOB_ACCOUNT_URL "https://<account>.blob.core.windows.net"
python scripts/sync_profiles_to_blob.py
```

This publishes every `.yaml` file as a blob for enterprise-wide policy access.

---

## 📝 Profile Authoring Guidelines

When creating new profiles:

1. Follow semantic versioning  
2. ALWAYS include:
   ```
   profile_id:
   version:
   metadata:
     title:
     standards:
     tags:
     description:
   ```
3. Validate before committing:
   ```sh
   python scripts/validate_profiles.py
   ```
4. Include mappings to external standards when possible
5. Keep rules modular and declarative
6. Document new profiles in `docs/PROFILE_INDEX.md`

---

## ✔ Best Practices

- Keep one profile per file  
- Use lowercase and hyphens in filenames  
- Store ONLY YAML here — no JSON or Python  
- New versions should be created as **new files** (`iso_42001-global@1.3.0.yaml`)  

---

## 📦 Output from PolicyEngine

During evaluation, PolicyEngine loads profiles from this folder unless overridden by:

- Azure Blob registry
- API configuration
- Remote profile layer

Profiles are the **core intelligence** of your governance engine.

---

## 🧪 Example: Quick Local Test

```sh
python scripts/run_agentic_demo.py
```

This uses:

```
profile_ref="iso_42001-global@1.2.0"
```

to verify the profile works end-to-end.

---

## 📄 Contact

Maintainer: **Dr. Freeman A. Jackson**  
Project: **4th.GRC – Agentic AI Governance Platform**

