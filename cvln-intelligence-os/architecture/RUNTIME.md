---
title: Runtime
purpose: Specify runtime state and degradation behaviour.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Runtime

## Implemented

META CVLN computes runtime mode automatically over seven signals — `total_pings`,
`up_pings`, `error_rate`, `avg_ms`, `p95_ms`, `active_incidents`, `window` — producing
`normal`, `degraded` or `critical` with hysteresis to prevent flapping, plus an
explicit administrative override. Agent Factory independently implements autonomy
modes and execution cycles.

## Degradation policy

Mode is derived, not declared. A policy document accompanies the computed mode, so a
reader can see why the system considers itself degraded. Hysteresis is the detail that
makes the signal trustworthy in operation.

## Gap

Runtime mode is not propagated. Agent Factory and Laurentia do not observe META's
mode, and META does not observe theirs. Estate-wide degradation is therefore not a
controllable state.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
