---
title: Webhooks API
purpose: Specification-only REST contract. No implementation.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: SPECIFICATION
---

# Webhooks API

Outbound notification contract. Delivery mechanisms observed: META adapters, Agent
Factory Telegram notifier, Laurentia social publication and OVH SMS.

| Direction | Endpoint | Purpose | Status |
|---|---|---|---|
| outbound | `POST /adapters/laurentia/briefing` | Deliver a briefing to the operator | IMPLEMENTED |
| outbound | `POST /adapters/labelos/push_catalogue` | Push a catalogue | PARTIAL |
| outbound | `POST /adapters/wallet/transaction` | Record a transaction | PARTIAL — upstream 404 |
| outbound | scheduled `POST /api/cron/registry-ping-all` | Liveness sweep | IMPLEMENTED |
| inbound | none observed | Receive third-party callbacks | PROPOSED |

## Delivery contract (target)

```json
{ "event_id": "evt_8f3a", "delivery_id": "dlv_77",
  "attempt": 1, "signature": "base64…", "key_id": "did:cvln:notary#1" }
```

## Rules

1. Deliveries are signed and idempotent by `delivery_id`.
2. Failed deliveries enter a dead letter queue and are replayable — the Agent
   Factory pattern.
3. Upstream errors are surfaced, never masked. The wallet `404` is visible by design
   and is tracked as `G-018` rather than hidden behind a retry.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
