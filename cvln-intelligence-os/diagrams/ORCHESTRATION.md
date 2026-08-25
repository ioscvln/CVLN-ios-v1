---
title: Multi-agent Orchestration
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Multi-agent Orchestration

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mermaid
sequenceDiagram
  participant O as Operator
  participant B as CVL BRAIN
  participant F as AGENT FACTORY
  participant A1 as AGT-014
  participant M as META
  O->>B: objective
  B->>B: REASON, PLAN
  B->>F: execute plan steps
  F->>F: gate check per step
  F->>A1: EXECUTE capability
  A1-->>F: result
  F->>M: signed REPORT with trace_id
  M-->>O: decision of record
```

No implemented path performs this sequence.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
