# API Reference — 4th.GRC™ PolicyEngine

**Base URL:** `https://api.4thgrc.example.com` (local: `http://localhost:8080`)

---

## GET /healthz
Returns service health.
```json
{"status": "ok"}
```

## POST /v1/evaluate
Evaluate a Policy Profile.
### Request
```json
{
  "request_id": "demo-001",
  "profile_ref": "iso_42001-global@1.2.0",
  "controls": ["ISO42001-6.3.2"],
  "target": {"system_id": "demo"},
  "evidence": [
    {"type":"blob_uri","uri":"https://.../audit/fairness/2025-11.json"}
  ],
  "params": {"min_score": 0.85}
}
```
### Response
```json
{
  "request_id": "demo-001",
  "profile_ref": "iso_42001-global@1.2.0",
  "summary": {"status": "pass", "score": 0.92, "totals":{"findings":1,"passes":1,"warns":0,"fails":0}},
  "findings": [
    {
      "control_id": "ISO42001-6.3.2",
      "rule_id": "bias_fairness",
      "status": "pass",
      "rationale": "score=0.86, disparity=1.07, conf=0.93",
      "signals": {"FAIRNESS_SCORE":0.86, "DISPARITY_RATIO":1.07},
      "remediation": {"playbook":"bias_mitigation@v2"}
    }
  ],
  "attestations": [{"algo":"ES256","signature":"...","key_id":"kv://..."}]
}
```
**Errors:** `404` (Profile not found), `500` (Evaluation error)

### Security
- Optionally protect with **APIM** subscription key or **JWT**.
- Rate-limits via APIM and Azure Front Door (recommended).

---
**OpenAPI:** `services/policyengine_svc/apim/api-contract.json`
