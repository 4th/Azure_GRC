#!/usr/bin/env python
"""
rotate_secrets_stub.py

Stub/example for secret rotation via Azure Key Vault for the 4th.GRC platform.

⚠ WARNING:
This script does NOT perform real rotation. It is intended as:
  - A reference implementation
  - A starting point for a proper rotation workflow
  - A tool for listing existing secrets and planning change management

You should extend this with:
  1. Logic to generate new credentials/keys.
  2. Calls to Azure Key Vault to set/update secrets.
  3. Automation to update dependent services (ACR, Container Apps, Cosmos, etc.).
  4. Safe rollout / rollback strategies.
"""

import os
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_env(name: str, required: bool = True) -> Optional[str]:
    """Fetch environment variable or exit with a clear message."""
    value = os.environ.get(name)
    if required and not value:
        raise SystemExit(f"Environment variable {name} is required but not set.")
    return value


def main() -> None:
    key_vault_url = get_env("KEY_VAULT_URL")  # e.g. https://4th-grc-dev-kv.vault.azure.net/

    print(f"[rotate] Connecting to Key Vault: {key_vault_url}")

    # Uses managed identity, workload identity, or local Azure CLI credentials
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_url, credential=credential)

    print("[rotate] Listing secrets (names only)...")
    for props in client.list_properties_of_secrets():
        print(f"  - {props.name}")

    print(
        "\n[rotate] This is a STUB implementation.\n"
        "In a real rotation workflow you would typically:\n"
        "  1. Identify which secrets should be rotated (e.g., COSMOS_KEY, ACR_PASSWORD).\n"
        "  2. Generate new credentials or keys (outside or inside this script).\n"
        "  3. Store them in Key Vault via client.set_secret(...).\n"
        "  4. Update dependent services (Container Apps, Functions, AKS, etc.)\n"
        "     to point to the new secret versions.\n"
        "  5. Trigger rolling restarts / deployments so new credentials take effect.\n"
        "  6. Optionally deprecate or disable old secrets after a safe cutover period.\n"
        "\n"
        "You can wire this script into CI/CD (GitHub Actions / Azure DevOps) as a\n"
        "manual or scheduled rotation job once real rotation logic is implemented.\n"
    )


if __name__ == "__main__":
    main()
