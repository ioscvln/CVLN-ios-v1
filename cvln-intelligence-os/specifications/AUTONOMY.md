---
title: Autonomy
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Autonomy

## Implemented — Agent Factory

`/mode` (get and set), `/cycle`, `/cycles`, `/cycles/{cycle_id}`, per-agent autonomy
levels at `/agents/{id}/autonomy`, and `detect_critical_intent()` which forces human
confirmation for critical actions.

## Constraints observed

1. Autonomy is bounded by gate levels; a higher autonomy level does not raise
   authority.
2. Critical intent interrupts autonomous execution.
3. Cycles are recorded and inspectable individually.

## Gap

Cycles have no instruction-level semantics, so an autonomous cycle cannot be audited
step by step (`G-014`). This is the strongest argument for ISA.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
