# `profile_sync` Function – README

**Location:** `functions/profile_sync/README.md`  
**Role:** Automate synchronization of 4th.GRC *policy profiles* (YAML) into a cloud Policy-as-Code registry (e.g., Azure Blob / ADLS Gen2).

This function is part of the 4th.GRC governance platform. It ensures that the latest versions of your governance **profiles** (ISO 42001, NIST, SOC 2, internal standards, etc.) are continuously synchronized from the repo into cloud storage, where they can be consumed by:

- The **PolicyEngine** microservice (`services/policyengine_svc/`)
- **Agentic planners** (`agents/planners/`) that resolve `profile_ref` dynamically
- The **TrustOps Scorecard** app (`apps/scorecard/`)
- Any external tools that treat Blob/ADLS as the canonical Policy-as-Code registry

---

## 🎯 Purpose

The `profile_sync` function provides:

1. **Automated distribution** of `profiles/*.yaml` from the repo to a central registry (Blob / ADLS).  
2. Optional **validation** of profiles before they are published.  
3. A consistent, cloud-native way to reference profiles via `profile_ref` across environments (dev/test/prod).  

This is essential for treating governance as **code** and enabling repeatable, auditable AI assurance workflows.

---

## ⚙️ Triggers & Execution Modes

You can configure `profile_sync` via `function.json` to run in different modes. Two common patterns:

### 1. Timer Trigger (Recommended)

Use a `timerTrigger` to periodically sync all profiles from the local repo into Azure Blob / ADLS.

**Typical use cases:**

- Nightly sync of profiles from `main` branch build artifacts  
- Hourly sync in dev/test environments  
- Scheduled “refresh” in multi-tenant / multi-region setups  

**Example schedule:** Run nightly at 02:00 UTC.

