#!/usr/bin/env python
"""
Stub/example for secret rotation via Azure Key Vault.
This does NOT perform real rotation; it's a template.
"""

import os
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")


def main() -> None:
    if not KEY_VAULT_URL:
        raise SystemExit("Set KEY_VAULT_URL in env.")

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)

    print("[rotate] Listing secrets (names only)...")
    for props in client.list_properties_of_secrets():
        print(f"- {props.name}")

    print(
        "\n[rotate] This is a stub. In a real rotation script, you would:\n"
        "  1. Generate new credentials/keys.\n"
        "  2. Set them in Key Vault (client.set_secret()).\n"
        "  3. Update dependent services (Container Apps, Functions, etc.)\n"
        "  4. Trigger rolling restarts.\n"
    )


if __name__ == "__main__":
    main()
