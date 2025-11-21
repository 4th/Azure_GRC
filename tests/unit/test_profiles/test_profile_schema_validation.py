import yaml
import pytest

from policyengine.validators import validate_profile, ProfileValidationError


def test_validate_profile_ok(sample_profile_yaml: str):
    data = yaml.safe_load(sample_profile_yaml)
    # Should not raise
    validate_profile(data)


def test_validate_profile_failure(malformed_profile_yaml: str):
    data = yaml.safe_load(malformed_profile_yaml)
    with pytest.raises(ProfileValidationError):
        validate_profile(data)
