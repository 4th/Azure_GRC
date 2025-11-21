#!/usr/bin/env python
"""
Export FastAPI OpenAPI schema and optionally push to APIM.
Usage: python scripts/publish_openapi.py
"""

import json
import os
from pathlib import Path

from services.policyengine_svc.main import app

OUT_FILE = Path(__file__).resolve().parents[1] / "docs" / "api" / "openapi.json"


def export_openapi() -> None:
    schema = app.openapi()
    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"[openapi] Wrote {OUT_FILE}")


def publish_to_apim() -> None:
    # Stub for APIM integration – replace with actual APIM SDK/REST call.
    apim_name = os.environ.get("APIM_NAME")
    if not apim_name:
        print("[openapi] APIM_NAME not set; skipping APIM publish.")
        return
    print(f"[openapi] Would publish to APIM instance: {apim_name}")
    # TODO: Implement APIM import/update logic here.


def main() -> None:
    export_openapi()
    publish_to_apim()


if __name__ == "__main__":
    main()
