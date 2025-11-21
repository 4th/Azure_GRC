# 4th.GRC PolicyEngine

This package implements the core **policy-as-code evaluation engine** for 4th.GRC.

## Key Concepts

- **Profiles** (`profiles/`): YAML-based governance profiles (e.g., ISO 42001, NIST, SOC 2).
- **Rules** (`rules_engine.py`): Each profile references rules by `id` and `params`.
- **Evaluation** (`core.evaluate`): Given a `profile_ref`, `context`, and `evidence`,
  the engine loads the profile, runs rules, computes a score, and returns an `EvalResponse`.

## Public API

```python
from policyengine import EvalRequest, EvalResponse, evaluate
