#!/usr/bin/env python
"""Write baseline snapshots used by the drift-control view.

- v1.1            : the frozen baseline, reconstructed by removing the rows that
                    audit/PATCH-001-KILTIKONET.md documents as added after the freeze.
- v1.1-patch.1    : the corpus as it stands after PATCH-001-KILTIKONET.

Snapshots are derived data, never a second source of truth: they are regenerated from
the Markdown corpus by this script.

Run: cd /app/backend && python ../scripts/snapshot_baseline.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path("/app/backend")))

from lib import baselines  # noqa: E402
from routers.freeze import REGISTRIES  # noqa: E402

# Rows added by PATCH-001-KILTIKONET (see audit/PATCH-001-KILTIKONET.md §"Scope of change")
PATCH_ROWS = {
    "ecosystem:Kiltikonet",
    "ecosystem:Culture Connect 2026",
    "ecosystem:Factory Maker Studio (EURL)",
    *(f"vulnerability:V-{i:03d}" for i in range(9, 13)),
    *(f"continuity:K-{i:03d}" for i in range(9, 12)),
    *(f"legal:L-{i:03d}" for i in range(8, 12)),
    *(f"decisions:D-{i:03d}" for i in range(15, 19)),
}
PATCH_REGISTRY_PREFIXES = ("kiltikonet-",)

# Rows added by the later tooling patches (PATCH-002, PATCH-003)
LATER_PATCH_ROWS = {
    "decisions:D-019",
    "vulnerability:V-013",
    "decisions:D-020",
    "decisions:D-021",
}
LATER_PATCH_PREFIXES = ("open-questions",)

now = datetime.now(timezone.utc).isoformat(timespec="seconds")
rows = baselines.snapshot_rows(REGISTRIES)

def without(exclude_rows: set[str], exclude_prefixes: tuple[str, ...]) -> dict:
    return {
        key: value
        for key, value in rows.items()
        if key not in exclude_rows and not key.startswith(exclude_prefixes)
    }


all_excluded = PATCH_ROWS | LATER_PATCH_ROWS
frozen = without(all_excluded, PATCH_REGISTRY_PREFIXES + LATER_PATCH_PREFIXES)
patch1 = without(LATER_PATCH_ROWS, LATER_PATCH_PREFIXES)

baselines.BASELINE_DIR.mkdir(parents=True, exist_ok=True)

for baseline_id, label, provenance, payload in [
    (
        "v1.1",
        "OS v1.1 — ARCHITECTURE BASELINE FROZEN",
        "reconstructed from the Markdown corpus minus the rows listed in "
        "audit/PATCH-001-KILTIKONET.md as added after the freeze",
        frozen,
    ),
    (
        "v1.1-patch.1",
        "OS v1.1 + PATCH-001-KILTIKONET",
        "snapshot of the Markdown corpus after PATCH-001-KILTIKONET, excluding the rows "
        "recorded as added by PATCH-002 and PATCH-003",
        patch1,
    ),
    (
        "v1.1-patch.3",
        "OS v1.1 + PATCH-001..003",
        "snapshot of the Markdown corpus after PATCH-003-ANCHORING-AND-OPEN-QUESTIONS",
        rows,
    ),
]:
    path = baselines.BASELINE_DIR / f"{baseline_id}.json"
    if path.exists():
        created = json.loads(path.read_text(encoding="utf-8")).get("created", now)
    else:
        created = now
    path.write_text(
        json.dumps(
            {
                "id": baseline_id,
                "label": label,
                "created": created,
                "provenance": provenance,
                "rows": payload,
            },
            indent=1,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote audit/baselines/{baseline_id}.json — {len(payload)} rows")
