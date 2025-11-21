#!/usr/bin/env python
"""
End-to-end demo:
- Gather sample evidence
- Call PolicyEngine service
- Print a human-readable summary
Usage: python scripts/run_agentic_demo.py
"""

import json
import os
from typing import Any, Dict

import requests

POLICYENGINE_URL = os.environ.get("POLICYENGINE_URL", "http://127.0.0.1:8080")


def build_demo_request() -> Dict[str, Any]:
    return {
        "profile_ref": "iso_42001-global@1.2.0",
        "context": {
            "system_name": "Demo LLM System",
            "owner": "Demo Owner",
        },
        "evidence": {
            "model_card": {
                "type": "inline",
                "value": {"has_bias_mitigation": True, "documented_risks": ["hallucination"]},
            }
        },
    }


def main() -> None:
    payload = build_demo_request()
    print("[agentic-demo] Request payload:")
    print(json.dumps(payload, indent=2))

    url = f"{POLICYENGINE_URL}/v1/evaluate"
    print(f"[agentic-demo] POST {url}")
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    print("\n[agentic-demo] Summary:")
    summary = data.get("summary", {})
    print(json.dumps(summary, indent=2))

    print("\n[agentic-demo] Findings:")
    for f in data.get("findings", []):
        print(
            f"- {f.get('id')} [{f.get('severity')} / {f.get('status')}]: "
            f"{f.get('title')}"
        )


if __name__ == "__main__":
    main()
