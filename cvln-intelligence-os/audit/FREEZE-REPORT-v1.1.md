---
title: Freeze Report v1.1
purpose: What v1.1 preserves, adds, freezes, verifies and leaves unverified.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Whole corpus
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# Freeze Report — OS v1.1 ARCHITECTURE BASELINE FROZEN

## 1. Preserved

The whole v1.0 corpus, unchanged: the forensic audit, component matrix, gap analysis,
contradictions register, constitution, architecture, protocols, API contracts,
specifications, RFCs and diagrams. Append-only rule D-005. No document was deleted,
moved or rewritten by the v1.1 operation.

## 2. Added

| Section | Content |
|---|---|
| `decisions/` | D-001…D-014 registry, one ADR per decision, ADR template |
| `constitution/FREEZE-001.md` | The freeze instrument |
| `security/` | Security baseline, zero-trust model, threat model |
| `resilience/` | Continuity model, offline profiles, power loss, recovery |
| `legal/` | Legal-by-design framework, lawful design space |
| `proof/` | Proof layer, EvidencePackage model, notarial boundary |
| `economics/` | CVE v1.2, JCC unit constraints, value-centric economics |
| `registry/` | Ecosystem, component, vulnerability, continuity and legal registries |
| `audit/` | This report and `freeze-manifest.yaml` |
| `rfc/` | RFC-0007 baseline freeze procedure |

## 3. Frozen

- Status vocabulary and the two non-implication rules (`IMPLEMENTED` ≠ `VERIFIED`,
  `CURRENT` ≠ `TARGET`).
- Layer responsibilities and the `Must Not Own` column of the ecosystem registry.
- The notarial boundary: digital evidence is in scope, legal attestation is not.
- JCC as an internal accounting unit only.
- Markdown as the sole canonical store.

## 4. Verified

Verification here means **asserted by an executable check**, not "believed correct".
`scripts/check_freeze_invariants.py` asserts INV-001…INV-008 over the corpus on demand,
and the portal recomputes every statistic from the files at request time — no dashboard
number is hardcoded.

## 5. Not verified — explicitly

| Claim | Why unverified |
|---|---|
| Gate enforcement actually blocks every critical action | No test artefact observed |
| Signed event verification rejects all tampering classes | No test corpus observed |
| Journals survive abrupt power loss | No test evidence (K-007, V-007) |
| Evidence package integrity end to end | Artefact not implemented (V-008) |
| Doctrine ownership | Contradiction C-002 remains open (D-011) |
| Any `TARGET` document in `security/`, `resilience/`, `legal/`, `proof/`, `economics/` | Specification only, no implementation |

## 6. Governance position

CVLN Brain remains `TARGET`: no dedicated repository was audited. FREKCORE remains
`UNKNOWN` in the technical corpus. Neither may be described as implemented.
