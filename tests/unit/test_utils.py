import pytest

from policyengine.utils import (
    normalize_severity,
    normalize_status,
    compute_simple_score,
)


def test_normalize_severity_known_values():
    assert normalize_severity("low") == "low"
    assert normalize_severity("MEDIUM") == "medium"
    assert normalize_severity(" High ") == "high"
    assert normalize_severity("critical") == "critical"


def test_normalize_severity_unknown_defaults_to_medium():
    assert normalize_severity("weird") == "medium"
    assert normalize_severity(None) == "medium"
    assert normalize_severity("") == "medium"


def test_normalize_status_known_values():
    assert normalize_status("pass") == "pass"
    assert normalize_status("WARN") == "warn"
    assert normalize_status(" Fail ") == "fail"


def test_normalize_status_unknown_defaults_to_warn():
    assert normalize_status("maybe") == "warn"
    assert normalize_status(None) == "warn"
    assert normalize_status("") == "warn"


@pytest.mark.parametrize(
    "statuses, expected_score",
    [
        ([], 1.0),                              # no findings -> full score
        (["pass"], 1.0),
        (["pass", "pass"], 1.0),
        (["pass", "warn"], 0.7),
        (["warn"], 0.7),
        (["fail"], 0.0),
        (["pass", "warn", "fail"], 0.0),
    ],
)
def test_compute_simple_score(statuses, expected_score):
    assert compute_simple_score(statuses) == pytest.approx(expected_score)
