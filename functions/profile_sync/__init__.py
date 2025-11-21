import logging
import os
from pathlib import Path

import azure.functions as func

from azure.storage.blob import BlobServiceClient
from policyengine.validators import validate_profile  # if available

ROOT_DIR = Path(__file__).resolve().parents[2]  # C:\4th\4th.GRC
PROFILES_DIR = ROOT_DIR / "profiles"

def _get_blob_client() -> BlobServiceClient:
    account_url = os.environ.get("PROFILES_BLOB_ACCOUNT_URL")
    if not account_url:
        raise RuntimeError("PROFILES_BLOB_ACCOUNT_URL is not set")
    return BlobServiceClient(account_url=account_url)

def _sync_profiles() -> None:
    service_client = _get_blob_client()
    container_name = os.environ.get("PROFILES_BLOB_CONTAINER", "policy-profiles")
    prefix = os.environ.get("PROFILES_BLOB_PREFIX", "profiles/")

    container = service_client.get_container_client(container_name)
    container.create_container(exist_ok=True)

    for path in sorted(PROFILES_DIR.glob("*.yaml")):
        blob_name = f"{prefix}{path.name}"
        logging.info("Syncing profile %s -> %s", path, blob_name)

        with path.open("rb") as f:
            container.upload_blob(name=blob_name, data=f, overwrite=True)

def main(mytimer: func.TimerRequest) -> None:
    logging.info("profile_sync timer trigger fired.")
    _sync_profiles()
    logging.info("profile_sync completed.")
