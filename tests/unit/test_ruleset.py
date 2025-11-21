"""Legacy ruleset tests for the old PolicyEngine API.

This module used to test `policyengine.ruleset` and functions like
`fairness_threshold`, which are no longer part of the new core design.

The new rules are covered under:
    - tests/unit/test_rules/

So this file is kept only as a historical placeholder and is skipped.
"""

from __future__ import annotations

import pytest

pytest.skip(
    "Legacy ruleset tests (policyengine.ruleset) are not applicable to the new engine.",
    allow_module_level=True,
)
