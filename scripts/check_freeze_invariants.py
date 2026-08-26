#!/usr/bin/env python
"""Freeze invariant checker — INV-001 … INV-008 over the Markdown corpus.

Exit code 0 when every invariant holds, 1 otherwise. Run:
    cd /app/backend && python ../scripts/check_freeze_invariants.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path("/app/backend")))

from lib import invariants  # noqa: E402

results = invariants.run_all()
failed = [r for r in results if not r["passed"]]

for r in results:
    print(f"[{'PASS' if r['passed'] else 'FAIL'}] {r['id']} — {r['rule']}\n        {r['detail']}")

print(f"\n{len(results) - len(failed)}/{len(results)} invariants hold")
sys.exit(1 if failed else 0)
