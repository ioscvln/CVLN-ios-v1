---
title: Architecture Evidence
purpose: Bind each architectural claim to a citable repository artefact.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Architecture Evidence

Every claim in this specification traces to a row below. Where a claim has no row,
it is a proposal and is labelled `PROPOSED` at its point of use.

| Claim | Evidence path | Verbatim marker |
|---|---|---|
| ADL exists as a validated language | `FACTORY/backend/adl_schema.py` | `AGENT_ID_RE = ^AGT-\d{3}$`, `SEMVER_RE` |
| Agent lifecycle has 7 ordered stages | `FACTORY/backend/adl_schema.py` | `LifecycleStatus`, `LIFECYCLE_ORDER`, `allowed_transitions()` |
| Agents bind to brain memory and events | `FACTORY/backend/adl_schema.py` | `BrainMemory(scope: session|persistent)`, `BrainEvents(subscribe, publish)` |
| ADL v2 is schema-defined | `FACTORY/backend/schemas/adl_v2_schema.json` | properties `adl_version, schema_uri, agent, brain, capabilities` |
| A provider boundary rule exists | `FACTORY/backend/provider_layer.py` | module docstring: no direct provider call outside this layer; `ADR-002` |
| A terminal sovereign fallback exists | `FACTORY/backend/provider_layer.py` | `sovereign: cvln-internal-deterministic`, `quality_rank: 99`, `class SovereignProvider` |
| Provider-agnosticism is doctrine | `FACTORY/backend/doctrine.py` | `DOC-ARC-04` |
| Event topics are namespaced | `FACTORY/backend/event_bus.py` | `VALID_TOPICS_PREFIXES = ("agent.", "factory.", "monitoring.", "memory.", "identity.", "daily.", "system.")` |
| Gates exist with levels and journalling | `FACTORY/backend/gate_routes.py` | `GATE_LEVELS`, `CRITICAL_ACTIONS`, `action_bloquee` |
| Cognition is deterministic classification | `FACTORY/backend/cognitive_engine.py` | only `classify_message()` and `internal_response()` |
| Brain access is a provider wrapper | `LAUR/backend/services/cvl_brain.py` | `Wrapper Claude pour Laurent.ia`; `LlmChat(...).with_model("anthropic", DEFAULT_MODEL)` |
| Persona forbids naming providers or CVL Brain | `LAUR/backend/services/cvl_brain_knowledge.py` | `Tu ne mentionnes JAMAIS: Anthropic, Claude, ... CVLN/CVL Brain` |
| Gateway streams tokens | `LAUR/backend/routes/laurentia_gateway.py` | `POST /api/laurentia/query → SSE stream` |
| Cookieless identity is HMAC-derived | `LAUR/backend/services/fingerprint.py` | HMAC-SHA256 device fingerprint |
| Encryption at rest exists in Laurentia only | `LAUR/backend/services/crypto.py` | AES-256-GCM |
| Retention is bounded at D+90 | `LAUR/backend/routes/rgpd_purge.py` | purge of `device_id ↔ frek_id` |
| Open-core split is a roadmap step | `LAUR/ARCHITECTURE.md` §4 | `Étape 1 — préparation documentaire (FAIT)`, later steps pending |
| Five inter-system contracts are defined | `META/backend/contracts.py` | `Event, Capability, RoutingDecision, SystemState, ExecutionStep/ExecutionPlan`, `ALL_CONTRACTS` |
| Events are signed and verifiable | `META/backend/server.py` | `/events/emit`, `/events/verify`, Ed25519, notary DID `key_id` |
| Runtime degradation is automatic | `META/backend/server.py` | `/runtime/state`, `normal|degraded|critical`, 7 signals, hysteresis |
| Doctrine change requires human approval | `META/backend/server.py` | `/learning/proposals/{id}/approve` writes `doctrine_history` with evidence |
| Capability discovery finds nothing | `META/docs/META_CVLN_EXISTING_SYSTEM_AUDIT.md` | 12/12 `DEGRADED`, no repo exposes `/api/capabilities` |
| The estate registry is static | `META/backend/registry_data.py` | hardcoded `github_url` / `preview_url` entries |

## Evidence rules applied

1. A directory name is never evidence of a capability.
2. A README claim is evidence of intent, not of implementation.
3. A test file is evidence of intent to verify; quoted pass rates are the
   repository's claim, not this audit's finding.
4. Absence of a grep hit across all three trees is recorded as absence, and the
   corresponding component is `PROPOSED`, not `DEFINED`.

## Future RFC references

`RFC-0002`, `RFC-0005`.
