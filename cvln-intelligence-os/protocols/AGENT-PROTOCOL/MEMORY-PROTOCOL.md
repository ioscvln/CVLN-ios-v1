---
title: Agent Memory Protocol
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Agent Memory Protocol

## Implemented

Agent Factory: `/memory`, `/memory-layers/summary`, and human validation at
`/memory/entries/{entry_id}/validate`. Laurentia: encrypted per-tenant memory. ADL
binds an agent to a memory scope (`session` or `persistent`) and an owner.

## Rules derived from implementation

1. Every entry has an owning agent — ADL `BrainMemory.owner`.
2. Scope is declared, not inferred.
3. Entries are validated before they influence behaviour. Memory poisoning is gated
   rather than assumed away.

## Not implemented

Cross-system read, shared identifiers, provenance chains, or graph traversal
(`G-010`).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
