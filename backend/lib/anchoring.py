"""External anchoring of evidence-package digests.

Provider-neutral by design: `ots` (OpenTimestamps, Bitcoin calendars) is implemented,
`rfc3161` (qualified eIDAS timestamp authority) is declared and returns `unavailable`
until a provider is configured — adding it later must not replace OpenTimestamps.

Vocabulary discipline (see proof/EXTERNAL-ANCHORING.md): an OpenTimestamps proof is
**independent evidence of temporal existence and integrity**. It is NOT a qualified or
eIDAS-opposable timestamp, and this module never labels it as one.

Anchors are derived artefacts stored under cvln-intelligence-os/audit/anchors/. The
Markdown corpus remains the canonical store.
"""
from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx

from lib import corpus

ANCHOR_DIR = corpus.CORPUS_ROOT / "audit/anchors"
INDEX_PATH = ANCHOR_DIR / "index.json"
ACCEPT = "application/vnd.opentimestamps.v1"

CALENDARS = [
    c.strip().rstrip("/")
    for c in os.environ.get(
        "OTS_CALENDARS",
        "https://a.pool.opentimestamps.org,https://b.pool.opentimestamps.org",
    ).split(",")
    if c.strip()
]
TIMEOUT = float(os.environ.get("OTS_TIMEOUT_SECONDS", "6"))

PROVIDERS = {
    "ots": "OpenTimestamps — Bitcoin calendar attestation (independent proof of temporal existence)",
    "rfc3161": "RFC 3161 timestamp authority — reserved for a future qualified provider",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def validate_digest(hex_digest: str) -> bytes:
    raw = bytes.fromhex(hex_digest.strip().lower())
    if len(raw) != 32:
        raise ValueError("digest must be a 64-character SHA-256 hex string")
    return raw


def _make_ots(digest: bytes, calendar_response: bytes) -> bytes:
    from opentimestamps.core.op import OpSHA256
    from opentimestamps.core.serialize import (
        BytesDeserializationContext,
        BytesSerializationContext,
    )
    from opentimestamps.core.timestamp import DetachedTimestampFile, Timestamp

    ts = Timestamp.deserialize(BytesDeserializationContext(calendar_response), digest)
    detached = DetachedTimestampFile(OpSHA256(), ts)
    ctx = BytesSerializationContext()
    detached.serialize(ctx)
    return ctx.getbytes()


def _read_ots(blob: bytes) -> tuple[bytes, object]:
    from opentimestamps.core.serialize import BytesDeserializationContext
    from opentimestamps.core.timestamp import DetachedTimestampFile

    detached = DetachedTimestampFile.deserialize(BytesDeserializationContext(blob))
    return detached.file_digest, detached


def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def _save_index(records: list[dict]) -> None:
    ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(
        json.dumps(records, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def find(digest: str, provider: str = "ots") -> dict | None:
    """Records are keyed by (digest, provider) so several providers can coexist."""
    return next(
        (
            r
            for r in load_index()
            if r["digest"] == digest.lower() and r.get("provider", "ots") == provider
        ),
        None,
    )


def proof_bytes(digest: str) -> bytes | None:
    path = ANCHOR_DIR / f"{digest.lower()}.ots"
    return path.read_bytes() if path.exists() else None


async def anchor(digest_hex: str, subject: str, provider: str = "ots") -> dict:
    """Submit a digest to the anchoring provider. Never raises on provider failure."""
    if provider not in PROVIDERS:
        raise ValueError(f"unknown provider: {provider}")

    digest_hex = digest_hex.strip().lower()
    raw = validate_digest(digest_hex)

    existing = find(digest_hex, provider)
    if existing and existing["status"] in {"pending", "confirmed"}:
        return existing

    record = {
        "digest": digest_hex,
        "subject": subject,
        "provider": provider,
        "provider_label": PROVIDERS[provider],
        "status": "unavailable",
        "calendar": None,
        "created_at": _now(),
        "upgraded_at": None,
        "attempts": (existing or {}).get("attempts", 0) + 1,
        "detail": "",
        "proof_file": None,
        "qualified_timestamp": False,
    }

    if provider == "rfc3161":
        record["detail"] = (
            "No RFC 3161 authority is configured. This provider is reserved so a "
            "qualified timestamp can be added later alongside OpenTimestamps, never "
            "replacing it."
        )
        _upsert(record)
        return record

    headers = {"Content-Type": "application/octet-stream", "Accept": ACCEPT}
    errors: list[str] = []
    async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT, connect=3)) as client:
        for calendar in CALENDARS:
            try:
                resp = await client.post(f"{calendar}/digest", content=raw, headers=headers)
                if 200 <= resp.status_code < 300 and resp.content:
                    proof = _make_ots(raw, resp.content)
                    ANCHOR_DIR.mkdir(parents=True, exist_ok=True)
                    (ANCHOR_DIR / f"{digest_hex}.ots").write_bytes(proof)
                    record.update(
                        status="pending",
                        calendar=calendar,
                        proof_file=f"audit/anchors/{digest_hex}.ots",
                        detail=(
                            "Calendar accepted the digest. The attestation is pending "
                            "until it is anchored in a Bitcoin block; upgrade the proof "
                            "to obtain the block attestation."
                        ),
                    )
                    _upsert(record)
                    return record
                errors.append(f"{calendar}: HTTP {resp.status_code}")
            except (httpx.HTTPError, ValueError, Exception) as exc:  # noqa: BLE001
                errors.append(f"{calendar}: {type(exc).__name__}")

    record["status"] = "offline"
    record["detail"] = "No calendar reachable — " + "; ".join(errors)
    _upsert(record)
    return record


async def upgrade(digest_hex: str) -> dict:
    """Ask the calendar for the Bitcoin attestation and merge it into the proof."""
    digest_hex = digest_hex.strip().lower()
    record = find(digest_hex, "ots")
    if record is None:
        raise KeyError(digest_hex)
    proof = proof_bytes(digest_hex)
    if proof is None or not record.get("calendar"):
        record["detail"] = "No stored proof to upgrade."
        _upsert(record)
        return record

    from opentimestamps.core.serialize import (
        BytesDeserializationContext,
        BytesSerializationContext,
    )
    from opentimestamps.core.timestamp import Timestamp

    raw, detached = _read_ots(proof)
    url = f"{record['calendar']}/timestamp/{raw.hex()}"
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(TIMEOUT, connect=3)) as client:
            resp = await client.get(url, headers={"Accept": ACCEPT})
        if resp.status_code == 404:
            record["detail"] = (
                "Calendar reports the attestation is not upgraded yet — still pending, "
                "not a failure."
            )
            record["upgraded_at"] = _now()
            _upsert(record)
            return record
        resp.raise_for_status()
        upgraded = Timestamp.deserialize(BytesDeserializationContext(resp.content), raw)
        detached.timestamp.merge(upgraded)  # type: ignore[attr-defined]
        ctx = BytesSerializationContext()
        detached.serialize(ctx)  # type: ignore[attr-defined]
        (ANCHOR_DIR / f"{digest_hex}.ots").write_bytes(ctx.getbytes())
        record.update(
            status="confirmed",
            upgraded_at=_now(),
            detail=(
                "Bitcoin attestation merged into the proof. Structural verification only: "
                "authoritative verification requires `ots verify` against a Bitcoin node. "
                "This is not a qualified timestamp."
            ),
        )
    except Exception as exc:  # noqa: BLE001
        record["detail"] = f"Upgrade attempt failed ({type(exc).__name__}) — still pending."
        record["upgraded_at"] = _now()
    _upsert(record)
    return record


