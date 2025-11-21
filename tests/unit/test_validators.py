import yaml
import pytest

from policyengine.validators import validate_profile, ProfileValidationError


def test_validate_profile_success(sample_profile_yaml: str):
    data = yaml.safe_load(sample_profile_yaml)
    # Should not raise
    validate_profile(data)


def test_validate_profile_missing_profile_id():
    data = {
        "version": "1.0.0",
        "rules": [],
    }
    with pytest.raises(ProfileValidationError):
        validate_profile(data)


def test_validate_profile_rules_must_be_list():
    data = {
        "profile_id": "bad",
        "version": "1.0.0",
        "rules": {"not": "a list"},
    }
    with pytest.raises(ProfileValidationError):
        validate_profile(data)
