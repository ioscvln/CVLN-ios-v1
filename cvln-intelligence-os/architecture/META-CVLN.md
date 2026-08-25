---
title: META CVLN
purpose: Specify the governance layer as audited.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# META CVLN

Layer 0. Purpose: operating system kernel — constitution, governance, registry,
permissions, runtime state, workflows, entities, objectives, capabilities.

## Implemented subsystems

Identity and RBAC (6 roles) · entity and repository registry · capability discovery
(`PARTIAL`) · signed event bus (Ed25519, notary DID) · decision system (6 verbs) ·
adaptive runtime state (`normal|degraded|critical`, 7 signals, hysteresis) · learning
proposals with human approval · notarisation with public verification · domain
overviews and loop maps · outbound adapters · scheduled registry pings.

## Architectural notes

The backend is a single 1,611-line FastAPI module. The frontend is JavaScript CRA,
diverging from the estate's TypeScript direction. Neither prevents operation, but both
raise the cost of the target integrations.

## Not implemented

Kernel status. Nothing in the estate depends on META. It observes and actuates; it
does not govern by dependency.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
