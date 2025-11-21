import yaml


def test_profile_structure_has_expected_keys(sample_profile_yaml: str):
    data = yaml.safe_load(sample_profile_yaml)

    assert "profile_id" in data
    assert "version" in data
    assert "metadata" in data
    assert "rules" in data
    assert isinstance(data["rules"], list)
