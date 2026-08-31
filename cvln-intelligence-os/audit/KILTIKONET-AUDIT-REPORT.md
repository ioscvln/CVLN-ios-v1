---
title: Kiltikonet Audit Report
purpose: What existed, what was missing, what was restored, what remains unknown.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: kiltikonet/
version: 1.1-patch.1
status: DECIDED
attribution: AUDIT
---

# Kiltikonet — Audit Report

Audited source: [https://github.com/cultureconnectorg/Kiltikonet-Aout2026](https://github.com/cultureconnectorg/Kiltikonet-Aout2026) — branch `main`, 747 commits, latest commit 15 Aug 2026.
Documents read: `README.md`, `KILTIKONET_DOCUMENTATION.md`. Terms searched across the
v1.1 corpus and the audited repository: Kiltikonet, KILTIKONET, Culture Connect,
Kiltikonet Network, JCC, FREK-ID, KORA, CVLN Academy, Factory Maker Studio, Command
Center, Agent Factory, Wallet.

## 1. What already existed in v1.1

- `JCC` was modelled as an internal accounting unit (`economics/JCC-UNIT-CONSTRAINTS.md`,
  D-008) and as legal row L-005.
- `FREKCORE` existed as a layer −1 row with status `UNKNOWN`.
- `Wallet`, `KORA`, `LabelOS` existed as `REFERENCED` layer-4 rows.
- Continuity, security, legal, proof and economics dimensions existed as sections.

## 2. What was absent from v1.1

- Kiltikonet itself: no ecosystem row, no system card, no relation, no programme.
- Culture Connect 2026 as an operated programme.
- Factory Maker Studio (EURL) as a named organiser entity.
- The Kiltikonet jeton and its conflict with the JCC constraints.
- Kiltikonet security weaknesses, continuity profile and legal questions.

## 3. What was incorrect or insufficient

- The estate map implied that layer 4 was limited to `REFERENCED` applications; an
  operating, revenue-bearing platform holding personal data was missing entirely.
- `FREKCORE` was `UNKNOWN` although a platform demonstrably consumes FREKcore identity
  endpoints — the row remains `UNKNOWN` for the entity, while the consumption is now
  evidenced as relation KR-001.

## 4. What was restored

Twelve `kiltikonet/` documents, four ADRs, 15 registry rows, six contradictions, 17
relations, 13 programme rows, 10 data flows, one system card, one patch record and this
report. All statuses are evidence-bound.

## 5. What remains UNKNOWN

Legal identity of the operating entity · Kiltikonet association · Kiltikonet Network SAS
· operator network, hubs, international footprint · programme catalogue (Music Lab,
Culture Lab, Kids, Festival, Connect, Academy, Stories, Talents) · franchise, royalties,
licence fees · operator certification · integrations with KORA, CVLN Academy, LabelOS,
Laurentia, Brain, Agent Factory, MetaCVLN · rights chain over cultural works.

## 6. What remains PROPOSED / TARGET

Objective of 40 000 FREK-IDs (`PROPOSED`) · Kiltikonet → CVLN OS data flow (`TARGET`) ·
power-loss durability of the field queue (`TARGET`) · data-governance coverage of the
Baserow mirror (`TARGET`).

## 7. Historical contradictions

KC-001 … KC-006 in `kiltikonet/CONTRADICTIONS-KILTIKONET.md`, all `OPEN`. C-002
(doctrine ownership) remains open in the v1.0 register, untouched.

## 8. Decisions created

D-015 (identity), D-016 (jeton vs JCC), D-017 (UNKNOWN ≠ absent), D-018 (governance
reach).

## 9. Files modified

`registry/ECOSYSTEM-REGISTRY.md` · `registry/VULNERABILITY-REGISTRY.md` ·
`registry/CONTINUITY-MATRIX.md` · `registry/LEGAL-MATRIX.md` ·
`decisions/DECISION-REGISTRY.md` · `audit/freeze-manifest.yaml` — additive rows only,
authorised by D-015…D-018 and recorded in `audit/PATCH-001-KILTIKONET.md`.

## 10. Files added

12 `kiltikonet/` documents · `decisions/ADR-0015-D-015.md` … `ADR-0018-D-018.md` ·
`audit/PATCH-001-KILTIKONET.md` · this report.

## 11. Tests executed

`python scripts/check_freeze_invariants.py` (INV-001 … INV-014) and the portal API and
browser checks.

## 12. Invariant results

INV-001 … INV-008 unchanged and green; INV-009 … INV-014 added by this patch and green.
Results are recomputed live at `/api/docs/freeze`; no verdict is hardcoded.

## 12b. Legacy finding (not caused by this patch)

INV-013 reports **48 broken relative Markdown links inside the frozen v1.0 documents**
(root-level files linking to `../audit/...`). They are reported, not repaired: v1.0 is
frozen and a repair requires its own ADR. INV-013 therefore asserts zero broken links
among documents added after v1.0 and reports the legacy count separately.

## 13. Impact on freeze v1.1

None on the frozen text. v1.1 remains the frozen baseline; this patch is registered as
`PATCH-001-KILTIKONET` in `audit/freeze-manifest.yaml` under `post_freeze_patches`.

## 14. Recommendation for the next freeze

Do not freeze v1.2 before: (a) an attested legal identity for the platform; (b) a
qualification of the jeton and its reconciliation with D-008; (c) remediation of V-009;
(d) a declared authoritative store for participant data; (e) a decision on whether
Kiltikonet becomes an OS-governed layer-4 system.
