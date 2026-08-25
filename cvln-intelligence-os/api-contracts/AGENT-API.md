---
title: Agent Runtime API
purpose: Specification-only REST contract. No implementation.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Agent Runtime API

Contract for the CVLN Agent Factory runtime, from observed routes.

| Method | Path | Purpose | Permission | Status |
|---|---|---|---|---|
| GET | `/api/agents` | List agents | actor | IMPLEMENTED |
| GET | `/api/agents/{agent_id}` | Agent definition | actor | IMPLEMENTED |
| POST | `/api/agents/{agent_id}/lifecycle` | Advance or archive | gate-scoped | IMPLEMENTED |
| GET | `/api/agents/{agent_id}/versions` | Version history | actor | IMPLEMENTED |
| GET | `/api/agents/{agent_id}/diff` | Definition diff | actor | IMPLEMENTED |
| POST | `/api/agents/{agent_id}/checkpoint` | Create a checkpoint | gate-scoped | IMPLEMENTED |
| POST | `/api/agents/{agent_id}/autonomy` | Set autonomy level | admin | PARTIAL |
| POST | `/api/agents/{agent_id}/wake` | Activate | gate-scoped | IMPLEMENTED |
| POST | `/api/check` | Gate decision for an action | actor | IMPLEMENTED |
| GET | `/api/levels` | Gate levels and critical actions | actor | IMPLEMENTED |
| POST | `/api/events/publish` | Publish to the factory bus | actor | IMPLEMENTED |
| GET | `/api/events/dlq` | Dead letter queue | ops | IMPLEMENTED |
| POST | `/api/events/replay-spool` | Replay spooled events | admin | IMPLEMENTED |
| GET | `/api/doctrine` | Doctrine articles | actor | IMPLEMENTED |
| POST | `/api/doctrine/check` | Test an action against doctrine | actor | PARTIAL |
| POST | `/api/compile` | Validate an ADL document | actor | IMPLEMENTED |
| POST | `/api/cycle` | Run an autonomy cycle | gate-scoped | PARTIAL |

## Example — gate decision

Request `POST /api/check`

```json
{ "actor": "AGT-014", "action": "expense.request", "amount": 4200, "level": 2 }
```

Response `200` — permitted

```json
{ "allowed": true, "level": 2, "decision": "…", "rule_source": "doctrine",
  "reason": "Autorisé au niveau 2" }
```

Negative case — denied: `{ "allowed": false }` with a journal entry of type
`action_bloquee` and escalation to the single expenditure queue.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
