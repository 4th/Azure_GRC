"""
agents.planners.remediation_flow

Planner for post-evaluation remediation.

Given a PolicyEngine evaluation result, this module:
- Inspects findings by severity and status
- Applies thresholds from settings.yaml (if present)
- Builds a structured remediation plan:
    - which findings should be fixed first
    - which need HITL escalation
    - which can be monitored

This planner does NOT:
- Directly create tickets (Jira, ServiceNow, etc.)
- Send notifications (Teams, email, etc.)

Those actions should be implemented by tools in agents.tools
and orchestrated by a higher-level workflow or service.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from agents.configs.loader import load_settings


Severity = Literal["low", "medium", "high", "critical"]
Status = Literal["pass", "warn", "fail", "unknown"]


@dataclass
class RemediationItem:
    """Represents one finding that needs remediation or review."""

    id: str
    title: str
    severity: Severity
    status: Status
    message: str = ""
    profile_id: Optional[str] = None
    system_id: Optional[str] = None
    recommended_action: str = ""
    requires_hitl: bool = False
    priority: int = 0  # lower = higher priority


@dataclass
class RemediationPlan:
    """Structured remediation plan derived from an evaluation result."""

    system_id: Optional[str]
    profile_id: Optional[str]
    verdict: Optional[str]
    score: Optional[float]
    items: List[RemediationItem] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "system_id": self.system_id,
            "profile_id": self.profile_id,
            "verdict": self.verdict,
            "score": self.score,
            "items": [
                {
                    "id": i.id,
                    "title": i.title,
                    "severity": i.severity,
                    "status": i.status,
                    "message": i.message,
                    "profile_id": i.profile_id,
                    "system_id": i.system_id,
                    "recommended_action": i.recommended_action,
                    "requires_hitl": i.requires_hitl,
                    "priority": i.priority,
                }
                for i in self.items
            ],
        }


def _severity_rank(severity: str) -> int:
    order = {"low": 3, "medium": 2, "high": 1, "critical": 0}
    return order.get(severity.lower(), 3)


def _bool_from_settings(settings: Dict[str, Any], path: List[str], default: bool) -> bool:
    """Helper to safely extract nested boolean flags from settings."""
    current: Any = settings
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return bool(current)


def _should_escalate_to_hitl(
    severity: Severity,
    status: Status,
    settings: Dict[str, Any],
) -> bool:
    """
    Decide whether a finding should be escalated to HITL
    based on severity/status and global settings.yaml.

    Uses:
      settings["engine"]["hitl_on_fail"]
      settings["engine"]["hitl_on_warn"]
    """
    if status == "fail":
        return _bool_from_settings(settings, ["engine", "hitl_on_fail"], True)
    if status == "warn":
        return _bool_from_settings(settings, ["engine", "hitl_on_warn"], False)
    return False


def _default_recommended_action(
    severity: Severity,
    status: Status,
) -> str:
    """Basic recommended actions based on severity/status."""
    if status == "fail":
        if severity in ("critical", "high"):
            return "Immediate remediation required; escalate to governance owner."
        return "Remediate in next governance sprint and document mitigation steps."

    if status == "warn":
        if severity in ("critical", "high"):
            return "Investigate root cause and plan remediation; consider HITL review."
        return "Monitor and address as part of regular maintenance."

    if status == "pass":
        return "No remediation required; continue monitoring."

    return "Status unknown; manual review recommended."


def build_remediation_plan(
    evaluation_result: Dict[str, Any],
    settings: Optional[Dict[str, Any]] = None,
) -> RemediationPlan:
    """
    Build a structured remediation plan from a PolicyEngine evaluation result.

    Expected evaluation_result structure (simplified):

    {
        "profile_id": "iso_42001-global@1.2.0",
        "summary": {
            "score": 0.82,
            "verdict": "warn"
        },
        "findings": [
            {
                "id": "bias_fairness",
                "title": "Bias & Fairness",
                "severity": "medium",
                "status": "warn",
                "message": "Some narrative..."
            },
            ...
        ]
    }

    Args:
        evaluation_result: Dict returned by PolicyEngine.
        settings: Optional pre-loaded settings dict. If None, load_settings()
                  is called internally.

    Returns:
        RemediationPlan object.
    """
    if settings is None:
        settings = load_settings()

    summary = evaluation_result.get("summary", {}) or {}
    findings = evaluation_result.get("findings", []) or []

    profile_id = evaluation_result.get("profile_id")
    system_id = evaluation_result.get("system_id") or evaluation_result.get("context", {}).get(
        "system_id"
    )

    plan = RemediationPlan(
        system_id=system_id,
        profile_id=profile_id,
        verdict=summary.get("verdict"),
        score=summary.get("score"),
    )

    for f in findings:
        sev = str(f.get("severity", "low")).lower()
        status = str(f.get("status", "unknown")).lower()

        # Normalize types
        sev_typed: Severity = (
            "critical" if sev == "critical"
            else "high" if sev == "high"
            else "medium" if sev == "medium"
            else "low"
        )
        status_typed: Status = (
            "fail" if status == "fail"
            else "warn" if status == "warn"
            else "pass" if status == "pass"
            else "unknown"
        )

        recommended_action = _default_recommended_action(sev_typed, status_typed)
        requires_hitl = _should_escalate_to_hitl(sev_typed, status_typed, settings)

        item = RemediationItem(
            id=str(f.get("id")),
            title=str(f.get("title", "")),
            severity=sev_typed,
            status=status_typed,
            message=str(f.get("message", "")),
            profile_id=profile_id,
            system_id=system_id,
            recommended_action=recommended_action,
            requires_hitl=requires_hitl,
            priority=_severity_rank(sev_typed),
        )
        plan.items.append(item)

    # Sort by priority (critical/high first), then by id for stability
    plan.items.sort(key=lambda i: (i.priority, i.id or ""))

    return plan


def plan_remediation(
    evaluation_result: Dict[str, Any],
    settings: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Public entrypoint for planners/services.

    Wraps build_remediation_plan() and returns a plain dict,
    convenient for JSON serialization or passing into tools.

    Example:
        from agents.planners.remediation_flow import plan_remediation

        remediation = plan_remediation(evaluation_result)
        print(remediation["items"][0]["recommended_action"])
    """
    plan = build_remediation_plan(evaluation_result, settings=settings)
    return plan.to_dict()
