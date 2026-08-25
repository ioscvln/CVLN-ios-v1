---
title: Objective Model
purpose: Define objectives as the link between doctrine and execution.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Objective Model

An objective is a stated, measurable intent that agents and operators are directed to
advance.

## Implemented

Agent Factory implements `backend/objectives_routes.py` and `mission_os_routes.py`
with `/missions`, `/briefing` and `/objectives` surfaces. META CVLN implements domain
loop maps — `/finance/loop` (9 stages) and `/people/loop` (11 stages) — where each
stage reports `OK` or `DATA_NOT_AVAILABLE`.

## The DATA_NOT_AVAILABLE property

META's loop maps return an explicit unavailability marker rather than a fabricated
value. Of nine finance stages, six report `OK` and three report `DATA_NOT_AVAILABLE`;
of eleven people stages, five and six respectively. This is a governance property
worth preserving estate-wide: an objective system that cannot lie about its inputs.

## Gap

Objectives are not linked to capabilities or gates. An objective cannot currently be
traced to the agent actions taken to advance it.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
