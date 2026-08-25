---
title: RFC-0003 — Agent Runtime
purpose: RFC: Agent Runtime.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0003 — Agent Runtime

| Field | Value |
|---|---|
| RFC | RFC-0003 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

Agent Factory is the largest implementation in the estate — ADL, gates, event bus, lifecycle, router — and nothing depends on it.

## Problem

The nervous system has no consumers. Laurentia executes its own workflows; META actuates by HTTP adapter.

## Proposal

Establish Agent Factory as the estate's capability execution runtime. Implement `GET /api/capabilities` first (`G-002`), then wire Laurentia to it for capability execution, then bind gate and registry authority to META.

## Alternatives considered

(a) Do nothing. (b) Move execution into Laurentia — rejected: discards the gate system and ADL. (c) Federated peers with contracts only — viable and cheaper; ranks second.

## Security impact

Positive. Routing execution through gates makes every capability invocation authorised and journalled.

## Migration

Three steps in the order above. Step one is non-breaking and independently valuable.

## Compatibility

Additive. Existing Agent Factory routes are unchanged.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
