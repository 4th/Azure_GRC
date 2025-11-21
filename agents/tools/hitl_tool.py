"""Human-in-the-loop (HITL) workflow helpers for 4th.GRC agents.

This module defines a set of **side-effect tools** that an agent can call
when a governance evaluation indicates that *human review or escalation is
required*. The helpers are intentionally thin wrappers around external
systems and are designed to be used from orchestration code, LangChain
tools, or Semantic Kernel plugins.

Currently supported targets
---------------------------

- **Microsoft Teams** via an incoming webhook.
- **Jira** via the REST API.
- **ServiceNow** via the incident table API.

All functions are safe to import even when the ``requests`` library is not
installed. In that case, they operate in a **dry-run mode**, returning the
payload that *would* have been sent instead of making an HTTP call. This
is useful for local development, unit tests, or air-gapped environments.

Environment variables
---------------------

- ``TEAMS_WEBHOOK_URL``:
    Incoming webhook URL for the Microsoft Teams channel that should
    receive summarized findings.
- ``JIRA_API_BASE``:
    Base URL for your Jira instance (for example,
    ``"https://your-org.atlassian.net"``).
- ``JIRA_TOKEN``:
    Bearer token or API token used to authenticate against Jira.
- ``SERVICENOW_BASE``:
    Base URL for your ServiceNow instance (for example,
    ``"https://your-instance.service-now.com"``).
- ``SERVICENOW_TOKEN``:
    Bearer token or other credential used to call the ServiceNow API.

Usage patterns
--------------

These helpers are typically invoked **after** a call to the PolicyEngine
has produced an ``EvalResponse``. For example, if a high-severity failure
is detected, an agent might:

1. Summarize the findings.
2. Call :func:`notify_teams` to alert a channel.
3. Call :func:`create_jira_ticket` or :func:`create_servicenow_incident`
   to open a tracking item for remediation.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

try:  # pragma: no cover - optional dependency
    import requests
except Exception:  # pragma: no cover
    requests = None

logger = logging.getLogger("agents.hitl_tool")
if not logger.handlers:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK_URL")
JIRA_API_BASE = os.getenv("JIRA_API_BASE")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
SERVICENOW_BASE = os.getenv("SERVICENOW_BASE")
SERVICENOW_TOKEN = os.getenv("SERVICENOW_TOKEN")


def _post(url: str, payload: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """POST a JSON payload to an external system with optional headers.

    If the :mod:`requests` library is not available, the call is not
    executed and a dry-run structure is returned instead.

    Args:
        url:
            Target URL to POST to.
        payload:
            JSON-serializable dictionary to send in the request body.
        headers:
            Optional HTTP headers to include with the request.

    Returns:
        A dictionary summarizing the outcome. In normal operation this
        includes the HTTP status code and a truncated response text. In
        dry-run mode, it contains the target URL and payload only.
    """
    if not requests:
        logger.warning("requests not installed; returning dry-run for %s", url)
        return {"dry_run": True, "url": url, "payload": payload, "headers": headers or {}}

    logger.info("HITL POST %s", url)
    logger.debug("HITL payload: %s", json.dumps(payload, indent=2))
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    return {"status_code": r.status_code, "text": r.text[:200]}


def notify_teams(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Send a summarized view of findings to a Microsoft Teams channel.

    This helper expects a list of finding-like dictionaries, each containing
    at least ``control_id`` and ``status`` keys (and optionally
    ``rationale``). It will render a simple Markdown-style bulleted list
    of the first 10 findings and POST it to the Teams webhook URL defined
    by ``TEAMS_WEBHOOK_URL``.

    Args:
        findings:
            A list of findings, typically taken from
            ``EvalResponse.findings``. Only the first 10 are included in
            the message body to keep the notification concise.

    Returns:
        A dictionary representing the outcome of the POST, or a structure
        indicating that the call was skipped or executed in dry-run mode.
    """
    if not TEAMS_WEBHOOK:
        logger.info("TEAMS_WEBHOOK_URL not set; skipping Teams notification")
        return {"skipped": "TEAMS_WEBHOOK_URL not set"}

    lines = []
    for f in findings[:10]:
        cid = f.get("control_id", "<unknown-control>")
        status = f.get("status", "<no-status>")
        rationale = f.get("rationale", "")
        lines.append(f"- {cid} [{status}]: {rationale}")

    text = "\n".join(lines) or "(no findings available)"
    payload = {"text": f"4th.GRC Findings (top 10):\n{text}"}
    return _post(TEAMS_WEBHOOK, payload)


def create_jira_ticket(project_key: str, summary: str, description: str) -> Dict[str, Any]:
    """Create a Jira issue for follow-up on governance findings.

    This helper uses the Jira REST API to create a simple ``Task`` issue.
    Authentication and base URL are derived from the environment.

    Args:
        project_key:
            Jira project key (for example, ``\"GRC\"``).
        summary:
            Short summary/title for the issue.
        description:
            Longer description body. This is a good place to embed a
            serialized subset of findings or a link to full evaluation
            details.

    Returns:
        A dictionary summarizing the outcome of the Jira API call, or a
        structure explaining why the call was skipped or executed in
        dry-run mode.
    """
    if not (JIRA_API_BASE and JIRA_TOKEN):
        logger.info("Jira env not set; skipping ticket creation")
        return {"skipped": "JIRA_API_BASE or JIRA_TOKEN not set"}

    url = JIRA_API_BASE.rstrip("/") + "/rest/api/3/issue"
    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,
            "issuetype": {"name": "Task"},
        }
    }
    headers = {"Authorization": f"Bearer {JIRA_TOKEN}"}

    if not requests:  # pragma: no cover - runtime fallback
        logger.warning("requests not installed; returning Jira dry-run for %s", url)
        return {"dry_run": True, "url": url, "payload": payload, "headers": headers}

    logger.info("Creating Jira issue in project %s", project_key)
    logger.debug("Jira payload: %s", json.dumps(payload, indent=2))
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    return {"status_code": r.status_code, "text": r.text[:200]}


def create_servicenow_incident(short_description: str, description: str) -> Dict[str, Any]:
    """Create a ServiceNow incident for governance-related issues.

    This helper opens an incident in ServiceNow's ``incident`` table using
    the configured base URL and token.

    Args:
        short_description:
            One-line description of the incident.
        description:
            Detailed description, often including evaluation context,
            affected systems, and a link to the full report.

    Returns:
        A dictionary summarizing the outcome of the ServiceNow API call, or
        a structure explaining why the call was skipped or executed in
        dry-run mode.
    """
    if not (SERVICENOW_BASE and SERVICENOW_TOKEN):
        logger.info("ServiceNow env not set; skipping incident creation")
        return {"skipped": "SERVICENOW_BASE or SERVICENOW_TOKEN not set"}

    url = SERVICENOW_BASE.rstrip("/") + "/api/now/table/incident"
    payload = {
        "short_description": short_description,
        "description": description,
    }
    headers = {"Authorization": f"Bearer {SERVICENOW_TOKEN}"}

    if not requests:  # pragma: no cover - runtime fallback
        logger.warning("requests not installed; returning ServiceNow dry-run for %s", url)
        return {"dry_run": True, "url": url, "payload": payload, "headers": headers}

    logger.info("Creating ServiceNow incident")
    logger.debug("ServiceNow payload: %s", json.dumps(payload, indent=2))
    r = requests.post(url, json=payload, headers=headers, timeout=20)
    return {"status_code": r.status_code, "text": r.text[:200]}
