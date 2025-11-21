# 4th.GRC Documentation

This directory contains the **authoritative documentation** set for the 4th.GRC™ Agentic AI Governance Platform.

Use this folder when you need to understand:

- How the platform is architected
- How to integrate with its APIs
- How governance actually operates (playbooks, roles, processes)
- How to structure Policy Profiles, Model Cards, and System Cards

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `ARCHITECTURE_OVERVIEW.md` | High-level architecture of 4th.GRC (PolicyEngine, Scorecard, agents, Azure services). |
| `API.md` | Entry point for API usage and integration patterns. |
| `GOVERNANCE_PLAYBOOK.md` | Governance operating model and processes. |
| `SCHEMA_POLICY_PROFILE.md` | Contract/schema for governance profiles (Policy-as-Code). |
| `MODEL_CARD_TEMPLATE.md` | Template for AI/ML model documentation. |
| `SYSTEM_CARD.md` | System card describing a governed AI system. |
| `api/` | Generated or structured per-endpoint API documentation. |
| `gen_api_pages.py` | Script to generate endpoint docs inside `docs/api/`. |
| `AUTO_INDEX.md` | Auto-index of documentation, categories, and navigation hints. |

---

## 🔧 Generating API Docs

The script:

- `gen_api_pages.py`

is responsible for generating detailed API documentation into the `docs/api/` directory.

Typical workflow:

```bash
cd <repo-root>
python docs/gen_api_pages.py
```

This will refresh or create endpoint Markdown files inside `docs/api/`.

---

## 🧭 Start Here

If you are new to the project:

1. Read `ARCHITECTURE_OVERVIEW.md` for the big picture  
2. Read `GOVERNANCE_PLAYBOOK.md` to understand roles and decision flows  
3. Review `SCHEMA_POLICY_PROFILE.md` and `MODEL_CARD_TEMPLATE.md` if you are authoring policies or documentation  
4. Use `API.md` and `docs/api/` when you are integrating a client or agent  

For a quick map of everything in this directory, see:

- [`AUTO_INDEX.md`](AUTO_INDEX.md)

---

## 👤 Maintainer

**Dr. Freeman A. Jackson**  
4th.GRC™ — Agentic AI Governance Platform  
Fourth Industrial Systems (4th)
