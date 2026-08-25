---
title: Agent Handshake
purpose: Specify an agent-protocol facility against repository evidence.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Agent Handshake

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


No handshake exists in any audited repository. The closest artefact is META's
capability probe, which currently receives no answer from any provider (`C-005`).

## Proposed handshake

1. Caller requests `GET /api/capabilities`.
2. Provider answers with `contracts.py::Capability` descriptors and an
   `adl_version`.
3. Caller verifies the provider identity — Agent Factory already implements service
   identities and rotation at `/identity/service/{agent_id}/rotate`.
4. Caller and provider agree the lowest common contract version.
5. The handshake result is emitted as a signed event.

Implementing step 2 alone resolves gap `G-002` and makes the existing prober useful.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0006`
