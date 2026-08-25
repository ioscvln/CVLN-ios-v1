---
title: Component Matrix
purpose: Canonical per-component evidence and status register for the CVLN estate.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Components observable in the three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Component Matrix

One row per significant component. Exactly one status per row. `Evidence` cites a
path in the audited repository; where a row has no path, its status is not
`IMPLEMENTED`.

Repository keys: `META` = MetaCVLN, `FACTORY` = CVLNAgentfactory, `LAUR` = Laurent.ia,
`—` = not present in any audited repository.

| Component | Repository | Path | Conceptual responsibility | Actual implementation | Evidence | Status | Dependencies | Consumers | Providers | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Governance API | META | backend/server.py | OS governance plane | ~50 FastAPI paths in one module | 1611-line server.py | IMPLEMENTED | MongoDB | META frontend | none | Monolith; no module split |
| Identity & RBAC | META | backend/server.py | Identity, authorisation | JWT + bcrypt, 6 roles | /auth/login, /auth/me | IMPLEMENTED | MongoDB | META frontend | none | Roles admin/cfo/hr_lead/ops_lead/legal_lead/employee |
| Entity Registry | META | backend/registry_data.py | Estate registry | Static list of CVLN repositories with URLs | registry_data.py | IMPLEMENTED | none | /registry/* | none | Static, not self-registering |
| Capability Discovery | META | backend/server.py | Discover repo capabilities | Prober expecting /api/capabilities | /registry/discover-all | PARTIAL | remote repos | registry | remote repos | Repo audit reports 12/12 DEGRADED — no repo exposes the endpoint |
| Signed Event Bus | META | backend/server.py | Tamper-evident events | Ed25519 sign + verify, notary DID key_id | /events/emit, /events/verify | IMPLEMENTED | MongoDB, cryptography | decisions, audit | none | Tampered payloads quarantined |
| Inter-system Contracts | META | backend/contracts.py | Versioned wire contracts | Event, Capability, RoutingDecision, SystemState, ExecutionStep/Plan | contracts.py | DEFINED | none | adapters | none | Pydantic models plus example catalog; no repo consumes them |
| Decision System | META | backend/server.py | Human decision of record | approve/reject/edit/escalate/pause/rollback | /decisions/{id}/action | IMPLEMENTED | MongoDB | command centre | none | Founder-in-the-loop |
| Adaptive Runtime State | META | backend/server.py | Degradation control | normal/degraded/critical over 7 signals with hysteresis | /runtime/state | IMPLEMENTED | ping history | META frontend | none | Admin override supported |
| Learning Loop | META | backend/server.py | Doctrine evolution | Threshold-gated proposals, manual approval, doctrine_history | /learning/proposals | PARTIAL | feedback | doctrine | none | Feedback-to-proposal aggregation not automatic |
| Notary & Public Audit | META | backend/server.py | Verifiable audit trail | Notarisations with verify and export, public read surface | /notarizations, /public/notarizations | IMPLEMENTED | Ed25519 keys | external verifiers | none | Notary private key stored unencrypted at rest |
| Outbound Adapters | META | backend/server.py | Cross-system actuation | Three HTTP adapters | /adapters/laurentia/briefing | PARTIAL | remote repos | META | LAUR, LabelOS, Wallet | Wallet adapter returns upstream 404 |
| ADL v1 | FACTORY | backend/adl_schema.py | Agent Definition Language | Pydantic models, AGT-nnn grammar, semver, 7-stage lifecycle | adl_schema.py | IMPLEMENTED | pydantic, yaml | agent routes | none | Canonical CVLN protocol that demonstrably exists |
| ADL v2 | FACTORY | backend/schemas/adl_v2_schema.json | Agent schema, next generation | JSON Schema: adl_version, schema_uri, agent, brain, capabilities | adl_v2_schema.json | DEFINED | none | adl_v2_routes | none | Schema present; migration path unstated |
| Agent Lifecycle Runtime | FACTORY | backend/server.py | Lifecycle, versions, checkpoints | lifecycle/state/versions/diff/checkpoint/export/wake | /agents/{id}/lifecycle | IMPLEMENTED | MongoDB | factory frontend | none | Ordered transitions enforced in code |
| Gate System | FACTORY | backend/gate_routes.py | Authority limits | GATE_LEVELS, CRITICAL_ACTIONS, /check, append-only journal | gate_routes.py | IMPLEMENTED | journal | agents | none | Blocked actions journalled as action_bloquee |
| Factory Event Bus | FACTORY | backend/event_bus.py | Internal eventing | Enforced topic prefixes, DLQ, spool replay | event_bus.py | IMPLEMENTED | MongoDB | factory modules | none | Namespace: agent./factory./monitoring./memory./identity./daily./system. |
| Model Router | FACTORY | backend/provider_layer.py | Provider selection & fallback | Provider table, strategies, journalling, sovereign terminal fallback | provider_layer.py | IMPLEMENTED | provider SDKs | cognitive routes | anthropic, openai, gemini, sovereign | ADR-002: no provider call outside this layer |
| Sovereign Provider | FACTORY | backend/provider_layer.py | Guaranteed local fallback | Deterministic non-model provider cvln-internal-deterministic | provider_layer.py line 63 | IMPLEMENTED | none | Model Router | none | Deterministic fallback, not a trained sovereign model |
| Doctrine Engine | FACTORY | backend/doctrine.py | Doctrine of record | Numbered articles, /doctrine, /doctrine/check | doctrine.py, doctrine_registry_routes.py | IMPLEMENTED | MongoDB | gates, cognition | none | Contradicts Brain-owns-doctrine rule; see C-002 |
| Constitution Service | FACTORY | backend/constitution_routes.py | Constitutional amendment | Amendments, signing, validation, alignment, consistency | /amendments/{id}/sign | IMPLEMENTED | founder_council | governance | none | Duplicates META governance intent |
| Autonomy Controller | FACTORY | backend/autonomous_routes.py | Autonomous operation | Modes, cycles, critical-intent detection | /cycle, /cycles | PARTIAL | gates | agents | Model Router | Cycles exist; no ISA instruction semantics |
| Layered Memory | FACTORY | backend/server.py | Agent memory | Memory entries, layer summary, human validation | /memory-layers/summary | PARTIAL | MongoDB | agents | none | No graph structure observed |
| Cognitive Engine | FACTORY | backend/cognitive_engine.py | Reasoning | classify_message + internal_response only | cognitive_engine.py | PARTIAL | none | cognitive routes | Model Router | Deterministic classifier, not model reasoning |
| Continuity & Closing | FACTORY | backend/continuity_routes.py | Backup, daily closing | /backup, /backups, /close, /closings | continuity_routes.py | IMPLEMENTED | MongoDB | ops | none | Operational hygiene |
| Brain Interface | LAUR | backend/services/cvl_brain.py | Access to intelligence | LlmChat wrapper over emergentintegrations | cvl_brain.py line 16-28 | IMPLEMENTED | EMERGENT_LLM_KEY | gateway, echo, jobs | anthropic | Header text: Wrapper Claude pour Laurent.ia |
| Brain Persona | LAUR | backend/services/cvl_brain_knowledge.py | Persona and doctrine of voice | Persona v1.2, anti-jailbreak and non-disclosure rules | cvl_brain_knowledge.py | IMPLEMENTED | none | Brain Interface | none | Instructs persona never to name providers or CVL Brain |
| Brain Agents | LAUR | backend/services/cvl_brain_agents.py | Task-scoped brain agents | Agent definitions in service code | cvl_brain_agents.py | PARTIAL | Brain Interface | orchestrator | none | Not ADL-defined |
| Sovereign Brain Core | LAUR | none | Sovereign model, routing, echo pipeline | Absent from public tree | README.md sovereign-brain/ block | PRIVATE / NOT VISIBLE | unknown | LAUR | unknown | Claimed private submodule; not present. See C-003 |
| Model training infrastructure | — | none | Weights, adapters, datasets, fine-tuning | No evidence | none | UNKNOWN | unknown | unknown | unknown | NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES |
| Laurentia Gateway | LAUR | backend/routes/laurentia_gateway.py | External query surface | POST /api/laurentia/query, SSE token stream | laurentia_gateway.py | IMPLEMENTED | Brain Interface | SDK, widget | none | Documented streaming path |
| Laurentia Orchestrator | LAUR | backend/orchestrator/orchestrator.py | Local agent orchestration | Orchestrator, agents, signals, circuit breaker, event bus | orchestrator/ | IMPLEMENTED | MongoDB | routes | none | Third independent event bus in the estate |
| Ghost Persistence | LAUR | backend/services/fingerprint.py | Cookieless identity | HMAC-SHA256 device fingerprint | fingerprint.py | IMPLEMENTED | none | sessions | none | 64-hex irreversible device_id |
| Encryption at Rest | LAUR | backend/services/crypto.py | Confidentiality | AES-256-GCM for conversations and memory | crypto.py | IMPLEMENTED | key env | persistence | none | Only audited repo with encryption at rest |
| RGPD Purge | LAUR | backend/routes/rgpd_purge.py | Data minimisation | D+90 purge of device_id to frek_id mapping | rgpd_purge.py | IMPLEMENTED | MongoDB | compliance | none | Documented retention limit |
| Echo Pipeline | LAUR | backend/jobs/social_agent.py | Omnichannel publication | Instagram Graph, LinkedIn, X publication | social_agent.py | IMPLEMENTED | provider tokens | echo routes | Meta, LinkedIn, X | Retry x3 then skip |
| Signed PDF Export | LAUR | backend/routes/pdf_export.py | Verifiable artefacts | PDF with QR signature | pdf_export.py | IMPLEMENTED | none | reports | none | Quota-tiered |
| Billing | LAUR | backend/routes/billing.py | Commerce | Stripe checkout via emergentintegrations | billing.py | IMPLEMENTED | Stripe | tiers | Stripe | Tier gating documented in README |
| External Bridges | LAUR | backend/services/kiltikonet_bridge.py | Interop with CVLN products | Bridge modules for Kiltikonet, LabelOS, FREKCORE | services/*_bridge.py | PARTIAL | remote APIs | routes | Kiltikonet, LabelOS, FREKCORE | Kiltikonet unavailable path present in code |
| Python SDK | LAUR | none | Programmatic access | Not present | README.md marks as forthcoming | PROPOSED | Gateway | third parties | none | pip install laurentia-sdk not published |
| Embeddable Widget | LAUR | none | Embedded surface | Not present | README.md marks as forthcoming | PROPOSED | Gateway | host sites | none | cdn.laurent.ia/widget.v1.js not present |
| ISA instruction set | — | none | Native execution cycle | Not found in any audited repository | absence of REASON/PLAN/MEMORY_READ semantics | PROPOSED | Agent runtime | agents | none | Newly proposed in this repository; see protocols/ISA |
| MCL language | — | none | Declarative OS language | Not found in any audited repository | no grammar, parser or file extension | PROPOSED | META | operators | none | Newly proposed; see protocols/MCL |
| Agent Protocol handshake | — | none | Agent-to-agent negotiation | No handshake found | absence of handshake in all repos | PROPOSED | Event bus | agents | none | Closest existing artefact is capability discovery |
| Unified Memory Graph | — | none | Estate-wide semantic memory | Three separate memory stores, no graph | FACTORY /memory, LAUR laurentia_memory, META collections | PROPOSED | all layers | Brain | none | No shared schema observed |
| Cross-repo observability | — | none | Estate-wide tracing | Absent; documented as a gap by META | META audit doc | PROPOSED | all layers | ops | none | OpenTelemetry named but not implemented |

## Future RFC references

`RFC-0002`, `RFC-0003`, `RFC-0005`, `RFC-0007`, `RFC-0008`.
