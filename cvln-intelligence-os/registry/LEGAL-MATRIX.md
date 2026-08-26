---
title: Legal Matrix
purpose: Obligation domains mapped to design constraints and owners.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: registry/
version: 1.1
status: TARGET
attribution: MIXED
---

# Legal Matrix

Architecture documentation, not legal advice. `TARGET` rows state constraints that no observed implementation satisfies.

| ID | Obligation Domain | Requirement | Design Constraint | Evidence | Status | Owner | Decision Ref |
|---|---|---|---|---|---|---|---|
| L-001 | Personal data | Lawful basis, minimisation, retention limits for memory stores | Memory writes carry purpose and retention metadata | none | TARGET | MetaCVLN | D-009 |
| L-002 | Automated decision-making | Human review of consequential decisions | Gate system blocks critical actions pending human decision | FACTORY gate_routes.py | PARTIAL | Agent Factory | D-003 |
| L-003 | Evidence and records | Records must be attributable, tamper-evident and time-anchored | Signed events + notarisation | META /events/verify | PARTIAL | MetaCVLN | D-007 |
| L-004 | Legal attestation | Only a competent authority attests legal effect | OS emits evidence packages; attestation is external | none | TARGET | Legal counsel | D-007 |
| L-005 | Monetary and payment regulation | Internal units must not be presented as currency or payment instrument | JCC constrained as internal accounting unit | none | TARGET | FREKCORE | D-008 |
| L-006 | Intellectual property of cultural artifacts | Rights chain per artifact | Artifact records carry rights provenance | none | TARGET | Laurentia | D-009 |
| L-007 | Cross-border transfer | Transfer conditions per jurisdiction | Provider routing constrained by jurisdiction tag | none | TARGET | MetaCVLN | D-009 |

## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.
