# Architecture Overview — 4th.GRC™

## Logical Architecture
```
+----------------+         +-----------------------+        +--------------------+
|  Profiles      |         |  PolicyEngine Svc     |        |  Scorecard UI      |
|  YAML repo     +--------->  (FastAPI, Python)    +-------> |  (Streamlit)       |
+--------+-------+         +-------+---------------+        +---------+----------+
         |                           | rules/*.yaml                    |
         |                           v                                 |
         |                 +-----------------------+          +--------v--------+
         |                 | Evidence Resolvers    |          | Cosmos DB       |
         |                 | (Blob/ADLS, Purview)  |          | (findings/scores)|
         |                 +-----------+-----------+          +-----------------+
         |                             |
         v                             v
   +-----+------+                +-----+------+
   | Agents    |                | Key Vault  |
   | (LangGraph|                | (Attest)   |
   +------------                +------------
```

## Sequence (Evaluation)
1. Agent selects `profile_ref` from `profiles/index.json`  
2. Service loads profile and referenced `rule_ref` YAMLs  
3. Evidence retrieved via resolvers  
4. Rule `engine_op` computes `signals` → `pass_criteria` evaluated  
5. Finding recorded; score weighted; attestation signed; response returned

## Deployment (Azure)
- **Container Apps/AKS** for services & UI  
- **APIM** provides auth/rate limits; **Front Door** optional  
- **Key Vault** for secrets + signing keys  
- **Monitor/App Insights** for traces and dashboards  
- **Event Grid/Functions** trigger re-evaluations

## Security Hardening
- Private endpoints to storage & databases  
- Managed Identity for all services  
- APIM JWT/subscription key validation  
- TLS 1.2+, KMS-backed encryption, RBAC least privilege

## Backlog (suggested)
- Rule op coverage parity with all YAMLs  
- Profile/rule JSON Schemas + CI gates  
- Auto-evidence discovery via Purview lineage

## Related API Modules

The architecture components map directly to modules in the API Reference:

### 1. Evaluation Engine
- [policyengine.engine](api/policyengine/engine.md) — core evaluation loop  
- [policyengine.ruleset](api/policyengine/ruleset.md) — rule operations  
- [policyengine.schema](api/policyengine/schema.md) — request/response models  

### 2. Evidence Layer
- [policyengine.evidence](api/policyengine/evidence.md) — resolving inline, blob, and Purview evidence  

### 3. Service Layer (FastAPI)
- [policyengine_svc.main](api/services/policyengine_svc/main.md) — HTTP entrypoint  
- [openapi_overrides](api/services/policyengine_svc/openapi_overrides.md)  
- [telemetry](api/services/policyengine_svc/telemetry.md)

### 4. Agentic Orchestration Layer
- [evaluate_flow planner](api/agents/planners/evaluate_flow.md)  
- [PolicyEngine SK plugin](api/agents/tools/sk_policyengine_plugin.md)  
- [Evidence collector tools](api/agents/tools/evidence_tool.md)
