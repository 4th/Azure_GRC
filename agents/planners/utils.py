"""
agents.planners.utils

Shared utilities for planner modules.

These helpers are intentionally:
- Pure (no I/O, no HTTP, no DB access)
- Focused on config handling, profile resolution, and common logic
- Reusable across evaluate_flow, remediation_flow, continuous_monitoring, etc.

Anything that talks to external services (Cosmos, PolicyEngine, Teams, etc.)
belongs in agents.tools, not here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from agents.configs.loader import (
    load_agent_profiles,
    load_policy_mappings,
    load_settings,
    resolve_profile_for_use_case,
)


# --------------------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------------------


@dataclass
class SystemContext:
    """
    Lightweight description of a system being governed.

    This is intentionally generic so it can be used by:
    - evaluation planners
    - remediation planners
    - continuous monitoring
    """

    system_id: str
    use_case: Optional[str] = None
    system_type: Optional[str] = None
    profile_ref: Optional[str] = None


# --------------------------------------------------------------------------------------
# Settings / config helpers
# --------------------------------------------------------------------------------------


def get_settings() -> Dict[str, Any]:
    """Load global settings.yaml via the config loader."""
    return load_settings()


def get_agent_profiles() -> Dict[str, Any]:
    """Load agent_profiles.yaml via the config loader."""
    return load_agent_profiles()


def get_policy_mappings() -> Dict[str, Any]:
    """Load policy_mappings.yaml via the config loader."""
    return load_policy_mappings()


def get_default_profile_ref(settings: Optional[Dict[str, Any]] = None) -> Optional[str]:
    """
    Retrieve the default profile_ref from settings.yaml (if present).

    Returns:
        default profile_ref or None if not defined.
    """
    if settings is None:
        settings = get_settings()
    return (settings.get("defaults") or {}).get("profile_ref")


def bool_from_settings(
    settings: Dict[str, Any],
    path: List[str],
    default: bool,
) -> bool:
    """
    Safely extract a nested boolean from the settings dict.

    Example:
        hitl_on_fail = bool_from_settings(settings, ["engine", "hitl_on_fail"], True)
    """
    current: Any = settings
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return bool(current)


# --------------------------------------------------------------------------------------
# Profile resolution helpers
# --------------------------------------------------------------------------------------


def resolve_profile_for_system(
    context: SystemContext,
    *,
    settings: Optional[Dict[str, Any]] = None,
    mappings: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """
    Resolve the governance profile_ref for a given system context.

    Resolution order:
    1. Explicit context.profile_ref
    2. policy_mappings.yaml (use_case + system_type)
    3. settings.defaults.profile_ref
    """
    if settings is None:
        settings = get_settings()
    if mappings is None:
        mappings = get_policy_mappings()

    # 1) Explicit override
    if context.profile_ref:
        return context.profile_ref

    # 2) Mapping-driven
    if context.use_case:
        resolved = resolve_profile_for_use_case(
            use_case=context.use_case,
            system_type=context.system_type,
            mappings=mappings,
        )
        if resolved:
            return resolved

    # 3) Global default
    return get_default_profile_ref(settings)


# --------------------------------------------------------------------------------------
# Severity / verdict / timestamp helpers
# --------------------------------------------------------------------------------------


def severity_rank(severity: str) -> int:
    """
    Map severity to a numeric priority.

    Lower values = higher priority.
    """
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return order.get(severity.lower(), 3)


def normalize_severity(severity: str) -> str:
    """
    Normalize severity to one of: low | medium | high | critical.
    Defaults to "low" for unknown values.
    """
    s = severity.lower()
    if s in {"critical", "high", "medium", "low"}:
        return s
    return "low"


def normalize_status(status: str) -> str:
    """
    Normalize status to one of: pass | warn | fail | unknown.
    Defaults to "unknown" for unknown values.
    """
    s = status.lower()
    if s in {"pass", "warn", "fail"}:
        return s
    return "unknown"


def normalize_verdict(verdict: Optional[str]) -> str:
    """
    Normalize a verdict string to a canonical form: pass|warn|fail|unknown.
    """
    if not verdict:
        return "unknown"
    return normalize_status(verdict)


def parse_iso8601(ts: Optional[str]) -> Optional[datetime]:
    """
    Parse an ISO 8601 timestamp string into a timezone-aware datetime.

    Returns:
        datetime in UTC or None if parsing fails.
    """
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def utc_now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------------------
# Evaluation-related helpers
# --------------------------------------------------------------------------------------


def extract_evaluation_summary(
    evaluation_result: Dict[str, Any],
) -> Tuple[Optional[str], Optional[float], Optional[str]]:
    """
    Extract (verdict, score, timestamp) from a PolicyEngine evaluation result.

    Expected structure (simplified):

    {
      "summary": {
        "score": 0.82,
        "verdict": "warn",
        "evaluated_at": "2025-11-18T08:30:00Z"
      },
      "timestamp": "...",  # optional
      ...
    }

    Returns:
        (verdict, score, timestamp_iso_or_none)
    """
    summary = evaluation_result.get("summary", {}) or {}
    verdict = normalize_verdict(summary.get("verdict"))
    score = summary.get("score")

    ts_raw = (
        summary.get("evaluated_at")
        or evaluation_result.get("timestamp")
        or evaluation_result.get("evaluated_at")
    )
    ts = parse_iso8601(ts_raw)
    ts_iso = ts.isoformat() if ts else None

    return verdict, score, ts_iso
