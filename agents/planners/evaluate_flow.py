"""Evaluate flow planner — discovery → evaluation → remediation.

This module wires together three core agent-side capabilities:

1. Evidence discovery via :func:`agents.tools.evidence_tool.discover_evidence`.
2. Governance evaluation via :class:`agents.tools.policyengine_tool.PolicyEngineTool`.
3. Human-in-the-loop (HITL) escalation via :mod:`agents.tools.hitl_tool`.

Typical use cases
-----------------
- CLI-driven evaluations of a given ``system_id`` against a specific
  governance profile.
- Batch jobs that periodically sweep systems and escalate failures.
- Orchestrator hooks that want a single call to "do the right thing":
  discover evidence, evaluate, and route failures to human review.

Environment variables
---------------------
- ``POLICYENGINE_URL`` (optional)
    Base URL of the PolicyEngine service. If omitted, the default from
    :class:`PolicyEngineTool` is used.
- ``JIRA_PROJECT`` (optional)
    Default Jira project key used when creating tickets for failed
    findings. Defaults to ``"GRC"`` when not set.
- ``LOG_LEVEL`` (optional)
    Log level for this module's logger. Defaults to ``"INFO"``.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

from agents.tools.policyengine_tool import PolicyEngineTool
from agents.tools.evidence_tool import discover_evidence
from agents.tools.hitl_tool import notify_teams, create_jira_ticket

logger = logging.getLogger("agents.evaluate_flow")
if not logger.handlers:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))


def plan_and_run(
    system_id: str,
    profile_ref: str,
    *,
    controls: Optional[List[str]] = None,
    extra_evidence: Optional[List[Dict[str, Any]]] = None,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Discover evidence, evaluate with PolicyEngine, and route remediation.

    High-level flow:

    1. Discover evidence for ``system_id`` via :func:`discover_evidence`.
    2. Merge any caller-provided ``extra_evidence`` with the discovered set.
    3. Build a ``target`` payload and invoke :class:`PolicyEngineTool`.
    4. Inspect the resulting findings:
       - If any have ``status == "fail"``, trigger HITL actions:
         * Send a summary to Teams via :func:`notify_teams`.
         * Open a Jira ticket via :func:`create_jira_ticket`.
       - Otherwise, log that no HITL actions were required.

    Args:
        system_id:
            Logical identifier of the system being evaluated (for example,
            a deployment, environment, or application ID). This value is
            passed through as part of the ``target`` and used by
            :func:`discover_evidence` to build evidence patterns.
        profile_ref:
            Governance profile reference, typically including a version,
            e.g. ``"iso_42001-global@1.2.0"``. This is forwarded directly
            to the PolicyEngine.
        controls:
            Optional subset of ``control_id`` values to evaluate. If
            omitted, the engine will run all controls defined by the
            profile.
        extra_evidence:
            Optional list of additional evidence specifications. These are
            appended to the automatically discovered evidence before the
            evaluation request is sent.
        params:
            Optional dictionary of parameter overrides for the profile and
            rule operations. If omitted, an empty dict is used.

    Returns:
        The parsed evaluation result as a dictionary, typically matching
        :class:`policyengine.schema.EvalResponse` in structure. For
        example, you can expect keys such as ``summary``, ``findings``,
        and ``attestations`` in a successful response.

    Notes:
        - HITL routing is deliberately simple in this reference
          implementation: any finding with ``status == "fail"`` triggers
          Teams and Jira calls (subject to environment configuration).
        - Errors in HITL integrations are logged but do not prevent the
          evaluation result from being returned to the caller.
    """
    logger.info(
        "Starting evaluation flow for system_id='%s', profile_ref='%s'",
        system_id,
        profile_ref,
    )

    # 1) Discover evidence for this system_id
    discovered = discover_evidence(system_id)
    logger.info("Discovered %d evidence items for system '%s'", len(discovered), system_id)

    # 2) Merge with any caller-provided evidence
    evidence = (extra_evidence or []) + discovered
    logger.debug("Total evidence items after merge: %d", len(evidence))

    # 3) Call PolicyEngine via the HTTP tool wrapper
    target = {"system_id": system_id, "request_id": f"{system_id}-eval"}
    engine = PolicyEngineTool(os.getenv("POLICYENGINE_URL"))
    result = engine.run(
        profile_ref,
        controls=controls,
        target=target,
        evidence=evidence,
        params=params or {},
    )

    # 4) Basic remediation routing based on findings
    findings = result.get("findings", [])
    failed = [f for f in findings if f.get("status") == "fail"]
    if failed:
        logger.warning("Found %d failed findings; routing to HITL", len(failed))
        # HITL notifications are best-effort; failures are logged but do not
        # cause the overall evaluation to fail.
        try:
            notify_teams(failed)
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("Teams notify failed: %s", exc)

        try:
            jira_project = os.getenv("JIRA_PROJECT", "GRC")
            create_jira_ticket(
                jira_project,
                "4th.GRC: governance failures detected",
                json.dumps(failed[:5], indent=2),
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.exception("Jira create failed: %s", exc)
    else:
        logger.info("No failed findings — no HITL actions created.")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Run a one-shot evaluation flow for a given system_id and profile_ref. "
            "This will discover evidence, call the PolicyEngine service, and, "
            "if failures are detected, route basic HITL actions (Teams + Jira)."
        )
    )
    parser.add_argument(
        "--system",
        required=True,
        help="system_id to evaluate (e.g. 'projA:chat-001')",
    )
    parser.add_argument(
        "--profile",
        required=True,
        help="profile_ref to evaluate against (e.g. 'iso_42001-global@1.2.0')",
    )
    parser.add_argument(
        "--controls",
        nargs="*",
        help="optional subset of control_ids to evaluate; if omitted, all controls are run",
    )

    args = parser.parse_args()
    output = plan_and_run(args.system, args.profile, controls=args.controls)
    print(json.dumps(output, indent=2))
