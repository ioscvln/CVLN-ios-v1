---
title: Laurentia Gateway API
purpose: Specification-only REST contract. No implementation.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Laurentia Gateway API

Contract for the Laurentia operator gateway, from observed routes.

| Method | Path | Purpose | Permission | Status |
|---|---|---|---|---|
| POST | `/api/laurentia/query` | Streamed answer (SSE tokens) | api key + tier | IMPLEMENTED |
| GET | `/api/brain/health` | Interface health | public | IMPLEMENTED |
| POST | `/api/reports` | Generate a report | Creator+ | IMPLEMENTED |
| POST | `/api/pdf/export` | Signed PDF with QR | tier-quota | IMPLEMENTED |
| GET | `/api/echo/{session_id}` | Public echo landing | public | IMPLEMENTED |
| POST | `/api/billing/checkout` | Stripe checkout session | authenticated | IMPLEMENTED |
| POST | `/api/rgpd/purge` | D+90 identity purge | admin | IMPLEMENTED |
| GET | `/api/capabilities` | Capability advertisement | public | PROPOSED — `G-002` |

## Example — query

Request `POST /api/laurentia/query`

```json
{ "session_id": "sess_41c", "message": "Analyse a 12-month tontine flow" }
```

Response `200`, `text/event-stream`

```
data: {"token":"Analysis"}
data: {"token":" of"}
data: {"done":true,"session_id":"sess_41c"}
```

Negative case: provider unavailable returns `503` with no fallback — gap `G-011`.
Interactions and memory are persisted AES-256-GCM encrypted; identity is a cookieless
HMAC-SHA256 `device_id`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
