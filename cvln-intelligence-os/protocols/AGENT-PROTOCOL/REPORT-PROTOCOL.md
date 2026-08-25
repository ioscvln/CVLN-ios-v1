---
title: Agent Report Protocol
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Agent Report Protocol

## Implemented

META: notarisations with verification and export, public verification surface,
weekly drop reports. Agent Factory: activity journal, daily closings, briefings.
Laurentia: signed PDF export with QR, reports and timelines.

## Rules

1. A report is signed. META's Ed25519 notarisation is the reference implementation.
2. A report is verifiable by a third party without privileged access —
   `/public/notarizations/{id}` implements this.
3. Absent data is reported as absent. META's loop maps return
   `DATA_NOT_AVAILABLE` rather than a fabricated value. This rule is binding on all
   future CVLN reporting.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
