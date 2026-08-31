import json
import subprocess
from pathlib import Path

BASELINE_DIR = Path("/app/cvln-intelligence-os/audit/baselines")
EXPECTED_COUNTS = {
    "v1.1": 92,
    "v1.1-patch.1": 164,
    "v1.1-patch.2": 166,
    "v1.1-patch.3": 211,
}


def _run_snapshot():
    result = subprocess.run(
        ["python", "../scripts/snapshot_baseline.py"],
        cwd="/app/backend",
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def _read_all():
    out = {}
    for baseline_id in EXPECTED_COUNTS:
        p = BASELINE_DIR / f"{baseline_id}.json"
        data = json.loads(p.read_text())
        out[baseline_id] = {"rows": len(data["rows"]), "created": data["created"]}
    return out


def test_regenerating_snapshot_twice_preserves_counts_and_created_timestamps():
    _run_snapshot()
    first = _read_all()
    _run_snapshot()
    second = _read_all()

    for baseline_id, expected_rows in EXPECTED_COUNTS.items():
        assert (BASELINE_DIR / f"{baseline_id}.json").exists(), f"{baseline_id} missing after regeneration"
        assert first[baseline_id]["rows"] == expected_rows, baseline_id
        assert second[baseline_id]["rows"] == expected_rows, baseline_id
        assert first[baseline_id]["created"] == second[baseline_id]["created"], (
            f"{baseline_id} created timestamp changed across regeneration"
        )
