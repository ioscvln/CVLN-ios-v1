---
title: MCL Validation (PROPOSED)
purpose: Sketch a proposed MCL facility.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# MCL Validation (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


Proposed validation rules for any MCL document.

| Rule | Failure mode |
|---|---|
| Every referenced entity is declared | dangling reference |
| Every capability referenced by a workflow is declared by some agent | unexecutable workflow |
| Every permission names at least one role and a gate level | unenforceable permission |
| Relationship direction is acyclic across layers | layering violation |
| Critical permissions require human approval | governance bypass |
| Version is semver | non-comparable revisions |

Validation must be a build-time gate, not a runtime warning; the estate's existing
ADL validation is the precedent to follow.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0008`
