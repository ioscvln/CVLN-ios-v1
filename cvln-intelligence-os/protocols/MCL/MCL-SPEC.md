---
title: MCL — MetaCVLN Language (PROPOSED)
purpose: Propose a declarative language for the CVLN operating system.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# MCL — MetaCVLN Language (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


## Audit result

No grammar, parser, file extension, test or reference to a MetaCVLN Language was
found in any audited repository. MCL has the weakest standing of the three named
protocols: ADL exists, ISA has close analogues, MCL has neither.

## Motivation

Entities, capabilities, objectives, permissions and workflows are currently expressed
as Python — `registry_data.py`, `doctrine.py`, `GATE_LEVELS`, route handlers. They
cannot be reviewed, diffed or governed as declarations.

## Proposed scope

Entities · capabilities · objectives · permissions · workflows · policies ·
relationships. Grammar sketches: [`ENTITY-SYNTAX.md`](ENTITY-SYNTAX.md),
[`WORKFLOW-SYNTAX.md`](WORKFLOW-SYNTAX.md),
[`PERMISSION-SYNTAX.md`](PERMISSION-SYNTAX.md),
[`VALIDATION.md`](VALIDATION.md).

## Precondition

MCL must not be specified further until `FD-001` and `FD-002` settle what META owns.
A declarative language for contested ownership would encode the contradictions rather
than resolve them.

## Decision

`RFC-0008`, gated by `FD-005`. Priority: below ISA.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0008`
