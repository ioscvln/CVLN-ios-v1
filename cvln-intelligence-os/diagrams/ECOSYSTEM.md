---
title: Ecosystem
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Ecosystem

Current state. Dotted edges are `UNVERIFIED` or unanswered.

```mermaid
graph LR
  META["META CVLN<br/>governance"] -->|adapter| LAUR["LAURENTIA"]
  META -.->|"capabilities · DEGRADED"| FACT["AGENT FACTORY"]
  META -.->|"capabilities · DEGRADED"| LAUR
  META -.->|"404"| WAL["Wallet"]
  LAUR --> PROV["Model providers"]
  FACT --> PROV
  META --> PROV
  LAUR --> KILT["Kiltikonet · LabelOS · FREKCORE"]
  FACT -.-> META
  LAUR -.-> FACT
```

The two dotted edges at the bottom do not exist. They are drawn to make their absence
legible.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
