---
title: Event Bus
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Event Bus

```mermaid
graph TB
  subgraph F["AGENT FACTORY · unsigned"]
    FT["topic prefixes"] --> FD["DLQ"] --> FS["spool replay"]
  end
  subgraph L["LAURENTIA · unsigned"]
    LO["orchestrator"] --> LC["circuit breaker"]
  end
  subgraph M["META · signed"]
    ME["/events/emit"] --> MS["Ed25519"] --> MV["/events/verify"] --> MQ["quarantine on tamper"]
  end
  F -.->|"no shared envelope"| M
  L -.->|"no shared envelope"| M
```


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
