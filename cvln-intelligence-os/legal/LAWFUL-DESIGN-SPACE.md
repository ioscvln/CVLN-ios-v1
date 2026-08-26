---
title: Lawful Design Space
purpose: The bounded region in which CVLN may design.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: legal/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Lawful Design Space — TARGET

## Definition

The lawful design space is the intersection of technically feasible designs and designs
permitted by applicable obligations. CVLN designs only inside it.

## Explicit exclusions (frozen)

| Excluded design | Reason | Status |
|---|---|---|
| Presenting JCC as legal currency or a payment instrument | Monetary regulation (L-005) | REJECTED |
| Emitting legal attestation from the OS | Attestation is an authority function (L-004) | REJECTED |
| Fully autonomous consequential decisions without human review | L-002, D-003 | REJECTED |
| Unbounded retention of personal data in memory stores | L-001 | REJECTED |

An excluded design may not reappear as a `TARGET` without an ADR that records counsel
input.
