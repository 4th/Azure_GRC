#!/usr/bin/env python
"""
Seed Cosmos DB with sample findings for the TrustOps Scorecard.
Usage: python scripts/seed_cosmos_with_sample_findings.py
"""

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict

from azure.cosmos import CosmosClient

COSMOS_URL = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DB = os.environ.get("COSMOS_DB", "trustops-db")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "findings")


def sample_finding(i: int) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "id": str(uuid.uuid4()),
        "run_id": f"demo-run-{i}",
        "profile_id": "iso_42001-global@1.2.0",
        "score": 0.8 - (i * 0.05),
        "verdict": "warn" if i % 2 else "pass",
        "timestamp": now,
        "findings": [
            {
                "id": "bias_fairness",
                "severity": "medium",
                "status": "warn",
                "message": "Sample fairness concern for demo.",
            }
        ],
    }


def main() -> None:
    if not COSMOS_URL or not COSMOS_KEY:
        raise SystemExit("Set COSMOS_ENDPOINT and COSMOS_KEY in env.")

    client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
    db = client.create_database_if_not_exists(id=COSMOS_DB)
    container = db.create_container_if_not_exists(
        id=COSMOS_CONTAINER,
        partition_key="/profile_id",
        offer_throughput=400,
    )

    for i in range(1, 6):
        doc = sample_finding(i)
        print(f"[seed] Upserting {doc['id']} ({doc['verdict']}, score={doc['score']})")
        container.upsert_item(doc)

    print("[seed] Done.")


if __name__ == "__main__":
    main()
