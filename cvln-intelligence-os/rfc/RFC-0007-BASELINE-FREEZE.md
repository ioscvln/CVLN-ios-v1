---
title: RFC-0007 — Baseline Freeze Procedure
purpose: Procedure by which a baseline is frozen, reported and re-opened.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Governance
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# RFC-0007 — Baseline Freeze Procedure

## Context

v1.0 established an evidence-based map of the estate. Nothing prevented a later editor
from promoting a `TARGET` row to `IMPLEMENTED` silently.

## Problem

Architecture drift is invisible without a frozen reference point and executable rules.

## Proposal

1. Declare a freeze instrument (`constitution/FREEZE-001.md`).
2. Enumerate foundational decisions as ADRs.
3. Emit a machine-readable manifest (`audit/freeze-manifest.yaml`).
4. Emit a human freeze report (`audit/FREEZE-REPORT-v1.1.md`).
5. Enforce invariants with an executable checker.

## Alternatives

Convention-only governance (rejected: untestable). Git tags alone (rejected: a tag does
not express which claims are unverified).

## Security impact

The freeze adds `registry/VULNERABILITY-REGISTRY.md`, making known weaknesses citable.

## Migration

Additive. No v1.0 path changes.

## Compatibility

Portal endpoints of v1.0 keep their contracts; v1.1 adds endpoints.

## Status

`DECIDED`.
