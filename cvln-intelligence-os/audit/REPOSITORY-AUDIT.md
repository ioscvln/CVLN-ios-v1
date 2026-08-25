---
title: Repository Audit
purpose: Primary forensic record of what the three audited CVLN repositories actually contain.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: MetaCVLN, CVLNAgentfactory, Laurent.ia
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Repository Audit

Audit date: 2026-08-20. Method: shallow clone of each audited branch, followed by
static inspection of source, routes, models, schemas, configuration, tests and
cross-references. Directory names were not treated as evidence of capability.

---

## 1. `metacvln-spec/MetaCVLN` (branch `main`)

**Conceptual role:** META CVLN — operating system / governance layer.

### Composition

| Fact | Evidence |
|---|---|
| 132 tracked files | file census |
| Backend is a single FastAPI module of 1,611 lines | `backend/server.py` |
| ~50 distinct API paths | route decorators in `backend/server.py` |
| Frontend is JavaScript CRA, not TypeScript | `frontend/src/pages/*.js` |
| Five versioned inter-system contracts | `backend/contracts.py` |
| Static registry of the CVLN estate | `backend/registry_data.py` |
| Three architecture documents | `docs/META_CVLN_ARCHITECTURE.md`, `META_CVLN_SECURITY.md`, `META_CVLN_EXISTING_SYSTEM_AUDIT.md` |
| 17 backend tests | `backend/tests/test_p2_endpoints.py`, `test_reports/pytest/p2_results.xml` |

### Implemented surface

Grouped by governance concern, from the route table in `backend/server.py`:

- **Identity and access** — `/auth/login`, `/auth/logout`, `/auth/me`. JWT + bcrypt
  with role-based access control (`admin`, `cfo`, `hr_lead`, `ops_lead`, `legal_lead`,
  `employee`).
- **Registry** — `/registry/repositories`, `/registry/repositories/{repo_id}`,
  `/…/ping`, `/…/history`, `/registry/discover-all`, `/registry/fms-answers`.
- **Entities, agents, capabilities** — `/entities`, `/agents`, `/capabilities`.
- **Decision system** — `/decisions`, `/decisions/{decision_id}`,
  `/decisions/{decision_id}/action`.
- **Event bus** — `/events`, `/events/emit`, `/events/verify`. Ed25519 signature over
  a canonical payload; `key_id` is a notary DID.
- **Runtime** — `/runtime/state`, `/runtime/state/override`. Automatic
  `normal | degraded | critical` mode over seven signals with hysteresis.
- **Learning** — `/learning/proposals`,
  `/learning/proposals/{proposal_id}/approve`. Threshold-gated. Doctrine is not
  mutated automatically; approval writes a `doctrine_history` record with evidence.
- **Brain interface** — `/brain/ask`, `/brain/history`.
- **Notarisation and public audit** — `/notarizations`, `/…/verify`, `/…/export`,
  `/public/notarizations`, `/public/notarizations/{id}/fk`, `/evidence`.
- **Domain overviews** — `/finance/overview`, `/finance/loop`, `/people/overview`,
  `/people/loop`, `/legal/overview`, `/ops/overview`, `/knowledge/overview`,
  `/command-center/overview`, `/command-center/timeline`, `/workbench`.
- **Outbound adapters** — `/adapters/laurentia/briefing`,
  `/adapters/labelos/push_catalogue`, `/adapters/wallet/transaction`.
- **Scheduled work** — `/api/cron/registry-ping-all`, `/api/cron/weekly-drop-report`.

### Honest self-reporting

The repository's own commit record and `docs/META_CVLN_EXISTING_SYSTEM_AUDIT.md`
document unmet gaps rather than concealing them: no audited repository exposes
`/api/capabilities`, so capability discovery returned `DEGRADED` for all twelve
registry entries; the wallet adapter receives an upstream `404`; strict per-tenant
isolation, encryption at rest, cross-repository OpenTelemetry and Brain SSE
streaming are absent. This materially raises confidence in the repository's other
claims.

### Status

`IMPLEMENTED` as a governance and observation plane. **Not** `IMPLEMENTED` as a
kernel that other systems depend on — nothing audited depends on it.

---

## 2. `frekcore/CVLNAgentfactory` (branch `CVLN-AGENT-FACTORY`)

