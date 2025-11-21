# policy_eval_webhook

This Azure Function exposes a POST endpoint that external systems can use to
request real-time policy evaluations from the 4th.GRC PolicyEngine.

## Endpoint

POST /api/policy/evaluate

## Required Fields

```json
{
  "system_id": "asset-123",
  "profile_ref": "iso_42001-global@1.2.0",
  "input": {
      "data": {...}
  }
}
