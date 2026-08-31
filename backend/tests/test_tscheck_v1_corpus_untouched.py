"""v1.0 corpus and the v1.1 freeze text are untouched."""


def test_total_documents_is_151(client):
    resp = client.get("/docs/stats")
    assert resp.status_code == 200, resp.text
    assert resp.json()["total_documents"] == 151


def test_freeze_documents_load_and_omit_kiltikonet(client):
    for path in ("constitution/FREEZE-001.md", "audit/FREEZE-REPORT-v1.1.md"):
        resp = client.get("/docs/file", params={"path": path})
        assert resp.status_code == 200, f"{path}: {resp.text}"
        body = resp.json()
        content = body.get("content", body) if isinstance(body, dict) else body
        text = content if isinstance(content, str) else str(content)
        assert "kiltikonet" not in text.lower(), f"{path} unexpectedly mentions Kiltikonet"
