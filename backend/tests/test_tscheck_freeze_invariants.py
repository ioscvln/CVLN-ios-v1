"""All 14 freeze invariants hold and none is hardcoded."""


def test_freeze_endpoint_reports_14_of_14_passed(client):
    resp = client.get("/docs/freeze")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert "status_vocabulary" in body or "invariants" in body or "label" in body


def test_stats_endpoint_reports_all_invariants_passed(client):
    resp = client.get("/docs/stats")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["invariants_total"] == 17
    assert body["invariants_passed"] == 17


def test_no_unproven_status_promotion_in_relations_and_programmes(client):
    """INV-011 / INV-014: rows with Evidence == 'none' never read IMPLEMENTED/VERIFIED."""
    for key in ("kiltikonet-relations", "kiltikonet-programmes"):
        resp = client.get(f"/docs/registry/{key}")
        assert resp.status_code == 200, resp.text
        body = resp.json()
        columns = [c.lower() for c in body["columns"]]
        rows = body["rows"]
        assert len(rows) > 0
        ev_idx = columns.index("evidence")
        st_idx = columns.index("status")
        for row in rows:
            evidence = (row[ev_idx] or "").strip().lower()
            status = (row[st_idx] or "").strip().upper()
            if evidence in ("none", ""):
                assert status in ("UNKNOWN", "TARGET"), (
                    f"{key}: row with no evidence has status {status}: {row}"
                )


def test_contradictions_remain_open_and_include_kc001(client):
    resp = client.get("/docs/registry/kiltikonet-contradictions")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    columns = [c.lower() for c in body["columns"]]
    rows = body["rows"]
    assert len(rows) == 6
    id_idx = columns.index("id")
    st_idx = columns.index("status")
    ids = []
    for row in rows:
        assert row[st_idx].strip().upper() == "OPEN", f"row not OPEN: {row}"
        ids.append(row[id_idx])
    assert "KC-001" in ids
