# Governance Playbook — 4th.GRC™

## Mission
Operationalize AI governance with measurable controls, rapid feedback loops, and human accountability.

## Roles & RACI
| Role | Responsibilities | R | A | C | I |
|------|-------------------|---|---|---|---|
| GRC Lead | policy stewardship, risk scoring | R | A | CISO | Execs |
| Product Owner | delivery, exemptions | R | A | GRC | Audit |
| Data Steward | evidence curation | R |  | Eng | GRC |
| Eng Lead | thresholds, implementation | R | A | GRC | Audit |
| Audit Officer | independent review |  |  | A | CISO |

## Operating Cycle (Continuous Assurance)
1. **Discover evidence** → agents (Purview/Blob/ADLS).  
2. **Evaluate** → PolicyEngine (`/v1/evaluate`).  
3. **Act** → auto-remediation or **HITL** ticket.  
4. **Attest & store** → signed results in Cosmos DB.  
5. **Report** → Scorecard; monthly/quarterly reviews.

## Exemptions
- Require ticket with **reason**, **compensating controls**, and **expiry date** (≤ 90 days).  
- Approvals: Product Owner + GRC Lead; CISO informed.

## Incident & Escalations
- **Fail (high severity)** → block deploy, page on-call, open Jira Sev-2.  
- **Warn** → plan within 7 days, re-evaluate after remediation.

## Cadence
- **Monthly:** fairness/PII audits; KPI thresholds.  
- **Quarterly:** control mappings & weights.  
- **Annually:** framework re-alignment (ISO/NIST/IEEE/EU).

## Metrics
- **Coverage %** of controls by system  
- **MTTR/MTTC** for remediation and compliance  
- **Exemption debt** (# open, avg. age)  
