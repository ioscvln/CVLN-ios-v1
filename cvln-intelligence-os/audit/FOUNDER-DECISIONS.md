---
title: Founder Decisions Required
purpose: Decisions that only the founder can make, each blocking downstream work.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Founder Decisions Required

These are the critical path. Each entry states the decision, what it unblocks, and
the cost of deferral. No option is pre-selected.

## FD-001 — Doctrine and Brain boundary

**Decision.** Which component owns doctrine of record, and what "CVL Brain" denotes:
a service, a library, a model, or an architectural concept.

**Options.** (a) Brain-owned doctrine, Brain extracted as a service; (b) META-owned
doctrine, Brain reduced to a reasoning service; (c) formalise the current triplication
with a reconciliation protocol.

**Blocks.** `G-004`, `G-009`, `G-010`; contradictions `C-002`, `C-008`; all of
`architecture/CVLN-BRAIN.md` beyond audit findings.

**Cost of deferral.** Three doctrine stores continue diverging with no reconciliation
mechanism.

## FD-002 — Dependency direction

**Decision.** Ratify, amend, or abandon the canonical layering
`META → Agent Factory → Brain → Laurentia → Applications`.

**Options.** (a) Ratify and fund integration; (b) adopt a federated peer model with
contracts only; (c) declare the layering conceptual and stop presenting it as
architecture.

**Blocks.** `G-001`, `G-008`; contradiction `C-001`.

**Cost of deferral.** Every integration estimate remains unbounded.

## FD-003 — Open-core boundary

**Decision.** Which concerns are sovereign, and whether the documented
`open-core/` versus `sovereign-brain/` split is executed.

**Options.** (a) Execute the migration in `LAUR/ARCHITECTURE.md` steps 2–4;
(b) correct the README to the future tense and defer; (c) redefine the boundary.

**Blocks.** `G-012`; contradiction `C-003`.

**Cost of deferral.** Anti-jailbreak and persona rules remain publicly readable,
which measurably weakens them.

## FD-004 — Model router ownership

**Decision.** Where model routing lives, and whether provider-agnosticism binds the
whole estate.

**Options.** (a) Promote `provider_layer.py` to a Brain-owned shared service;
(b) leave routing in Agent Factory and require Laurentia to call it; (c) permit
per-system routing and withdraw doctrine article `DOC-ARC-04`.

**Blocks.** `G-011`; contradictions `C-004`, `C-006`.

**Cost of deferral.** Laurentia remains a single-provider single point of failure.

## FD-005 — ISA and MCL

**Decision.** Adopt, defer, or reject the proposed ISA instruction set and MCL
language.

**Options.** (a) Adopt one or both via `RFC-0007` / `RFC-0008`; (b) defer pending
integration work; (c) reject and remove the proposal directories.

**Blocks.** `G-014`, `G-015`.

**Cost of deferral.** Low. Both are `PROPOSED` and quarantined; nothing depends on
them. Deferral is a legitimate outcome.

---

## Sequencing

`FD-002` first, since it determines whether integration is funded at all. `FD-001`
and `FD-004` next. `FD-003` is independent and can proceed in parallel. `FD-005`
last.

## Future RFC references

`RFC-0001` through `RFC-0008`.
