---
title: MCL Permission Syntax (PROPOSED)
purpose: Sketch a proposed MCL facility.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# MCL Permission Syntax (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mcl
permission report.emit {
  roles      [ admin, ops_lead ]
  gate_level 2
  critical   false
}

permission doctrine.amend {
  roles      [ admin ]
  gate_level 4
  critical   true
  requires   human_approval + evidence
}
```

Maps to META's implemented RBAC roles and Agent Factory's `GATE_LEVELS` and
`CRITICAL_ACTIONS`, unifying two models that are currently unrelated.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0008`
