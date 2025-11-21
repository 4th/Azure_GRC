from pathlib import Path

import pytest

from policyengine.profiles import load_profile_by_ref, PROFILES_DIR
from policyengine.exceptions import ProfileNotFoundError


def test_profiles_dir_exists():
    assert PROFILES_DIR.exists(), f"Profiles dir does not exist: {PROFILES_DIR}"


def test_load_existing_profile_by_ref():
    """
    Assumes you have a file:
        profiles/iso_42001-global.yaml
    with version "1.2.0".
    """
    profile = load_profile_by_ref("iso_42001-global@1.2.0")

    assert profile.profile_id == "iso_42001-global"
    assert profile.version == "1.2.0"
    assert isinstance(profile.metadata.title, (str, type(None)))
    assert isinstance(profile.rules, list)


def test_load_nonexistent_profile_raises():
    with pytest.raises(ProfileNotFoundError):
        load_profile_by_ref("this_profile_should_not_exist@0.0.1")
