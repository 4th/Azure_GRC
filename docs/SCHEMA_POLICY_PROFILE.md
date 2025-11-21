# Schema Reference — Policy Profile (YAML)

## Top-Level
```yaml
profile_id: iso_42001-global
version: 1.2.0
title: ISO/IEC 42001 Governance Profile
controls:
  - control_id: ISO42001-6.3.2
    name: Bias & Fairness
    rule_ref: { id: bias_fairness, version: ">=1.0.0" }
    weight: 0.12
    evidence:
      - type: blob_uri
        pattern: "audit/fairness/*.json"
    override_params:
      min_score: 0.85
metadata:
  owner: Fourth Industrial Systems
  last_reviewed: 2025-11-10
```

## Controls
- `control_id` — unique ID (string)  
- `rule_ref` — `id` (maps to `rules/<id>.yaml`) and optional `version` range  
- `weight` — numeric (0..1), used for overall score weighting  
- `evidence` — list of sources (`blob_uri`, `json`, `inline`, `purview`)  
- `override_params` — per-control overrides to rule defaults

## Rule YAML (reference)
```yaml
rule_id: bias_fairness
version: 1.0.0
engine_op: fairness_threshold
inputs:
  required_evidence:
    - type: blob_uri
      pattern: audit/fairness/*.json
  params:
    min_score: 0.80
outputs:
  pass_criteria: FAIRNESS_SCORE >= min_score
  signals: [FAIRNESS_SCORE, DISPARITY_RATIO]
remediation:
  playbook: bias_mitigation@v2
```

## Validation
Use `policyengine.validators.validate_profile(profile_dict)` to ensure `profile_id`, `version`, and valid `controls` structure. CI should run `scripts/validate_profiles.py` to lint both profiles and rules against JSON Schemas.