def verify(digest_hex: str) -> dict:
    """Structural verification: the stored proof parses and is bound to the digest."""
    digest_hex = digest_hex.strip().lower()
    proof = proof_bytes(digest_hex)
    if proof is None:
        return {"parsed": False, "bound_to_digest": False, "detail": "no proof stored"}
    try:
        raw, _ = _read_ots(proof)
    except Exception as exc:  # noqa: BLE001
        return {"parsed": False, "bound_to_digest": False, "detail": str(exc)}
    return {
        "parsed": True,
        "bound_to_digest": raw.hex() == digest_hex,
        "detail": (
            "Structural verification only. Bitcoin attestation verification requires "
            "`ots verify <file>.ots` against a Bitcoin node; format validity is not "
            "confirmation."
        ),
    }


def _upsert(record: dict) -> None:
    records = [
        r
        for r in load_index()
        if not (
            r["digest"] == record["digest"]
            and r.get("provider", "ots") == record.get("provider", "ots")
        )
    ]
    records.append(record)
    records.sort(key=lambda r: r["created_at"], reverse=True)
    _save_index(records)


def proof_b64(digest_hex: str) -> str | None:
    proof = proof_bytes(digest_hex)
    return base64.b64encode(proof).decode() if proof else None


def anchor_for(digest_hex: str, provider: str = "ots") -> dict | None:
    return find(digest_hex, provider)


def anchors_dir_relative() -> str:
    return str(Path("audit/anchors"))
