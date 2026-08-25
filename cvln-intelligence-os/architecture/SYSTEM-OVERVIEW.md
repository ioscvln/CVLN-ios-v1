---
title: System Overview
purpose: Single-page orientation to the CVLN Intelligence OS as audited and as targeted.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# System Overview

CVLN today is three independently deployable systems that share a vocabulary. The
five-layer OS is the target, not the current state.

| Layer | Component | Audited status |
|---|---|---|
| 0 | META CVLN | IMPLEMENTED as a governance plane; depended upon by nothing |
| 1 | CVL BRAIN | PARTIAL — interface, persona and knowledge exist; no Brain service |
| 2 | CVLN AGENT FACTORY | IMPLEMENTED — largest codebase, ADL, gates, router |
| 3 | LAURENTIA | IMPLEMENTED — standalone operator product |
| 4 | Applications | REFERENCED |

## Where the weight actually is

Agent Factory holds ~143 routes across 30 modules and the estate's only agent
definition language. META holds the estate's only cryptographic trust chain.
Laurentia holds the estate's only encryption at rest and its only external product
surface. No single system holds intelligence.

## Diagrams

Current state: [`../diagrams/ECOSYSTEM.md`](../diagrams/ECOSYSTEM.md) ·
layers: [`../diagrams/LAYERED-OS.md`](../diagrams/LAYERED-OS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`
