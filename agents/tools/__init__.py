"""
agents.tools

Tool adapters for the 4th.GRC agentic toolkit.

This package includes:

- PolicyEngine client
- Evidence discovery helpers
- Human-in-the-loop (HITL) escalation helpers
- Semantic Kernel plugin for PolicyEngine

Typical usage:

    from agents.tools import (
        PolicyEngineTool,
        discover_evidence,
        notify_teams,
        create_jira_issue,
        create_servicenow_incident,
        PolicyEnginePlugin,
    )

    tool = PolicyEngineTool()
    evidence = discover_evidence(system_id="demo-llm-system")
"""

from __future__ import annotations

# Explicit re-exports for convenience. If any import fails (e.g., during partial
# refactors), we fail loudly instead of silently hiding problems.

from .policyengine_tool import PolicyEngineTool
from .evidence_tool import discover_evidence
from .hitl_tool import (
    notify_teams,
    create_jira_issue,
    create_servicenow_incident,
)
from .sk_policyengine_plugin import PolicyEnginePlugin

__all__ = [
    "PolicyEngineTool",
    "discover_evidence",
    "notify_teams",
    "create_jira_issue",
    "create_servicenow_incident",
    "PolicyEnginePlugin",
]
