import policyengine.profiles as pe_profiles
from policyengine import evaluate


def test_end_to_end_eval_matches_api(api_client, monkeypatch, data_profiles_dir):
    # First, patch engine to use test profiles
    monkeypatch.setattr(pe_profiles, "PROFILES_DIR", data_profiles_dir)

    payload = {
        "profile_ref": "iso_42001-global@1.2.0",
        "context": {"system_name": "Demo LLM System"},
        "evidence": {},
    }

    # Direct engine call
    direct_result = evaluate(
        profile_ref=payload["profile_ref"],
        context=payload["context"],
        evidence=payload["evidence"],
    )

    # API call
    resp = api_client.post("/v1/evaluate", json=payload)
    assert resp.status_code == 200
    api_result = resp.json()

    # Basic consistency checks
    assert direct_result["summary"]["verdict"] == api_result["summary"]["verdict"]
    assert len(direct_result["findings"]) == len(api_result["findings"])
