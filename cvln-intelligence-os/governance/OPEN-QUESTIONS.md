---
title: Open Questions Register
purpose: Every open question, contradiction, unknown and undecided risk of the corpus, with owner and due date.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Whole corpus
version: 1.1-patch.3
status: OPEN
attribution: GOVERNANCE
---

# Open Questions Register

One row per question that must be answered before the next freeze can be declared. The
register is generated from the registries by `scripts/gen_open_questions.py`; the
`Owner` and `Due` columns are **human-owned** and preserved across regenerations.

`Owner = UNASSIGNED` and `Due = TBD` mean exactly that: nobody has been assigned and no
date has been set. Neither is invented by any tool.

## Classification rules

| Kind | Rule |
|---|---|
| `freeze-blocker` | a contradiction, an OPEN legal obligation, or an observed CRITICAL/HIGH vulnerability |
| `contradiction` | recorded in a contradictions register (all are freeze blockers) |
| `unknown-needs-evidence` | status `UNKNOWN`: an artefact must be produced before any promotion |
| `risk-needs-decision` | a registered weakness below HIGH severity awaiting a decision |
| `open-question` | any other `OPEN` row |

## Distribution

| Kind | Rows |
|---|---|
| `freeze-blocker` | 16 |
| `risk-needs-decision` | 4 |
| `unknown-needs-evidence` | 23 |

## Register

