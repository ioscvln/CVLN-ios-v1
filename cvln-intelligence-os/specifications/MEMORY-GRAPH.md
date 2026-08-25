---
title: Memory Graph
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Memory Graph

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


No graph exists. Three unrelated stores exist (`G-010`).

## Proposed node and edge types

| Node | Source today |
|---|---|
| Entity | META registry |
| Agent | ADL definition |
| Capability | ADL v2 `capabilities` |
| Decision | META `/decisions` |
| Evidence | META `/evidence` |
| Memory entry | Factory `/memory`, `laurentia_memory` |
| Doctrine article | Factory `doctrine.py`, META `doctrine_history` |

Edges: `agent DECLARES capability` · `capability EXECUTED_IN decision` ·
`decision SUPPORTED_BY evidence` · `memory_entry VALIDATED_BY actor` ·
`doctrine_article AMENDED_BY decision`.

## Preconditions

An addressable Brain (`G-004`) and a shared identifier space (`G-008`). Attempting the
graph before either exists would produce a fourth disconnected store.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
