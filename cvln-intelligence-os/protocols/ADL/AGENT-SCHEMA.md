---
title: ADL Agent Schema
purpose: Specify part of the implemented ADL protocol.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# ADL Agent Schema

Field-level schema of a CVLN agent, as validated in code.

| Field | Type | Constraint | Status |
|---|---|---|---|
| `agent_id` | string | `^AGT-\d{3}$` | IMPLEMENTED |
| `version` | string | semver | IMPLEMENTED |
| `lifecycle_status` | enum | 7 stages | IMPLEMENTED |
| `brain.memory.scope` | enum | session / persistent | IMPLEMENTED |
| `brain.memory.owner` | string | — | IMPLEMENTED |
| `brain.events.subscribe` | list | topic prefixes | IMPLEMENTED |
| `brain.events.publish` | list | topic prefixes | IMPLEMENTED |
| `capabilities` | list | ADL v2 top-level property | DEFINED |
| `autonomy_level` | integer | route exists at `/agents/{id}/autonomy` | PARTIAL |
| `risk_level` | enum | referenced by gates | PARTIAL |
| `permissions` | list | not observed in schema | PROPOSED |
| `tools` | list | not observed in schema | PROPOSED |

Rows marked `PROPOSED` are fields the brief expects but the schema does not contain.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`