| ID | Question | Kind | Source | Row | Status | Owner | Due | Evidence |
|---|---|---|---|---|---|---|---|---|
| Q-001 | Holding and industrial origin of the estate | unknown-needs-evidence | registry/ECOSYSTEM-REGISTRY.md | FREKCORE | UNKNOWN | UNASSIGNED | TBD | none in audited repositories |
| Q-002 | Learning surface | unknown-needs-evidence | registry/ECOSYSTEM-REGISTRY.md | CVLN Academy | UNKNOWN | UNASSIGNED | TBD | no evidence in audited repositories |
| Q-003 | Weights, adapters, datasets, fine-tuning | unknown-needs-evidence | audit/COMPONENT-MATRIX.md | Model training infrastructure | UNKNOWN | UNASSIGNED | TBD | none |
| Q-004 | Notary private key stored unencrypted at rest | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-001 | OBSERVED | UNASSIGNED | TBD | backend/server.py |
| Q-005 | Single monolithic governance module (~1611 lines, ~50 paths) | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-002 | OBSERVED | UNASSIGNED | TBD | backend/server.py |
| Q-006 | No observed mutual authentication between layers | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-003 | OBSERVED | UNASSIGNED | TBD | adapters in META |
| Q-007 | Capability discovery probes remote repos that expose nothing | risk-needs-decision | registry/VULNERABILITY-REGISTRY.md | V-004 | OBSERVED | UNASSIGNED | TBD | /registry/discover-all — 12/12 DEGRADED |
| Q-008 | Provider credentials handled inside a single provider layer with journalling | risk-needs-decision | registry/VULNERABILITY-REGISTRY.md | V-005 | OBSERVED | UNASSIGNED | TBD | backend/provider_layer.py |
| Q-009 | No observed rate limiting or abuse control on public read surfaces | risk-needs-decision | registry/VULNERABILITY-REGISTRY.md | V-006 | OBSERVED | UNASSIGNED | TBD | /public/notarizations |
| Q-010 | Admin login bypass documented for a named address, with no code required | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-009 | OBSERVED | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: 'Admin Bypass : cc@kiltikonet.fr (pas de code requis)' |
| Q-011 | Live-mode payment keys and eight secret classes required in a single backend .env | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-010 | OBSERVED | UNASSIGNED | TBD | KILT repo: README.md: env var list (STRIPE_API_KEY sk_live_, BREVO, VAPID, GOOGLE, BASEROW) |
| Q-012 | Primary data mirrored to an external low-code store (Baserow table 865847) | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-011 | OBSERVED | UNASSIGNED | TBD | KILT repo: README.md: 'Baserow sync (table 865847)' |
| Q-013 | Offline scan queue held client-side in IndexedDB on field devices | risk-needs-decision | registry/VULNERABILITY-REGISTRY.md | V-012 | OBSERVED | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: 'Service Worker, IndexedDB, Background Sync' |
| Q-014 | Export signing key stored unencrypted at rest on the portal host | freeze-blocker | registry/VULNERABILITY-REGISTRY.md | V-013 | OBSERVED | UNASSIGNED | TBD | backend/lib/baselines.py (EXPORT_SIGNING_KEY_PATH) |
| Q-015 | The operating entity of a platform holding personal data must be identifiable | freeze-blocker | registry/LEGAL-MATRIX.md | L-008 | OPEN | UNASSIGNED | TBD | none |
| Q-016 | An internal unit sold through a live payment processor requires qualification | freeze-blocker | registry/LEGAL-MATRIX.md | L-009 | OPEN | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: jeton packs, Stripe live |
| Q-017 | Ownership of the Kiltikonet brand and platform IP must be attested | freeze-blocker | registry/LEGAL-MATRIX.md | L-011 | OPEN | UNASSIGNED | TBD | KILT repo: README.md: 'Propriétaire — Culture Connect / Kiltikonet.fr' |
| Q-018 | no observed integration | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-008 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-019 | no observed integration; model access is direct to a provider | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-009 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-020 | no occurrence in the audited repository | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-010 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-021 | no occurrence in the audited repository | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-011 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-022 | no occurrence in the audited repository | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-012 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-023 | no occurrence in the audited repository | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-013 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-024 | not registered in META registry_data.py at v1.0 audit time | unknown-needs-evidence | kiltikonet/RELATIONS-REGISTRY.md | KR-016 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-025 | Music Lab | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-006 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-026 | Culture Lab | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-007 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-027 | Kids | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-008 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-028 | Festival | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-009 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-029 | Connect | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-010 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-030 | Academy | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-011 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-031 | Stories | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-012 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-032 | Talents | unknown-needs-evidence | kiltikonet/PROGRAMMES-REGISTRY.md | KP-013 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-033 | network KPIs per operator and territory | unknown-needs-evidence | kiltikonet/DATA-FLOWS.md | KD-007 | UNKNOWN | UNASSIGNED | TBD | none — no network model in the audited repository |
| Q-034 | works, rights, provenance | unknown-needs-evidence | kiltikonet/DATA-FLOWS.md | KD-008 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-035 | Kiltikonet association | unknown-needs-evidence | kiltikonet/IDENTITY-RECONCILIATION.md | KI-006 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-036 | Kiltikonet réseau (network) | unknown-needs-evidence | kiltikonet/IDENTITY-RECONCILIATION.md | KI-007 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-037 | Kiltikonet Network SAS | unknown-needs-evidence | kiltikonet/IDENTITY-RECONCILIATION.md | KI-008 | UNKNOWN | UNASSIGNED | TBD | none |
| Q-038 | JCC described as 'Monnaie digitale CC' in the Kiltikonet documentation, while CVLN OS D-008 freezes JCC as an internal accounting unit that is never a currency | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-001 | OPEN | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: 'Jetons (Monnaie digitale CC)' vs decisions/ADR-0008-D-008.md |
| Q-039 | Jeton packs are sold through Stripe in live mode, which couples an internal unit to a real payment flow | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-002 | OPEN | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/jetons/checkout'; KILT repo: README.md: 'Stripe (mode live)' |
| Q-040 | Legal identity of Kiltikonet is not attested: organiser is Factory Maker Studio (EURL) / CVLN Group, licence line names Culture Connect / Kiltikonet.fr, while the brief mentions an | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-003 | OPEN | UNASSIGNED | TBD | identity reconciliation KI-003, KI-005, KI-006, KI-008 |
| Q-041 | The platform names a 'Command Center' dashboard, while the estate also names a CVLN Command Center; the two are not shown to be the same system | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-004 | OPEN | UNASSIGNED | TBD | KILT repo: KILTIKONET_DOCUMENTATION.md: '/api/v1/dashboard/cc2026/live' |
| Q-042 | Kiltikonet holds cultural identity data yet no CVLN OS integration is observed, so estate-level governance does not reach it | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-005 | OPEN | UNASSIGNED | TBD | relations KR-008, KR-009, KR-016 |
| Q-043 | Kiltikonet mirrors primary data to Baserow, creating a second store outside the estate's canonical rules | freeze-blocker | kiltikonet/CONTRADICTIONS-KILTIKONET.md | KC-006 | OPEN | UNASSIGNED | TBD | KILT repo: README.md: 'Baserow sync (table 865847)' |

## Rules bound to this register

1. A freeze may not be declared while a `freeze-blocker` row is unresolved.
2. Resolving a row requires evidence and, where a status changes, an ADR — see
   `audit/DRIFT-CONTROL.md`.
3. Deleting a row without a resolution record is a freeze violation.
4. `Owner` and `Due` are filled by humans; tools never guess them.
