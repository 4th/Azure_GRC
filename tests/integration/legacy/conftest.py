from __future__ import annotations

import pytest

# Skip the entire legacy integration suite under the new engine
pytestmark = pytest.mark.skip(
    reason="Legacy integration tests (old PolicyEngine API) – skipped under new core."
)
