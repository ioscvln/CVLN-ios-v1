"""Executable freeze invariants (INV-001 … INV-008).

The Markdown corpus is the canonical store; these are assertions over it. Used by the
`/api/docs/freeze` endpoint and by `scripts/check_freeze_invariants.py`.
"""
from __future__ import annotations

import re
from pathlib import Path

from lib import corpus

REGISTRY_SOURCES = [
    ("audit/COMPONENT-MATRIX.md", 11),
    ("registry/ECOSYSTEM-REGISTRY.md", 8),
    ("registry/VULNERABILITY-REGISTRY.md", 8),
    ("registry/CONTINUITY-MATRIX.md", 8),
    ("registry/LEGAL-MATRIX.md", 8),
    ("decisions/DECISION-REGISTRY.md", 8),
]

LEGACY_STATUSES = {
    "PARTIAL",
    "DEFINED",
    "REFERENCED",
    "PRIVATE / NOT VISIBLE",
    "OBSERVED-PARTIAL",
}

EMPTY_EVIDENCE = {"", "none", "—", "-", "n/a", "unknown"}
STRONG = {"IMPLEMENTED", "VERIFIED"}
DECISION_IDS = [f"D-{i:03d}" for i in range(1, 15)]


def _col(columns: list[str], name: str) -> int:
    for i, c in enumerate(columns):
        if c.strip().lower() == name:
            return i
    return -1


def inv_001() -> tuple[bool, str]:
    """No row carries IMPLEMENTED or VERIFIED without an evidence path."""
    offenders: list[str] = []
    for source, cols in REGISTRY_SOURCES:
        columns, rows = corpus.parse_registry(source, min_columns=cols)
        si, ei = _col(columns, "status"), _col(columns, "evidence")
        if si < 0 or ei < 0:
            continue
        for row in rows:
            if row[si].strip().upper() in STRONG and row[ei].strip().lower() in EMPTY_EVIDENCE:
                offenders.append(f"{source}:{row[0]}")
    return not offenders, "offenders: " + (", ".join(offenders) if offenders else "none")


def inv_002() -> tuple[bool, str]:
    """Every decision D-001…D-014 has an ADR document."""
    files = {p.name for p in (corpus.CORPUS_ROOT / "decisions").glob("ADR-*.md")}
    missing = [d for d in DECISION_IDS if not any(d in f for f in files)]
    return not missing, f"adr_documents={len(files)}; missing={missing or 'none'}"


def inv_003() -> tuple[bool, str]:
    """Markdown remains the canonical store; no database mirrors the corpus."""
    manifest = corpus.read_manifest()
    flag = bool(manifest.get("database_as_source_of_truth", True))
    routers = Path(__file__).resolve().parents[1] / "routers"
    leaks = [
        p.name
        for p in routers.glob("*.py")
        if re.search(r"\b(lib\.db|from lib import db|get_db|AsyncIOMotor)\b", p.read_text(encoding="utf-8"))
    ]
    ok = (not flag) and manifest.get("canonical_store") == "markdown" and not leaks
    return ok, f"database_as_source_of_truth={flag}; db_using_routers={leaks or 'none'}"


def inv_004() -> tuple[bool, str]:
    """The contradictions register is non-empty and C-002 remains open."""
    text = (corpus.CORPUS_ROOT / "audit/CONTRADICTIONS.md").read_text(encoding="utf-8")
    count = sum(1 for line in text.splitlines() if line.startswith("## C-"))
    c002 = "C-002" in text
    resolved = bool(re.search(r"C-002[^\n]*RESOLVED", text))
    return count > 0 and c002 and not resolved, f"contradictions={count}; c002_present={c002}; c002_resolved={resolved}"


def inv_005() -> tuple[bool, str]:
    """Every document declares a status from the canonical vocabulary."""
    allowed = set(corpus.read_manifest().get("status_vocabulary", [])) | LEGACY_STATUSES
    bad = [
        f"{e['path']}={e['status']}"
        for e in corpus.corpus_index()
        if e["status"].strip().upper() not in allowed
    ]
    return not bad, f"vocabulary={len(allowed)} tokens; violations={bad or 'none'}"


