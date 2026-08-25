---
title: Brain Internals
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Brain Internals

Solid = implemented somewhere in the estate. Dashed = `PROPOSED`.

```mermaid
graph TB
  Q["Query surface<br/>3 separate entry points"] --> P["Persona Engine<br/>LAUR · IMPLEMENTED"]
  P --> R["Reasoning<br/>classifier only · PARTIAL"]
  R --> MR["Model Router<br/>FACTORY · IMPLEMENTED"]
  MR --> SOV["Sovereign fallback<br/>deterministic"]
  MR --> EXT["External providers"]
  R -.-> D["Doctrine Engine<br/>3 owners · CONTESTED"]
  R -.-> SM["Semantic Memory<br/>PROPOSED"]
  R -.-> IM["Institutional Memory<br/>PROPOSED"]
  R -.-> LE["Learning Engine<br/>META · PARTIAL"]
  R -.-> EM["Emergency Engine<br/>PROPOSED"]
```


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
