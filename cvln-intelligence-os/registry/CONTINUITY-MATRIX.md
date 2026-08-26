---
title: Continuity Matrix
purpose: Per-capability behaviour across Normal, Degraded, Offline and Recovery.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: registry/
version: 1.1
status: PARTIAL
attribution: MIXED
---

# Continuity Matrix

One row per continuity-relevant capability. A cell describes intended behaviour; the `Status` column states whether that behaviour is implemented.

| ID | Capability | Normal | Degraded | Offline | Recovery | Evidence | Status |
|---|---|---|---|---|---|---|---|
| K-001 | Human decision of record | Available | Available | Queued locally, replayed on reconnect | Replay with conflict report | META decisions endpoints | TARGET |
| K-002 | Agent execution | Available | Reduced concurrency | Deterministic sovereign provider only | Checkpoint resume | FACTORY provider_layer.py sovereign fallback | PARTIAL |
| K-003 | Event bus delivery | Available | Spool + DLQ | Local spool, no external fan-out | Spool replay in order | FACTORY event_bus.py | IMPLEMENTED |
| K-004 | Model routing | Full provider table | Fallback chain | Sovereign deterministic provider | Re-probe providers | FACTORY provider_layer.py | IMPLEMENTED |
| K-005 | Runtime state signalling | normal | degraded | critical / offline | Hysteresis-guarded return to normal | META /runtime/state | IMPLEMENTED |
| K-006 | Evidence packaging | Available | Available | Local hashing only, no anchoring | Anchor backlog flush | none | TARGET |
| K-007 | Power-loss durability of journals | Durable | Durable | Durable append-only spool | Integrity scan on boot | none | TARGET |
| K-008 | Documentation portal | Available | Available | Static corpus read from disk | No recovery step required | backend/lib/corpus.py | IMPLEMENTED |

## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.
