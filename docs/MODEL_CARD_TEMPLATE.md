# Model Card Template — 4th.GRC™

**Model Name:** ____________________________________  
**Version:** ____________    **Date:** November 11, 2025  
**Owner:** __________________ **Contact:** __________________

## 1. Summary
- **Intended Use(s):** _______________________________________________
- **Out-of-Scope Uses:** _____________________________________________

## 2. Model Details
- **Type:** LLM / Classifier / Recommender / Other
- **Architecture:** GPT / BERT / Tree / Ensemble / Custom
- **Training Data:** Internal / Public / Licensed / Synthetic
- **Preprocessing:** _________________________________________________
- **Fine-tuning:** _________________________________________________

## 3. Performance
| Metric | Eval Split | Value | Threshold | Notes |
|-------:|------------|------:|----------:|-------|
| Accuracy | test | | | |
| F1 | test | | | |
| Latency p95 (ms) | prod | | 500 | |
| Fairness score | audit | | ≥ 0.80 | from `bias_fairness.yaml` |
| Drift PSI | prod | | ≤ 0.20 | feature population change |

## 4. Fairness & Safety
- **Groups evaluated:** (sex, race, age_bucket, region, …)  
- **Parity metric:** demographic_parity / equal_opportunity / equalized_odds  
- **Remediations:** reweight, post-process, change data collection  
- **Guardrails:** `output_guardrails.yaml` categories with max severity

## 5. Data, Privacy, and Security
- **PII Handling:** masking / tokenization / minimization (`pii.yaml`)  
- **Encryption:** TLS ≥ 1.2, KMS at-rest (`encryption.yaml`)  
- **RBAC:** least privilege (`rbac.yaml`)

## 6. Governance
- **Lifecycle gates:** design → train → eval → deploy (`lifecycle.yaml`)  
- **HITL requirements:** risk-based approvals (`human_review.yaml`)  
- **Disclosure:** user-facing & API docs (`transparency.yaml`)

## 7. Limitations & Ethical Considerations
- Domain shift sensitivity; subgroup performance variance; prompt injection

## 8. Monitoring
- Online metrics: latency, error rates, cost; offline audits: fairness, PII scans

## 9. Change History
- vX.Y.Z — notes, datasets, hyperparams, thresholds
