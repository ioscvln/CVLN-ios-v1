---
title: MCL Entity Syntax (PROPOSED)
purpose: Sketch a proposed MCL facility.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# MCL Entity Syntax (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


```mcl
entity KORA {
  kind        product
  owner       cvln.group
  repository  "https://github.com/..."
  runtime     "https://kora.cvln"
  capabilities [ catalogue.read, catalogue.write ]
  relationships {
    consumes  LAURENTIA
    governed_by META_CVLN
  }
}
```

Maps to the implemented static register in `META/backend/registry_data.py`, adding
declared relationships that the current register lacks.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0008`
