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
| `current` | The working corpus, computed at request time |

Snapshots live in `audit/baselines/` and are derived artefacts (D-019).

## Surfaces

`GET /api/docs/baselines` · `GET /api/docs/drift?base=<id>&target=<id>` · portal view
`/drift`.
