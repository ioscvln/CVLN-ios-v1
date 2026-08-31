---
title: Kiltikonet Data Flows
purpose: Source, data, destination, status and evidence per flow.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: PARTIAL
attribution: MIXED
---

# Kiltikonet — Data Flows

| ID | Source | Data | Destination | Status | Evidence |
|---|---|---|---|---|---|
| KD-001 | Badge creation (platform) | badge record, badge type, access zones | FREKcore /badges/create | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: FREKcore endpoint |
| KD-002 | Accreditation form | participant identity, tier, payment state | MongoDB (primary) | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: 'MongoDB (primary)' |
| KD-003 | NFC badge data | badge id, holder, status | Baserow table 865847 (mirror) | IMPLEMENTED | KILT repo: README.md: 'Baserow sync (table 865847)' |
| KD-004 | Field scan | scan events, timestamps, zone | MongoDB, then export CSV | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/stats/export/scans' |
| KD-005 | Jeton purchase | transaction, pack, amount | Stripe + wallet ledger | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/jetons/checkout', '/api/webhook/stripe' |
| KD-006 | Live dashboard | aggregate counts | CC2026 dashboard endpoint | IMPLEMENTED | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/v1/dashboard/cc2026/live' |
| KD-007 | Operator / territory network telemetry | network KPIs per operator and territory | none | UNKNOWN | none — no network model in the audited repository |
| KD-008 | Cultural works / catalogue | works, rights, provenance | none | UNKNOWN | none |
| KD-009 | Platform data → CVLN Intelligence OS | evidence packages, decisions, doctrine feedback | CVLN OS | TARGET | none — no CVLN OS integration observed |
| KD-010 | Historical counters in documentation | 48 badges, 12 active, 30 inscrits, 0 jetons, 20 scans | documentation snapshot only | HISTORICAL | KILT repo: KILTIKONET_DOCUMENTATION.md: snapshot figures, not live KPIs |

## Evidence rule

`Evidence` cites the audited Kiltikonet repository (`KILT`) or reads `none`. A row with
`none` may not carry `IMPLEMENTED` or `VERIFIED`. Statuses used here follow the v1.1
vocabulary extended by this patch with `HISTORICAL` (attested in an earlier body of work,
not reconcilable against the audited repository) and `OPEN` (question deliberately left
unanswered).

KD-010 is `HISTORICAL`: the counters are a documentation snapshot and are never rendered
as live KPIs by this corpus or by the portal.
