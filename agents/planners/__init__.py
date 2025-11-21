"""
agents.planners

Planner utilities for the 4th.GRC agentic toolkit.

Planners orchestrate:
- Evidence discovery
- PolicyEngine evaluation
- Optional human-in-the-loop (HITL) escalation

Currently provided:

- `plan_and_run` – end-to-end evaluation flow for a single system/profile

Example:

    from agents.planners import plan_and_run

    result = plan_and_run(
        system_id="demo-llm-system",
        profile_ref="iso_42001-global@1.2.0",
    )

    print(result.get("summary", {}))
"""

from __future__ import annotations

from .evaluate_flow import plan_and_run

__all__ = [
    "plan_and_run",
]
