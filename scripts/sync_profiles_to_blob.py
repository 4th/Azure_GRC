#!/usr/bin/env python
"""
Sync profiles/ to Azure Blob Storage or ADLS Gen2 as a Policy-as-Code registry.
Usage: python scripts/sync_profiles_to_blob.py
"""

import os
from pathlib import Path

from azure.storage.blob import BlobServiceClient

ROOT_DIR = Path(__file__).resolve().parents[1]
PROFILES_DIR = ROOT_DIR / "profiles"

ACCOUNT_URL = os.environ.get("PROFILES_BLOB_ACCOUNT_URL")
CONTAINER = os.environ.get("PROFILES_BLOB_CONTAINER", "policy-profiles")
PREFIX = os.environ.get("PROFILES_BLOB_PREFIX", "profiles/")


def main() -> None:
    if not ACCOUNT_URL:
        raise SystemExit("Set PROFILES_BLOB_ACCOUNT_URL in env.")

    service_client = BlobServiceClient(account_url=ACCOUNT_URL)
    container_client = service_client.get_container_client(CONTAINER)
    container_client.create_container(exist_ok=True)  # type: ignore[arg-type]

    for path in sorted(PROFILES_DIR.glob("*.yaml")):
        blob_name = f"{PREFIX}{path.name}"
        print(f"[sync] Uploading {path} -> {blob_name}")
        with path.open("rb") as f:
            container_client.upload_blob(
                name=blob_name,
                data=f,
                overwrite=True,
            )

    print("[sync] Done.")
    

if __name__ == "__main__":
    main()
