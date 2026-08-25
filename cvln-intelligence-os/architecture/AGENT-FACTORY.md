---
title: CVLN Agent Factory
purpose: Specify the agent runtime as audited.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# CVLN Agent Factory

Layer 2. Purpose: nervous system — ADL, runtime, scheduler, event bus, autonomy,
capability execution, lifecycle, evolution, journal, gates.

## Implemented subsystems

ADL v1 (Pydantic, `AGT-nnn`, semver, 7-stage lifecycle with computed transitions) ·
ADL v2 (JSON Schema, `DEFINED`) · agent lifecycle, versions, diffs, checkpoints,
export, wake · gate system with levels, critical actions and an append-only journal ·
event bus with an enforced topic namespace, dead letter queue and spool replay ·
model router with four providers and a guaranteed terminal fallback · doctrine engine ·
constitution and amendment service · autonomy modes and cycles (`PARTIAL`) · layered
memory with human entry validation (`PARTIAL`) · continuity, backup and daily closing.

## Precise statement about cognition

`backend/cognitive_engine.py` provides `classify_message()` and
`internal_response()`. This is deterministic classification and templated response.
Model-based reasoning is reachable only through `provider_layer.py`. The repository's
own doctrine (`DOC-ARC-04`) is consistent with this separation.

## Not implemented

Any dependency on META, and any consumer relationship with Laurentia. Agent Factory
executes, but nothing outside it currently asks it to.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
