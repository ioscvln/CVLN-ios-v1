---
title: Security Model
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Security Model

## Trust anchors

| Anchor | Location | Weakness |
|---|---|---|
| Ed25519 notary key | META `db.system_keys.private_b64` | stored unencrypted (`G-005`) |
| AES-256-GCM data key | Laurentia environment | scoped to one system (`G-006`) |
| HMAC fingerprint salt | Laurentia environment | — |
| Service identities | Agent Factory `/identity/service/{id}/rotate` | not verified by other systems |

## Threat notes

Registry poisoning, context poisoning and memory poisoning are named in META's own
next-action list and remain unexecuted as tests (`G-020`). Memory poisoning is
partially mitigated today by Agent Factory's human validation of memory entries.

## Priority order

`G-005` first — a compromised notary key invalidates every notarisation and therefore
the entire public audit surface. Then `G-006`, then `G-008`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
