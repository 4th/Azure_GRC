#!/usr/bin/env python
"""
Export Cosmos findings to CSV for external analysis.
Usage: python scripts/export_cosmos_findings.py output.csv
"""

import csv
import os
import sys
from typing import Any, Dict

from azure.cosmos import CosmosClient

COSMOS_URL = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")
COSMOS_DB = os.environ.get("COSMOS_DB", "trustops-db")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "findings")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: export_cosmos_findings.py output.csv")
        return 1

    if not COSMOS_URL or not COSMOS_KEY:
        raise SystemExit("Set COSMOS_ENDPOINT and COSMOS_KEY in env.")

    out_path = argv[1]

    client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)
    db = client.get_database_client(COSMOS_DB)
    container = db.get_container_client(COSMOS_CONTAINER)

    query = "SELECT c.id, c.run_id, c.profile_id, c.score, c.verdict, c.timestamp FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "run_id", "profile_id", "score", "verdict", "timestamp"],
        )
        writer.writeheader()
        for item in items:
            writer.writerow(item)

    print(f"[export] Wrote {len(items)} rows to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
