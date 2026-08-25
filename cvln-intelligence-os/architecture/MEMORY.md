---
title: Memory
purpose: Specify memory as audited.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Memory

Three unrelated stores, no shared schema, no cross-system retrieval.

| Store | Owner | Properties |
|---|---|---|
| Layered memory | Agent Factory | `/memory`, `/memory-layers/summary`, human validation of entries |
| `laurentia_memory` | Laurentia | per-tenant, AES-256-GCM encrypted |
| Evidence and event history | META | signed events, notarisations, `doctrine_history` |

## Notable property

Agent Factory requires human validation of memory entries
(`/memory/entries/{id}/validate`). Memory poisoning is therefore gated rather than
assumed away — a defensible design that the target should preserve.

## Not implemented

Any graph structure, shared identifier space, or semantic retrieval across systems. A
"CVLN Memory Graph" is `PROPOSED` — see
[`../specifications/MEMORY-GRAPH.md`](../specifications/MEMORY-GRAPH.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