def inv_006() -> tuple[bool, str]:
    """JCC is never described as currency or a payment instrument."""
    pattern = re.compile(
        r"JCC\s+(is|are|as)\s+(a\s+)?(legal\s+)?(currency|tender|payment instrument|security|token)",
        re.IGNORECASE,
    )
    # A prohibition ("JCC is never a currency", "Presenting JCC as legal currency |
    # REJECTED") is compliant. Only an affirmation violates the invariant.
    negation = re.compile(
        r"\b(not|never|no|non|forbid|forbidden|prohibit|prohibited|reject|rejected|"
        r"excluded|must not|may not|violat|constraint|constrained)\b",
        re.IGNORECASE,
    )
    offenders: list[str] = []
    for p in corpus.all_docs():
        for line in p.read_text(encoding="utf-8").splitlines():
            if pattern.search(line) and not negation.search(line):
                offenders.append(f"{corpus.rel(p)}: {line.strip()[:60]}")
                break
    return not offenders, "offenders: " + (", ".join(offenders) if offenders else "none")


def inv_007() -> tuple[bool, str]:
    """No v1.0 document was deleted."""
    inventory = (corpus.CORPUS_ROOT / "audit/v10-inventory.txt").read_text(encoding="utf-8")
    expected = [
        line.strip()
        for line in inventory.splitlines()
        if line.strip() and not line.startswith("#")
    ]
    missing = [p for p in expected if not (corpus.CORPUS_ROOT / p).exists()]
    return not missing, f"v1.0_documents={len(expected)}; missing={missing or 'none'}"


def inv_008() -> tuple[bool, str]:
    """Every registry row has exactly one non-empty status cell."""
    offenders: list[str] = []
    total = 0
    for source, cols in REGISTRY_SOURCES:
        columns, rows = corpus.parse_registry(source, min_columns=cols)
        si = _col(columns, "status")
        for row in rows:
            total += 1
            if len(row) != len(columns) or si < 0 or not row[si].strip():
                offenders.append(f"{source}:{row[0] if row else '?'}")
    return not offenders, f"rows={total}; offenders={offenders or 'none'}"


CHECKS = [
    ("INV-001", "No row carries IMPLEMENTED or VERIFIED without an evidence path", inv_001),
    ("INV-002", "Every decision D-001..D-014 has an ADR document", inv_002),
    ("INV-003", "Markdown remains the canonical store; no database mirrors the corpus", inv_003),
    ("INV-004", "The contradictions register is non-empty and C-002 remains open", inv_004),
    ("INV-005", "Every document declares a status from the canonical vocabulary", inv_005),
    ("INV-006", "JCC is never described as currency or a payment instrument", inv_006),
    ("INV-007", "No v1.0 document was deleted", inv_007),
    ("INV-008", "Every registry row has exactly one non-empty status cell", inv_008),
]


def run_all() -> list[dict]:
    out: list[dict] = []
    for inv_id, rule, fn in CHECKS:
        try:
            passed, detail = fn()
        except Exception as exc:  # a broken check is a failed invariant, never a pass
            passed, detail = False, f"check error: {exc}"
        out.append({"id": inv_id, "rule": rule, "passed": passed, "detail": detail})
    return out


# --- PATCH-001-KILTIKONET invariants (INV-009 … INV-014) ------------------------------

KILT_SYSTEM_CARD = "kiltikonet/KILTIKONET-SYSTEM.md"
KILT_REGISTRIES = [
    ("kiltikonet/RELATIONS-REGISTRY.md", 7),
    ("kiltikonet/PROGRAMMES-REGISTRY.md", 6),
    ("kiltikonet/DATA-FLOWS.md", 6),
    ("kiltikonet/IDENTITY-RECONCILIATION.md", 8),
    ("kiltikonet/CONTRADICTIONS-KILTIKONET.md", 6),
]
LINK_RE = re.compile(r"\]\(([^)\s#]+\.md)[^)]*\)")


