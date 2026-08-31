"""Drift control, signed freeze export and per-system cards. Read-only, on api_router."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from lib import baselines, corpus, invariants
from models.insight import (
    BaselineInfo,
    DriftReport,
    DriftRow,
    EvidenceArtefact,
    EvidenceClaim,
    EvidencePackage,
    SystemCard,
    SystemSummary,
)
from routers.freeze import REGISTRIES, REPO_TO_SYSTEM, _load

router = APIRouter(prefix="/docs", tags=["insight"])


def _baseline(baseline_id: str) -> dict:
    if baseline_id == "current":
        return baselines.current_baseline(REGISTRIES)
    try:
        return baselines.load_baseline(baseline_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"unknown baseline: {baseline_id}")


def _info(data: dict) -> BaselineInfo:
    return BaselineInfo(
        id=data["id"],
        label=data["label"],
        created=data["created"],
        provenance=data["provenance"],
        total_rows=len(data["rows"]),
    )


@router.get("/baselines", response_model=list[BaselineInfo])
async def get_baselines() -> list[BaselineInfo]:
    out = [BaselineInfo(**b) for b in baselines.list_baselines()]
    out.append(_info(baselines.current_baseline(REGISTRIES)))
    return out


@router.get("/drift", response_model=DriftReport)
async def get_drift(base: str = "v1.1", target: str = "current") -> DriftReport:
    """Compare two baselines and flag any status promoted without an ADR reference."""
    b, t = _baseline(base), _baseline(target)
    rows = [DriftRow(**r) for r in baselines.diff(b, t)]
    without_adr = sum(1 for r in rows if r.promotion_without_adr)
    advisories = sum(1 for r in rows if r.advisory)
    verdict = (
        f"{without_adr} status promotion(s) without an ADR reference — freeze violation"
        if without_adr
        else (
            f"no promotion without an ADR reference; {advisories} new row(s) recorded with a "
            "strong status and no decision reference (advisory)"
            if advisories
            else "no drift: no promotion and no untraced addition"
        )
    )
    return DriftReport(
        base=_info(b),
        target=_info(t),
        rows=rows,
        total_compared=len(set(b["rows"]) | set(t["rows"])),
        added=sum(1 for r in rows if r.change == "added"),
        removed=sum(1 for r in rows if r.change == "removed"),
        status_changed=sum(1 for r in rows if r.change == "status_changed"),
        promotions=sum(1 for r in rows if r.promotion),
        promotions_without_adr=without_adr,
        advisories=advisories,
        verdict=verdict,
    )


@router.get("/export/{baseline_id}", response_model=EvidencePackage)
async def export_package(baseline_id: str) -> EvidencePackage:
    """Signed evidence package over a baseline. Digital evidence only, no legal effect."""
    data = _baseline(baseline_id)
    artefacts = baselines.artefact_hashes()
    inv = invariants.run_all()
    decisions = [f"{r[0]} — {r[1]} ({r[7]})" for r in _load("decisions").rows]

    claims = [
        EvidenceClaim(
            statement=f"{i['id']}: {i['rule']}",
            status="VERIFIED" if i["passed"] else "REJECTED",
            evidence=i["detail"],
        )
        for i in inv
    ]
    claims.append(
        EvidenceClaim(
            statement=f"Baseline {data['id']} covers {len(data['rows'])} registry rows",
            status="OBSERVED",
            evidence=data["provenance"],
        )
    )
    claims.append(
        EvidenceClaim(
            statement="IMPLEMENTED never implies VERIFIED; CURRENT never implies TARGET",
            status="DECIDED",
            evidence="constitution/FREEZE-001.md",
        )
    )

    chain_input = "\n".join(f"{a['sha256']}  {a['path']}" for a in artefacts)
    chain_input += "\n" + "\n".join(f"{c.status}  {c.statement}" for c in claims)
    chain_hash = hashlib.sha256(chain_input.encode()).hexdigest()
    signature, public_key = baselines.sign(chain_hash)

    return EvidencePackage(
        package_id=f"EP-{data['id']}-{chain_hash[:12]}",
        subject=f"CVLN Intelligence OS baseline {data['id']}",
        baseline=data["id"],
        generated_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        claims=claims,
        artefacts=[EvidenceArtefact(**a) for a in artefacts],
        decisions=decisions,
        chain_hash=chain_hash,
        signature=signature,
        signature_algorithm="Ed25519",
        public_key=public_key,
        anchored_at=None,
        legal_effect="none",
        verification=(
            "Recompute sha256 of each artefact at its path, rebuild the chain input as "
            "'<sha256>  <path>' lines sorted by path followed by '<status>  <statement>' "
            "claim lines, sha256 the result, then verify the Ed25519 signature over that "
            "hex digest with public_key. Any failing step rejects the whole package. "
            "This package is digital evidence and carries no legal effect "
            "(proof/NOTARIAL-BOUNDARY.md)."
        ),
    )


# ---------------------------------------------------------------- system cards


def _system_rows() -> tuple[list[str], list[list[str]]]:
    eco = _load("ecosystem")
    return eco.columns, eco.rows


def _components_for(system: str) -> tuple[list[str], list[list[str]]]:
    comp = _load("component")
    keys = [k for k, v in REPO_TO_SYSTEM.items() if v.lower() == system.lower()]
    rows = [r for r in comp.rows if r[1].strip().upper() in keys]
    if not rows:
        rows = [r for r in comp.rows if system.lower() in " ".join(r).lower()]
    return comp.columns, rows


def _match_rows(key: str, system: str) -> tuple[list[str], list[list[str]]]:
    table = _load(key)
    needle = system.lower()
    return table.columns, [r for r in table.rows if needle in " ".join(r).lower()]


@router.get("/systems", response_model=list[SystemSummary])
async def get_systems() -> list[SystemSummary]:
    columns, rows = _system_rows()
    si = columns.index("Status") if "Status" in columns else 5
    out = []
    for row in rows:
        name = row[0].strip()
        out.append(
            SystemSummary(
                name=name,
                layer=row[1],
                role=row[2],
                status=row[si],
                evidence=row[4],
                components=len(_components_for(name)[1]),
                vulnerabilities=len(_match_rows("vulnerability", name)[1]),
                decisions=len(_match_rows("decisions", name)[1]),
            )
        )
    return out


@router.get("/system/{name}", response_model=SystemCard)
async def get_system(name: str) -> SystemCard:
    columns, rows = _system_rows()
    match = next((r for r in rows if r[0].strip().lower() == name.strip().lower()), None)
    if match is None:
        raise HTTPException(status_code=404, detail=f"unknown system: {name}")
    si = columns.index("Status") if "Status" in columns else 5
    system = match[0].strip()

    comp_cols, comp_rows = _components_for(system)
    vul_cols, vul_rows = _match_rows("vulnerability", system)
    dec_cols, dec_rows = _match_rows("decisions", system)
    rel_cols, rel_rows = _match_rows("kiltikonet-relations", system)

    needle = system.lower()
    documents = [
        e["path"]
        for e in corpus.corpus_index()
        if needle in e["title"].lower() or needle in e["path"].lower()
    ]

    return SystemCard(
        name=system,
        layer=match[1],
        role=match[2],
        repository=match[3],
        evidence=match[4],
        status=match[si],
        owns=match[6],
        must_not_own=match[7],
        components=comp_rows,
        component_columns=comp_cols,
        vulnerabilities=vul_rows,
        vulnerability_columns=vul_cols,
        decisions=dec_rows,
        decision_columns=dec_cols,
        relations=rel_rows,
        relation_columns=rel_cols,
        documents=documents,
    )
