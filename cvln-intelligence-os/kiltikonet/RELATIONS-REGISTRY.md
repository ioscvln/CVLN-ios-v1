---
title: Kiltikonet Relations Registry
purpose: Declared relations between Kiltikonet and the estate.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Relations Registry

An edge exists only where an artefact declares it. Shared ecosystem membership creates
no relation (D-017).

| ID | Source | Target | Relation | Status | Evidence | Decision Ref |
|---|---|---|---|---|---|---|
| KR-001 | Kiltikonet | FREKCORE | consumes identity service (badge creation, JWT) | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: 'FREKcore (identités)', 'POST /badges/create', 'POST /v1/auth/token' | D-015 |
| KR-002 | Kiltikonet | FREK-ID | issues cultural identifiers; stated objective 40 000 | PARTIAL | KILT repo: KILTIKONET_DOCUMENTATION.md: 'Objectif : 40 000 FREK-IDs culturels' | D-015 |
| KR-003 | Kiltikonet | Wallet (JCC jetons) | operates an in-platform jeton wallet per badge | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: 'GET /api/jetons/wallet/{badge_id}' | D-016 |
| KR-004 | Kiltikonet | Command Center | exposes a live CC2026 dashboard; not the CVLN Command Center | PARTIAL | KILT repo: KILTIKONET_DOCUMENTATION.md: 'GET /api/v1/dashboard/cc2026/live' | D-017 |
| KR-005 | Kiltikonet | Stripe | live-mode payment processing for badges and jeton packs | IMPLEMENTED | KILT repo: README.md: 'Paiements · Stripe (mode live)' | none |
| KR-006 | Kiltikonet | Baserow | mirrors NFC badge data to table 865847 | IMPLEMENTED | KILT repo: README.md: 'NFC · Baserow sync (table 865847)' | none |
| KR-007 | Kiltikonet | Claude Sonnet (Emergent LLM key) | cultural AI features | IMPLEMENTED | KILT repo: README.md: 'IA · Claude Sonnet via Emergent LLM Key' | none |
| KR-008 | Kiltikonet | CVLN Agent Factory | no observed integration | UNKNOWN | none | D-017 |
| KR-009 | Kiltikonet | CVLN Brain / Intelligence OS | no observed integration; model access is direct to a provider | UNKNOWN | none | D-017 |
| KR-010 | Kiltikonet | KORA | no occurrence in the audited repository | UNKNOWN | none | D-017 |
| KR-011 | Kiltikonet | CVLN Academy | no occurrence in the audited repository | UNKNOWN | none | D-017 |
| KR-012 | Kiltikonet | LabelOS | no occurrence in the audited repository | UNKNOWN | none | D-017 |
| KR-013 | Kiltikonet | Laurentia | no occurrence in the audited repository | UNKNOWN | none | D-017 |
| KR-014 | Kiltikonet | Factory Maker Studio (EURL) | named organiser of the event | OBSERVED | KILT repo: KILTIKONET_DOCUMENTATION.md: organiser line | D-015 |
| KR-015 | Kiltikonet | CVLN Group | named co-organiser; estate parent | OBSERVED | KILT repo: KILTIKONET_DOCUMENTATION.md: organiser line | D-015 |
| KR-016 | Kiltikonet | MetaCVLN | not registered in META registry_data.py at v1.0 audit time | UNKNOWN | none | D-017 |
| KR-017 | Kiltikonet | CVLN Intelligence OS | documented as a system of the estate by this patch | DECIDED | audit/PATCH-001-KILTIKONET.md | D-015 |

## Evidence rule

`Evidence` cites the audited Kiltikonet repository (`KILT`) or reads `none`. A row with
`none` may not carry `IMPLEMENTED` or `VERIFIED`. Statuses used here follow the v1.1
vocabulary extended by this patch with `HISTORICAL` (attested in an earlier body of work,
not reconcilable against the audited repository) and `OPEN` (question deliberately left
unanswered).