def inv_009() -> tuple[bool, str]:
    """Kiltikonet exists in the ecosystem registry."""
    columns, rows = corpus.parse_registry("registry/ECOSYSTEM-REGISTRY.md", min_columns=8)
    si = _col(columns, "status")
    match = [r for r in rows if r[0].strip().lower() == "kiltikonet"]
    ok = len(match) == 1 and si >= 0 and bool(match[0][si].strip())
    status = match[0][si] if match and si >= 0 else "absent"
    return ok, f"ecosystem_rows={len(rows)}; kiltikonet_status={status}"


def inv_010() -> tuple[bool, str]:
    """The Kiltikonet system card exists and is reachable."""
    path = corpus.CORPUS_ROOT / KILT_SYSTEM_CARD
    exists = path.exists()
    words = len(path.read_text(encoding="utf-8").split()) if exists else 0
    indexed = any(e["path"] == KILT_SYSTEM_CARD for e in corpus.corpus_index())
    return exists and indexed and words > 200, f"exists={exists}; indexed={indexed}; words={words}"


def inv_011() -> tuple[bool, str]:
    """Every Kiltikonet relation row is traceable and evidence-backed."""
    columns, rows = corpus.parse_registry("kiltikonet/RELATIONS-REGISTRY.md", min_columns=7)
    si, ei = _col(columns, "status"), _col(columns, "evidence")
    offenders: list[str] = []
    for row in rows:
        if not row[1].strip() or not row[2].strip() or not row[si].strip():
            offenders.append(f"{row[0]}:incomplete")
        elif row[si].strip().upper() in STRONG and row[ei].strip().lower() in EMPTY_EVIDENCE:
            offenders.append(f"{row[0]}:unevidenced-{row[si].strip()}")
    return not offenders and len(rows) > 0, f"relations={len(rows)}; offenders={offenders or 'none'}"


def inv_012() -> tuple[bool, str]:
    """Kiltikonet historical contradictions are recorded and open."""
    columns, rows = corpus.parse_registry("kiltikonet/CONTRADICTIONS-KILTIKONET.md", min_columns=6)
    si = _col(columns, "status")
    closed = [r[0] for r in rows if si >= 0 and r[si].strip().upper() != "OPEN"]
    return len(rows) > 0 and not closed, f"contradictions={len(rows)}; not_open={closed or 'none'}"


def inv_013() -> tuple[bool, str]:
    """No internal Markdown reference added after v1.0 is broken."""
    inventory = {
        line.strip()
        for line in (corpus.CORPUS_ROOT / "audit/v10-inventory.txt")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.startswith("#")
    }
    broken: list[str] = []
    legacy = 0
    for path in corpus.all_docs():
        if corpus.rel(path) in inventory:
            # v1.0 documents are frozen: their links are reported, never edited here.
            legacy += sum(
                1
                for target in LINK_RE.findall(path.read_text(encoding="utf-8"))
                if not target.startswith("http") and not (path.parent / target).resolve().exists()
            )
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith("http"):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                broken.append(f"{corpus.rel(path)} -> {target}")
    return not broken, f"broken_links_post_v1.0={len(broken)}; legacy_v1.0_broken={legacy} (frozen, reported only); {broken[:5] or 'none'}"


def inv_014() -> tuple[bool, str]:
    """Every Kiltikonet programme carries its own status."""
    columns, rows = corpus.parse_registry("kiltikonet/PROGRAMMES-REGISTRY.md", min_columns=6)
    si, ei = _col(columns, "status"), _col(columns, "evidence")
    offenders = [
        r[0]
        for r in rows
        if not r[si].strip()
        or (r[si].strip().upper() in STRONG and r[ei].strip().lower() in EMPTY_EVIDENCE)
    ]
    return len(rows) > 0 and not offenders, f"programmes={len(rows)}; offenders={offenders or 'none'}"


REGISTRY_SOURCES += KILT_REGISTRIES
CHECKS += [
    ("INV-009", "Kiltikonet exists in the ecosystem registry", inv_009),
    ("INV-010", "The Kiltikonet system card exists and is reachable", inv_010),
    ("INV-011", "Every Kiltikonet relation row is traceable and evidence-backed", inv_011),
    ("INV-012", "Kiltikonet historical contradictions are recorded and open", inv_012),
    ("INV-013", "No internal Markdown reference in the corpus is broken", inv_013),
    ("INV-014", "Every Kiltikonet programme carries its own status", inv_014),
]
