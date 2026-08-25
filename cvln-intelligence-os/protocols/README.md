---
title: Protocols — Status Notice
purpose: Separate protocols that exist from protocols that are proposed.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Protocols — Status Notice

The initial brief named three protocols: ISA, ADL and MCL. The audit tested each
against the repositories. They are **not** equivalent in standing.

| Protocol | Found in repositories | Status | Location |
|---|---|---|---|
| **ADL** — Agent Definition Language | Yes — `FACTORY/backend/adl_schema.py` + `schemas/adl_v2_schema.json` | IMPLEMENTED (v1), DEFINED (v2) | [`ADL/`](ADL/ADL-v1.md) |
| **ISA** — Intelligence System Architecture instruction set | No | PROPOSED | [`ISA/`](ISA/ISA-SPEC.md) |
| **MCL** — MetaCVLN Language | No | PROPOSED | [`MCL/`](MCL/MCL-SPEC.md) |
| **Agent Protocol** — handshake, messages, memory, tools, reports, errors | Partially — event bus and contracts exist; no handshake | Mixed | [`AGENT-PROTOCOL/`](AGENT-PROTOCOL/HANDSHAKE.md) |

ISA and MCL are quarantined proposals introduced by this specification. Neither is
CVLN technology, and neither may be cited as one until `RFC-0007` / `RFC-0008` are
ratified. Presenting them otherwise would retroactively attribute invented
terminology to CVLN — the exact failure this repository exists to prevent.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0007`, `RFC-0008`
