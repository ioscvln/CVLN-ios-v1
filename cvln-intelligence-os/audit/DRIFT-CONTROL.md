---
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
| `v1.1-patch.2` | The corpus after PATCH-002-GOVERNANCE-TOOLING |
| `v1.1-patch.3` | The corpus after PATCH-003-ANCHORING-AND-OPEN-QUESTIONS |
| `current` | The working corpus, computed at request time |

Snapshots live in `audit/baselines/` and are derived artefacts (D-019).

**History continuity.** Every patch recorded in `audit/freeze-manifest.yaml` keeps its own
snapshot, and a snapshot is never replaced by a later one: the drift history must remain
continuous and comparable pairwise. `INV-017` asserts that every expected baseline file
exists and is non-empty. A missing snapshot is regenerated deterministically by
`scripts/snapshot_baseline.py`, which excludes from each baseline exactly the rows that
the later patch records document as added.

## Surfaces

`GET /api/docs/baselines` · `GET /api/docs/drift?base=<id>&target=<id>` · portal view
`/drift`.
