---
title: RFC-0005 — Model Router
purpose: RFC: Model Router.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0005 — Model Router

| Field | Value |
|---|---|
| RFC | RFC-0005 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

The only implemented router is `FACTORY/backend/provider_layer.py`, with four providers, named strategies, per-call journalling and a guaranteed terminal sovereign fallback under `ADR-002`.

## Problem

The conceptual model places the router in the Brain (Layer 1), the implementation places it in the nervous system (Layer 2), and Laurentia bypasses it entirely — violating doctrine article `DOC-ARC-04`.

## Proposal

Promote the existing provider layer to a shared, Brain-owned routing service without redesigning it, and require every model call in the estate to pass through it.

## Alternatives considered

(a) Leave routing in Agent Factory and require Laurentia to call it — lower cost, retains the layering contradiction. (b) Permit per-system routing and withdraw `DOC-ARC-04` — honest but forfeits fallback guarantees.

## Security impact

Positive. One audited provider boundary, one journal of model calls, and a fallback that cannot fail.

## Migration

Expose the provider layer over HTTP; migrate Laurentia's `cvl_brain.py` to a client; keep the sovereign fallback terminal.

## Compatibility

Additive for Agent Footprint; breaking for Laurentia's internal path only.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
