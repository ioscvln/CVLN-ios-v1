---
title: Entity Model
purpose: Define what a CVLN entity is and how entities are registered.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Entity Model

An entity is an organisational or product unit of the CVLN estate — for example KORA,
Academy, Wallet, LabelOS, Good Mood, Laurentia.

## Implemented

META CVLN maintains the register at `/entities` and a static estate list in
`backend/registry_data.py` carrying, per entry, an identifier, a GitHub URL and a
preview URL. Agent Factory independently implements `/entities` and
`/dashboard/{entity_id}`.

## Properties observed

| Property | Source |
|---|---|
| identifier | registry entry key |
| repository URL | `github_url` |
| runtime URL | `preview_url` |
| lifecycle status | discovery result: HEALTHY / DEGRADED / UNAVAILABLE / UNKNOWN |
| capabilities | discovery result — currently empty for all entries |

## Limitations

The register is static and hand-maintained; entities do not self-register. Capability
fields are empty estate-wide because no entity implements `/api/capabilities`
(`G-002`). Entity ownership is contested between META and Agent Factory.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0001`, `RFC-0002`
