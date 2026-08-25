---
title: Versioning (specifications)
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Versioning (specifications)

## Rules

1. Documents carry a `version` in front matter and change only by RFC.
2. Contracts are versioned independently of documents;
   `META/backend/contracts.py` declares v1.0 stable.
3. ADL versions are semver, enforced by `SEMVER_RE`.
4. A status change (for example `PROPOSED` → `DEFINED`) is a version change and
   requires the ratifying RFC number in the changelog.
5. Where two generations coexist — ADL v1 and v2 — one must be declared
   authoritative (`G-016`).

See also [`../VERSIONING.md`](../VERSIONING.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
