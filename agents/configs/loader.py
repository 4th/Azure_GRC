"""
agents.configs.loader

Centralized helpers for loading agent configuration files:

- agent_profiles.yaml     (models, tools, policies/guardrails)
- settings.yaml           (global engine settings)
- policy_mappings.yaml    (use case / system type → profile_ref mappings)

These helpers keep YAML loading logic in one place so that planners,
tools, and services can all consume a consistent configuration API.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import yaml


# Base directory: agents/configs/
BASE_DIR = Path(__file__).resolve().parent


def _load_yaml(path: Path, *, required: bool = True) -> Dict[str, Any]:
    """
    Low-level YAML loader.

    Args:
        path: Full path to YAML file.
        required: If True, raise FileNotFoundError when missing.
                  If False, return {} when missing.

    Returns:
        Parsed YAML as a dict (or {} if not required and missing).
    """
    if not path.exists():
        if required:
            raise FileNotFoundError(f"Config file not found: {path}")
        return {}

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at root of YAML file: {path}")
    return data


def load_agent_profiles(path: Optional[str | Path] = None) -> Dict[str, Any]:
    """
    Load agent profile configuration (models, tools, policies).

    Args:
        path: Optional override path. If None, defaults to
              BASE_DIR / "agent_profiles.yaml".

    Returns:
        Dict representing agent profiles configuration.
    """
    cfg_path = Path(path) if path else BASE_DIR / "agent_profiles.yaml"
    return _load_yaml(cfg_path, required=True)


def load_settings(path: Optional[str | Path] = None) -> Dict[str, Any]:
    """
    Load global agent engine settings.

    Args:
        path: Optional override path. If None, defaults to
              BASE_DIR / "settings.yaml".

    Returns:
        Dict representing settings. If file is missing, returns {}.
    """
    cfg_path = Path(path) if path else BASE_DIR / "settings.yaml"
    return _load_yaml(cfg_path, required=False)


def load_policy_mappings(path: Optional[str | Path] = None) -> Dict[str, Any]:
    """
    Load use case / system type → PolicyEngine profile mappings.

    Args:
        path: Optional override path. If None, defaults to
              BASE_DIR / "policy_mappings.yaml".

    Returns:
        Dict representing mappings. If file is missing, returns {}.
    """
    cfg_path = Path(path) if path else BASE_DIR / "policy_mappings.yaml"
    return _load_yaml(cfg_path, required=False)


def resolve_profile_for_use_case(
    use_case: str,
    system_type: Optional[str] = None,
    *,
    mappings: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """
    Convenience helper: given a use_case and optional system_type,
    return the appropriate PolicyEngine profile_ref based on
    policy_mappings.yaml.

    Resolution order:
    1. overrides (matching use_case + system_type)
    2. use_cases[use_case].profile_ref
    3. system_types[system_type].profile_ref (if provided)
    4. None if nothing matches

    Args:
        use_case: Logical use case key (e.g., "llm_agent_general").
        system_type: Optional system type key (e.g., "realtime_api").
        mappings: Optional pre-loaded mappings dict. If None, this
                  function will call load_policy_mappings().

    Returns:
        profile_ref string or None if no mapping is found.
    """
    if mappings is None:
        mappings = load_policy_mappings()

    # 1. overrides block
    overrides = mappings.get("overrides", []) or []
    for rule in overrides:
        match = rule.get("match", {})
        if match.get("use_case") == use_case and (
            system_type is None or match.get("system_type") == system_type
        ):
            return rule.get("profile_ref")

    # 2. use_cases mapping
    use_cases = mappings.get("use_cases", {}) or {}
    if use_case in use_cases:
        uc_cfg = use_cases[use_case] or {}
        if "profile_ref" in uc_cfg:
            return uc_cfg["profile_ref"]

    # 3. system_types mapping (fallback)
    if system_type:
        system_types = mappings.get("system_types", {}) or {}
        if system_type in system_types:
            st_cfg = system_types[system_type] or {}
            if "profile_ref" in st_cfg:
                return st_cfg["profile_ref"]

    # 4. nothing found
    return None
