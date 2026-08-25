---
title: RFC-0004 — Laurentia
purpose: RFC: Laurentia.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0004 — Laurentia

| Field | Value |
|---|---|
| RFC | RFC-0004 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

Laurentia is a complete standalone product with the estate's strongest privacy engineering and its only paying surface.

## Problem

It owns doctrine of voice, hardcodes one model provider without fallback, and consumes neither Brain nor runtime — so it is a product, not a layer.

## Proposal

Reposition Laurentia as a Layer 3 consumer: read doctrine from the Brain, execute capabilities via Agent Factory, route models through the shared router, and advertise capabilities.

## Alternatives considered

(a) Do nothing — accept Laurentia as an independent product and drop the layering claim; a legitimate outcome. (b) Partial adoption: router and capabilities only, retaining local persona.

## Security impact

Positive. It removes the single-provider failure mode (`G-011`) and brings the persona under governance.

## Migration

Adopt the shared router first — it is the only change that reduces risk immediately. Doctrine migration follows RFC-0002.

## Compatibility

Breaking for internal Laurentia modules. No change to the public gateway contract.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
