---
title: Decision Model
purpose: Define the anatomy of a CVLN decision.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Decision Model

## Verbs

META CVLN implements six decision verbs at `/decisions/{decision_id}/action`:
`approve`, `reject`, `edit`, `escalate`, `pause`, `rollback`. `rollback` is
significant: it makes decisions reversible rather than merely recorded.

## Anatomy

| Field | Meaning |
|---|---|
| subject | what is being decided |
| actor | authenticated human, by RBAC role |
| verb | one of the six |
| evidence | linked records supporting the decision |
| timestamp | server-anchored |
| signature | Ed25519 where emitted as a signed event |

## Properties

1. Decisions are human acts. No implemented path auto-approves.
2. Decisions are evidenced — `/evidence` links supporting records.
3. Decisions are notarisable and publicly verifiable via `/public/notarizations`.
4. Doctrine changes to `doctrine_history` occur only through an approved decision.

This is the most complete governance subsystem in the audited estate.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
