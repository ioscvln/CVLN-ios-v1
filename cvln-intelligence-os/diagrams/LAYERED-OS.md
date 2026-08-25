---
title: Layered OS
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Layered OS

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mermaid
graph TB
  L4["Layer 4 · Applications"] --> L3["Layer 3 · LAURENTIA"]
  L3 --> L2["Layer 2 · CVLN AGENT FACTORY"]
  L3 --> L1["Layer 1 · CVL BRAIN"]
  L2 --> L1
  L1 --> L0["Layer 0 · META CVLN"]
  L2 --> L0
```

No edge above is implemented today.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
