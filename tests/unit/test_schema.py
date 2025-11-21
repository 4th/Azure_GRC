import yaml
import pytest

from policyengine.schema import PolicyProfile, ProfileMetadata, RuleRef


def test_policy_profile_valid(sample_profile_yaml: str):
    data = yaml.safe_load(sample_profile_yaml)
    profile = PolicyProfile.model_validate(data)

    assert profile.profile_id == "iso_42001-global"
    assert profile.version == "1.2.0"
    assert isinstance(profile.metadata, ProfileMetadata)
    assert isinstance(profile.rules, list)
    assert all(isinstance(r, RuleRef) for r in profile.rules)


def test_policy_profile_missing_required_fields_raises():
    with pytest.raises(Exception):
        PolicyProfile.model_validate(
            {
                "name": "Bad",
                "metadata": {},
                "rules": [],
            }
        )
