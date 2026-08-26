---
title: Zero Trust Model
purpose: Layer-to-layer trust rules.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: security/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Zero Trust Model — TARGET

> This document specifies intent. No mutual-authentication implementation was observed
> in the audited repositories.

## Principles

1. Network position grants no privilege. Layer 3 calling Layer 0 authenticates exactly
   as an external caller would.
2. Every call carries a verifiable caller identity and an authorisation scope.
3. Every privileged action is journalled with the caller identity.
4. Deny by default: an unknown capability request fails closed, not open.

## Trust boundaries

| Boundary | Current control | Target control |
|---|---|---|
| Client → MetaCVLN | JWT | JWT + short TTL + audience scoping |
| MetaCVLN → Laurentia | HTTP adapter, no observed auth | Signed service token or mTLS |
| Agent Factory → provider | Provider layer credentials | Scoped credentials per agent risk level |
| External verifier → notary | Public read surface | Signed, rate-limited read surface |

Decision: D-010.
