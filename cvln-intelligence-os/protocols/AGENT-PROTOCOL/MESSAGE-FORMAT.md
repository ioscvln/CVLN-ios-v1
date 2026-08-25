---
title: Agent Message Format
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: DEFINED
attribution: IMPLEMENTATION
---

# Agent Message Format

`META/backend/contracts.py::Event` is the estate's defined envelope. It has no
consumers (`G-017`).

## Required envelope fields

`event_id` · `type` · `source` · `subject` · `occurred_at` · `payload` ·
`signature` · `key_id`.

## Rules

1. Signature is mandatory. META already quarantines tampered payloads on verify.
2. `type` uses the implemented Agent Factory namespace: `agent.`, `factory.`,
   `monitoring.`, `memory.`, `identity.`, `daily.`, `system.`.
3. A trace identifier is propagated unchanged across every hop (`G-013`).

Today three buses use three incompatible formats (`C-007`).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
