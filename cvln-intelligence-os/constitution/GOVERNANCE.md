---
title: Governance
purpose: Define how CVLN decisions are made and recorded.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Governance

Governance is exercised through decisions of record. META CVLN implements the
decision system at `/decisions/{id}/action` with six verbs: approve, reject, edit,
escalate, pause, rollback. Every decision is retained and linked to evidence.

## Bodies

| Body | Authority | Implementation |
|---|---|---|
| Founder | Final authority on constitution, doctrine ownership, sovereignty claims | `FACTORY/backend/founder_council.py`, `founder_routes.py` — IMPLEMENTED |
| Governance plane | Decisions of record, notarisation, learning approval | META `/decisions`, `/notarizations` — IMPLEMENTED |
| Runtime authority | Gate decisions, lifecycle transitions | Agent Factory `gate_routes.py` — IMPLEMENTED |

## Escalation

Gate denial escalates to a single queue rather than a per-domain queue — an
implemented Agent Factory property that prevents authority fragmentation.

## Contested ownership

Governance and constitution are implemented in both META and Agent Factory with no
cross-reference. See `audit/CONTRADICTIONS.md` C-002 and founder decision `FD-002`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
