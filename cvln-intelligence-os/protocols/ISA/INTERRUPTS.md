---
title: ISA Interrupts (PROPOSED)
purpose: Specify a proposed ISA facility.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# ISA Interrupts (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


An interrupt suspends a cycle before its next instruction.

| Interrupt | Trigger | Effect | Existing analogue |
|---|---|---|---|
| `GATE_DENIED` | Gate refuses `EXECUTE` | Cycle ends, journalled, escalated | `gate_routes.py` `action_bloquee` — IMPLEMENTED |
| `CRITICAL_INTENT` | Intent classifier flags a critical action | Human confirmation required | `detect_critical_intent()` — IMPLEMENTED |
| `RUNTIME_CRITICAL` | Runtime mode enters `critical` | Non-essential cycles suspended | META `/runtime/state` — IMPLEMENTED |
| `PROVIDER_EXHAUSTED` | All providers fail | Terminal sovereign fallback | `provider_layer.py` — IMPLEMENTED |
| `CIRCUIT_OPEN` | Downstream circuit breaker opens | Cycle deferred | Laurentia `circuit_breaker.py` — IMPLEMENTED |
| `DOCTRINE_CONFLICT` | Plan conflicts with doctrine | Escalated to a decision | `/doctrine/check` — PARTIAL |

## Observation

Five of six proposed interrupts already have working implementations in the estate.
ISA's interrupt model is therefore mostly a naming exercise over proven behaviour,
which is the strongest argument in its favour.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0007`
