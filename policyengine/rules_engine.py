from __future__ import annotations

from typing import Any, Dict, List

from .models import Finding
from .schema import PolicyProfile
from .utils import normalize_severity, normalize_status


def evaluate_rule(
    rule_id: str,
    params: Dict[str, Any],
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Finding | None:
    """
    Placeholder for actual rule evaluation logic.

    For now, we implement a trivial demo behavior:
    - If context["system_name"] contains "demo", return a 'pass'
    - Otherwise, return a 'warn' to show something happened.
    """

    system_name = context.get("system_name") or context.get("system_id") or "unknown-system"
    severity = params.get("severity", "medium")

    if "demo" in str(system_name).lower():
        status = "pass"
        message = f"Rule {rule_id} passed for system '{system_name}'."
    else:
        status = "warn"
        message = f"Rule {rule_id} produced a warning for system '{system_name}'."

    return Finding(
        id=rule_id,
        title=params.get("title") or f"Rule {rule_id}",
        severity=normalize_severity(severity),
        status=normalize_status(status),
        message=message,
        data={"system": system_name, "params": params},
    )


def run_rules(
    profile: PolicyProfile,
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> List[Finding]:
    """
    Run all rules in a profile and return a list of findings.

    Real implementation would:
    - Map rule.id to a concrete rule function
    - Use rule.params for thresholds, fields, etc.
    - Use evidence to perform checks
    """
    findings: List[Finding] = []

    for rule_ref in profile.rules:
        params = dict(rule_ref.params)
        params.setdefault("severity", "medium")
        params.setdefault("title", f"Rule {rule_ref.id}")

        finding = evaluate_rule(
            rule_id=rule_ref.id,
            params=params,
            context=context,
            evidence=evidence,
        )
        if finding is not None:
            findings.append(finding)

    return findings
