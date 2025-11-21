# 🧩 Rules Authoring Guide
This guide explains how to design, structure, and maintain **PolicyEngine rules** inside the `/rules/` folder for the 4th.GRC Agentic Governance Platform.

Rules define the *evaluative logic* used by PolicyEngine to assess systems against governance profiles (ISO 42001, NIST AI RMF, SOC 2, etc.).  
Profiles reference rules, but **rules themselves act as reusable building blocks**.

---

# 📁 Directory Structure

Example:

```
rules/
│
├── bias_fairness.yaml
├── security_encryption.yaml
├── data_retention.yaml
└── explainability.yaml
```

Each file contains **one rule module**, which may include multiple related checks.

---

# 🎯 Purpose of Rules

Rules:

- Provide **atomic, testable evaluations**
- Are referenced by profiles via:
  ```yaml
  rules:
    - id: bias_fairness.check_mitigation
  ```
- Are reusable across multiple governance standards
- Enable versioned, modular policy-as-code

Profiles = the “framework”  
Rules = the “logic engine”

---

# 🧱 Rule File Structure

Each rule YAML file should follow this pattern:

```yaml
rule_id: bias_fairness
version: 1.0.0
metadata:
  title: "Bias & Fairness"
  description: "Checks mitigation steps, data diversity, and fairness indicators."
  tags: ["fairness", "bias", "ethics"]

checks:
  - id: check_mitigation
    title: "Model includes documented bias mitigation steps"
    severity: medium
    evidence_key: model_card
    evaluator: equals
    params:
      path: has_bias_mitigation
      value: true

  - id: diversity_check
    title: "Training data covers sufficient demographic diversity"
    severity: high
    evidence_key: dataset_report
    evaluator: contains
    params:
      path: demographics
      value: ["age", "gender", "race"]
```

---

# ⚙ Rule Fields Explained

| Field | Required | Description |
|-------|----------|-------------|
| `rule_id` | Yes | A unique namespace for rule module |
| `version` | Yes | Semantic version |
| `metadata` | Yes | Title, description, tags |
| `checks[]` | Yes | List of independent rule checks |
| `checks[].id` | Yes | Unique within rule_id |
| `checks[].title` | Yes | Human-readable summary |
| `checks[].severity` | Yes | low / medium / high / critical |
| `checks[].evidence_key` | Yes | Which evidence object to inspect |
| `checks[].evaluator` | Yes | equals / contains / exists / not_exists / regex / numeric_range |
| `checks[].params` | Optional | Evaluator-specific arguments |

---

# 🧠 Evaluation Logic

Evaluators control *how* rules inspect evidence:

### `equals`
```yaml
evaluator: equals
params:
  path: has_bias_mitigation
  value: true
```

### `contains`
```yaml
evaluator: contains
params:
  path: demographics
  value: ["gender", "age"]
```

### `regex`
```yaml
evaluator: regex
params:
  path: model_description
  pattern: "differential privacy"
```

### `numeric_range`
```yaml
evaluator: numeric_range
params:
  path: drift_score
  min: 0
  max: 0.1
```

---

# 🧪 Testing Rules

Before pushing:

### **Validate syntax + structure**
```bash
python scripts/validate_profiles.py
```

### **Run unit tests**
```bash
python scripts/run_unit_tests.py
```

### **Run integration tests (if evidence sources are external)**
```bash
python scripts/run_integration_tests.py
```

---

# 🏗 Creating New Rules

Follow this checklist:

1. Create new file in `/rules/`
2. Use lowercase + underscores for filename
3. Add:
   - rule_id
   - version
   - metadata
   - one or more checks
4. Validate:
   ```bash
   python scripts/validate_profiles.py
   ```
5. Reference the rule in a profile under `/profiles/`
6. Commit rule + updated profile(s)

---

# 🔄 Versioning Rules

Rules are versioned with **semantic versions**:

- `1.0.0` — first stable
- `1.1.0` — new non-breaking checks
- `2.0.0` — breaking changes or renaming checks

Profiles should reference *exact rule versions* to guarantee reproducibility.

---

# 🔗 Referencing Rules in Profiles

Profiles include rules like this:

```yaml
rules:
  - id: bias_fairness.check_mitigation
    weight: 0.3
  - id: security_encryption.at_rest
    weight: 0.2
```

---

# 🛡 Best Practices

- Keep rules **atomic** (one responsibility per check)
- Use human-readable titles
- Include good metadata
- Avoid mixing unrelated concerns in one file
- Prefer reusable checks across multiple frameworks
- Add test evidence samples in `/tests/data/`

---

# 🧭 Future Expansion Ideas

- Composite rules (multi-step logic)
- ML-based evaluators
- Remote rule registries
- Rule dependency graphs
- Explainability outputs (“rule fired because…”)

---

# 👤 Maintainer

**Dr. Freeman A. Jackson**  
4th.GRC™ – Agentic AI Governance Platform  
Fourth Industrial Systems (4th)

