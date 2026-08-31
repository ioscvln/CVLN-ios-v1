---
title: Ecosystem Registry
purpose: Canonical register of ecosystem systems, layers and ownership boundaries.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: registry/
version: 1.1
status: PARTIAL
attribution: MIXED
---

# Ecosystem Registry

One row per system of the estate. `Must Not Own` is binding: a system found owning a forbidden responsibility is a contradiction, not a feature. Core responsibilities may not change without an ADR.

| System | Layer | Role | Repository | Evidence | Status | Owns | Must Not Own |
|---|---|---|---|---|---|---|---|
| FREKCORE | Layer -1 | Holding and industrial origin of the estate | — | none in audited repositories | UNKNOWN | capital, mandate | runtime execution, doctrine |
| MetaCVLN | Layer 0 | OS kernel: governance, registry, permissions, runtime state | META | backend/server.py | IMPLEMENTED | governance, registry, decisions | cultural production, agent execution |
| CVLN Brain | Layer 1 | Sovereign intelligence engine | — | no dedicated repository audited | TARGET | doctrine, reasoning, memory | workflow execution |
| CVLN Agent Factory | Layer 2 | Nervous system: ADL, runtime, gates, event bus | FACTORY | backend/adl_schema.py, gate_routes.py | IMPLEMENTED | agent execution, gates | doctrine of record |
| Laurentia | Layer 3 | Cultural industry operator | LAUR | public branch application code | PARTIAL | sessions, artifacts, reports | doctrine, agent runtime internals |
| KORA | Layer 4 | Application on the estate contracts | — | referenced in META registry_data.py | REFERENCED | product surface | OS primitives |
| LabelOS | Layer 4 | Application on the estate contracts | — | META adapter target | REFERENCED | product surface | OS primitives |
| Wallet | Layer 4 | Value and accounting surface | — | META adapter returns upstream 404 | REFERENCED | accounting surface | legal currency issuance |
| CVLN Academy | Layer 4 | Learning surface | — | no evidence in audited repositories | UNKNOWN | unknown | unknown |
| Proof Layer | Cross-cutting | Digital evidence packaging and verification | META | notarizations, signed event bus | PARTIAL | digital evidence | legal attestation |
| Kiltikonet | Layer 4 | Sovereign cultural platform operating Culture Connect 2026 (accreditation, NFC badges, payments, cultural AI) | KILT | KILT repo: README.md | IMPLEMENTED | accreditation, badges, jetons ledger, event data | doctrine, agent runtime, legal currency issuance |
| Culture Connect 2026 | Layer 4 · programme | Event operated on the Kiltikonet platform | KILT | KILT repo: KILTIKONET_DOCUMENTATION.md | OBSERVED | event scope | platform architecture |
| Factory Maker Studio (EURL) | Layer -1 | Named organiser entity of CC2026 alongside CVLN Group | KILT | KILT repo: KILTIKONET_DOCUMENTATION.md | OBSERVED | organiser mandate | runtime execution, doctrine |

## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.
