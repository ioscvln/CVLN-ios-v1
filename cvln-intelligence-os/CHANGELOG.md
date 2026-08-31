---
title: Changelog
purpose: Changelog of the CVLN Intelligence OS specification.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Changelog

## OS v1.0 — TITAN FOUNDATION — 2026-08-20

Initial release. Forensic audit of three public repositories, architecture
reconstruction, and the first formal specification set.

### Added
- `audit/` — repository audit, component matrix, implementation status, dependency
  map, architecture evidence, cross-repository integration, contradictions, open
  questions, current-state architecture, responsibility matrix, target architecture,
  gap analysis, founder decisions.
- `constitution/`, `architecture/`, `protocols/`, `api-contracts/`,
  `specifications/`, `rfc/`, `diagrams/`.
- `RFC-0001` to `RFC-0006`, all `PROPOSED`. RFC template.

### Findings of record
- 9 contradictions (`C-001`–`C-009`), 20 gaps (`G-001`–`G-020`), 10 open questions,
  5 founder decisions.
- ADL recorded as `IMPLEMENTED`. ISA and MCL recorded as `PROPOSED` — not found in any
  audited repository.
- CVL Brain sovereignty and training: **NOT VERIFIABLE FROM THE AUDITED PUBLIC
  REPOSITORIES**.

### Explicitly not asserted
- No component is claimed at `DEPLOYED RUNTIME`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`

## v1.1 — ARCHITECTURE BASELINE FROZEN

Append-only upgrade of the v1.0 baseline, authorised by `constitution/FREEZE-001.md`
and `rfc/RFC-0007-BASELINE-FREEZE.md` (decision D-005).

- Added `decisions/` (D-001…D-014 with one ADR each), `security/`, `resilience/`,
  `legal/`, `proof/`, `economics/`, `registry/`.
- Added `audit/freeze-manifest.yaml` and `audit/FREEZE-REPORT-v1.1.md`.
- No v1.0 document deleted, moved or rewritten. This CHANGELOG entry is an append.

## v1.1-patch.1 — PATCH-001-KILTIKONET (post-freeze completeness patch)

Registered in `audit/freeze-manifest.yaml` under `post_freeze_patches`. The v1.1 freeze
text is unchanged; this patch is not part of the original freeze.

- Added the `kiltikonet/` section (12 documents) and `audit/KILTIKONET-AUDIT-REPORT.md`.
- Added decisions D-015…D-018 with ADRs, and invariants INV-009…INV-014.
- Appended rows to the ecosystem, vulnerability, continuity, legal and decision
  registries. No v1.0 document was touched.

## v1.1-patch.2 — PATCH-002-GOVERNANCE-TOOLING (post-freeze tooling patch)

- Added drift control (`audit/DRIFT-CONTROL.md`, baselines in `audit/baselines/`),
  signed evidence-package export, and per-system cards in the portal.
- Added decision D-019 with `decisions/ADR-0019-D-019.md`, vulnerability V-013.
- `proof/EVIDENCE-PACKAGE.md` moved TARGET → PARTIAL, traced by ADR-0019.

## v1.1-patch.3 — PATCH-003-ANCHORING-AND-OPEN-QUESTIONS (post-freeze tooling patch)

- Added external anchoring (`proof/EXTERNAL-ANCHORING.md`, OpenTimestamps provider,
  `rfc3161` reserved as TARGET) and the open-questions register
  (`governance/OPEN-QUESTIONS.md`).
- Added decisions D-020, D-021 with ADRs, and invariants INV-015, INV-016.
- No v1.0 document touched; the v1.1 freeze text is unchanged.
