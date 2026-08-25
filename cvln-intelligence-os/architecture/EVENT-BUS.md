---
title: Event Bus
purpose: Specify eventing across the estate.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Event Bus

Three independent buses exist (`C-007`).

| Bus | Guarantees | Trust |
|---|---|---|
| Agent Factory `event_bus.py` | Topic namespace, dead letter queue, spool replay | unsigned |
| Laurentia `orchestrator/event_bus.py` | Circuit breaker, signals | unsigned |
| META `/events/emit` | Ed25519 signature over canonical payload, quarantine on tamper | signed |

## Topic namespace (Agent Factory, implemented)

`agent.` · `factory.` · `monitoring.` · `memory.` · `identity.` · `daily.` ·
`system.` — enforced by prefix validation.

## Target envelope

`META/backend/contracts.py::Event`, signed, with a propagated trace identifier. The
contract already exists and has no consumers (`G-017`); adoption is the whole task.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
