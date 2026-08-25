---
title: CVLN Constitution v1
purpose: Establish the binding rules of the CVLN Intelligence Operating System.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: SPECIFICATION
---

# CVLN Constitution v1

## Article I — Vocabulary

`META CVLN` is the operating system and governance layer. `CVLN AGENT FACTORY` is the
nervous system and agent runtime. `CVL BRAIN` is the sovereign intelligence.
`LAURENTIA` is the cultural-industry operator. These terms are canonical and may not
be renamed by any subordinate repository.

**Sovereign** denotes control over data, keys and jurisdiction. It does **not** denote
a fallback provider. Contradiction `C-008` records the current conflation.

## Article II — Evidence

No CVLN document may present a concept as an implementation. Every architectural
claim carries an attribution level (`CONCEPT`, `SPECIFICATION`, `IMPLEMENTATION`,
`DEPLOYED RUNTIME`) and every component carries exactly one implementation status.

## Article III — Doctrine

Doctrine is the estate's binding operational rule set. Doctrine change requires human
approval and an evidence record. Automatic mutation of doctrine is prohibited.
META CVLN implements this rule today at `/learning/proposals/{id}/approve`.

**Current state:** doctrine is implemented in three components. Ownership is contested
pending `FD-001`.

## Article IV — Authority and gates

No capability executes without an authority decision. Blocked and escalated actions
are journalled append-only. Agent Factory implements this in `gate_routes.py`.

## Article V — Provider neutrality

No component may call a model provider outside a designated routing boundary. Agent
Factory doctrine article `DOC-ARC-04` and `ADR-002` state this rule; Laurentia does
not currently satisfy it (`C-004`).

## Article VI — Amendment

This constitution is amended by RFC only. Amendments are signed and recorded. Agent
Factory implements a compatible mechanism at `/amendments/{id}/sign`.

## Article VII — Ratification

**This constitution is not yet ratified.** It states rules that the estate partially
observes. Ratification is `RFC-0001`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001` (ratification), `RFC-0002` (doctrine ownership)
