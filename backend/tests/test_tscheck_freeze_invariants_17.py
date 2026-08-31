import subprocess

import httpx

BASE_URL = "http://localhost:8001/api"


def test_check_freeze_invariants_script_exits_0_with_17_of_17():
    result = subprocess.run(
        ["python", "scripts/check_freeze_invariants.py"],
        cwd="/app",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "17/17 invariants hold" in result.stdout
    inv017_lines = [l for l in result.stdout.splitlines() if "INV-017" in l]
    idx = result.stdout.splitlines().index(inv017_lines[0])
    detail = result.stdout.splitlines()[idx + 1]
    for snap in ["v1.1", "v1.1-patch.1", "v1.1-patch.2", "v1.1-patch.3"]:
        assert snap in detail
    assert "missing=none" in detail


def test_freeze_endpoint_reports_17_invariants_all_passed():
    r = httpx.get(f"{BASE_URL}/docs/freeze", timeout=30)
    assert r.status_code == 200, r.text
    data = r.json()
    invariants = data["invariants"]
    assert len(invariants) == 17
    assert all(i["passed"] is True for i in invariants), [i for i in invariants if not i["passed"]]
