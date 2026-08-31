"""PATCH-002-GOVERNANCE-TOOLING — append-only, post-freeze.

Records the drift-control, signed-export and system-card capabilities added to the
portal, with the decision that authorises the status change of the EvidencePackage
specification. Run: python scripts/gen_patch2_tooling.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/app/cvln-intelligence-os")

D019 = (
    "D-019",
    "Baseline snapshots and evidence-package export are derived artefacts",
    "Snapshots and packages are recomputed from the Markdown corpus; they never become a second source of truth",
    "ARCHITECTURE",
    "backend/lib/baselines.py, backend/routers/insight.py",
    "IMPLEMENTED",
    "proof/, audit/baselines/",
    "ADR-0019",
)

V013 = (
    "V-013",
    "Export signing key stored unencrypted at rest on the portal host",
    "portal export",
    "backend/lib/baselines.py (EXPORT_SIGNING_KEY_PATH)",
    "HIGH",
    "OBSERVED",
    "Move to a KMS or sealed secret; rotate and publish the public key out of band",
    "D-019",
)


def append_rows(rel: str, rows: list[tuple], marker: str) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print("skip", rel)
        return
    lines = text.splitlines()
    last = max(i for i, line in enumerate(lines) if line.startswith("|"))
    lines[last + 1: last + 1] = ["| " + " | ".join(r) + " |" for r in rows]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("patched", rel)


def write(rel: str, text: str) -> None:
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("wrote", rel)


write(
    "decisions/ADR-0019-D-019.md",
    """---
title: ADR-0019 — Baseline snapshots and evidence-package export are derived artefacts
purpose: Architecture decision record for D-019.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/, audit/baselines/
version: 1.1-patch.2
status: DECIDED
attribution: GOVERNANCE
---

# ADR-0019 — Baseline snapshots and evidence-package export are derived artefacts

## Context

Drift control requires a comparable reference point, and the freeze needed an exportable
artefact. Both risk becoming a second source of truth beside the Markdown corpus (D-004).

## Decision

1. Baseline snapshots (`audit/baselines/*.json`) are **derived**: regenerated from the
   corpus by `scripts/snapshot_baseline.py`, never hand-edited, never authoritative.
2. The evidence package served by `GET /api/docs/export/{baseline}` is computed at
   request time: SHA-256 over every corpus document plus the live invariant verdicts,
   signed with Ed25519.
3. The package carries `legal_effect: "none"` and remains digital evidence only
   (D-007, `proof/NOTARIAL-BOUNDARY.md`).
4. Drift semantics: an in-place status promotion without a decision reference is a
   **freeze violation**; a newly recorded row with a strong status and no decision
   reference is an **advisory**, because nothing was promoted.
5. Consequently `proof/EVIDENCE-PACKAGE.md` moves from `TARGET` to `PARTIAL`: the
   artefact now exists, while external anchoring stays absent (V-008).

## Evidence

`backend/lib/baselines.py` · `backend/routers/insight.py` ·
`scripts/snapshot_baseline.py` · `GET /api/docs/drift` · `GET /api/docs/export/v1.1`.

## Status

`DECIDED`. The export implementation is `IMPLEMENTED` and **not** `VERIFIED`: no
independent verifier has re-computed a package outside this repository.

## Consequences

- Deleting a snapshot loses nothing: it is regenerable.
- A new weakness is registered: the signing key is unencrypted at rest (V-013).

## Alternatives considered

Storing statuses in a database (rejected: violates D-004). Signing at snapshot time and
caching the signature (rejected: a cached signature can outlive the corpus it describes).

## Security impact

V-013 (HIGH) registered against the portal export path.

## Legal impact

None: the package asserts no legal effect.

## Continuity impact

None: export is read-only and stateless apart from the key file.

## Supersedes / Superseded by

Supersedes: none. Superseded by: none.
""",
)

write(
    "audit/DRIFT-CONTROL.md",
    """---
title: Drift Control
purpose: How baseline drift is measured and what counts as a violation.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: audit/baselines/
version: 1.1-patch.2
status: IMPLEMENTED
attribution: GOVERNANCE
---

