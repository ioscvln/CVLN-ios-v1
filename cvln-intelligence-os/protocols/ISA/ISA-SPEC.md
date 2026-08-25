---
title: ISA — Intelligence System Architecture (PROPOSED)
purpose: Propose a native execution cycle for CVLN agents.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# ISA — Intelligence System Architecture (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


## Why proposed and not documented

The audit searched all three repositories for instruction-set semantics. None exists.
The closest implemented artefacts are Agent Factory's autonomy cycles
(`/cycle`, `/cycles`) and META's `ExecutionStep` / `ExecutionPlan` contracts. Neither
defines instructions with ownership, permissions and error handling.

## Proposed instruction set

Eight instructions: `REASON`, `PLAN`, `MEMORY_READ`, `MEMORY_WRITE`, `EXECUTE`,
`OBSERVE`, `LEARN`, `REPORT`. Each is specified in
[`INSTRUCTION-SET.md`](INSTRUCTION-SET.md).

## Proposed invariants

1. Every instruction is journalled with actor, agent, inputs digest and outcome.
2. `EXECUTE` requires a prior gate decision — reusing Agent Factory's implemented
   gate system rather than inventing an authority model.
3. `MEMORY_WRITE` requires validation, reusing the implemented human-validation
   pattern at `/memory/entries/{id}/validate`.
4. `LEARN` may only produce proposals. It may never mutate doctrine — this preserves
   META's implemented and strongest governance property.
5. Instructions are deterministic in their effects on state, even when `REASON` is
   non-deterministic in output.

## Adoption cost

Moderate. Invariants 2, 3 and 4 map onto subsystems that already exist. Adoption is
mainly a matter of naming and journalling what Agent Factory already does.

## Decision

`RFC-0007`, gated by founder decision `FD-005`. Rejection is a legitimate outcome:
nothing in the estate depends on ISA.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0007`
