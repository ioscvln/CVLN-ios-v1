---
title: Implementation Status
purpose: Aggregate status distribution across the audited estate.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Implementation Status

Derived from [`COMPONENT-MATRIX.md`](COMPONENT-MATRIX.md). Each component holds
exactly one status.

## Distribution

| Status | Count | Reading |
|---|---|---|
| IMPLEMENTED | 26 | Executable code verified by path |
| PARTIAL | 8 | Code exists, subsystem incomplete or unwired |
| DEFINED | 2 | Schema or contract only |
| REFERENCED | 0 | No component rests on this status alone |
| PRIVATE / NOT VISIBLE | 1 | `sovereign-brain/` |
| PROPOSED | 7 | ISA, MCL, handshake, memory graph, observability, SDK, widget |
| UNKNOWN | 1 | Model training infrastructure |
| **Total** | **45** | Rows in `COMPONENT-MATRIX.md` |

These counts are computed live by the portal from the component matrix table; the
matrix, not this summary, is authoritative.

## By repository

| Repository | IMPLEMENTED | PARTIAL | DEFINED | Other |
|---|---|---|---|---|
| CVLN AGENT FACTORY | 10 | 3 | 1 | 0 |
| META CVLN | 7 | 4 | 1 | 0 |
| LAURENTIA | 9 | 1 | 0 | 3 |
| No repository | 0 | 0 | 0 | 6 |

Agent Factory carries the highest implemented weight; Laurentia carries the highest
count of externally-facing implemented capability; META carries the estate's only
cryptographic trust chain.

## Attribution discipline

No component in v1.0 is asserted at `DEPLOYED RUNTIME`. Static analysis cannot
establish deployment, and the audit does not claim what it did not observe.

## Future RFC references

`RFC-0002`, `RFC-0003`, `RFC-0007`, `RFC-0008`.
