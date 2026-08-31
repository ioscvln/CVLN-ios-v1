"""Kiltikonet registries are served by the API and browsable."""


def test_registries_list_includes_kiltikonet_keys(client):
    resp = client.get("/docs/registries")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    keys = {r["key"]: r["total"] for r in body["registries"]}
    assert keys.get("kiltikonet-relations") == 17
    assert keys.get("kiltikonet-programmes") == 13
    assert keys.get("kiltikonet-data") == 10
    assert keys.get("kiltikonet-identity") == 8
    assert keys.get("kiltikonet-contradictions") == 6


def test_each_kiltikonet_registry_is_browsable(client):
    expected = {
        "kiltikonet-relations": 17,
        "kiltikonet-programmes": 13,
        "kiltikonet-data": 10,
        "kiltikonet-identity": 8,
        "kiltikonet-contradictions": 6,
    }
    for key, total in expected.items():
        resp = client.get(f"/docs/registry/{key}")
        assert resp.status_code == 200, f"{key}: {resp.text}"
        body = resp.json()
        rows = body["rows"]
        assert len(rows) == total, f"{key}: expected {total} rows, got {len(rows)}"


def test_unknown_registry_key_returns_404(client):
    resp = client.get("/docs/registry/does-not-exist-tscheck")
    assert resp.status_code == 404, resp.text
