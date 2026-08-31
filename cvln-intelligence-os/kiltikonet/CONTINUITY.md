---
title: Kiltikonet Continuity
purpose: Dependencies and behaviour under degradation.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Continuity and Resilience

## Dependencies

| Dependency class | Dependency | Consequence of loss | Status |
|---|---|---|---|
| Network | Ingress and API availability | Field scanning falls back to the offline queue | IMPLEMENTED |
| Cloud | MongoDB Atlas, Emergent platform, Baserow | Writes and mirror stop | OBSERVED |
| Payment | Stripe live | Jeton and badge purchase unavailable | OBSERVED |
| Identity | FREKcore | Badge creation and token issuance stop | OBSERVED |
| Model provider | Claude Sonnet via Emergent LLM key | Cultural AI features stop; no sovereign fallback evidenced | OBSERVED |
| Power | Field devices | Client-side queue durability unverified | TARGET |
| Operator | Field staff availability | Scanning throughput degrades | UNKNOWN |

## States

Normal → Degraded (deferred sync) → Offline (PWA queue in IndexedDB) → Recovery
(Background Sync flush). Rows K-009 … K-011 in `registry/CONTINUITY-MATRIX.md`.

Unlike the Agent Factory, no deterministic sovereign fallback is evidenced for model
access: under provider loss the AI features stop rather than degrade.
