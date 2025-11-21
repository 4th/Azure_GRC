"""Semantic Kernel plugin for calling the 4th.GRC PolicyEngine service.

This plugin provides a thin, async wrapper around the 4th.GRC PolicyEngine
HTTP API so that Semantic Kernel (SK) planners and orchestrators can request
governance evaluations as part of an agentic workflow.

Key features
------------
- Exposes a single `evaluate` kernel function that SK can invoke.
- Supports direct service calls or Azure API Management (APIM) as a front door.
- Uses configurable timeouts and retries, suitable for production use.
- Reads configuration from environment variables where possible.

Environment variables
---------------------
- ``POLICYENGINE_URL`` (optional):
    Base URL to POST an EvalRequest to. Defaults to
    ``http://localhost:8080/v1/evaluate``.
- ``APIM_SUBSCRIPTION_KEY`` or ``OCP_APIM_SUBSCRIPTION_KEY`` (optional):
    APIM subscription key. If set, it is sent as the
    ``Ocp-Apim-Subscription-Key`` header.
- ``POLICYENGINE_BEARER`` (optional):
    Bearer token (JWT) to use for the ``Authorization`` header. The plugin
    will prepend ``"Bearer "`` when building the header.

Example
-------
Typical usage inside an SK planner/orchestrator::

    plugin = PolicyEnginePlugin()
    kernel.import_plugin(plugin, plugin_name="policy")

    result_json = await kernel.plugins["policy"]["evaluate"].invoke_async(
        system_id="projA:chat-001",
        profile_ref="iso_42001-global@1.2.0",
        evidence_prefix="foundry/projA/chat-001",
        params_json='{"min_score": 0.85}',
    )

The ``profile_ref`` should usually be of the form ``"<id>@<version>"``
(e.g., ``"iso_42001-global@1.2.0"``), matching the expectations of the
underlying PolicyEngine.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional

import httpx
from semantic_kernel.functions import kernel_function

logger = logging.getLogger("agents.sk_policyengine_plugin")


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return a trimmed environment variable value, or a default if unset."""
    raw = os.environ.get(name)
    if raw is None:
        return default
    value = raw.strip()
    return value or default


