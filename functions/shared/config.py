import os
from typing import Any, Dict

from agents.configs.loader import load_settings  # if you want to reuse core settings


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name, default)
    return value


def get_policyengine_url() -> str:
    url = get_env("POLICYENGINE_URL")
    if not url:
        raise RuntimeError("POLICYENGINE_URL is not set")
    return url


def get_default_profile_ref() -> str | None:
    # Option 1: from env
    env_val = get_env("DEFAULT_PROFILE_REF")
    if env_val:
        return env_val

    # Option 2: from settings.yaml
    settings: Dict[str, Any] = load_settings()
    return (settings.get("defaults") or {}).get("profile_ref")