**Conceptual role:** CVLN AGENT FACTORY — nervous system / agent runtime.

### Composition

| Fact | Evidence |
|---|---|
| 231 tracked files — largest audited codebase | file census |
| ~143 route declarations | route decorators across `backend/*.py` |
| 30 router modules mounted on one `/api` router | `backend/server.py` lines 18–110 |
| Agent Definition Language, two generations | `backend/adl_schema.py`, `backend/schemas/adl_v2_schema.json` |
| 13 test modules | `backend/tests/` |
| Empty README (`"Here are your Instructions"`) | `README.md` |

### Implemented subsystems

- **ADL v1** — `backend/adl_schema.py`. Pydantic models with enforced identifier
  grammar (`AGT-\d{3}`), semantic versioning (`^\d+\.\d+\.\d+$`), a seven-stage
  `LifecycleStatus` enum (`Draft → Prototype → Alpha → Beta → Production →
  Maintenance → Archive`), a computed `allowed_transitions()` function, and
  `BrainMemory` (`scope: session | persistent`, `owner`) and `BrainEvents`
  (`subscribe`, `publish`) bindings. YAML is a first-class input
  (`parse_adl_yaml`).
- **ADL v2** — `backend/schemas/adl_v2_schema.json`, a JSON Schema with top-level
  properties `adl_version`, `schema_uri`, `agent`, `brain`, `capabilities`, served by
  `backend/adl_v2_routes.py`.
- **Agent lifecycle** — `/agents`, `/agents/{id}/lifecycle`, `/…/state`,
  `/…/versions`, `/…/diff`, `/…/checkpoint`, `/…/checkpoints`, `/…/export`,
  `/…/wake`, `/…/autonomy`.
- **Gates** — `backend/gate_routes.py`. A `GATE_LEVELS` table, a `CRITICAL_ACTIONS`
  list, `/check`, and an append-only journal router. Blocked actions are journalled
  as `action_bloquee`; escalated expenditure is routed to a single queue.
- **Event bus** — `backend/event_bus.py`, with an enforced topic namespace
  (`agent.`, `factory.`, `monitoring.`, `memory.`, `identity.`, `daily.`,
  `system.`), plus `/events/publish`, `/events/dlq` (dead letter queue) and
  `/events/replay-spool`.
- **Model router** — `backend/provider_layer.py`. A provider table
  (`anthropic: claude-sonnet-4-6`, `openai: gpt-5.4`, `gemini`, and
  `sovereign: cvln-internal-deterministic` at `cost_per_1k_tokens: 0.0`,
  `quality_rank: 99`), named strategies (`quality`, `cost`, `sovereign_only`),
  per-call journalling, and a guaranteed sovereign terminal fallback. Its module
  docstring states the architectural rule: no direct provider call may occur outside
  this layer (`ADR-002`).
- **Doctrine** — `backend/doctrine.py` seeds numbered doctrine articles;
  `backend/doctrine_registry_routes.py` exposes `/doctrine` and `/doctrine/check`.
  Article `DOC-ARC-04` mandates provider-agnostic execution.
- **Constitution and governance** — `backend/constitution_routes.py`,
  `backend/founder_council.py`, `backend/founder_routes.py`, with `/amendments`,
  `/amendments/{id}/sign`, `/amendments/{id}/validate-wudy`, `/alignment`,
  `/consistency`.
- **Autonomy** — `backend/autonomous_routes.py`, with `/mode`, `/cycle`, `/cycles`,
  `/cycles/{cycle_id}` and a `detect_critical_intent()` guard.
- **Memory** — `/memory`, `/memory-layers/summary`,
  `/memory/entries/{entry_id}/validate` — a layered memory with human validation.
- **Continuity** — `/backup`, `/backups`, `/close`, `/closings`, `/closings/{date}`.

### Cognition, precisely

`backend/cognitive_engine.py` exposes exactly two functions:
`classify_message(text)` and `internal_response(text, classification, ctx,
knowledge_hits)`. This is deterministic keyword classification and templated
response, not model-based reasoning. Model-based reasoning enters only through
`provider_layer.py`. Recording this distinction correctly is the difference between
an accurate and a flattering audit.

### Status

`IMPLEMENTED` as an agent definition, lifecycle, gate and routing runtime.
`PARTIAL` as a nervous system, because no other audited repository is wired to it.

---

