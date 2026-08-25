---
title: Meta API
purpose: Specification-only REST contract. No implementation.
ownership: META CVLN — Office of Governance
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Meta API

Specification-only contract for the META CVLN governance plane. Paths are those
observed in `META/backend/server.py`. No implementation is provided here.

| Method | Path | Purpose | Permission | Status |
|---|---|---|---|---|
| POST | `/api/auth/login` | Authenticate an operator | public | IMPLEMENTED |
| GET | `/api/auth/me` | Current actor and role | authenticated | IMPLEMENTED |
| GET | `/api/entities` | List estate entities | authenticated | IMPLEMENTED |
| GET | `/api/registry/repositories` | List registered repositories | authenticated | IMPLEMENTED |
| POST | `/api/registry/repositories/{repo_id}/ping` | Probe liveness | ops_lead | IMPLEMENTED |
| POST | `/api/registry/discover-all` | Probe `/api/capabilities` estate-wide | admin | PARTIAL |
| GET | `/api/decisions` | Pending decisions | authenticated | IMPLEMENTED |
| POST | `/api/decisions/{decision_id}/action` | approve/reject/edit/escalate/pause/rollback | role-scoped | IMPLEMENTED |
| POST | `/api/events/emit` | Emit a signed event | authenticated | IMPLEMENTED |
| POST | `/api/events/verify` | Verify a signature | public | IMPLEMENTED |
| GET | `/api/runtime/state` | Current runtime mode and signals | authenticated | IMPLEMENTED |
| POST | `/api/runtime/state/override` | Administrative override | admin | IMPLEMENTED |
| GET | `/api/learning/proposals` | Threshold-gated proposals | authenticated | PARTIAL |
| POST | `/api/learning/proposals/{id}/approve` | Approve; writes `doctrine_history` | admin | IMPLEMENTED |
| GET | `/api/notarizations` | Notarised records | authenticated | IMPLEMENTED |
| GET | `/api/public/notarizations/{id}` | Third-party verification | public | IMPLEMENTED |
| GET | `/api/contracts` | Contract catalogue | authenticated | DEFINED |

## Example — emit a signed event

Request `POST /api/events/emit`

```json
{ "type": "decision.approved", "source": "meta.cvln",
  "subject": "DEC-0142", "payload": { "verb": "approve", "actor": "admin" } }
```

Response `200`

```json
{ "event_id": "evt_8f3a", "signature": "base64…", "key_id": "did:cvln:notary#1",
  "verification": "VALID" }
```

Negative case: a payload altered after signing returns
`{ "verification": "quarantined" }`.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
