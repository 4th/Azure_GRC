# 4th.GRC Test Suite

This directory contains the automated tests for the **4th.GRC PolicyEngine**,
its HTTP service, and the supporting agent tooling.

Tests are written with **pytest** and are organized into:

- **Unit tests** – fast, isolated tests for core modules
- **Integration tests** – slower, multi-component tests (engine + service + agents)

---

## 1. Quick Start

From the **repo root**:

```bash
# Run all tests (unit + integration)
pytest
```

By default, pytest will:

- Look for tests under `tests/`
- Collect coverage for the `policyengine` package
- Fail fast on the first error (`--maxfail=1`)

(These defaults are configured in `pytest.ini`.)

---

## 2. Unit vs Integration Tests

### Unit Tests

**Goal:** Verify individual functions/modules in isolation.

Typical locations:

- `tests/unit/test_engine.py`
- `tests/unit/test_ruleset.py`
- `tests/unit/test_evidence.py`
- `tests/unit/test_validators.py`

Typical characteristics:

- Use in-memory fixtures (`temp_repo`, `sample_profile_iso42001`, etc.)
- Do **not** require a running HTTP service
- Run quickly and deterministically

Run only unit tests (i.e., everything **not** marked as integration):

```bash
pytest -m "not integration"
```

---

### Integration Tests

**Goal:** Exercise multiple components working together, for example:

- HTTP service ↔ PolicyEngine core
- Agent tools ↔ PolicyEngine service ↔ HITL integrations

Integration tests are marked with the `@pytest.mark.integration` marker.

Examples (hypothetical):

- `tests/integration/test_policyengine_endpoint.py`
- `tests/integration/test_evidence_resolver.py`
- `tests/integration/test_provenance_signing.py`

Run **only** integration tests:

```bash
pytest -m "integration"
```

Run **all tests except** integration:

```bash
pytest -m "not integration"
```

> The `integration` marker is declared in `pytest.ini` and enforced via
> `--strict-markers`, so new markers must be added there.

---

## 3. Coverage

The test suite is configured to collect coverage for the `policyengine`
package with branch coverage enabled.

From the repo root:

```bash
pytest
```

Generates a terminal report showing which lines are covered. To see a more
detailed HTML report:

```bash
pytest --cov=policyengine --cov-branch --cov-report=html
```

Then open `htmlcov/index.html` in a browser.

---

## 4. Useful Commands

From repo root (`C:\4th\4th.GRC`):

```bash
# Run all tests with verbose output
pytest -v

# Run a single test file
pytest tests/unit/test_engine.py

# Run a single test function
pytest tests/unit/test_engine.py::test_engine_end_to_end

# Re-run only tests that failed in the last run
pytest --last-failed

# Stop after the first failure (also in pytest.ini)
pytest --maxfail=1
```

---

## 5. Test Fixtures (Summary)

Common fixtures defined in `tests/conftest.py`:

- `temp_repo`
  Creates an isolated temp repo with `profiles/` and `rules/` directories.

- `sample_rule_bias_fairness`
  Installs a minimal test rule under `rules/`.

- `sample_profile_iso42001`
  Installs a minimal ISO 42001-style profile under `profiles/`.

- `chdir_temp`
  Changes the current working directory to the temp repo (useful for tests
  that assume relative paths like `profiles/` and `rules/` exist).

Example usage in a test:

```python
def test_engine_evaluates_profile(chdir_temp, sample_profile_iso42001):
    from policyengine.engine import evaluate
    from policyengine.schema import EvalRequest

    req = EvalRequest(
        request_id="test-1",
        profile_ref="iso_42001-global@1.2.0",
        controls=None,
        target={"system_id": "demo-system"},
        evidence=[],
        params={},
    )
    resp = evaluate(req)
    assert resp.summary.status in {"pass", "warn", "fail"}
```

---

## 6. CI / Pipelines (Optional Pattern)

A typical CI pipeline might run:

```bash
# Fast lane: unit tests only
pytest -m "not integration"

# Full lane: unit + integration (nightly or pre-release)
pytest
```

You can also enforce a minimum coverage threshold, e.g.:

```bash
pytest --cov=policyengine --cov-branch --cov-fail-under=80
```

---

If you add new test modules or markers:

1. Place tests under `tests/`
2. Use `@pytest.mark.integration` for slow / cross-component tests
3. Update `pytest.ini` if you introduce new markers
