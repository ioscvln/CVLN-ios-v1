"""Baseline snapshots, drift detection and signed evidence-package export.

Snapshots live on disk as JSON under cvln-intelligence-os/audit/baselines/ and are read
only — the Markdown corpus stays the canonical store.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from lib import corpus

BASELINE_DIR = corpus.CORPUS_ROOT / "audit/baselines"

# Status strength. A move upward is a promotion and requires an ADR reference.
RANK = {
    "REJECTED": 0,
    "UNKNOWN": 0,
    "OPEN": 0,
    "DEPRECATED": 1,
    "HISTORICAL": 1,
    "REFERENCED": 1,
    "PROPOSED": 2,
    "TARGET": 2,
    "DEFINED": 2,
    "DECIDED": 3,
    "OBSERVED": 4,
    "PARTIAL": 5,
    "IMPLEMENTED": 6,
    "VERIFIED": 7,
}

EMPTY = {"", "none", "—", "-", "n/a"}


def rank(status: str) -> int:
    return RANK.get(status.strip().upper(), 0)


def _col(columns: list[str], names: tuple[str, ...]) -> int:
    for i, c in enumerate(columns):
        if c.strip().lower() in names:
            return i
    return -1


def snapshot_rows(registries: dict[str, dict]) -> dict[str, dict[str, str]]:
    """Current status + ADR reference of every registry row, keyed registry:row_id."""
    out: dict[str, dict[str, str]] = {}
    for key, spec in registries.items():
        columns, rows = corpus.parse_registry(spec["source"], min_columns=spec["columns"])
        si = _col(columns, ("status",))
        ai = _col(columns, ("adr", "decision ref", "decision", "decision_ref"))
        for row in rows:
            out[f"{key}:{row[0].strip()}"] = {
                "status": row[si].strip() if si >= 0 else "",
                "adr": row[ai].strip() if ai >= 0 else "",
            }
    return out


def load_baseline(baseline_id: str) -> dict:
    path = BASELINE_DIR / f"{baseline_id}.json"
    if not path.exists():
        raise FileNotFoundError(baseline_id)
    return json.loads(path.read_text(encoding="utf-8"))


def list_baselines() -> list[dict]:
    if not BASELINE_DIR.exists():
        return []
    out = []
    for path in sorted(BASELINE_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out.append(
            {
                "id": data["id"],
                "label": data["label"],
                "created": data["created"],
                "provenance": data["provenance"],
                "total_rows": len(data["rows"]),
            }
        )
    return out


def current_baseline(registries: dict[str, dict]) -> dict:
    return {
        "id": "current",
        "label": "Working corpus (live)",
        "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "provenance": "computed from the Markdown corpus at request time",
        "rows": snapshot_rows(registries),
    }


def diff(base: dict, target: dict) -> list[dict]:
    rows: list[dict] = []
    keys = sorted(set(base["rows"]) | set(target["rows"]))
    for key in keys:
        registry, _, row_id = key.partition(":")
        b = base["rows"].get(key)
        t = target["rows"].get(key)
        if b is None and t is not None:
            strong = rank(t["status"]) >= RANK["OBSERVED"]
            rows.append(
                {
                    "registry": registry,
                    "row_id": row_id,
                    "change": "added",
                    "base_status": "",
                    "target_status": t["status"],
                    "adr": t["adr"],
                    # A new row is not a promotion: nothing was promoted, a fact was
                    # recorded. Strong statuses without a decision reference are
                    # reported as advisories, not as freeze violations.
                    "promotion": False,
                    "promotion_without_adr": False,
                    "advisory": strong and t["adr"].lower() in EMPTY,
                }
            )
        elif t is None and b is not None:
            rows.append(
                {
                    "registry": registry,
                    "row_id": row_id,
                    "change": "removed",
                    "base_status": b["status"],
                    "target_status": "",
                    "adr": b["adr"],
                    "promotion": False,
                    "promotion_without_adr": False,
                    "advisory": False,
                }
            )
        elif b and t and b["status"].strip().upper() != t["status"].strip().upper():
            promotion = rank(t["status"]) > rank(b["status"])
            rows.append(
                {
                    "registry": registry,
                    "row_id": row_id,
                    "change": "status_changed",
                    "base_status": b["status"],
                    "target_status": t["status"],
                    "adr": t["adr"],
                    "promotion": promotion,
                    "promotion_without_adr": promotion and t["adr"].lower() in EMPTY,
                    "advisory": False,
                }
            )
    return rows


# ---------------------------------------------------------------- evidence package export

KEY_PATH = Path(os.environ.get("EXPORT_SIGNING_KEY_PATH", "/app/backend/.keys/export_ed25519.key"))


def _signing_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    if KEY_PATH.exists():
        return Ed25519PrivateKey.from_private_bytes(KEY_PATH.read_bytes())
    key = Ed25519PrivateKey.generate()
    KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
    KEY_PATH.write_bytes(
        key.private_bytes_raw()
        if hasattr(key, "private_bytes_raw")
        else key.private_bytes(
            encoding=__import__("cryptography.hazmat.primitives.serialization", fromlist=["x"]).Encoding.Raw,
            format=__import__("cryptography.hazmat.primitives.serialization", fromlist=["x"]).PrivateFormat.Raw,
            encryption_algorithm=__import__(
                "cryptography.hazmat.primitives.serialization", fromlist=["x"]
            ).NoEncryption(),
        )
    )
    KEY_PATH.chmod(0o600)
    return key


def artefact_hashes() -> list[dict]:
    out = []
    for path in corpus.all_docs():
        raw = path.read_bytes()
        out.append(
            {
                "path": corpus.rel(path),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        )
    manifest = corpus.CORPUS_ROOT / corpus.FREEZE_MANIFEST
    raw = manifest.read_bytes()
    out.append(
        {
            "path": corpus.FREEZE_MANIFEST,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "bytes": len(raw),
        }
    )
    return sorted(out, key=lambda a: a["path"])


def sign(chain_hash: str) -> tuple[str, str]:
    key = _signing_key()
    signature = key.sign(chain_hash.encode()).hex()
    pub = key.public_key().public_bytes_raw().hex()
    return signature, pub
