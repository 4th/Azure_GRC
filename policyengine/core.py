# C:\4th\4th.GRC\policyengine\core.py

from __future__ import annotations

from typing import Any, Dict, List

from .exceptions import EvaluationError, ProfileNotFoundError
from .models import Finding
from .profiles import load_profile_by_ref
from .rules_engine import run_rules
from .schema import PolicyProfile


def evaluate(
    profile_ref: str,
    context: Dict[str, Any],
    evidence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Core evaluation entrypoint used by:
    - services/policyengine_svc/main.py (FastAPI)
    - scripts/run_agentic_demo.py
    - any external tools calling PolicyEngine

    It loads the profile, runs all rules, and returns a dict that matches
    the EvalResponse schema.
    """
    try:
        profile: PolicyProfile = load_profile_by_ref(profile_ref)
    except ProfileNotFoundError as exc:
        # Re-raise so API layer can turn into a 404
        raise
    except Exception as exc:  # noqa: BLE001
        # Wrap anything else as an EvaluationError
        raise EvaluationError(
            f"Failed to load profile '{profile_ref}': {exc}"
        ) from exc

    # Run rules for this profile
    findings: List[Finding] = run_rules(
        profile=profile,
        context=context or {},
        evidence=evidence or {},
    )

    finding_count = len(findings)

    # Simple scoring: all pass => 1.0, any warn/fail => 0.8/0.5, etc.
    # For now, keep it trivial but deterministic.
    if not findings:
        # No findings -> treat as neutral/pass with full score
        verdict = "pass"
        score = 1.0
    else:
        severities = {f.severity for f in findings}
        statuses = {f.status for f in findings}

        if "fail" in statuses:
            verdict = "fail"
            score = 0.5
        elif "warn" in statuses:
            verdict = "warn"
            score = 0.8
        else:
            verdict = "pass"
            score = 1.0

    summary: Dict[str, Any] = {
        "profile_ref": profile_ref,
        "profile_id": profile.profile_id,
        "version": profile.version,
        "verdict": verdict,
        "score": score,
        "finding_count": finding_count,
    }

    # IMPORTANT: Top-level keys must match EvalResponse
    return {
        "profile_ref": profile_ref,
        "profile_id": profile.profile_id,
        "version": profile.version,
        "summary": summary,
        "findings": findings,
    }
