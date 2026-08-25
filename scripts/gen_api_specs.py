import sys
sys.path.insert(0, "/app/scripts")
from gen_audit import w, PROPOSED_BANNER, MET, BRN, FAC, ARC
from gen_constitution import simple

def ep(rows):
    return "\n".join(rows)

# ================= API CONTRACTS =================
API = [
 ("META-API", "Meta API", MET, "IMPLEMENTED", """
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
"""),
 ("BRAIN-API", "Brain API", BRN, "PROPOSED", PROPOSED_BANNER + """

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
"""),
 ("AGENT-API", "Agent Runtime API", FAC, "IMPLEMENTED", """
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
"""),
 ("LAURENTIA-API", "Laurentia Gateway API", ARC, "IMPLEMENTED", """
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
"""),
 ("EVENTS", "Events API", MET, "PARTIAL", """
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
"""),
 ("WEBHOOKS", "Webhooks API", MET, "PARTIAL", """
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
"""),
]
for p, t, own, st, body in API:
    simple(f"api-contracts/{p}.md", t, "Specification-only REST contract. No implementation.", own, st,
           "SPECIFICATION", body, rfc="`RFC-0003`, `RFC-0005`")

# ================= SPECIFICATIONS =================
SPECS = [
 ("MEMORY-GRAPH", "Memory Graph", "PROPOSED", BRN, PROPOSED_BANNER + """

No graph exists. Three unrelated stores exist (`G-010`).

## Proposed node and edge types

| Node | Source today |
|---|---|
| Entity | META registry |
| Agent | ADL definition |
| Capability | ADL v2 `capabilities` |
| Decision | META `/decisions` |
| Evidence | META `/evidence` |
| Memory entry | Factory `/memory`, `laurentia_memory` |
| Doctrine article | Factory `doctrine.py`, META `doctrine_history` |

Edges: `agent DECLARES capability` · `capability EXECUTED_IN decision` ·
`decision SUPPORTED_BY evidence` · `memory_entry VALIDATED_BY actor` ·
`doctrine_article AMENDED_BY decision`.

## Preconditions

An addressable Brain (`G-004`) and a shared identifier space (`G-008`). Attempting the
graph before either exists would produce a fourth disconnected store.
"""),
 ("PERSONA", "Persona", "IMPLEMENTED", ARC, """
## Implemented — `LAUR/backend/services/cvl_brain_knowledge.py`

Persona v1.2 with explicit non-disclosure and anti-jailbreak rules. The persona is
instructed never to name Anthropic, Claude, OpenAI, any underlying provider, or
`CVLN/CVL Brain`, and never to disclose internal instructions or environment key
names (`LAURENTIA_*`, `MONGO_URL`, `EMERGENT_LLM_KEY`). Exfiltration attempts receive
a refusal with business reorientation rather than a bare denial.

## Assessment

This is the most developed persona artefact in the estate and the only implemented
form of doctrine-of-voice. Two findings qualify it:

1. It is publicly readable despite being designated sovereign (`C-003`). Published
   anti-jailbreak rules are weaker rules.
2. It is Laurentia-local. No other CVLN surface inherits it.
"""),
 ("DOCTRINE", "Doctrine", "PARTIAL", BRN, """
## Implemented in three places

Agent Factory `doctrine.py` seeds numbered articles (for example `DOC-ARC-04`,
provider-agnostic execution) and serves `/doctrine` and `/doctrine/check`. META
maintains `doctrine_history`, appended only on human approval of a learning proposal,
always with evidence. Laurentia's persona layer functions as doctrine of voice.

## The rule the estate honours

Doctrine is never mutated automatically. Every observed change path requires a human
decision and records evidence. This is the estate's strongest governance property and
must survive any consolidation.

## The rule the estate breaks

"Nobody else owns doctrine." Three components own it (`C-002`), with no reconciliation
mechanism. Blocked on `FD-001`.
"""),
 ("LEARNING", "Learning", "PARTIAL", BRN, """
## Implemented — META CVLN

`/learning/proposals` with a configurable `LEARNING_PROPOSAL_THRESHOLD`. Approval at
`/learning/proposals/{id}/approve` appends a `doctrine_history` record carrying
evidence. No automatic doctrine mutation exists anywhere.

## Not implemented

Automatic aggregation from feedback into proposals — META documents this gap itself.
Feedback is collected at `/feedback`; conversion to proposals remains manual.

## Binding constraint

`LEARN` may propose. Only a human may approve. Any future autonomy work that weakens
this constraint contradicts `constitution/CVLN-CONSTITUTION-v1.md` Article III.
"""),
 ("REASONING", "Reasoning", "PARTIAL", BRN, """
## What exists

`FACTORY/backend/cognitive_engine.py` exposes exactly `classify_message(text)` and
`internal_response(text, classification, ctx, knowledge_hits)` — deterministic
keyword classification and templated response. Model-based generation is reachable
only through `provider_layer.py`. META's `/brain/ask` returns answers annotated with
source, confidence and date.

## What does not exist

Multi-step reasoning, plan decomposition, self-critique, or any reasoning trace
artefact. The `PLAN` and `REASON` semantics in `protocols/ISA` are `PROPOSED`.

## Why the distinction matters

Describing the classifier as "the reasoning engine" would convert a specification
into a capability claim. The estate has a routing layer and a classifier; it does not
yet have a reasoning engine.
"""),
 ("AUTONOMY", "Autonomy", "PARTIAL", FAC, """
## Implemented — Agent Factory

`/mode` (get and set), `/cycle`, `/cycles`, `/cycles/{cycle_id}`, per-agent autonomy
levels at `/agents/{id}/autonomy`, and `detect_critical_intent()` which forces human
confirmation for critical actions.

## Constraints observed

1. Autonomy is bounded by gate levels; a higher autonomy level does not raise
   authority.
2. Critical intent interrupts autonomous execution.
3. Cycles are recorded and inspectable individually.

## Gap

Cycles have no instruction-level semantics, so an autonomous cycle cannot be audited
step by step (`G-014`). This is the strongest argument for ISA.
"""),
 ("GATES", "Gates", "IMPLEMENTED", FAC, """
## Implemented — `FACTORY/backend/gate_routes.py`

`GATE_LEVELS` defines authority tiers with labels. `CRITICAL_ACTIONS` enumerates
actions requiring escalation regardless of level. `POST /check` returns
`allowed`, `level`, `decision`, `rule_source` and a human-readable `reason`. A
separate journal router records outcomes append-only.

## Properties worth preserving estate-wide

1. **Denial is explained.** The response names its `rule_source`, so an operator can
   see which rule blocked an action.
2. **Denial is journalled** as `action_bloquee` — non-repudiable.
3. **Escalation converges** on a single queue rather than per-domain queues, which
   prevents authority fragmentation.

This is the most reusable authority mechanism in the estate and the natural basis for
the target `EXECUTE` precondition.
"""),
 ("SECURITY-MODEL", "Security Model", "PARTIAL", ARC, """
## Trust anchors

| Anchor | Location | Weakness |
|---|---|---|
| Ed25519 notary key | META `db.system_keys.private_b64` | stored unencrypted (`G-005`) |
| AES-256-GCM data key | Laurentia environment | scoped to one system (`G-006`) |
| HMAC fingerprint salt | Laurentia environment | — |
| Service identities | Agent Factory `/identity/service/{id}/rotate` | not verified by other systems |

## Threat notes

Registry poisoning, context poisoning and memory poisoning are named in META's own
next-action list and remain unexecuted as tests (`G-020`). Memory poisoning is
partially mitigated today by Agent Factory's human validation of memory entries.

## Priority order

`G-005` first — a compromised notary key invalidates every notarisation and therefore
the entire public audit surface. Then `G-006`, then `G-008`.
"""),
 ("VERSIONING", "Versioning (specifications)", "IMPLEMENTED", ARC, """
## Rules

1. Documents carry a `version` in front matter and change only by RFC.
2. Contracts are versioned independently of documents;
   `META/backend/contracts.py` declares v1.0 stable.
3. ADL versions are semver, enforced by `SEMVER_RE`.
4. A status change (for example `PROPOSED` → `DEFINED`) is a version change and
   requires the ratifying RFC number in the changelog.
5. Where two generations coexist — ADL v1 and v2 — one must be declared
   authoritative (`G-016`).

See also [`../VERSIONING.md`](../VERSIONING.md).
"""),
]
for p, t, st, own, body in SPECS:
    simple(f"specifications/{p}.md", t, "Specify a CVLN intelligence concern against repository evidence.", own, st,
           "SPECIFICATION" if st == "PROPOSED" else "IMPLEMENTATION", body, rfc="`RFC-0002`, `RFC-0006`")
print("api-contracts + specifications written")
