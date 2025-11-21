def test_root_returns_metadata(api_client):
    resp = api_client.get("/")
    assert resp.status_code == 200

    data = resp.json()
    assert "service" in data
    assert "version" in data
    assert "docs_url" in data
    assert "openapi_url" in data


def test_healthz_ok(api_client):
    resp = api_client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
