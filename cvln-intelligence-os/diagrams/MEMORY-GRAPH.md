---
title: Memory Graph
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Memory Graph

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mermaid
graph LR
  E["Entity"] --> A["Agent · ADL"]
  A --> C["Capability"]
  C --> DEC["Decision"]
  DEC --> EVD["Evidence"]
  A --> M["Memory entry"]
  M --> V["Validation · human"]
  DOC["Doctrine article"] --> DEC
```

Today three unrelated stores exist and none of these edges is materialised.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
