---
title: Kiltikonet Contradictions
purpose: Historical and cross-source contradictions, all open.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: OPEN
attribution: AUDIT
---

# Kiltikonet — Contradictions

A contradiction is recorded, never resolved by fiat. All rows are `OPEN`.

| ID | Contradiction | Evidence | Status | Required resolution | Decision Ref |
|---|---|---|---|---|---|
| KC-001 | JCC described as 'Monnaie digitale CC' in the Kiltikonet documentation, while CVLN OS D-008 freezes JCC as an internal accounting unit that is never a currency | KILT repo: KILTIKONET_DOCUMENTATION.md: 'Jetons (Monnaie digitale CC)' vs decisions/ADR-0008-D-008.md | OPEN | Founder + counsel decision required; no silent reconciliation | D-016 |
| KC-002 | Jeton packs are sold through Stripe in live mode, which couples an internal unit to a real payment flow | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/jetons/checkout'; KILT repo: README.md: 'Stripe (mode live)' | OPEN | Qualify the jeton legally before the next freeze | D-016 |
| KC-003 | Legal identity of Kiltikonet is not attested: organiser is Factory Maker Studio (EURL) / CVLN Group, licence line names Culture Connect / Kiltikonet.fr, while the brief mentions an association and a Network SAS | identity reconciliation KI-003, KI-005, KI-006, KI-008 | OPEN | Provide incorporation and brand-ownership documents | D-015 |
| KC-004 | The platform names a 'Command Center' dashboard, while the estate also names a CVLN Command Center; the two are not shown to be the same system | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/v1/dashboard/cc2026/live' | OPEN | Name disambiguation required | D-017 |
| KC-005 | Kiltikonet holds cultural identity data yet no CVLN OS integration is observed, so estate-level governance does not reach it | relations KR-008, KR-009, KR-016 | OPEN | Decide whether Kiltikonet becomes an OS-governed layer-4 system | D-018 |
| KC-006 | Kiltikonet mirrors primary data to Baserow, creating a second store outside the estate's canonical rules | KILT repo: README.md: 'Baserow sync (table 865847)' | OPEN | Define which store is authoritative | D-018 |

These rows are additive: `audit/CONTRADICTIONS.md` (v1.0) is untouched and C-002 remains
open there.
