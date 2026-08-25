---
title: Learning
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Learning

## Implemented — META CVLN

`/learning/proposals` with a configurable `LEARNING_PROPOSAL_THRESHOLD`. Approval at
`/learning/proposals/{id}/approve` appends a `doctrine_history` record carrying
evidence. No automatic doctrine mutation exists anywhere.

## Not implemented

Automatic aggregation from feedback into proposals — META documents this gap itself.
Feedback is collected at `/feedback`; conversion to proposals remains manual.

## Binding constraint

`LEARN` may propose. Only a human may approve. Any future autonomy work that weakens
this constraint contradicts `constitution/CVLN-CONSTITUTION-v1.md` Article III.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
