---
title: Security
purpose: Specify the security posture as audited.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Security

## Implemented controls

| Control | Location | Note |
|---|---|---|
| Ed25519 signed events with quarantine | META | estate's only tamper-evident path |
| Notarisation with public verification | META | externally checkable |
| JWT + bcrypt + RBAC | META | 6 roles |
| Gate levels and critical-action escalation | Agent Factory | denial journalled |
| Append-only journals | Agent Factory | non-repudiation |
| AES-256-GCM at rest | Laurentia | only system with it |
| HMAC-SHA256 cookieless identity | Laurentia | irreversible 64-hex device id |
| Distributed rate limiting via MongoDB TTL | Laurentia | no Redis dependency |
| RGPD D+90 purge | Laurentia | bounded retention |
| Anti-jailbreak persona rules | Laurentia | publicly readable — see `C-003` |

## Weaknesses recorded

`G-005` notary private key stored unencrypted at rest · `G-006` no encryption at rest
outside Laurentia · `G-008` no shared identity · `G-019` no strict tenant isolation in
META · `G-020` red-team scenarios named but unexecuted · `C-003` sovereign persona
rules published.

## Assessment

Individual controls are above average for the estate's maturity. The weakness is
compositional: strong controls in one system do not protect the others, and the single
unencrypted notary key can invalidate the whole trust chain.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
