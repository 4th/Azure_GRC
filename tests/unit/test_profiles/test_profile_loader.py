from pathlib import Path

import yaml
import pytest

import policyengine.profiles as pe_profiles
from policyengine.profiles import load_profile_by_ref
from policyengine.exceptions import ProfileNotFoundError


def test_load_profile_by_ref_uses_profiles_dir(monkeypatch, data_profiles_dir: Path):
    # Point PolicyEngine's PROFILES_DIR to tests/data/profiles
    monkeypatch.setattr(pe_profiles, "PROFILES_DIR", data_profiles_dir)

    profile = load_profile_by_ref("iso_42001-global@1.2.0")

    assert profile.profile_id == "iso_42001-global"
    assert profile.version == "1.2.0"
    assert len(profile.rules) >= 1


def test_load_nonexistent_profile_raises(monkeypatch, data_profiles_dir: Path):
    monkeypatch.setattr(pe_profiles, "PROFILES_DIR", data_profiles_dir)

    with pytest.raises(ProfileNotFoundError):
        load_profile_by_ref("does_not_exist@0.0.1")
