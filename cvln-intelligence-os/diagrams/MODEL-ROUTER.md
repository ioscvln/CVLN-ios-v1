---
title: Model Router
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Model Router

```mermaid
graph LR
  CALL["Cognition request"] --> S{"strategy"}
  S -->|quality| A1["anthropic"]
  S -->|cost| G1["gemini"]
  S -->|sovereign_only| SV["sovereign"]
  A1 -->|fail| O1["openai"]
  O1 -->|fail| G1
  G1 -->|fail| SV["sovereign<br/>cvln-internal-deterministic<br/>cannot fail"]
  A1 --> JR["Journal every call"]
  SV --> JR
```

Laurentia does not participate in this graph — gap `G-011`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
