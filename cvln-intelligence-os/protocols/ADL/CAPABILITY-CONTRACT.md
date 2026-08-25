---
title: ADL Capability Contract
purpose: Specify part of the implemented ADL protocol.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# ADL Capability Contract

An agent's capabilities are declared in its definition, not discovered at runtime.

## Implemented

ADL v2 carries `capabilities` as a top-level schema property. Agent Factory executes
declared capabilities through its gate system, so declaration and authorisation are
coupled by construction.

## Defined but unconsumed

`META/backend/contracts.py::Capability` is the estate's intended wire format for
capability advertisement. No component consumes it (`G-017`), and no component serves
`/api/capabilities` (`G-002`).

## Required contract shape

```json
{
  "id": "report.weekly_drop",
  "version": "1.0.0",
  "owner": "AGT-014",
  "inputs": { "period": "string" },
  "outputs": { "artifact_url": "string" },
  "permissions": ["report.read"],
  "gate_level": 2,
  "risk": "medium"
}
```

Fields beyond `contracts.py::Capability` are `PROPOSED`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`
