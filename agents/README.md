# 4th.GRC Agents  
**Autonomous + Human-Aligned Governance Agents for PolicyEngine**

This directory contains the **Agentic AI layer** of the 4th.GRC Platform.  
Agents in this subsystem orchestrate:

- Evidence gathering  
- Governance evaluation using PolicyEngine  
- Multi-step reasoning, planning, and action  
- Integration with Semantic Kernel, Azure OpenAI, DeepSeek, OpenAI, and Anthropic models  
- Optional Human-in-the-Loop (HITL) escalation  
- Automated documentation and scorecard generation  

The **agents/** package is purposely lightweight—each folder contains logic that composes into a full governance agent.

---

## 📁 Directory Structure

```
agents/
├── __init__.py
├── READEME.md         # <- this file
├── configs/
│   ├── __init__.py
│   └── agent_profiles.yaml     (model + tool config)
├── planners/
│   ├── __init__.py
│   └── evaluate_flow.py        (plan & execute governance cycle)
├── tools/
│   ├── __init__.py
│   ├── sk_policyengine_plugin.py
│   ├── evidence_collectors.py
│   └── utils.py
└── functions/
    ├── __init__.py
    └── (Optional: workflow functions for agents)
```

---

# 🧠 Agent Overview

## What is an Agent in 4th.GRC?
An **Agent** is an orchestrated combination of:

- Large Language Model  
- Tools  
- Planner  
- Config-driven behavior  

Agents follow the workflow:
1. Identify governance requirements  
2. Collect evidence  
3. Evaluate with PolicyEngine  
4. Summarize  
5. Generate scorecards  
6. Persist results  

---

# 🚀 Quick Start

```python
from agents.planners import plan_and_run

result = plan_and_run(
    system_id="demo",
    profile_ref="iso_42001-global@1.2.0"
)

print(result["summary"])
```
