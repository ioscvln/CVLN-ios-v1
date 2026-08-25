---
title: RFC-0006 — Multiagent
purpose: RFC: Multiagent.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# RFC-0006 — Multiagent

| Field | Value |
|---|---|
| RFC | RFC-0006 |
| Status | **PROPOSED** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

Three event buses exist with three trust models; only META signs events. META's `contracts.py::Event` is defined and unconsumed.

## Problem

Multi-agent orchestration across systems is impossible: no shared envelope, no shared topic namespace, no correlated trace, no handshake.

## Proposal

Adopt `contracts.py::Event` as the estate envelope with mandatory Ed25519 signing, the Agent Factory topic namespace, a propagated `trace_id`, and the capability handshake in `protocols/AGENT-PROTOCOL/HANDSHAKE.md`.

## Alternatives considered

(a) Do nothing. (b) Adopt the envelope without signing — cheaper, forfeits tamper evidence. (c) Introduce a message broker — premature before the envelope is agreed.

## Security impact

Positive. Signed, correlated events make cross-system causality reconstructible and tampering detectable.

## Migration

Envelope and signing first (no founder decision needed), then trace propagation, then handshake.

## Compatibility

Breaking at the bus level for Agent Factory and Laurentia; META is already conformant.

## Status

**PROPOSED.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

this document
