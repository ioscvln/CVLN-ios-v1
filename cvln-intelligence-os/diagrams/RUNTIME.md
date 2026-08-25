---
title: Runtime
purpose: Mermaid architecture diagram bound to audit evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Runtime

Agent Factory execution with gate authority.

```mermaid
graph TB
  REQ["Request"] --> GATE{"Gate check<br/>GATE_LEVELS"}
  GATE -->|denied| J["Journal · action_bloquee"] --> ESC["Single escalation queue"]
  GATE -->|permitted| LC["Lifecycle check<br/>7 stages"]
  LC --> COG["classify_message"]
  COG --> MR["provider_layer"]
  MR --> EV["event_bus · agent.*"]
  EV -->|failure| DLQ["Dead letter queue"] --> SPOOL["Replay spool"]
```


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
