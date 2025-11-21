"""
agents.planners.continuous_monitoring

Planner for continuous / scheduled governance monitoring.

This module does NOT:
- Talk to Cosmos, Blob, or any external systems directly.
- Call PolicyEngine directly.

Instead, it:
- Loads monitoring-related thresholds from settings.yaml
- Uses a callback to fetch the last evaluation for each system
- Decides whether each system should be re-evaluated
- Produces a structured "monitoring plan" that a scheduler or
  higher-level orchestrator can execute.

Typical flow:

1. A background job (e.g., Azure Function, Container App, cron) calls
   plan_monitoring() with:
   - A list of systems to monitor
   - A function to fetch the last evaluation result for a system_id

2. This planner returns a list of actions like:
   - "run_evaluation"
   - "skip"

3. The caller uses that plan to trigger evaluations via the main
   evaluate_flow planner and PolicyEngine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional

from agents.configs.loader import (
    load_settings,
    load_policy_mappings,
    resolve_profile_for_use_case,
)


# Type alias for a function that retrieves the last evaluation result for a system.
# You are expected to implement this in agents.tools or in your infra layer.
GetLastEvaluationFn = Callable[[str], Optional[Dict[str, Any]]]


@dataclass
class MonitoringTarget:
    """Represents a system that may need governance re-evaluation."""

    system_id: str
    use_case: Optional[str] = None
    system_type: Optional[str] = None
    profile_ref: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringAction:
    """Represents a single monitoring decision for a system."""

    system_id: str
    action: str  # "run_evaluation" | "skip"
    reason: str
    profile_ref: Optional[str] = None
    use_case: Optional[str] = None
    system_type: Optional[str] = None
    last_evaluated_at: Optional[str] = None  # ISO timestamp
    last_verdict: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MonitoringPlan:
    """Aggregated monitoring plan for all systems in scope."""

    generated_at: str
    actions: List[MonitoringAction] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "generated_at": self.generated_at,
            "actions": [
                {
                    "system_id": a.system_id,
                    "action": a.action,
                    "reason": a.reason,
                    "profile_ref": a.profile_ref,
                    "use_case": a.use_case,
                    "system_type": a.system_type,
                    "last_evaluated_at": a.last_evaluated_at,
                    "last_verdict": a.last_verdict,
                    "extra": a.extra,
                }
                for a in self.actions
            ],
        }


def _get_monitoring_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract monitoring-related settings from settings.yaml.

    Example structure (optional, with defaults):

    monitoring:
      max_age_days: 7
      rerun_on_verdict:
        - "fail"
      rerun_on_warn: true
      min_score_delta: 0.05   # placeholder for future use
    """
    monitoring = settings.get("monitoring", {}) or {}
    return {
        "max_age_days": monitoring.get("max_age_days", 7),
        "rerun_on_verdict": monitoring.get("rerun_on_verdict", ["fail"]),
        "rerun_on_warn": bool(monitoring.get("rerun_on_warn", True)),
    }


