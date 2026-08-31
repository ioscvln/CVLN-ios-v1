"""PATCH-003-ANCHORING-AND-OPEN-QUESTIONS — append-only, post-freeze.

Records external anchoring (OpenTimestamps, provider-neutral) and the open-questions
register. Run: python scripts/gen_patch3_anchoring.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/app/cvln-intelligence-os")

D020 = (
    "D-020",
    "External anchoring is independent temporal evidence, never a qualified timestamp",
    "OpenTimestamps proves that a digest existed and is unchanged; legal qualification requires a separate qualified authority",
    "ARCHITECTURE",
    "backend/lib/anchoring.py, audit/anchors/index.json",
    "DECIDED",
    "proof/",
    "ADR-0020",
)

D021 = (
    "D-021",
    "Open questions are a governed register with human-owned ownership fields",
    "Owner and Due are never generated; UNASSIGNED and TBD are truthful values, not placeholders to be filled by a tool",
    "GOVERNANCE",
    "governance/OPEN-QUESTIONS.md, scripts/gen_open_questions.py",
    "DECIDED",
    "governance/",
    "ADR-0021",
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
    "proof/EXTERNAL-ANCHORING.md",
    """---
title: External Anchoring
purpose: How an evidence-package digest is anchored outside the estate, and what that does and does not prove.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1-patch.3
status: PARTIAL
attribution: MIXED
---

# External Anchoring

## What is anchored

The `chain_hash` of an evidence package — a SHA-256 digest over every corpus document
hash and every invariant verdict. The corpus itself is never transmitted: a calendar sees
a 32-byte digest and nothing else.

## What an OpenTimestamps proof proves

- That the digest **existed** at the moment it was accepted, and later that it was
  included in a Bitcoin block once the attestation is upgraded.
- That the anchored corpus state **has not changed** since: any edit changes the digest.

## What it does not prove — stated explicitly

| Claim | Position |
|---|---|
| Qualified electronic timestamp (eIDAS) | **No.** OpenTimestamps is not a qualified trust service. |
| Legal opposability / legal effect | **No.** `legal_effect` stays `"none"` (D-007). |
| Legal attestation of content | **No.** Digital evidence only (`proof/NOTARIAL-BOUNDARY.md`). |
| Confirmation on submission | **No.** A submitted digest is `pending` until the Bitcoin attestation is merged. |
| Full verification by the portal | **No.** The portal performs structural verification; authoritative verification is `ots verify <digest>.ots` against a Bitcoin node. |

The correct wording, used throughout this corpus and the portal, is: *independent
evidence of temporal existence and integrity*.

## Provider model

The interface is provider-neutral so a qualified authority can be **added alongside**
OpenTimestamps, never replacing it.

| Provider | Status | Meaning |
|---|---|---|
| `ots` | IMPLEMENTED | OpenTimestamps public Bitcoin calendars, no credentials required |
| `rfc3161` | TARGET | Reserved for a qualified RFC 3161 / eIDAS authority; returns `unavailable` until configured |

A future qualified anchor is recorded as a second record over the same digest, so a
package can carry both.

## States

| State | Meaning |
|---|---|
| `pending` | A calendar accepted the digest; the Bitcoin attestation is not yet merged |
| `confirmed` | The Bitcoin attestation has been merged into the stored `.ots` proof |
| `offline` | No calendar was reachable; nothing is claimed |
| `unavailable` | The requested provider has no configuration (e.g. `rfc3161`) |

Anchors are derived artefacts stored in `audit/anchors/` (`index.json` plus one `.ots`
file per digest). Losing them loses no canonical content; the corpus remains the source
of truth (D-004, D-019).

## Surfaces

`GET /api/docs/anchor/providers` · `GET /api/docs/anchors` ·
`POST /api/docs/anchor/{baseline}` · `POST /api/docs/anchor/{digest}/upgrade` ·
`GET /api/docs/anchor/{digest}/verify`. The evidence package carries the anchor record
and the base64 `.ots` proof when one exists; `anchored_at` is set only for a `confirmed`
anchor.

Decision: D-020 (`decisions/ADR-0020-D-020.md`). Configuration: `OTS_CALENDARS`,
`OTS_TIMEOUT_SECONDS`.
""",
)

write(
    "decisions/ADR-0020-D-020.md",
    """---
title: ADR-0020 — External anchoring is independent temporal evidence, never a qualified timestamp
purpose: Architecture decision record for D-020.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1-patch.3
status: DECIDED
attribution: GOVERNANCE
---

# ADR-0020 — External anchoring is independent temporal evidence

## Context

An evidence package signed by the estate's own key proves integrity but not that a state
existed at a given time: the estate could re-sign a rewritten corpus. An external anchor
removes that degree of freedom.

## Decision

1. The `chain_hash` of an evidence package may be anchored with an external provider.
2. `ots` (OpenTimestamps, Bitcoin calendars) is the implemented provider. No credentials
   are required and only the digest leaves the estate.
3. The proof is described **only** as independent evidence of temporal existence and
   integrity. It is never described as a qualified, eIDAS or legally opposable timestamp.
4. `rfc3161` is reserved as a second provider so a qualified authority can be added
   **alongside** OpenTimestamps; adding it must not remove or supersede the OTS anchor.
5. Submission yields `pending`. Only a merged Bitcoin attestation yields `confirmed`, and
   only a `confirmed` anchor sets `anchored_at` in the package.
6. The portal performs structural verification only. Authoritative verification is
   `ots verify` against a Bitcoin node, and is documented as such.
