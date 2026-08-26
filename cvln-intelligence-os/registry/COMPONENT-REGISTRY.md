---
title: Component Registry
purpose: Governance wrapper over the v1.0 component matrix.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: registry/
version: 1.1
status: IMPLEMENTED
attribution: GOVERNANCE
---

# Component Registry

The canonical per-component evidence table remains `audit/COMPONENT-MATRIX.md` (v1.0,
preserved unchanged under D-005). This registry adds the governance rules that now bind
every row, and the portal renders both from the same source.

## Rules bound to each row

1. Exactly one status per row (D-012).
2. Exactly one evidence cell; `none` is a valid, explicit value (D-001).
3. A row without an evidence path may not carry `IMPLEMENTED` or `VERIFIED`.
4. `IMPLEMENTED` never implies `VERIFIED`; verification requires a test artefact.
5. Promotion of a row's status requires an ADR reference.

## Related registries

`registry/ECOSYSTEM-REGISTRY.md` · `registry/VULNERABILITY-REGISTRY.md` ·
`registry/CONTINUITY-MATRIX.md` · `registry/LEGAL-MATRIX.md` ·
`decisions/DECISION-REGISTRY.md`
