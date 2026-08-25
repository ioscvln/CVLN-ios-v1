---
title: Brain API
purpose: Specification-only REST contract. No implementation.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# Brain API

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


No addressable Brain service exists (`G-004`). The contract below is the target
surface; only the two rows marked `IMPLEMENTED` have any counterpart today.

| Method | Path | Purpose | Permission | Status |
|---|---|---|---|---|
| POST | `/api/brain/ask` | Answer with source, confidence and date | authenticated | IMPLEMENTED in META |
| GET | `/api/brain/history` | Prior exchanges | authenticated | IMPLEMENTED in META |
| POST | `/api/brain/reason` | Assessment over supplied context | `brain.reason` | PROPOSED |
| POST | `/api/brain/plan` | Decompose an objective | `brain.plan` | PROPOSED |
| GET | `/api/brain/doctrine` | Doctrine of record | authenticated | PROPOSED |
| POST | `/api/brain/memory/read` | Scoped retrieval with provenance | `memory.read` | PROPOSED |
| POST | `/api/brain/memory/write` | Write pending validation | `memory.write` | PROPOSED |
| POST | `/api/brain/route` | Provider routing decision | `brain.route` | PROPOSED |
| GET | `/api/capabilities` | Capability advertisement | public | PROPOSED |

## Example — reason

Request `POST /api/brain/reason`

```json
{ "objective": "Assess Q3 cashflow exposure",
  "context_refs": ["evidence:EV-114"], "strategy": "quality" }
```

Response `200`

```json
{ "assessment": "…", "confidence": 0.72,
  "provider": "anthropic", "fallback_used": false,
  "doctrine_refs": ["DOC-ARC-04"], "trace_id": "trc_19c" }
```

`fallback_used: true` indicates the terminal sovereign provider answered. Callers must
surface this, never hide it.

## Sovereignty note

This contract makes no claim about a sovereign trained model. See
[`../architecture/CVLN-BRAIN.md`](../architecture/CVLN-BRAIN.md).


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
