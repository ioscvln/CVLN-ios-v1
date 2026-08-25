---
title: Capability Model
purpose: Define capabilities as the unit of executable competence.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Capability Model

A capability is a named, versioned, permission-scoped competence that a CVLN
component can execute on request.

## Defined contract

META CVLN defines `Capability` in `backend/contracts.py` as one of five versioned
inter-system contracts. Status: `DEFINED` — the model exists; no component consumes
it.

## Implemented execution

Agent Factory executes capabilities through ADL-declared agents. The ADL v2 schema
carries a top-level `capabilities` property, making capability declaration part of
agent identity rather than an afterthought.

## Required advertisement

Every CVLN service is required to expose `GET /api/capabilities` returning
contract-conformant descriptors. **No service currently does**, which is why estate
discovery returns `DEGRADED` for all twelve registry entries. This is the single
cheapest high-value fix available (`G-002`).

## Capability descriptor fields

`id`, `version`, `owner`, `inputs`, `outputs`, `permissions`, `risk`, `gate_level`.
Fields beyond those present in `contracts.py::Capability` are `PROPOSED`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
