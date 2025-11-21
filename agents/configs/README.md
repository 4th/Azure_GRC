# 4th.GRC – Agent Configuration Layer

**Directory:** `agents/configs/`  
**Purpose:** Centralized, declarative configuration for all Agentic AI workflows.

The configuration layer defines the behavioral, governance, and operational parameters that govern all agents inside the **4th.GRC** platform.  
It ensures:

- Deterministic agent behavior  
- Governance-driven enforcement  
- Declarative (YAML-based) control  
- Easy overrides per environment  
- Full separation between *logic* and *policy*  

---

## 📁 Directory Structure

```
agents/
└── configs/
    ├── agent_profiles.yaml
    ├── settings.yaml
    ├── policy_mappings.yaml
    ├── loader.py
    └── README.md
```

---

# 📄 File Descriptions

## 1. `agent_profiles.yaml`

Defines **roles**, **capabilities**, and **constraints** for each agent type.

Contains:

- Agent descriptions  
- Allowed tools and model families  
- Security constraints  
- Risk level classifications  
- Optional planner instructions  

Example:

```yaml
agents:
  policy_evaluator:
    description: "Evaluates LLM systems using PolicyEngine."
    allowed_tools: ["policyengine_api"]
    risk_level: "high"
```

---

## 2. `settings.yaml`

Global default runtime settings and platform-wide parameters.

Includes:

- Default LLM and generation settings  
- Streamlit / API toggles  
- Logging and audit rules  
- PolicyEngine connection  
- Agentic features (HITL, retries, timeouts)  
- Plugin enable/disable flags  

Example:

```yaml
llm:
  default_model: "gpt-4o"
  temperature: 0.2
```

---

## 3. `policy_mappings.yaml`

Maps **use cases** and **system types** to **PolicyEngine governance profiles**.

This drives governance selection automatically at runtime.

Contains:

- `use_cases:` mapping  
- `system_types:` mapping  
- Optional `overrides:`  

Example:

```yaml
use_cases:
  medical_cds:
    profile_ref: "nist_ai_rmfx_medical@0.1.0"
```

Purpose:

- Ensures agents apply the correct governance framework  
- Eliminates hardcoded references in Python  
- Supports multi-domain agent deployments (legal, medical, internal tools, etc.)

---

## 4. `loader.py`

Central utility to load and validate configuration files.

Responsibilities:

- Load YAML configs  
- Merge and normalize values  
- Validate required fields  
- Provide typed accessors  
- Cache results for fast runtime use  

Example usage:

```python
from agents.configs.loader import load_settings

settings = load_settings()
print(settings["llm"]["default_model"])
```

---

# 🧪 Recommended Test Files (optional)

Suggested tests under `tests/configs/`:

- `test_loader.py`  
- `test_agent_profiles.py`  
- `test_policy_mappings.py`  
- `test_settings_schema.py`  

These ensure:

- No invalid YAML  
- No missing keys  
- All schemas validated  
- Governance rules remain stable  

---

# 🔁 Configuration Flow Inside 4th.GRC

1. **Planner** loads `settings.yaml`  
2. Planner detects system type & use case  
3. **loader.py** uses `policy_mappings.yaml` to pick correct `profile_ref`  
4. Agent loads its own metadata from `agent_profiles.yaml`  
5. PolicyEngine evaluates system using chosen profile  
6. Scorecard, logs, and audits consume output  

This ensures:

- Full traceability  
- Reproducibility  
- Policy-as-code alignment  
- Clear separation of logic vs configuration  

---

# ✅ Summary

The `agents/configs/` directory is the **single source of truth** for:

- Agent identity  
- Default runtime behavior  
- Allowed models/tools  
- Governance mappings  
- Profile selection  
- PolicyEngine integration  

All values should be **declarative**.  
All behavior should flow **from YAML → loader → agent → PolicyEngine → Scorecard**.

