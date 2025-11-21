"""Agent tool wrapper for calling the 4th.GRC PolicyEngine HTTP API.

This module provides a lightweight, synchronous helper class,
:class:`PolicyEngineTool`, which wraps the PolicyEngine ``/v1/evaluate``
endpoint. It is designed to be used by agent frameworks (LangChain tools,
custom orchestrators, CLI scripts, etc.) that want a simple way to run a
governance evaluation from Python.

High-level behavior
-------------------

* Constructs a payload compatible with :class:`policyengine.schema.EvalRequest`.
* POSTs the payload to the configured PolicyEngine service endpoint.
* Returns the decoded JSON body (which should conform to
  :class:`policyengine.schema.EvalResponse`).

If the optional ``requests`` dependency is not available, the tool operates
in a **dry-run** mode and returns the would-be request payload instead of
performing an HTTP call. This can be useful for local testing, debugging,
or environments where outbound HTTP is not yet configured.

Environment variables
---------------------

- ``POLICYENGINE_URL`` (optional):
    Base URL for the PolicyEngine ``/v1/evaluate`` endpoint. Defaults to
    ``"http://localhost:8080/v1/evaluate"`` if not set. If a base URL
    without the path is provided, the tool will append ``/v1/evaluate``.
- ``APIM_SUBSCRIPTION_KEY`` or ``OCP_APIM_SUBSCRIPTION_KEY`` (optional):
    If set, the value is sent as the ``Ocp-Apim-Subscription-Key`` header
    on each request. This is commonly used when the service is fronted by
    Azure API Management (APIM).
- ``POLICYENGINE_BEARER`` (optional):
    If set, the tool will send an ``Authorization: Bearer <token>`` header
    on each request, suitable for JWT-based protection in front of the
    PolicyEngine service.
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

# Module-level logger for all agent-side PolicyEngine calls
logger = logging.getLogger("agents.policyengine_tool")
if not logger.handlers:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# Default endpoint for the PolicyEngine service
POLICYENGINE_URL = os.getenv("POLICYENGINE_URL", "http://localhost:8080/v1/evaluate")

# Optional APIM subscription key and bearer token
APIM_SUBSCRIPTION_KEY = os.getenv("APIM_SUBSCRIPTION_KEY") or os.getenv(
    "OCP_APIM_SUBSCRIPTION_KEY"
)
POLICYENGINE_BEARER = os.getenv("POLICYENGINE_BEARER")


class PolicyEngineTool:
    """Synchronous wrapper for the PolicyEngine ``/v1/evaluate`` HTTP API.

    This class is intentionally minimal and framework-agnostic. It can be
    wired into LangChain ``Tool`` objects, custom agent frameworks, or even
    simple scripts that want to invoke a governance check.

    Attributes:
        name: Logical name for the tool, suitable for agent registries.
        description: Short human-readable description of what the tool does.

    Args:
        base_url:
            Base URL for the PolicyEngine evaluation endpoint. If the URL
            does not already end with ``/v1/evaluate``, the constructor will
            append that path segment automatically.
    """

    name = "policyengine.evaluate"
    description = "Run a policy evaluation against a YAML profile and evidence."

    def __init__(self, base_url: Optional[str] = None) -> None:
        self.base_url = base_url or POLICYENGINE_URL
        if not self.base_url.endswith("/v1/evaluate"):
            self.base_url = self.base_url.rstrip("/") + "/v1/evaluate"

    def _headers(self) -> Dict[str, str]:
        """Build HTTP headers for a call to the PolicyEngine service.

        Returns:
            A dictionary of HTTP headers, including content type and any
            APIM / bearer token configuration derived from environment
            variables.
        """
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if APIM_SUBSCRIPTION_KEY:
            headers["Ocp-Apim-Subscription-Key"] = APIM_SUBSCRIPTION_KEY
        if POLICYENGINE_BEARER:
            headers["Authorization"] = f"Bearer {POLICYENGINE_BEARER}"
        return headers

    def run(
        self,
        profile_ref: str,
        *,
        controls: Optional[List[str]] = None,
        target: Optional[Dict[str, Any]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute a governance evaluation via the PolicyEngine service.

        This method constructs an evaluation request payload and performs
        an HTTP POST to the configured ``/v1/evaluate`` endpoint. It is
        synchronous by design and uses the ``requests`` library if
        available.

        Args:
            profile_ref:
                Profile reference string, e.g. ``"iso_42001-global@1.2.0"``.
                This should typically include an explicit version suffix.
            controls:
                Optional subset of ``control_id`` values to run. If omitted,
                the PolicyEngine will evaluate all controls defined in the
                profile.
            target:
                Arbitrary metadata about the system under evaluation. This
                dictionary is passed through as ``target`` in the request
                payload. If it contains a ``"request_id"`` key, that value
                will be used as the top-level ``request_id``; otherwise a
                default value of ``"agents-run"`` is used.
            evidence:
                Optional list of evidence specifications (``json``, ``inline``,
                ``blob_uri``, or ``purview``). These are forwarded directly
                and resolved by the PolicyEngine evidence layer.
            params:
                Optional dictionary of parameter overrides used by the
                profile and rule operations.

        Returns:
            A dictionary parsed from the JSON response body. In normal
            operation, this should conform to the structure of an
            ``EvalResponse`` from :mod:`policyengine.schema`. If the
            ``requests`` library is not available, a "dry-run" structure
            is returned instead::

                {
                    "dry_run": True,
                    "url": "...",
                    "payload": {...}
                }

        Raises:
            requests.HTTPError:
                If the HTTP response signals an error status and the
                ``requests`` library is available.
        """
        request_id = (target or {}).get("request_id", "agents-run")
        payload: Dict[str, Any] = {
            "request_id": request_id,
            "profile_ref": profile_ref,
            "controls": controls,
            "target": target or {},
            "evidence": evidence or [],
            "params": params or {},
        }

        logger.info("PolicyEngine POST %s", self.base_url)
        logger.debug("PolicyEngine payload: %s", json.dumps(payload, indent=2))

        # If requests is not installed, return a dry-run structure useful for debugging.
        if requests is None:  # pragma: no cover - runtime fallback
            logger.warning(
                "requests is not available; returning payload only (dry-run mode)"
            )
            return {"dry_run": True, "url": self.base_url, "payload": payload}

        response = requests.post(
            self.base_url, headers=self._headers(), json=payload, timeout=45
        )
        response.raise_for_status()
        return response.json()