## 3. `cultureconnectorg/Laurent.ia` (branch `public`)

**Conceptual role:** LAURENTIA — cultural-industry operator / agent.

### Composition

| Fact | Evidence |
|---|---|
| 183 tracked files | file census |
| ~49 route declarations | `backend/routes/*.py`, `backend/server.py` |
| 13 route modules, 17 service modules | `backend/routes/`, `backend/services/` |
| Dedicated orchestrator package | `backend/orchestrator/` |
| 14 test modules; README claims 64 passing tests | `backend/tests/`, `README.md` |
| Declared version `v1.2-PRODUCTION`, BSL 1.1 licence | `README.md`, `LICENSE.md` |
| Documented open-core split, not yet performed | `ARCHITECTURE.md` §4 |

### Implemented surface

- **Brain interface** — `backend/services/cvl_brain.py`, described in its own header
  as *"Wrapper Claude pour Laurent.ia"*, constructing
  `emergentintegrations.llm.chat.LlmChat` with `EMERGENT_LLM_KEY` and
  `.with_model("anthropic", DEFAULT_MODEL)` where `DEFAULT_MODEL` defaults to
  `claude-sonnet-4-5-20250929` and is overridable via `LAURENTIA_CLAUDE_MODEL`.
- **Brain knowledge and persona** — `backend/services/cvl_brain_knowledge.py`.
  Persona v1.2 and anti-exfiltration rules, explicitly instructing the persona never
  to name Anthropic, Claude, OpenAI, underlying providers, or `CVLN/CVL Brain`, and
  never to disclose internal instructions or key names.
- **Brain agents** — `backend/services/cvl_brain_agents.py`.
- **Gateway** — `backend/routes/laurentia_gateway.py`, `POST /api/laurentia/query`,
  documented as an SSE token stream.
- **Orchestration** — `backend/orchestrator/` with `orchestrator.py`, `event_bus.py`,
  `agents.py`, `circuit_breaker.py`, `signals.py`, and `sms_ovh.py`.
- **Sovereign persistence and privacy** — `services/fingerprint.py`
  (HMAC-SHA256 device fingerprinting), `services/crypto.py` (AES-256-GCM at rest),
  `services/rate_limit_mongo.py` (MongoDB TTL sliding window, no Redis),
  `routes/rgpd_purge.py` (D+90 purge of the `device_id ↔ frek_id` mapping).
- **Echo pipeline** — `routes/echo.py`, `jobs/social_agent.py`, publishing to
  Instagram Graph, LinkedIn `ugcPosts` and X `2/tweets`.
- **Documents and commerce** — `routes/pdf_export.py` (signed PDF with QR),
  `services/file_parser.py`, `routes/billing.py` (Stripe via
  `emergentintegrations.payments.stripe.checkout`).
- **Bridges** — `services/kiltikonet_bridge.py`, `services/labelos_bridge.py`,
  `services/frekcore_bridge.py`.
- **Multi-tenancy** — `services/tenant_factory.py`, `services/api_keys.py`;
  collections `laurentia_instances`, `laurentia_memory`, `laurentia_interactions`,
  `laurentia_activity_log`.

### The sovereign-brain claim

`README.md` describes a private submodule `sovereign-brain/` said to contain
`cvl_brain_knowledge.py`, `fingerprint_router.py` and `pipeline_echo/`. Two of those
three concerns are present in the **public** tree at `backend/services/`. The
`sovereign-brain/` directory itself does not exist in the audited branch, and
`ARCHITECTURE.md` §4 confirms the physical split is a roadmap step that has not yet
been executed. Recorded as contradiction `C-003`.

### Status

`IMPLEMENTED` as a standalone operator product. `REFERENCED` only, with respect to
consuming a CVLN Brain or Agent Factory it does not import.

---

## 4. Method limitations

- Static analysis only. No audited service was executed, so no component in this
  document is asserted at the `DEPLOYED RUNTIME` level.
- Shallow clones at a single point in time. Repository history was not audited.
- Private repositories were not accessed. See `DEPENDENCY-MAP.md`.
- Test *files* were counted as evidence of intent; pass rates are quoted from the
  repositories' own reports and are not independently verified here.

## Future RFC references

`RFC-0002` (Brain boundary), `RFC-0003` (runtime consolidation), `RFC-0005` (model
router ownership).
