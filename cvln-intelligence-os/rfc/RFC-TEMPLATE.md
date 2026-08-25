---
title: RFC Template
purpose: Canonical template for every CVLN RFC.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# RFC Template

Every CVLN RFC contains exactly these sections, in this order.

```markdown
---
title: RFC-NNNN — <Title>
version: 1.0
status: DRAFT | PROPOSED | ACCEPTED | REJECTED | SUPERSEDED
attribution: SPECIFICATION
---

# RFC-NNNN — <Title>

| Field | Value |
|---|---|
| RFC | RFC-NNNN |
| Status | DRAFT |
| Author | |
| Supersedes | |

## Context
## Problem
## Proposal
## Alternatives considered
## Security impact
## Migration
## Compatibility
## Status
```

## Rules

1. An RFC states evidence before proposal. Claims cite a repository path.
2. An RFC that changes a component's status must say which status, from what, to what.
3. `Alternatives considered` may not be empty. "Do nothing" is always an alternative.
4. An RFC is not ratified by being written.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`