```jsonc
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "name": "mytimer",
      "type": "timerTrigger",
      "direction": "in",
      "schedule": "0 0 2 * * *"  // 2:00 AM every day
    }
  ]
}
2. Blob or Event-Based Trigger (Optional)
You can also configure profile_sync to react to changes published elsewhere:

Blob Trigger – when a file is uploaded to a “staging” container, validate and move to “official” registry.

Event Grid Trigger – when a CI pipeline or Git hook publishes a new profile artifact event.

Example blob trigger binding:

jsonc
Copy code
{
  "scriptFile": "__init__.py",
  "bindings": [
    {
      "type": "blobTrigger",
      "name": "inputBlob",
      "path": "incoming-profiles/{name}",
      "direction": "in",
      "connection": "AzureWebJobsStorage"
    }
  ]
}
In both modes, the core logic should live in shared helpers, not directly in the function body.

📁 Directory Structure
Inside functions/profile_sync/ you should have:

text
Copy code
functions/profile_sync/
├── README.md              # This file
├── __init__.py            # Azure Function entrypoint
└── function.json          # Trigger configuration (timer / blob / event)
Dependencies and shared utilities are defined at higher levels:

functions/shared/ for common config, logging, and client helpers

scripts/sync_profiles_to_blob.py for standalone/local sync logic

profiles/ as the source-of-truth directory for profile YAMLs

🔧 Behavior (Conceptual Flow)
A typical timer-triggered run does the following:

Resolve paths & clients

Determine repo root (e.g., C:\4th\4th.GRC)

Locate profiles/ directory

Instantiate a BlobServiceClient using PROFILES_BLOB_ACCOUNT_URL

Scan local profiles

Enumerate profiles/*.yaml

Optionally compute checksums / timestamps for change detection

Validate profiles (optional but recommended)

Load each YAML file

Optionally run policyengine.validators.validate_profile(data)

Optionally validate against a pydantic model like PolicyProfile

Upload to Blob / ADLS

For each valid profile file, upload to container PROFILES_BLOB_CONTAINER

Use prefix PROFILES_BLOB_PREFIX (e.g., profiles/iso_42001-global@1.2.0.yaml)

Use overwrite=True for idempotent sync

Log results

Log counts of uploaded, skipped, and failed records

Emit errors in a way that’s visible in Application Insights / Functions logs

🔐 Required Configuration & Environment Variables
The function assumes the following environment variables are set (via local.settings.json for local dev and Function App Configuration in Azure):

Variable	Required	Default	Description
PROFILES_BLOB_ACCOUNT_URL	✅	—	Storage account URL for the profiles registry (e.g., https://mystorage.blob.core.windows.net).
PROFILES_BLOB_CONTAINER	➕	policy-profiles	Container to which profile files will be uploaded.
PROFILES_BLOB_PREFIX	➕	profiles/	Path prefix within the container (acting like a virtual directory).
AZURE_STORAGE_CONNECTION_STRING or AzureWebJobsStorage	⚠️	varies	Used if relying on a connection string-based client instead of account URL auth.
ENVIRONMENT_NAME	➕	dev	Optional label (dev/test/prod) for logging / routing.

Example local.settings.json (do not commit real secrets):

json
Copy code
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "PROFILES_BLOB_ACCOUNT_URL": "https://<your-storage>.blob.core.windows.net",
    "PROFILES_BLOB_CONTAINER": "policy-profiles",
    "PROFILES_BLOB_PREFIX": "profiles/",
    "ENVIRONMENT_NAME": "dev"
  }
}
🧪 Validation & Quality Gates
You can integrate validation directly in the function or reuse core logic from scripts/validate_profiles.py by refactoring the shared parts into a small library function.

Possible steps per profile:

Load YAML with yaml.safe_load

Run validate_profile(data) (custom structural checks)

Run PolicyProfile.model_validate(data) (pydantic schema-based validation)

If any step fails:

Log an error

Skip upload (or write to a rejected/ prefix for offline review)

This ensures that only structurally correct, schema-compliant policies are published.

🔌 Integration With Other Components
Once profiles are synced, they can be consumed in several ways:

1. PolicyEngine Microservice
services/policyengine_svc/ can be configured to read profiles from Blob / ADLS.

It may cache profiles locally for performance.

profile_ref strings like iso_42001-global@1.2.0 map to files uploaded by profile_sync.

2. Agentic Planners
agents.planners.utils.resolve_profile_for_system(...) and agents.configs.policy_mappings.yaml can assume that any referenced profile is present in the registry.

This allows you to manage mappings between use_case / system_type and profile_ref without changing code.

3. TrustOps Scorecard App
The Scorecard UI can read profile metadata from Blob or from a generated index (e.g., docs/profile_index.json) and present them as selectable evaluation profiles.

▶️ Running Locally
Install Azure Functions Core Tools

bash
Copy code
npm install -g azure-functions-core-tools@4
Set up local.settings.json (based on the example above).

Start the Functions host from the functions/ root:

bash
Copy code
func start --verbose
Trigger profile_sync

If timer-triggered, you can wait for the schedule or change it to run every minute while testing.

If blob-triggered, upload a file to the configured container/path.

🚀 Deployment
To deploy profile_sync as part of your 4th.GRC Functions app:

bash
Copy code
func azure functionapp publish <YOUR_FUNCTION_APP_NAME>
Or via CI/CD (GitHub Actions / Azure DevOps), referencing the functions/ directory and your chosen runtime stack.

Make sure the following are set in the Azure Function App configuration:

PROFILES_BLOB_ACCOUNT_URL

PROFILES_BLOB_CONTAINER

PROFILES_BLOB_PREFIX

Any credentials or MSI/role assignments required for Blob access

✅ Best Practices
Treat profiles/ as source-of-truth in Git (PRs, reviews, version tags).

Use profile_sync to publish to Blob as the runtime registry.

Enable validation to fail fast on malformed profiles.

Use different containers or prefixes per environment (e.g., dev/profiles/, prod/profiles/).

Monitor logs / Application Insights for upload failures and validation errors.

📌 Summary
The profile_sync function is a key part of the 4th.GRC Policy-as-Code architecture:

Automates propagation of governance profiles into a runtime registry

Supports validation and quality gates

Keeps PolicyEngine, planners, and Scorecard operating against current, trusted profiles

Fits naturally into CI/CD, agentic workflows, and multi-environment deployments

By leveraging profile_sync, you ensure that AI governance in 4th.GRC remains centralized, consistent, and auditable across your entire platform.