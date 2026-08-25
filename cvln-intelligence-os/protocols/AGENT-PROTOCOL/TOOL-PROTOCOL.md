---
title: Agent Tool Protocol
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Agent Tool Protocol

## Implemented

Tool invocation exists as capability execution in Agent Factory, gated by
`gate_routes.py`, and as bridges in Laurentia
(`kiltikonet_bridge.py`, `labelos_bridge.py`, `frekcore_bridge.py`).

## Rules

1. A tool call is a capability execution and requires a gate decision.
2. Tool failure is an `OBSERVE` result, never a silent retry — Laurentia's echo
   pipeline retries three times then skips and records the skip.
3. External tool credentials never leave the calling service.

## Not implemented

A declared `tools` field in ADL. Tools are bound in code, not in agent definitions.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
