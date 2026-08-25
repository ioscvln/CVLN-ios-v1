---
title: Events API
purpose: Specification-only REST contract. No implementation.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: SPECIFICATION
---

# Events API

Estate-wide eventing contract. Three incompatible buses exist today (`C-007`); this
document specifies the intended single contract.

| Method | Path | Purpose | Permission | Status |
|---|---|---|---|---|
| POST | `/api/events/emit` | Emit a signed event | authenticated | IMPLEMENTED (META) |
| POST | `/api/events/verify` | Verify signature and integrity | public | IMPLEMENTED (META) |
| GET | `/api/events` | Query the event log | authenticated | IMPLEMENTED (META) |
| POST | `/api/events/publish` | Publish to the runtime bus | actor | IMPLEMENTED (Factory) |
| GET | `/api/events/dlq` | Undelivered events | ops | IMPLEMENTED (Factory) |
| POST | `/api/events/replay-spool` | Replay spooled events | admin | IMPLEMENTED (Factory) |

## Envelope — `contracts.py::Event`

```json
{ "event_id": "evt_8f3a", "type": "agent.report.ready",
  "source": "cvln.agent-factory", "subject": "AGT-014",
  "occurred_at": "2026-08-20T09:14:00Z",
  "payload": { "artifact_url": "…" },
  "trace_id": "trc_19c",
  "signature": "base64…", "key_id": "did:cvln:notary#1" }
```

## Rules

Topic prefix must be one of `agent.`, `factory.`, `monitoring.`, `memory.`,
`identity.`, `daily.`, `system.`. Signature is mandatory in the target contract; today
only META signs. `trace_id` is `PROPOSED` and required to close `G-013`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
