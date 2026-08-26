---
title: Legal-by-Design Framework
purpose: Legal constraints as design inputs.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: legal/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Legal-by-Design Framework — TARGET

Legal constraints are **design inputs**, not post-hoc review. A specification that
cannot be built lawfully is `REJECTED` at specification time, before implementation.

## Method

1. Identify the obligation domain (`registry/LEGAL-MATRIX.md`).
2. Express each obligation as a **design constraint** in machine-checkable terms.
3. Attach the constraint to the components it binds.
4. Classify: inside the lawful design space, outside it, or `UNKNOWN` pending counsel.

## Boundary

This corpus is architecture documentation. It is **not** legal advice and does not
substitute for counsel in any jurisdiction. Decision: D-009.
