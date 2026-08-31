"""Generate governance/OPEN-QUESTIONS.md from the registries.

Canonical rules:
- Nothing is invented: Owner defaults to UNASSIGNED and Due to TBD.
- Owner and Due are **human-edited fields**. A regeneration preserves whatever a human
  wrote in those two columns, keyed by question ID.
- The Markdown file stays the canonical store; the portal reads it dynamically.

Classification (deterministic, documented in governance/OPEN-QUESTIONS.md):
  freeze-blocker            contradictions, OPEN legal obligations, CRITICAL/HIGH
                            observed vulnerabilities
  contradiction             any row of a contradictions register
  unknown-needs-evidence    rows with status UNKNOWN
  risk-needs-decision       vulnerabilities below HIGH, or TARGET security controls
  open-question             every other OPEN row

Run: cd /app/backend && python ../scripts/gen_open_questions.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path("/app/backend")))

from lib import corpus  # noqa: E402
from routers.freeze import REGISTRIES  # noqa: E402

OUT = corpus.CORPUS_ROOT / "governance/OPEN-QUESTIONS.md"
COLUMNS = ["ID", "Question", "Kind", "Source", "Row", "Status", "Owner", "Due", "Evidence"]

CONTRADICTION_REGISTRIES = {"kiltikonet-contradictions"}

# Column preferred as the question text, per registry shape. Falls back to column 1.
QUESTION_COLUMNS = (
    "contradiction",
    "question",
    "finding",
    "requirement",
    "capability",
    "programme",
    "identity",
    "relation",
    "decision",
    "conceptual responsibility",
    "role",
    "data",
    "description",
)
OPENISH = {"OPEN", "UNKNOWN"}


def _idx(columns: list[str], names: tuple[str, ...]) -> int:
    lowered = [c.strip().lower() for c in columns]
    for name in names:
        if name in lowered:
            return lowered.index(name)
    return -1


def classify(registry: str, status: str, severity: str) -> str:
    if registry in CONTRADICTION_REGISTRIES:
        return "freeze-blocker"
    if registry == "vulnerability":
        return "freeze-blocker" if severity.upper() in {"CRITICAL", "HIGH"} else "risk-needs-decision"
    if registry == "legal" and status.upper() == "OPEN":
        return "freeze-blocker"
    if status.upper() == "UNKNOWN":
        return "unknown-needs-evidence"
    return "open-question"


def existing_human_fields() -> dict[str, tuple[str, str]]:
    """Owner and Due already written by a human, keyed by question ID."""
    if not OUT.exists():
        return {}
    out: dict[str, tuple[str, str]] = {}
    for line in OUT.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| Q-"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 8:
            out[cells[0]] = (cells[6], cells[7])
    return out


def collect() -> list[list[str]]:
    rows: list[list[str]] = []
    n = 0
    for registry, spec in REGISTRIES.items():
        if registry == "open-questions":
            continue  # never fold the register into itself
        columns, table = corpus.parse_registry(spec["source"], min_columns=spec["columns"])
        si = _idx(columns, ("status",))
        sev = _idx(columns, ("severity",))
        ei = _idx(columns, ("evidence",))
        for row in table:
            status = row[si].strip() if si >= 0 else ""
            severity = row[sev].strip() if sev >= 0 else ""
            is_contradiction = registry in CONTRADICTION_REGISTRIES
            if status.upper() not in OPENISH and not is_contradiction:
                # A registered weakness that is only OBSERVED still needs a decision.
                if not (registry == "vulnerability" and status.upper() == "OBSERVED"):
                    continue
            n += 1
            qi = _idx(columns, QUESTION_COLUMNS)
            if qi < 0:
                qi = 1
            question = re.sub(r"\s+", " ", row[qi]).strip() or row[0].strip()
            rows.append(
                [
                    f"Q-{n:03d}",
                    question[:180],
                    classify(registry, status, severity),
                    spec["source"],
                    row[0].strip(),
                    status or "OPEN",
                    "UNASSIGNED",
                    "TBD",
                    (row[ei].strip() if ei >= 0 else "none") or "none",
                ]
            )
    return rows


rows = collect()
preserved = existing_human_fields()
for row in rows:
    owner, due = preserved.get(row[0], ("UNASSIGNED", "TBD"))
    row[6], row[7] = owner or "UNASSIGNED", due or "TBD"

kinds = {}
for row in rows:
    kinds[row[2]] = kinds.get(row[2], 0) + 1
kind_lines = "\n".join(f"| `{k}` | {v} |" for k, v in sorted(kinds.items()))

head = "| " + " | ".join(COLUMNS) + " |"
sep = "|" + "---|" * len(COLUMNS)
body = "\n".join("| " + " | ".join(r) + " |" for r in rows)

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    f"""---
title: Open Questions Register
purpose: Every open question, contradiction, unknown and undecided risk of the corpus, with owner and due date.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Whole corpus
version: 1.1-patch.3
status: OPEN
attribution: GOVERNANCE
---

# Open Questions Register

One row per question that must be answered before the next freeze can be declared. The
register is generated from the registries by `scripts/gen_open_questions.py`; the
`Owner` and `Due` columns are **human-owned** and preserved across regenerations.

`Owner = UNASSIGNED` and `Due = TBD` mean exactly that: nobody has been assigned and no
date has been set. Neither is invented by any tool.

## Classification rules

| Kind | Rule |
|---|---|
| `freeze-blocker` | a contradiction, an OPEN legal obligation, or an observed CRITICAL/HIGH vulnerability |
| `contradiction` | recorded in a contradictions register (all are freeze blockers) |
| `unknown-needs-evidence` | status `UNKNOWN`: an artefact must be produced before any promotion |
| `risk-needs-decision` | a registered weakness below HIGH severity awaiting a decision |
| `open-question` | any other `OPEN` row |

## Distribution

| Kind | Rows |
|---|---|
{kind_lines}

## Register

{head}
{sep}
{body}

## Rules bound to this register

1. A freeze may not be declared while a `freeze-blocker` row is unresolved.
2. Resolving a row requires evidence and, where a status changes, an ADR — see
   `audit/DRIFT-CONTROL.md`.
3. Deleting a row without a resolution record is a freeze violation.
4. `Owner` and `Due` are filled by humans; tools never guess them.
""",
    encoding="utf-8",
)
print(f"wrote governance/OPEN-QUESTIONS.md — {len(rows)} questions, kinds: {kinds}")
