---
title: RFC-0002 — Brain
purpose: RFC: Brain.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0002 — Brain

| Field | Value |
|---|---|
| RFC | RFC-0002 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

CVL Brain exists as a provider wrapper in Laurentia, a route in META and a statistics endpoint in Agent Factory. Doctrine is implemented in all three.

## Problem

Because there is no addressable Brain, no component can own doctrine on the Brain's behalf. Sovereignty claims about the Brain are also unverifiable from public evidence (`Q-001`, `Q-002`).

## Proposal

Define the Brain boundary and extract one Brain service per `api-contracts/BRAIN-API.md`, owning persona, doctrine, memory, learning, reasoning, routing and emergency behaviour. Until ratified, every document states: NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.

## Alternatives considered

(a) Do nothing — three doctrine stores continue diverging. (b) META owns doctrine and the Brain is reduced to reasoning. (c) Formalise triplication with a reconciliation protocol — highest long-term cost.

## Security impact

Significant and positive. One doctrine of record removes the possibility of contradictory rules being enforced by different components.

## Migration

Extract behind the Brain API; migrate Laurentia's in-process wrapper to a client; freeze doctrine writes in Agent Factory and META during cutover.

## Compatibility

Breaking for Laurentia's internal call path. No external contract changes.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