class PolicyEnginePlugin:
    """Semantic Kernel plugin for the 4th.GRC PolicyEngine service.

    This class exposes a single kernel function, :meth:`evaluate`, which
    posts an EvalRequest payload to the PolicyEngine HTTP endpoint.

    Args:
        url:
            Base URL for the PolicyEngine ``/v1/evaluate`` endpoint. If
            omitted, the value of ``POLICYENGINE_URL`` is used, defaulting
            to ``"http://localhost:8080/v1/evaluate"``.
        subscription_key:
            Optional APIM subscription key. If omitted, the plugin will look
            for ``APIM_SUBSCRIPTION_KEY`` and ``OCP_APIM_SUBSCRIPTION_KEY``.
        bearer_token:
            Optional bearer token (without the ``"Bearer "`` prefix) to include
            in the ``Authorization`` header. If omitted, the plugin will look
            for ``POLICYENGINE_BEARER``.
        timeout_seconds:
            Request timeout in seconds for HTTP calls.
        max_retries:
            Maximum number of retry attempts on timeout/HTTP errors.
        backoff_seconds:
            Base backoff interval used for exponential backoff between retries.

    Notes:
        The payload schema sent over the wire matches
        :class:`policyengine.schema.EvalRequest`:

        .. code-block:: json

            {
              "request_id": "sk-<system_id>",
              "profile_ref": "<id>@<version>",
              "target": { "system_id": "<system_id>" },
              "evidence": [ ... ],
              "params": { ... }
            }
    """

    def __init__(
        self,
        url: Optional[str] = None,
        subscription_key: Optional[str] = None,
        bearer_token: Optional[str] = None,
        timeout_seconds: float = 60.0,
        max_retries: int = 3,
        backoff_seconds: float = 0.6,
    ) -> None:
        self.url = url or _env("POLICYENGINE_URL", "http://localhost:8080/v1/evaluate")
        # Accept common env names for APIM key
        self.subscription_key = (
            subscription_key
            or _env("APIM_SUBSCRIPTION_KEY")
            or _env("OCP_APIM_SUBSCRIPTION_KEY")
        )
        self.bearer_token = bearer_token or _env("POLICYENGINE_BEARER")
        self.timeout = float(timeout_seconds)
        self.max_retries = int(max_retries)
        self.backoff = float(backoff_seconds)

        logger.debug(
            "PolicyEnginePlugin initialized url=%s, timeout=%s, max_retries=%s",
            self.url,
            self.timeout,
            self.max_retries,
        )

    def _headers(self) -> Dict[str, str]:
        """Build HTTP headers for a request to PolicyEngine."""
        headers: Dict[str, str] = {"Content-Type": "application/json"}
        if self.subscription_key:
            headers["Ocp-Apim-Subscription-Key"] = self.subscription_key
        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        return headers

    async def _post_json(self, payload: Dict[str, Any]) -> str:
        """POST a JSON payload to PolicyEngine with retries.

        Args:
            payload:
                JSON-serializable dictionary to send in the request body.

        Returns:
            The raw response text (JSON string) from the PolicyEngine service.

        Raises:
            httpx.TimeoutException:
                If all retry attempts ultimately fail due to timeouts.
            httpx.HTTPError:
                If all retry attempts fail with HTTP errors.
        """
        last_exc: Optional[BaseException] = None
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.debug(
                        "Posting EvalRequest to PolicyEngine attempt=%d url=%s",
                        attempt,
                        self.url,
                    )
                    resp = await client.post(
                        self.url,
                        headers=self._headers(),
                        json=payload,
                    )
                    resp.raise_for_status()
                    logger.debug(
                        "PolicyEngine response status=%d, bytes=%d",
                        resp.status_code,
                        len(resp.content or b""),
                    )
                    return resp.text  # JSON string
                except (httpx.TimeoutException, httpx.HTTPError) as exc:
                    last_exc = exc
                    logger.warning(
                        "PolicyEngine call failed attempt=%d/%d: %s",
                        attempt,
                        self.max_retries,
                        exc,
                    )
                    if attempt >= self.max_retries:
                        break
                    # Exponential backoff (no jitter to keep behavior predictable)
                    delay = self.backoff * (2 ** (attempt - 1))
                    logger.debug("Sleeping for %.2f seconds before retry", delay)
                    await asyncio.sleep(delay)

        if last_exc:
            logger.error("PolicyEngine call exhausted retries: %s", last_exc)
            raise last_exc
        raise RuntimeError("Unknown error posting to PolicyEngine")

    @kernel_function(
        name="evaluate",
        description=(
            "Evaluate a system against a governance profile using the 4th.GRC PolicyEngine. "
            "Arguments: system_id, profile_ref, evidence_prefix (optional), params_json (optional JSON), "
            "request_id (optional). Returns JSON string (EvalResponse) from PolicyEngine."
        ),
    )
    async def evaluate(
        self,
        system_id: str,
        profile_ref: str,
        evidence_prefix: str = "",
        params_json: str = "{}",
        request_id: Optional[str] = None,
    ) -> str:
        """Post an EvalRequest to the PolicyEngine service.

        Parameters:
            system_id:
                Target system identifier (e.g., ``"projA:chat-001"``).
            profile_ref:
                Profile reference (e.g., ``"iso_42001-global@1.2.0"``). It is
                recommended to include an explicit version suffix.
            evidence_prefix:
                Optional blob prefix or path segment used to build evidence
                URIs (for example, ``"foundry/projA/chat-001"``). If provided,
                the plugin emits a small set of conventional evidence patterns
                that the PolicyEngine evidence layer can resolve.
            params_json:
                Optional JSON string of extra parameters passed through as
                ``params`` in the EvalRequest. Must be valid JSON if provided.
            request_id:
                Optional request id. If omitted, defaults to ``"sk-<system_id>"``.

        Returns:
            JSON string representing :class:`policyengine.schema.EvalResponse`
            as returned by the PolicyEngine service.

        Raises:
            ValueError:
                If ``params_json`` cannot be parsed as valid JSON.
            httpx.TimeoutException or httpx.HTTPError:
                If the underlying HTTP request ultimately fails after retries.
        """
        logger.info(
            "SK PolicyEngine evaluate invoked system_id='%s', profile_ref='%s'",
            system_id,
            profile_ref,
        )

        try:
            params: Dict[str, Any] = json.loads(params_json) if params_json else {}
        except json.JSONDecodeError as exc:
            logger.error("Invalid params_json: %s", exc)
            raise ValueError(f"params_json must be valid JSON: {exc}") from exc

        evidence: List[Dict[str, Any]] = []
        if evidence_prefix:
            # Default evidence mapping; customize per your profile if needed.
            # These are resolved by the PolicyEngine evidence layer.
            evidence = [
                {
                    "type": "blob_uri",
                    "pattern": f"{evidence_prefix}/evals/*-bias.json",
                },
                {
                    "type": "blob_uri",
                    "pattern": f"{evidence_prefix}/evals/*-safety.json",
                },
                # Additional patterns could be added here, e.g.:
                # {"type": "blob_uri", "pattern": f"{evidence_prefix}/traces/*.json"},
                # {"type": "blob_uri", "pattern": f"{evidence_prefix}/lifecycle/*.json"},
            ]
            logger.debug(
                "Constructed %d evidence patterns from prefix '%s'",
                len(evidence),
                evidence_prefix,
            )

        payload: Dict[str, Any] = {
            "request_id": request_id or f"sk-{system_id}",
            "profile_ref": profile_ref,
            "target": {"system_id": system_id},
            "evidence": evidence,
            "params": params,
        }

        logger.debug("EvalRequest payload: %s", payload)
        return await self._post_json(payload)
