"""Evidence discovery helper for 4th.GRC agents.

This module provides a small, framework-agnostic helper that builds
*evidence specifications* suitable for the 4th.GRC PolicyEngine. It is
intended to be used by agents, orchestrators, or CLI tools that want a
simple, convention-based way to locate logs, metrics, and documents
associated with a given ``system_id``.

The current implementation is intentionally conservative and file-pattern
based. It does **not** directly talk to storage or Purview; instead it
returns a list of evidence specs that the core :mod:`policyengine.evidence`
layer knows how to resolve.

High-level behavior
-------------------

- Derives blob URI patterns from a ``system_id`` using a simple folder
  convention (for example, ``evidence/<system_id>/logs/*.json``).
- Optionally appends a Purview-style evidence spec when the
  ``ENABLE_PURVIEW`` environment variable is set.
- Logs the number of discovered specs for observability.

Environment variables
---------------------

- ``LOG_LEVEL``:
    Optional log level for the module logger.
- ``ENABLE_PURVIEW``:
    If set to a truthy value (``"true"``, ``"1"``, ``"yes"`` etc.), an
    additional Purview evidence spec is appended to the returned list.

Azure SDK note
--------------

The module attempts to import :class:`azure.identity.DefaultAzureCredential`
so that future implementations can evolve into *real* Purview/ADLS discovery
without breaking imports. If the import fails, a ``None`` placeholder is
set and the helper continues to operate in a purely pattern-based mode.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger("agents.evidence_tool")
if not logger.handlers:
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# Optional Azure SDKs; keep app import-safe even when azure packages
# are not installed in the current environment.
try:  # pragma: no cover - optional dependency
    from azure.identity import DefaultAzureCredential  # noqa: F401
except Exception:  # pragma: no cover
    DefaultAzureCredential = None  # type: ignore[assignment]


def _is_truthy(value: str) -> bool:
    """Return True if the given string looks like a truthy value.

    This helper is used to interpret the ``ENABLE_PURVIEW`` environment
    variable in a flexible way, accepting common truthy strings such as
    ``"true"``, ``"1"``, or ``"yes"`` (case-insensitive).

    Args:
        value:
            Raw string read from an environment variable.

    Returns:
        ``True`` if the value appears truthy, ``False`` otherwise.
    """
    return value.lower() in {"true", "1", "yes", "y", "on"}


def discover_evidence(system_id: str, *, kinds: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Return a list of evidence specs suitable for the PolicyEngine.

    This function is designed to be predictable and easy to test. It does
    **not** attempt to contact external systems or list storage accounts.
    Instead, it emits path patterns and logical URIs that the core
    PolicyEngine evidence layer can later resolve.

    By default, the following conventions are used for the given
    ``system_id``::

        evidence/<system_id>/logs/*.json
        evidence/<system_id>/metrics/*.json
        evidence/<system_id>/docs/*.pdf

    The caller can restrict which groups of evidence are generated using
    the ``kinds`` parameter.

    Args:
        system_id:
            Logical identifier of the system under evaluation (for example,
            ``"projA:chat-001"`` or a deployment/environment ID). This is
            interpolated into the emitted path patterns.
        kinds:
            Optional list of evidence groups to include. Supported values
            are ``"logs"``, ``"metrics"``, and ``"docs"``. If omitted,
            all three groups are included.

    Returns:
        A list of evidence specifications, each a dictionary with at least
        a ``"type"`` key. For example::

            [
                {"type": "blob_uri", "pattern": "evidence/sys1/logs/*.json"},
                {"type": "blob_uri", "pattern": "evidence/sys1/metrics/*.json"},
                {"type": "blob_uri", "pattern": "evidence/sys1/docs/*.pdf"},
                {"type": "purview", "uri": "purview://assets?system=sys1"},
            ]

        The optional Purview spec is only included when ``ENABLE_PURVIEW``
        is set to a truthy value.
    """
    kinds = kinds or ["logs", "metrics", "docs"]
    results: List[Dict[str, Any]] = []

    # Simple blob folder conventions; you can adapt these to match your
    # actual storage layout (ADLS, S3, etc.).
    if "logs" in kinds:
        results.append(
            {"type": "blob_uri", "pattern": f"evidence/{system_id}/logs/*.json"}
        )
    if "metrics" in kinds:
        results.append(
            {"type": "blob_uri", "pattern": f"evidence/{system_id}/metrics/*.json"}
        )
    if "docs" in kinds:
        results.append(
            {"type": "blob_uri", "pattern": f"evidence/{system_id}/docs/*.pdf"}
        )

    # Purview placeholder – the PolicyEngine evidence layer is expected to
    # know how to interpret and resolve these URIs.
    enable_purview = os.getenv("ENABLE_PURVIEW", "false")
    if _is_truthy(enable_purview):
        results.append(
            {"type": "purview", "uri": f"purview://assets?system={system_id}"}
        )

    logger.info("Discovered %d evidence items for '%s'", len(results), system_id)
    return results
