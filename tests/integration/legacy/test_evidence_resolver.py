"""Integration test — evidence resolver pipeline (legacy).

This test exercises :func:`policyengine.evidence.resolve` with a mix of
evidence specification types to ensure that:

- The function accepts a heterogeneous list of evidence specs.
- A list is returned.
- The number of resolved items matches the number of input specs.

The goal is not to fully unit-test the resolver internals here (that
belongs in unit tests), but to verify that the "happy path" works when
called the way agents and profiles actually use it.

This legacy test is skipped by default under the new PolicyEngine core.
"""

from __future__ import annotations

from typing import Any, Dict, List

import pytest

from policyengine.evidence import resolve

# Mark this whole file as legacy / skipped
pytestmark = pytest.mark.skip(
    reason="Legacy test; evidence.resolve not implemented in the new engine yet."
)


@pytest.mark.integration
def test_resolve_mixed_evidence_types() -> None:
    """Resolve a mix of inline, JSON, blob, and Purview evidence specs."""
    specs: List[Dict[str, Any]] = [
        {"type": "inline", "payload": {"a": 1}},
        {"type": "json", "payload": {"b": 2}},
        {"type": "blob_uri", "uri": "https://example.com/blob.json"},
        {"type": "purview", "uri": "purview://asset/id"},
    ]

    out = resolve(specs)

    # Basic shape checks
    assert isinstance(out, list), "resolve() should return a list"
    assert len(out) == len(specs), "resolver should return one item per spec"

    # Optional lightweight sanity checks that should be robust across implementations
    for item in out:
        assert isinstance(item, dict), "each resolved evidence item should be a dict"
        assert item, "resolved evidence items should not be empty"
