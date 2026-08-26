---
title: FREEZE-001 — Architecture Baseline Freeze
purpose: Constitutional instrument that freezes the v1.1 architecture baseline.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Whole corpus
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# FREEZE-001 — Architecture Baseline Freeze

Version: **OS v1.1 — ARCHITECTURE BASELINE FROZEN**
Predecessor: **OS v1.0 — TITAN FOUNDATION** (preserved, not superseded)

## 1. Purpose

FREEZE-001 declares the v1.1 corpus a **frozen baseline**: a known, citable state of
the architecture from which every later change must be a traced delta.

## 2. What freeze means

1. The v1.0 corpus is preserved in place. No document is deleted, moved or rewritten.
2. New dimensions are **added** as new sections: `decisions/`, `security/`,
   `resilience/`, `legal/`, `proof/`, `economics/`, `registry/`.
3. A v1.0 document may only be edited when the edit is documented, traced and
   referenced by an ADR or RFC (D-005).
4. Markdown on disk remains the sole canonical store (D-004). The portal renders it.

## 3. What freeze forbids

- Promoting any status without evidence and an ADR (D-001, D-012).
- Merging `CURRENT` and `TARGET` namespaces (D-002).
- Describing a `TARGET` capability in the present tense.
- Closing contradiction `C-002` (doctrine ownership) by fiat (D-011).
- Presenting JCC as legal currency: forbidden, JCC is never a currency (D-008).
- Presenting a digital evidence package as legal attestation (D-007).

## 4. Instruments of the freeze

| Instrument | Path |
|---|---|
| Decision registry | `decisions/DECISION-REGISTRY.md` |
| Architecture decision records | `decisions/ADR-*.md` |
| Freeze manifest | `audit/freeze-manifest.yaml` |
| Freeze report | `audit/FREEZE-REPORT-v1.1.md` |
| Executable invariants | `scripts/check_freeze_invariants.py` |
| Registries | `registry/*.md` |


## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.


## 5. Amendment procedure

`AUDIT → MAP → PRESERVE → GOVERN`. Reuse what exists; create only against a real gap;
classify anything unimplemented as `TARGET` or `PROPOSED`; never alter the core
responsibilities of MetaCVLN, CVLN Brain, Agent Factory, Laurentia or FREKCORE without
an ADR.
