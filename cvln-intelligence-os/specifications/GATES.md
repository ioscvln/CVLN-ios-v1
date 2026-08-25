---
title: Gates
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Gates

## Implemented — `FACTORY/backend/gate_routes.py`

`GATE_LEVELS` defines authority tiers with labels. `CRITICAL_ACTIONS` enumerates
actions requiring escalation regardless of level. `POST /check` returns
`allowed`, `level`, `decision`, `rule_source` and a human-readable `reason`. A
separate journal router records outcomes append-only.

## Properties worth preserving estate-wide

1. **Denial is explained.** The response names its `rule_source`, so an operator can
   see which rule blocked an action.
2. **Denial is journalled** as `action_bloquee` — non-repudiable.
3. **Escalation converges** on a single queue rather than per-domain queues, which
   prevents authority fragmentation.

This is the most reusable authority mechanism in the estate and the natural basis for
the target `EXECUTE` precondition.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
