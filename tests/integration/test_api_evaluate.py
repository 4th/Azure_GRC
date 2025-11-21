def test_api_evaluate_happy_path(api_client, sample_eval_request_dict):
    resp = api_client.post("/v1/evaluate", json=sample_eval_request_dict)
    assert resp.status_code == 200

    data = resp.json()
    assert "summary" in data
    assert "findings" in data

    summary = data["summary"]
    assert summary["profile_ref"] == sample_eval_request_dict["profile_ref"]
    assert summary["verdict"] in ("pass", "warn", "fail")


def test_api_evaluate_missing_profile_ref_returns_422(api_client):
    resp = api_client.post(
        "/v1/evaluate",
        json={"context": {}, "evidence": {}},
    )
    assert resp.status_code == 422
