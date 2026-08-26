---
title: Continuity Model
purpose: Normal, degraded, offline and recovery states.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: resilience/
version: 1.1
status: PARTIAL
attribution: MIXED
---

# Continuity Model

## State machine

```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Degraded: signal loss / provider failure
    Degraded --> Offline: connectivity or power loss
    Degraded --> Normal: signals recovered (hysteresis)
    Offline --> Recovery: connectivity restored
    Recovery --> Normal: replay complete + integrity scan passed
    Recovery --> Degraded: replay conflicts outstanding
```

## State definitions

| State | Definition | Observed control |
|---|---|---|
| Normal | All signals nominal | META `/runtime/state` = normal |
| Degraded | Reduced capability, service preserved | META degraded/critical states with hysteresis |
| Offline | No external connectivity or provider access | FACTORY sovereign deterministic provider |
| Recovery | Reconnected, replaying spooled work | FACTORY event-bus spool replay |

## Rule

Recovery is complete only when replay finished **and** an integrity scan passed. A
partially replayed system remains `Degraded`.

Matrix: `registry/CONTINUITY-MATRIX.md`. Decision: D-006.
