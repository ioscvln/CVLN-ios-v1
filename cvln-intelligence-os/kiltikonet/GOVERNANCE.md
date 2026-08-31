---
title: Kiltikonet Governance
purpose: Governance surfaces observed and missing.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Governance

## Observed

| Surface | Finding | Status |
|---|---|---|
| Roles | admin / founder space (`/admin/core`), Espace Pro, field scanner | OBSERVED |
| Authentication | JWT httpOnly 30 d, WebAuthn, Google OAuth, Magic Link | IMPLEMENTED |
| Reconciliation | administrative reconciliation endpoint | OBSERVED |
| Organiser mandate | Factory Maker Studio (EURL) / CVLN Group | OBSERVED |

## Missing against the estate's governance model

- No decision of record mechanism comparable to MetaCVLN's (`UNKNOWN`).
- No gate system bounding automated actions (`UNKNOWN`).
- No append-only governance journal evidenced (`UNKNOWN`).
- No escalation path, audit trail or quality-control regime evidenced (`UNKNOWN`).
- Estate governance does not reach the platform today (D-018).

Bringing Kiltikonet under OS governance is a `TARGET` requiring its own RFC.
