"""
agents

Agentic toolkit for the 4th.GRC platform.

This package provides:
- Config-driven agent profiles (see configs/agent_profiles.yaml)
- Tool adapters for PolicyEngine, evidence discovery, and HITL escalation
- Planners that orchestrate end-to-end evaluation flows

Typical usage:

    from agents.planners.evaluate_flow import plan_and_run

    result = plan_and_run(
        system_id="demo-llm-system",
        profile_ref="iso_42001-global@1.2.0",
    )

    print(result["summary"])
"""

from importlib import metadata

# Package version (falls back gracefully if not installed as a distribution)
try:
    __version__ = metadata.version("agents")  # if packaged
except Exception:  # pragma: no cover
    __version__ = "0.1.0-dev"

__all__ = [
    "__version__",
]
