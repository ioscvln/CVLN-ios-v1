---
title: Versioning
purpose: Versioning of the CVLN Intelligence OS specification.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Versioning

## Scheme

`OS vMAJOR.MINOR — CODENAME`. Current: `OS v1.0 — TITAN FOUNDATION`.

- **MAJOR** — a change to the layer model, the canonical vocabulary, or the status
  taxonomy.
- **MINOR** — new specifications, ratified RFCs, or status transitions.
- Documents carry an independent `version` in front matter.

## Independent version lines

| Artefact | Line | Current |
|---|---|---|
| This specification | `OS vX.Y` | 1.0 |
| Inter-system contracts | semver | 1.0 stable (`contracts.py`) |
| ADL | semver | v1 implemented, v2 defined — authority undeclared (`G-016`) |
| Agent definitions | semver, enforced | per agent |

## Rules

1. A status transition is a version change and cites its ratifying RFC.
2. Contracts are versioned independently; consumers negotiate the lowest common
   version.
3. Two coexisting generations require a declared authoritative version and a
   converter.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`
