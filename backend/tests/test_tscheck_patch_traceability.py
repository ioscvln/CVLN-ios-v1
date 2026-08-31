"""Patch is traceable as post-freeze with its decisions."""


def test_patch_and_audit_report_documents_load(client):
    for path in (
        "audit/PATCH-001-KILTIKONET.md",
        "audit/KILTIKONET-AUDIT-REPORT.md",
    ):
        resp = client.get("/docs/file", params={"path": path})
        assert resp.status_code == 200, f"{path}: {resp.text}"


def test_decisions_registry_has_18_including_d015_to_d018(client):
    resp = client.get("/docs/registry/decisions")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    columns = [c.lower() for c in body["columns"]]
    rows = body["rows"]
    assert len(rows) == 18
    id_idx = columns.index("id")
    ids = {row[id_idx] for row in rows}
    for expected_id in ("D-015", "D-016", "D-017", "D-018"):
        assert expected_id in ids, f"missing {expected_id} in decisions: {ids}"
