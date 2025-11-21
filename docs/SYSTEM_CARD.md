# System Card — 4th.GRC™ PolicyEngine
**Date:** November 11, 2025  
**Owner:** Fourth Industrial Systems®  
**Tagline:** *Autonomy with Accountability™*

---

## 1) Purpose & Scope
4th.GRC is an Azure-native, agentic Governance-Risk-Compliance (GRC) platform. It converts governance frameworks (ISO 42001, NIST AI RMF, IEEE 7000, EU AI Act) into **Policy-as-Code** using YAML. An evaluation service (PolicyEngine) executes profiles against evidence (logs, models, configs) and emits **signed findings** and a **compliance score**.

## 2) Capabilities
- **Policy-as-Code:** Versioned YAML **profiles** reference reusable **rules** (bias, PII, encryption, etc.).
- **Agent Orchestration:** LangGraph/Semantic Kernel agents discover evidence, call the engine, and open HITL tickets.
- **Attestation:** Results signed with Azure Key Vault; audit-immutable storage.
- **Continuous Assurance:** Event-driven re-evaluations on deploy, schema change, or drift alerts.
- **Scorecards:** Streamlit dashboards; Cosmos DB metrics; App Insights traces.

## 3) System Context
```
┌──────────────┐     profiles/*.yaml      ┌───────────────────────┐
│  Stakeholders├──────────────────────────►│   PolicyEngine Svc    │
└──────┬───────┘                          │   (FastAPI, Uvicorn)  │
       │ findings & score                 └──────────┬────────────┘
       │                                            │ rules/*.yaml + evidence
       ▼                                            ▼
┌──────────────┐  dashboards/alerts      ┌─────────────────────────┐
│ Scorecard UI │◄────────────────────────│ Evidence & Rule Runtime │
└──────────────┘                         └─────────────────────────┘
```

## 4) Key Risks & Mitigations
| Risk | Description | Mitigation |
|------|-------------|------------|
| Model bias | Disparate outcomes | `rules/bias_fairness.yaml`, periodic audits, drift checks |
| Data leakage | PII/Secrets exfiltration | `pii.yaml`, `network_egress.yaml`, encryption, RBAC |
| Shadow models | Unapproved models in prod | `model_allowlist.yaml`, APIM policies |
| Missing audit | No forensic trail | `logging_audit.yaml`, centralized SIEM |
| Weak lifecycle | Skipping approvals | `lifecycle.yaml`, HITL enforcement |

## 5) Safety & Alignment
- **Human-in-the-loop** for high/critical risk (`human_review.yaml`).
- **Transparency** controls and documented decisions.
- **Exemptions** require risk acceptance and expiry.

## 6) Monitoring & Telemetry
- App Insights traces and metrics (latency, pass/fail rates).
- Drift monitors (PSI) routed to Event Grid → re-evaluate.

## 7) Governance & RACI
| Activity | R | A | C | I |
|----------|---|---|---|---|
| Policy updates | GRC Lead | CISO | Legal | Eng |
| Threshold tuning | Eng | GRC Lead | Product | Audit |
| Evidence registry | Data Steward | Eng Lead | GRC | Audit |
| Exemptions | Product | GRC Lead | CISO | Audit |

## 8) Limitations
- Requires curated evidence sources and access.
- Thresholds are context-specific and require calibration.

## 9) Change Log
Track in Git tags and docs/SYSTEM_CARD.md revisions.

## Implementation Details

The 4th.GRC PolicyEngine and its orchestration layer are fully documented in the API Reference:

- **PolicyEngine core**  
  [policyengine.engine](api/policyengine/engine.md)  
  [policyengine.schema](api/policyengine/schema.md)  
  [policyengine.validators](api/policyengine/validators.md)

- **Evidence & provenance**  
  [policyengine.evidence](api/policyengine/evidence.md)  
  [policyengine.provenance](api/policyengine/provenance.md)

- **Rule operations**  
  [policyengine.ruleset](api/policyengine/ruleset.md)

- **Agentic integrations**  
  [agents.planners.evaluate_flow](api/agents/planners/evaluate_flow.md)  
  [agents.tools.sk_policyengine_plugin](api/agents/tools/sk_policyengine_plugin.md)  
  [agents.tools.policyengine_tool](api/agents/tools/policyengine_tool.md)

- **HTTP service layer**  
  [services.policyengine_svc.main](api/services/policyengine_svc/main.md)



---
© 2025 Fourth Industrial Systems Corporation.
