---
title: JCC Internal Unit Constraints
purpose: Hard constraints on the JCC accounting unit.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: economics/
version: 1.1
status: DECIDED
attribution: GOVERNANCE
---

# JCC — Internal Accounting Unit Constraints

JCC is an **internal accounting unit**. It is not a currency, not a payment instrument,
not a security and not a token.

## Constraints (frozen)

1. JCC is not exchangeable for legal tender inside any CVLN system.
2. JCC carries no price, no market and no redemption promise.
3. No CVLN interface may present JCC in a currency position or with a currency symbol.
4. JCC balances are accounting records, not claims.
5. Any change to these constraints requires an ADR with counsel input (D-008, L-005).

Violating any constraint is a freeze violation and is asserted by
`scripts/check_freeze_invariants.py`.