def _parse_timestamp(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        # Accept both naive and Z-terminated timestamps
        if ts.endswith("Z"):
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def _needs_rerun(
    last_eval: Optional[Dict[str, Any]],
    monitoring_cfg: Dict[str, Any],
) -> (bool, str, Optional[datetime], Optional[str]):
    """
    Core decision function: given the last evaluation result and monitoring
    configuration, determine whether a re-run is required.
    """
    if last_eval is None:
        return True, "No previous evaluation found.", None, None

    summary = last_eval.get("summary", {}) or {}
    verdict = str(summary.get("verdict", "unknown")).lower()
    ts_raw = (
        last_eval.get("timestamp")
        or last_eval.get("evaluated_at")
        or summary.get("evaluated_at")
    )
    ts = _parse_timestamp(ts_raw)

    # 1. Verdict-based rules
    rerun_verdicts = [v.lower() for v in monitoring_cfg.get("rerun_on_verdict", [])]
    if verdict in rerun_verdicts:
        return True, f"Verdict is '{verdict}', which requires re-evaluation.", ts, verdict

    if verdict == "warn" and monitoring_cfg.get("rerun_on_warn", True):
        return True, "Verdict is 'warn' and rerun_on_warn is enabled.", ts, verdict

    # 2. Age-based rules
    max_age_days = monitoring_cfg.get("max_age_days", 7)
    if ts is None:
        return True, "Previous evaluation has no valid timestamp.", None, verdict

    now = datetime.now(timezone.utc)
    age_days = (now - ts).total_seconds() / 86400.0
    if age_days > max_age_days:
        return True, f"Last evaluation is {age_days:.1f} days old (> {max_age_days}).", ts, verdict

    # 3. Default: no rerun needed
    return False, "Within acceptable age and verdict thresholds.", ts, verdict


def _resolve_profile(
    target: MonitoringTarget,
    settings: Dict[str, Any],
    mappings: Dict[str, Any],
) -> Optional[str]:
    """
    Resolve the governance profile_ref for a monitoring target,
    using (in order):

    1. Explicit target.profile_ref
    2. policy_mappings.yaml (use_case + system_type)
    3. settings.defaults.profile_ref
    """
    if target.profile_ref:
        return target.profile_ref

    if target.use_case:
        resolved = resolve_profile_for_use_case(
            use_case=target.use_case,
            system_type=target.system_type,
            mappings=mappings,
        )
        if resolved:
            return resolved

    defaults = settings.get("defaults", {}) or {}
    return defaults.get("profile_ref")


def build_monitoring_plan(
    targets: List[MonitoringTarget],
    get_last_evaluation: GetLastEvaluationFn,
    settings: Optional[Dict[str, Any]] = None,
) -> MonitoringPlan:
    """
    Build a monitoring plan for a set of systems.

    Args:
        targets: List of MonitoringTarget objects representing systems in scope.
        get_last_evaluation: Callable that returns the last evaluation result
                             for a given system_id, or None if none exists.
                             This is where you plug in Cosmos/DB/Blob logic.
        settings: Optional pre-loaded settings dict. If None, load_settings()
                  will be used.

    Returns:
        MonitoringPlan containing a list of MonitoringAction decisions.
    """
    if settings is None:
        settings = load_settings()

    mappings = load_policy_mappings()
    monitoring_cfg = _get_monitoring_settings(settings)
    now = datetime.now(timezone.utc).isoformat()

    plan = MonitoringPlan(generated_at=now)

    for target in targets:
        profile_ref = _resolve_profile(target, settings, mappings)
        last_eval = get_last_evaluation(target.system_id)
        should_rerun, reason, ts, verdict = _needs_rerun(last_eval, monitoring_cfg)

        action = MonitoringAction(
            system_id=target.system_id,
            action="run_evaluation" if should_rerun else "skip",
            reason=reason,
            profile_ref=profile_ref,
            use_case=target.use_case,
            system_type=target.system_type,
            last_evaluated_at=ts.isoformat() if ts else None,
            last_verdict=verdict,
            extra=target.metadata,
        )
        plan.actions.append(action)

    return plan


def plan_monitoring(
    systems: List[Dict[str, Any]],
    get_last_evaluation: GetLastEvaluationFn,
    settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Public entrypoint for services or scripts.

    Args:
        systems:
            A list of dicts describing systems, e.g.:

            [
              {
                "system_id": "llm-system-1",
                "use_case": "llm_agent_general",
                "system_type": "realtime_api",
                "profile_ref": null,
                "metadata": {"owner": "Team A"}
              },
              ...
            ]

        get_last_evaluation:
            Callable that takes system_id and returns the last
            evaluation result dict or None.

        settings:
            Optional pre-loaded settings dict.

    Returns:
        A dict representation of MonitoringPlan, suitable for JSON serialization.
    """
    targets = [
        MonitoringTarget(
            system_id=s["system_id"],
            use_case=s.get("use_case"),
            system_type=s.get("system_type"),
            profile_ref=s.get("profile_ref"),
            metadata=s.get("metadata", {}),
        )
        for s in systems
    ]

    plan = build_monitoring_plan(
        targets=targets,
        get_last_evaluation=get_last_evaluation,
        settings=settings,
    )
    return plan.to_dict()
