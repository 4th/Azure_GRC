# 4th.GRC – Notebooks Guide  
**Location:** `agents/notebooks/`  
**Purpose:** Exploration • Prototyping • Demonstrations • Visualization

Notebooks in this directory are *not* part of the production runtime.  
They import and demonstrate logic from the main `agents/` package.

---

## 🎯 Purpose of This Folder

Use notebooks for:
- Architecture exploration (C4 models, system context, capability maps)
- Evidence visualization demos
- Scorecard rendering examples
- Prototyping new governance flows
- Semantic Kernel / Agentic workflow experiments
- Teaching, documentation, walkthroughs

Do **not** use notebooks for:
- Runtime implementation
- Evidence or policy logic
- Planner workflow logic
- Agent tools
- Production code

Those must live under:

```
agents/
  planners/
  tools/
  flows/
  functions/
  configs/
```

---

## 📌 Required First Cell in Every Notebook

Add this block so notebooks can import runtime modules:

```python
import sys
from pathlib import Path

# Points to C:\4th\4th.GRC
REPO_ROOT = Path().resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

print("Repo root:", REPO_ROOT)

from agents.planners import plan_and_run
```

Now notebooks can call core agent workflows.

---

## 🚀 Example Demo Notebook Pattern

### Cell 1 – Imports & Environment Setup
```python
from agents.planners import plan_and_run
```

### Cell 2 – Inputs
```python
SYSTEM_ID = "demo-llm-system"
PROFILE_REF = "iso_42001-global@1.2.0"
```

### Cell 3 – Run Evaluation
```python
result = plan_and_run(system_id=SYSTEM_ID, profile_ref=PROFILE_REF)
result["summary"]
```

### Cell 4 – Visualize Findings
```python
import pandas as pd
pd.DataFrame(result["findings"])
```

---

## 📁 Suggested Folder Layout

```
agents/notebooks/
├── README.md
├── agent_workflow_demo.ipynb
├── evidence_visualizer.ipynb
├── scorecard_render.ipynb
└── architecture/
    ├── c4_context.ipynb
    ├── capability_map.ipynb
    └── trust_boundary.ipynb
```

---

## 🔧 Converting Notebook Logic to Modules

If notebook code is worth keeping:

1. Create a module:
   ```
   agents/flows/my_flow.py
   ```

2. Move code from the notebook into that module.

3. Import it back into the notebook:
   ```python
   from agents.flows.my_flow import build_evidence
   ```

4. Keep the notebook clean.

---

## 🧪 Testing Notebook Logic

Never test logic *inside* a notebook.

Instead:

- Move logic into a module
- Create `tests/agents/...`
- Write unit tests there

Example:

```python
def test_telemetry_flow():
    from agents.flows.telemetry_flow import build_telemetry_evidence
    assert isinstance(build_telemetry_evidence("demo"), list)
```

---

## ✔ Summary

- **Notebooks = demos, documentation, visualization**
- **Modules = runtime logic**
- Always import modules, never duplicate logic
- Use notebooks as teaching tools and exploration sandboxes
- Keep notebooks clean, thin, and import-only

This structure makes 4th.GRC enterprise-grade, testable, scalable, and future-proof.
