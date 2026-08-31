import httpx

BASE_URL = "http://localhost:8001/api"


def test_v1_1_patch_2_snapshot_file_non_empty():
    import json
    from pathlib import Path

    p = Path("/app/cvln-intelligence-os/audit/baselines/v1.1-patch.2.json")
    assert p.exists(), "v1.1-patch.2.json baseline file missing"
    data = json.loads(p.read_text())
    assert data.get("id") == "v1.1-patch.2"
    rows = data.get("rows")
    assert isinstance(rows, dict) and len(rows) > 0
    assert len(rows) == 166


def test_baselines_endpoint_lists_all_four_plus_current():
    r = httpx.get(f"{BASE_URL}/docs/baselines", timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    by_id = {b["id"]: b["total_rows"] for b in data}
    assert by_id.get("v1.1") == 92
    assert by_id.get("v1.1-patch.1") == 164
    assert by_id.get("v1.1-patch.2") == 166
    assert by_id.get("v1.1-patch.3") == 211
    assert "current" in by_id
