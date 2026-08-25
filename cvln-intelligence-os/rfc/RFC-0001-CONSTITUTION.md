---
title: RFC-0001 — Constitution
purpose: RFC: Constitution.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0001 — Constitution

| Field | Value |
|---|---|
| RFC | RFC-0001 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

The estate has three constitutional artefacts: the conceptual model, META's governance plane, and Agent Factory's constitution and amendment service. None references the others.

## Problem

There is no ratified constitution. Rules are observed inconsistently and no document is authoritative, so no rule can be enforced across repository boundaries.

## Proposal

Ratify `constitution/CVLN-CONSTITUTION-v1.md` as authoritative, with amendment via Agent Factory's implemented `/amendments/{id}/sign` mechanism and ratification recorded as a META decision of record.

## Alternatives considered

(a) Do nothing — divergence continues. (b) Adopt META's governance plane as the constitution — rejected: it implements decisions, not rules. (c) Adopt Agent Factory's constitution service — rejected: Layer 2 cannot bind Layer 0.

## Security impact

Positive. A ratified constitution makes the provider-neutrality and human-approval rules enforceable rather than advisory.

## Migration

No code change. Record ratification as a decision; publish the constitution version in every repository README.

## Compatibility

Backwards compatible. No existing behaviour changes.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
