---
title: Kiltikonet Programmes Registry
purpose: Programme catalogue with per-programme status.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Programmes Registry

One row per programme. Operational status is per row: no programme inherits the status
of another.

| ID | Programme | Description | Status | Evidence | Notes |
|---|---|---|---|---|---|
| KP-001 | Culture Connect 2026 (event) | Four-day cultural event, Fort-de-France | OBSERVED | KILT repo: KILTIKONET_DOCUMENTATION.md: dates and venue | Operational scope limited to the 2026 edition |
| KP-002 | Concert / line-up | Artist line-up served from a dynamic CMS | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: '/concert · Line-up artistes (CMS dynamique)' | Route observed in the platform |
| KP-003 | Exposants (Bronze→Diamond, VIP) | Exhibitor tiers with badge types EXP-B/S/G/P/D/VIP | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: badge type table | Tiers are badge types, not a franchise model |
| KP-004 | Conférences / intervenants | Speaker badges with SALLE_CONF access zone | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: 'INT · Intervenant', zone SALLE_CONF | No programme catalogue attached |
| KP-005 | Scan terrain / accreditation | NFC badge scanning with offline queue | IMPLEMENTED | KILT repo: README.md: route '/scan'; PWA offline-first | See kiltikonet/CONTINUITY.md |
| KP-006 | Music Lab | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE — not in the audited repository |
| KP-007 | Culture Lab | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-008 | Kids | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-009 | Festival | Programme named in the patch brief; CC2026 is an event, not a named 'Festival' programme | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-010 | Connect | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-011 | Academy | Programme named in the patch brief; no Academy artefact in the repository | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-012 | Stories | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE |
| KP-013 | Talents | Programme named in the patch brief | UNKNOWN | none | SOURCE TO RECONCILE |

## Evidence rule

`Evidence` cites the audited Kiltikonet repository (`KILT`) or reads `none`. A row with
`none` may not carry `IMPLEMENTED` or `VERIFIED`. Statuses used here follow the v1.1
vocabulary extended by this patch with `HISTORICAL` (attested in an earlier body of work,
not reconcilable against the audited repository) and `OPEN` (question deliberately left
unanswered).
