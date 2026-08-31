---
title: EvidencePackage Model
purpose: Specification of the evidence package artefact.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: proof/
version: 1.1
status: PARTIAL
attribution: SPECIFICATION
---

# EvidencePackage — PARTIAL

> Status changed from `TARGET` to `PARTIAL` by `decisions/ADR-0019-D-019.md`: the portal now emits signed packages at `GET /api/docs/export/{baseline}`. External anchoring remains absent (V-008), and `IMPLEMENTED` does not imply `VERIFIED`.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `package_id` | string | Stable identifier |
| `subject` | string | What the package proves something about |
| `claims` | list | Each claim: statement, status, evidence reference |
| `artefacts` | list | Content-addressed items with hash and algorithm |
| `events` | list | Signed event identifiers included in the chain |
| `decisions` | list | Human decisions of record referenced |
| `chain_hash` | string | Hash over the ordered artefact and event hashes |
| `signature` | string | Signature over `chain_hash` by the emitting notary key |
| `anchored_at` | string \| null | External anchor time, `null` when unanchored |
| `legal_effect` | literal | Always `"none"` — see the notarial boundary |

## Verification

Recompute artefact hashes → recompute `chain_hash` → verify `signature` → report each
step independently. A package that fails any step is `REJECTED`, never partially valid.
