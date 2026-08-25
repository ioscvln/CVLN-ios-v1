---
title: Permissions
purpose: Define the CVLN permission model.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Permissions

## Implemented models

| System | Model | Subjects |
|---|---|---|
| META CVLN | Role-based access control | admin, cfo, hr_lead, ops_lead, legal_lead, employee |
| Agent Factory | Actor + gate level | `get_current_actor`, `GATE_LEVELS`, `CRITICAL_ACTIONS` |
| Laurentia | API key + commercial tier | Free, Creator, Infinite, Enterprise |

Three permission models exist with no shared subject. An actor in one system has no
identity in another — gap `G-008`.

## Principles

1. Permission is checked before execution, never after.
2. Denial is journalled with actor, action and reason.
3. Critical actions require escalation regardless of role.
4. Tier is a commercial control and must not be used as a security boundary.

## Target

A single identity plane owned by META CVLN issuing tokens that Agent Factory and
Laurentia verify. `PROPOSED`, blocked on `FD-002`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
