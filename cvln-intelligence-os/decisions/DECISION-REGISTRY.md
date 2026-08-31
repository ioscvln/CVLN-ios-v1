---
title: Decision Registry
purpose: Canonical register of foundational decisions D-001 to D-014.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Whole corpus
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# Decision Registry

Each row is a foundational decision of the v1.1 baseline freeze. A decision is binding
until superseded by a later ADR. `Evidence` cites the artefact that motivated the
decision, or the literal string `none` where the decision is normative rather than
observed.

| ID | Decision | Rationale | Type | Evidence | Status | Scope | ADR |
|---|---|---|---|---|---|---|---|
| D-001 | Evidence first | No statement enters the corpus without a citable artefact or an explicit UNKNOWN | PRINCIPLE | audit/REPOSITORY-AUDIT.md | DECIDED | whole corpus | ADR-0001 |
| D-002 | CURRENT is not TARGET | Observed state and intended state are separate namespaces and never merge | PRINCIPLE | audit/COMPONENT-MATRIX.md | DECIDED | whole corpus | ADR-0002 |
| D-003 | Human authority is final | Autonomy is bounded by gates; a human decision of record outranks any agent output | PRINCIPLE | FACTORY backend/gate_routes.py | DECIDED | runtime, agents | ADR-0003 |
| D-004 | Markdown is the only canonical store | The portal renders; no database replicates canonical truth | ARCHITECTURE | backend/lib/corpus.py | DECIDED | portal | ADR-0004 |
| D-005 | Append-only baseline | v1.0 documents are preserved; corrections require a traced ADR reference | GOVERNANCE | constitution/FREEZE-001.md | DECIDED | whole corpus | ADR-0005 |
| D-006 | Resilience is a first-class dimension | Degradation, offline operation and recovery are specified, not improvised | ARCHITECTURE | META backend/server.py runtime state | DECIDED | resilience/ | ADR-0006 |
| D-007 | Proof layer is digital evidence only | The OS produces evidence packages; it does not produce legal attestation | ARCHITECTURE | META backend/server.py notarizations | DECIDED | proof/ | ADR-0007 |
| D-008 | JCC is an internal accounting unit | JCC is never described, priced or exchanged as legal currency | ECONOMIC | none — no monetary implementation observed | DECIDED | economics/ | ADR-0008 |
| D-009 | Legal-by-design bounds the design space | A capability outside the lawful design space is REJECTED at specification time | GOVERNANCE | legal/LAWFUL-DESIGN-SPACE.md | DECIDED | legal/ | ADR-0009 |
| D-010 | Zero-trust between layers | Layer-to-layer calls authenticate; internal position grants no privilege | SECURITY | META backend/server.py JWT | DECIDED | security/ | ADR-0010 |
| D-011 | Doctrine ownership is contested and frozen as a contradiction | C-002 is not resolved by fiat; it stays an open contradiction until an ADR closes it | GOVERNANCE | audit/CONTRADICTIONS.md | DECIDED | architecture/ | ADR-0011 |
| D-012 | One status per row | Every registry row carries exactly one status and one evidence cell | GOVERNANCE | registry/ | DECIDED | registries | ADR-0012 |
| D-013 | Traceability is mandatory | Every gap, decision and vulnerability links to at least one component or system node | GOVERNANCE | registry/ | DECIDED | whole corpus | ADR-0013 |
| D-014 | Freeze is verifiable by machine | Invariants are executable assertions over the corpus, not prose | GOVERNANCE | scripts/check_freeze_invariants.py | DECIDED | whole corpus | ADR-0014 |
| D-015 | Kiltikonet is a layer-4 system of the estate with an unattested legal identity | The platform is observable and operating; its legal identity is not attested in any audited source | GOVERNANCE | KILT repo: README.md, KILT repo: KILTIKONET_DOCUMENTATION.md | DECIDED | kiltikonet/ | ADR-0015 |
| D-016 | The Kiltikonet jeton is not reconciled with JCC by this patch | One source calls it a digital currency, D-008 forbids that reading; the conflict is recorded, not resolved | ECONOMIC | kiltikonet/CONTRADICTIONS-KILTIKONET.md | DECIDED | economics/, kiltikonet/ | ADR-0016 |
| D-017 | Absence of evidence of integration is recorded as UNKNOWN, never as absence of relation | Ecosystem membership never implies a technical integration | ARCHITECTURE | kiltikonet/RELATIONS-REGISTRY.md | DECIDED | kiltikonet/ | ADR-0017 |
| D-018 | Estate governance does not currently reach Kiltikonet | No OS integration is observed; governance coverage is a TARGET, not a fact | GOVERNANCE | relations KR-008, KR-009, KR-016 | DECIDED | kiltikonet/, registry/ | ADR-0018 |
| D-019 | Baseline snapshots and evidence-package export are derived artefacts | Snapshots and packages are recomputed from the Markdown corpus; they never become a second source of truth | ARCHITECTURE | backend/lib/baselines.py, backend/routers/insight.py | IMPLEMENTED | proof/, audit/baselines/ | ADR-0019 |


## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.


## Relationships

- Frozen by `constitution/FREEZE-001.md`.
- Reported in `audit/FREEZE-REPORT-v1.1.md`.
- Enforced by `scripts/check_freeze_invariants.py`.
