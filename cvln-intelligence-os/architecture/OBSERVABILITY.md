---
title: Observability
purpose: Specify what can currently be observed.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Observability

## Implemented

META: registry pings with history, runtime signals, timeline, evidence store, public
audit surface. Agent Factory: append-only activity journal, gate journal, per-call
provider journalling, dead letter queue. Laurentia: activity log, circuit-breaker
signals.

## Not implemented

Distributed tracing, correlated identifiers, or any estate-wide view. A cross-system
incident cannot currently be reconstructed (`G-013`). META documents this gap itself.

## Minimum target

One trace identifier, generated at the entry edge and propagated in the shared event
envelope. This requires the envelope decision (`G-003`) and nothing else.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