7. Anchors are derived artefacts under `audit/anchors/`; the Markdown corpus stays
   canonical (D-004, D-019).

## Evidence

`backend/lib/anchoring.py` · `backend/routers/insight.py` · `audit/anchors/index.json` ·
live calendar response from `https://a.pool.opentimestamps.org`.

## Status

`DECIDED`; the OTS provider is `IMPLEMENTED` and **not** `VERIFIED`: no Bitcoin-node
verification has been executed inside this environment.

## Consequences

- A rewritten corpus can be detected against any anchored digest.
- Calendar unavailability degrades to `offline` and claims nothing.
- `proof/EVIDENCE-PACKAGE.md` gains `anchor` and `anchor_proof_ots_base64` fields.

## Alternatives considered

A commercial qualified TSA only (rejected for now: credentials and contract absent — and
it would still be added, not substituted). Self-anchoring in a local ledger (rejected:
not independent).

## Security impact

Only a digest is transmitted; no corpus content leaves the estate. Calendars observe
submission timing, which is acceptable for a public specification corpus.

## Legal impact

None asserted. `legal_effect` remains `"none"`; qualification remains an open legal
question (`registry/LEGAL-MATRIX.md`).

## Continuity impact

Anchoring is optional and non-blocking: an unreachable calendar never fails a read path.

## Supersedes / Superseded by

Supersedes: none. Superseded by: none.
""",
)

write(
    "decisions/ADR-0021-D-021.md",
    """---
title: ADR-0021 — Open questions are a governed register with human-owned ownership fields
purpose: Architecture decision record for D-021.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: governance/
version: 1.1-patch.3
status: DECIDED
attribution: GOVERNANCE
---

# ADR-0021 — Open questions are a governed register

## Context

Open questions were scattered across contradictions, UNKNOWN rows and vulnerability
entries. Nothing showed, in one place, what blocks the next freeze.

## Decision

1. `governance/OPEN-QUESTIONS.md` is the register of every open question in the corpus,
   generated from the registries by `scripts/gen_open_questions.py`.
2. Rows are classified `freeze-blocker`, `contradiction`, `unknown-needs-evidence`,
   `risk-needs-decision` or `open-question` by the documented rules in that file.
3. `Owner` and `Due` are **human-owned**: they default to `UNASSIGNED` and `TBD` and are
   preserved verbatim across regenerations. No tool ever guesses an owner or a date.
4. A freeze may not be declared while a `freeze-blocker` row is unresolved.
5. Deleting a row without a resolution record is a freeze violation (INV-015).

## Evidence

`governance/OPEN-QUESTIONS.md` · `scripts/gen_open_questions.py` ·
`GET /api/docs/registry/open-questions`.

## Status

`DECIDED`. The register exists and is rendered; the answers do not.

## Consequences

- The next freeze has an explicit, countable precondition list.
- Assigning an owner is a human act recorded in Markdown, not a portal mutation.

## Alternatives considered

An issue tracker (rejected: would move governance state outside the canonical corpus).
Auto-assigning owners from registry Owner columns (rejected: it would invent
accountability).

## Security impact

None.

## Legal impact

None; several rows concern legal questions but the register asserts no legal position.

## Continuity impact

None.

## Supersedes / Superseded by

Supersedes: none. Superseded by: none.
""",
)

append_rows("decisions/DECISION-REGISTRY.md", [D020, D021], "| D-020 |")

mp = ROOT / "audit/freeze-manifest.yaml"
mtext = mp.read_text(encoding="utf-8")
if "PATCH-003" not in mtext:
    mtext = mtext.replace(
        "sections_added:\n",
        "  - id: PATCH-003-ANCHORING-AND-OPEN-QUESTIONS\n"
        "    record: proof/EXTERNAL-ANCHORING.md\n"
        "    register: governance/OPEN-QUESTIONS.md\n"
        "    decisions: [decisions/ADR-0020-D-020.md, decisions/ADR-0021-D-021.md]\n"
        "    type: tooling\n"
        "    freeze_rewritten: false\n"
        "sections_added:\n",
    )
    mtext = mtext.replace("  - kiltikonet\n", "  - kiltikonet\n  - governance\n")
    mtext = mtext.replace(
        "registries:\n",
        "registries:\n  open-questions: governance/OPEN-QUESTIONS.md\n",
    )
    mtext = mtext.replace(
        "unverified_claims_policy:",
        "  - id: INV-015\n"
        "    rule: every freeze-blocker in the open-questions register carries an owner field and a due field\n"
        "  - id: INV-016\n"
        "    rule: no anchoring artefact is described as a qualified or eIDAS timestamp\n"
        "unverified_claims_policy:",
    )
    mp.write_text(mtext, encoding="utf-8")
    print("patched audit/freeze-manifest.yaml")

cl = ROOT / "CHANGELOG.md"
ctext = cl.read_text(encoding="utf-8")
if "PATCH-003" not in ctext:
    cl.write_text(
        ctext.rstrip()
        + """

## v1.1-patch.3 — PATCH-003-ANCHORING-AND-OPEN-QUESTIONS (post-freeze tooling patch)

- Added external anchoring (`proof/EXTERNAL-ANCHORING.md`, OpenTimestamps provider,
  `rfc3161` reserved as TARGET) and the open-questions register
  (`governance/OPEN-QUESTIONS.md`).
- Added decisions D-020, D-021 with ADRs, and invariants INV-015, INV-016.
- No v1.0 document touched; the v1.1 freeze text is unchanged.
""",
        encoding="utf-8",
    )
    print("appended CHANGELOG.md")

print("PATCH-003 generated")
