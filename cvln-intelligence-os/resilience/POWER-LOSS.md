---
title: Power Loss Model
purpose: Durability expectations across abrupt loss.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: resilience/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Power Loss Model — TARGET

## Requirements

1. Journals and spools are append-only and flushed before acknowledgement.
2. A record is acknowledged only once durable; an unacknowledged record may be lost.
3. On boot, an integrity scan classifies each journal as `intact`, `truncated` or
   `corrupt`; a `corrupt` journal blocks promotion out of `Recovery`.
4. No in-memory-only state is authoritative.

## Current position

No power-loss test evidence exists in the audited repositories. Status is `TARGET`
(V-007, K-007).
