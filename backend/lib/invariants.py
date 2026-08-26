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