# Drift Control

## Method

Two baselines are compared row by row across every registry. For each row the status and
the decision reference are read from the Markdown table; nothing is cached.

| Situation | Classification |
|---|---|
| Row present in both, status strengthened, decision reference present | traced promotion |
| Row present in both, status strengthened, no decision reference | **freeze violation** |
| Row present in both, status weakened | recorded, not a violation |
| Row added with a strong status and no decision reference | advisory |
| Row removed | reported (append-only means this should not happen) |

Status strength order: `REJECTED`/`UNKNOWN`/`OPEN` < `DEPRECATED`/`HISTORICAL`/`REFERENCED`
< `PROPOSED`/`TARGET`/`DEFINED` < `DECIDED` < `OBSERVED` < `PARTIAL` < `IMPLEMENTED` <
`VERIFIED`.

## Baselines

| ID | Meaning |
|---|---|
| `v1.1` | The frozen baseline, reconstructed by removing the rows that `audit/PATCH-001-KILTIKONET.md` records as added after the freeze |
| `v1.1-patch.1` | The corpus after PATCH-001-KILTIKONET |
| `current` | The working corpus, computed at request time |

Snapshots live in `audit/baselines/` and are derived artefacts (D-019).

## Surfaces

`GET /api/docs/baselines` · `GET /api/docs/drift?base=<id>&target=<id>` · portal view
`/drift`.
""",
)

append_rows("decisions/DECISION-REGISTRY.md", [D019], "| D-019 |")
append_rows("registry/VULNERABILITY-REGISTRY.md", [V013], "| V-013 |")

# Traced edit of a v1.1 document, authorised by D-019.
p = ROOT / "proof/EVIDENCE-PACKAGE.md"
text = p.read_text(encoding="utf-8")
if "ADR-0019" not in text:
    text = text.replace("status: TARGET", "status: PARTIAL", 1)
    text = text.replace(
        "# EvidencePackage — TARGET\n\n> Specification only. No implementation of this artefact was observed.",
        "# EvidencePackage — PARTIAL\n\n> Status changed from `TARGET` to `PARTIAL` by "
        "`decisions/ADR-0019-D-019.md`: the portal now emits signed packages at "
        "`GET /api/docs/export/{baseline}`. External anchoring remains absent (V-008), and "
        "`IMPLEMENTED` does not imply `VERIFIED`.",
    )
    p.write_text(text, encoding="utf-8")
    print("patched proof/EVIDENCE-PACKAGE.md (traced by ADR-0019)")

# Manifest: register the second post-freeze patch.
mp = ROOT / "audit/freeze-manifest.yaml"
mtext = mp.read_text(encoding="utf-8")
if "PATCH-002-GOVERNANCE-TOOLING" not in mtext:
    mtext = mtext.replace(
        "sections_added:\n",
        "  - id: PATCH-002-GOVERNANCE-TOOLING\n"
        "    record: audit/DRIFT-CONTROL.md\n"
        "    decision: decisions/ADR-0019-D-019.md\n"
        "    type: tooling\n"
        "    freeze_rewritten: false\n"
        "sections_added:\n",
    )
    mp.write_text(mtext, encoding="utf-8")
    print("patched audit/freeze-manifest.yaml")

cl = ROOT / "CHANGELOG.md"
ctext = cl.read_text(encoding="utf-8")
if "PATCH-002" not in ctext:
    cl.write_text(
        ctext.rstrip()
        + """

## v1.1-patch.2 — PATCH-002-GOVERNANCE-TOOLING (post-freeze tooling patch)

- Added drift control (`audit/DRIFT-CONTROL.md`, baselines in `audit/baselines/`),
  signed evidence-package export, and per-system cards in the portal.
- Added decision D-019 with `decisions/ADR-0019-D-019.md`, vulnerability V-013.
- `proof/EVIDENCE-PACKAGE.md` moved TARGET → PARTIAL, traced by ADR-0019.
""",
        encoding="utf-8",
    )
    print("appended CHANGELOG.md")

print("PATCH-002 generated")
