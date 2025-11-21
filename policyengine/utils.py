from __future__ import annotations

from typing import Iterable


_SEVERITY_ORDER = ["low", "medium", "high", "critical"]
_STATUS_ORDER = ["pass", "warn", "fail"]


def normalize_severity(value: str | None) -> str:
    if not value:
        return "medium"
    v = value.lower().strip()
    if v in _SEVERITY_ORDER:
        return v
    return "medium"


def normalize_status(value: str | None) -> str:
    if not value:
        return "warn"
    v = value.lower().strip()
    if v in _STATUS_ORDER:
        return v
    return "warn"


def severity_rank(value: str) -> int:
    return _SEVERITY_ORDER.index(normalize_severity(value))


def status_rank(value: str) -> int:
    return _STATUS_ORDER.index(normalize_status(value))


def compute_simple_score(statuses: Iterable[str]) -> float:
    """
    Very simple scoring function:
    - pass  -> 1.0
    - warn  -> 0.7
    - fail  -> 0.0
    Aggregated as the minimum status across all findings.
    """
    ranks = [status_rank(s) for s in statuses]
    if not ranks:
        return 1.0
    worst = max(ranks)
    if worst == 0:  # pass
        return 1.0
    if worst == 1:  # warn
        return 0.7
    return 0.0
