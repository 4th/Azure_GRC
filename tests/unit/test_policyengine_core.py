from pathlib import Path

import yaml
import pytest

import policyengine.profiles as pe_profiles
from policyengine import evaluate


def test_evaluate_returns_summary_and_findings(monkeypatch, data_profiles_dir: Path):
    # Point PolicyEngine's PROFILES_DIR to tests/data/profiles
    monkeypatch.setattr(pe_profiles, "PROFILES_DIR", data_profiles_dir)

    result = evaluate(
        profile_ref="iso_42001-global@1.2.0",
        context={"system_name": "Demo LLM System"},
        evidence={},
    )

    assert "summary" in result
    assert "findings" in result

    summary = result["summary"]
    findings = result["findings"]

    assert summary["profile_ref"] == "iso_42001-global@1.2.0"
    assert summary["profile_id"] == "iso_42001-global"
    assert summary["verdict"] in ("pass", "warn", "fail")
    assert isinstance(findings, list)
    assert len(findings) >= 1
