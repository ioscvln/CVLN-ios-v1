---
title: Agent Error Protocol
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Agent Error Protocol

## Implemented behaviours

| Failure | Response | Location |
|---|---|---|
| Provider failure | Next provider, then terminal sovereign fallback | `provider_layer.py` |
| Event delivery failure | Dead letter queue, replayable from spool | `event_bus.py` |
| Downstream instability | Circuit breaker opens | Laurentia `circuit_breaker.py` |
| Gate denial | Journalled and escalated | `gate_routes.py` |
| Tampered event | Quarantined | META `/events/verify` |
| Model unavailable in Laurentia | `503`, no fallback | `social_admin.py` — `G-011` |
| Missing upstream endpoint | Upstream `404` surfaced, not masked | wallet adapter — `G-018` |

## Rules

1. Failures are journalled, never swallowed.
2. Every execution path terminates in a defined outcome; Agent Factory guarantees
   this via an infallible terminal provider.
3. Absence of data is reported as absence.

The estate's error handling is materially better than its integration; the single
exception is Laurentia's missing fallback.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
