import os, textwrap
ROOT = "/app/cvln-intelligence-os"

def w(path, title, purpose, owner, scope, status, attrib, body, version="1.0"):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    fm = (f"---\ntitle: {title}\npurpose: {purpose}\nownership: {owner}\n"
          f"scope: {scope}\nversion: {version}\nstatus: {status}\nattribution: {attrib}\n---\n\n")
    open(full, "w").write(fm + f"# {title}\n\n" + textwrap.dedent(body).strip() + "\n")

MET = "META CVLN — Office of Governance"
BRN = "CVL BRAIN — Sovereign Intelligence"
FAC = "CVLN AGENT FACTORY — Runtime Authority"
ARC = "CVLN Group — Office of the Principal Systems Architect"

PROPOSED_BANNER = """> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.
"""

# ---------------- audit remainder ----------------
w("audit/IMPLEMENTATION-STATUS.md", "Implementation Status", "Aggregate status distribution across the audited estate.", ARC, "Three audited repositories", "IMPLEMENTED", "IMPLEMENTATION", """
Derived from [`COMPONENT-MATRIX.md`](COMPONENT-MATRIX.md). Each component holds
exactly one status.

## Distribution

| Status | Count | Reading |
|---|---|---|
| IMPLEMENTED | 24 | Executable code verified by path |
| PARTIAL | 9 | Code exists, subsystem incomplete or unwired |
| DEFINED | 3 | Schema or contract only |
| REFERENCED | 0 | — |
| PRIVATE / NOT VISIBLE | 1 | `sovereign-brain/` |
| PROPOSED | 7 | ISA, MCL, handshake, memory graph, observability, SDK, widget |
| UNKNOWN | 1 | Model training infrastructure |

## By repository

| Repository | IMPLEMENTED | PARTIAL | DEFINED | Other |
|---|---|---|---|---|
| CVLN AGENT FACTORY | 9 | 3 | 1 | 0 |
| META CVLN | 7 | 4 | 1 | 0 |
| LAURENTIA | 8 | 2 | 0 | 3 |
| No repository | 0 | 0 | 0 | 6 |

Agent Factory carries the highest implemented weight; Laurentia carries the highest
count of externally-facing implemented capability; META carries the estate's only
cryptographic trust chain.

## Attribution discipline

No component in v1.0 is asserted at `DEPLOYED RUNTIME`. Static analysis cannot
establish deployment, and the audit does not claim what it did not observe.

## Future RFC references

`RFC-0002`, `RFC-0003`, `RFC-0007`, `RFC-0008`.
""")

w("audit/DEPENDENCY-MAP.md", "Dependency Map", "Map every declared and referenced dependency, including inaccessible ones.", ARC, "Audited repositories and their named counterparties", "IMPLEMENTED", "IMPLEMENTATION", """
## Inter-repository dependencies (audited scope)

| From | To | Kind | Status |
|---|---|---|---|
| META CVLN | LAURENTIA | HTTP adapter `/adapters/laurentia/briefing` | IMPLEMENTED |
| META CVLN | LabelOS | HTTP adapter `/adapters/labelos/push_catalogue` | PARTIAL |
| META CVLN | Wallet | HTTP adapter `/adapters/wallet/transaction` | PARTIAL — upstream 404 |
| META CVLN | all registered repos | capability probe | PARTIAL — 12/12 DEGRADED |
| LAURENTIA | Agent Factory | — | absent |
| Agent Factory | META CVLN | — | absent |

**Import-level dependencies between audited repositories: none.**

## Referenced but not audited

Named in code or registry data, outside audit scope, contents not inspected. Marked
`PRIVATE / NOT ACCESSIBLE` where no public tree was reachable.

| Counterparty | Referenced from | Status |
|---|---|---|
| Kiltikonet | `LAUR/backend/services/kiltikonet_bridge.py` | REFERENCED |
| LabelOS | `LAUR/services/labelos_bridge.py`, META adapter | REFERENCED |
| FREKCORE | `LAUR/services/frekcore_bridge.py`, META registry | Excluded by instruction |
| KORA | META `registry_data.py` | REFERENCED |
| CVL Academy | META `registry_data.py` | REFERENCED |
| Wallet | META adapter | REFERENCED |
| Good Mood, Gala Cook, FMS, Blockchain | META `registry_data.py` | REFERENCED |
| `sovereign-brain/` | `LAUR/README.md` | PRIVATE / NOT ACCESSIBLE |

No speculation is offered about the contents of any entry above.

## External service dependencies

| Service | Consumer | Evidence |
|---|---|---|
| Model providers via `emergentintegrations` | LAUR, FACTORY, META | `cvl_brain.py`, `provider_layer.py` |
| Stripe | LAUR | `routes/billing.py` |
| OVH SMS + OVH S3 | LAUR | `orchestrator/sms_ovh.py`, `jobs/corpus_pipeline.py` |
| Instagram Graph, LinkedIn, X | LAUR | `jobs/social_agent.py` |
| Telegram | FACTORY | `backend/notifier.py` |
| MongoDB | all three | per-repository `database.py` / `lib` |

## Future RFC references

`RFC-0003`, `RFC-0006`.
""")

w("audit/ARCHITECTURE-EVIDENCE.md", "Architecture Evidence", "Bind each architectural claim to a citable repository artefact.", ARC, "Three audited repositories", "IMPLEMENTED", "IMPLEMENTATION", """
Every claim in this specification traces to a row below. Where a claim has no row,
it is a proposal and is labelled `PROPOSED` at its point of use.

| Claim | Evidence path | Verbatim marker |
|---|---|---|
| ADL exists as a validated language | `FACTORY/backend/adl_schema.py` | `AGENT_ID_RE = ^AGT-\\d{3}$`, `SEMVER_RE` |
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
""")

w("audit/CROSS-REPO-INTEGRATION.md", "Cross-Repository Integration", "State precisely how the audited systems do and do not interoperate.", ARC, "Three audited repositories", "IMPLEMENTED", "IMPLEMENTATION", """
## Realised integration

Exactly one class of realised edge exists: outbound HTTP from META CVLN.

```mermaid
graph LR
  META["META CVLN"] -->|"POST /adapters/laurentia/briefing"| LAUR["LAURENTIA"]
  META -->|"POST /adapters/labelos/push_catalogue"| LABEL["LabelOS · not audited"]
  META -.->|"POST /adapters/wallet/transaction · 404"| WALLET["Wallet · not audited"]
  META -.->|"GET /api/capabilities · DEGRADED"| FACT["AGENT FACTORY"]
  META -.->|"GET /api/capabilities · DEGRADED"| LAUR
  LAUR -->|"bridge modules"| KILT["Kiltikonet · not audited"]
  FACT -->|"notifier"| TG["Telegram"]
```

Solid edges are confirmed by code. Dotted edges are implemented on the caller side
and unanswered on the provider side.

## Unrealised integration

| Expected edge | Reality |
|---|---|
| Laurentia consumes the Brain as a service | Consumes a local module instead |
| Laurentia consumes the Agent Runtime | No reference of any kind |
| Agent Factory consumes META governance | No reference of any kind |
| Any system consumes `contracts.py` | No consumer found |
| Shared identity across systems | Three separate auth systems |
| Shared event envelope | Three separate event models |

## Integration readiness assessment

The estate is better positioned than the absence of edges suggests. Three assets make
integration tractable rather than speculative:

1. **META already defines the contracts** — `Event`, `Capability`,
   `RoutingDecision`, `SystemState`, `ExecutionPlan`. The wire vocabulary exists;
   only adoption is missing.
2. **META already implements the prober.** Providers need only answer.
3. **Agent Factory already proves the provider-boundary pattern**, fallback
   included. The target does not require inventing it, only relocating it.

The blocking constraint is therefore ownership, not engineering. See
[`FOUNDER-DECISIONS.md`](FOUNDER-DECISIONS.md).

## Future RFC references

`RFC-0003`, `RFC-0006`.
""")

w("audit/RESPONSIBILITY-MATRIX.md", "Responsibility Matrix", "Record which component owns each responsibility today, without reassigning any.", ARC, "Three audited repositories", "IMPLEMENTED", "IMPLEMENTATION", """
This is a Phase 2 document: it documents reality. Responsibilities are **not** moved
here. Target ownership is proposed only in
[`TARGET-ARCHITECTURE.md`](TARGET-ARCHITECTURE.md).

`✔` owns it in code · `~` partial · `·` no implementation · `!` contested ownership

| Responsibility | META | FACTORY | LAUR | Current owner of record | Status |
|---|---|---|---|---|---|
| Identity | ✔ | ✔ | ✔ | contested — three systems | ! |
| Entities | ✔ | ✔ | · | contested | ! |
| Governance | ✔ | ✔ | · | contested | ! |
| Constitution | ✔ | ✔ | · | contested | ! |
| Permissions | ✔ | ~ | ~ | META (RBAC) | IMPLEMENTED |
| Capabilities | ~ | ✔ | · | Agent Factory | PARTIAL |
| Agents | ✔ | ✔ | ~ | Agent Factory (ADL) | IMPLEMENTED |
| Agent lifecycle | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Orchestration | · | ✔ | ✔ | contested | ! |
| Cognition | ~ | ~ | ✔ | Laurentia | PARTIAL |
| Reasoning | · | ~ | ~ | none — classifier only | PARTIAL |
| Memory | ~ | ✔ | ✔ | contested — three stores | ! |
| Doctrine | ✔ | ✔ | ✔ | contested — see C-002 | ! |
| Persona | · | · | ✔ | Laurentia | IMPLEMENTED |
| Model selection | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Model fallback | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Learning | ✔ | ~ | · | META | PARTIAL |
| Execution | · | ✔ | ✔ | contested | ! |
| Tools | · | ✔ | ✔ | contested | ! |
| Events | ✔ | ✔ | ✔ | contested — three buses | ! |
| Sessions | · | · | ✔ | Laurentia | IMPLEMENTED |
| Workflows | ~ | ✔ | ✔ | contested | ! |
| Observability | ✔ | ~ | ~ | META (runtime state) | PARTIAL |
| Security | ~ | ~ | ✔ | Laurentia (crypto, RGPD) | PARTIAL |
| Persistence | ✔ | ✔ | ✔ | per-system, no sharing | IMPLEMENTED |
| Gates | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Trust chain / notarisation | ✔ | · | ~ | META | IMPLEMENTED |
| Autonomy | · | ✔ | · | Agent Factory | PARTIAL |
| Continuity / backup | · | ✔ | · | Agent Factory | IMPLEMENTED |

## Findings

- **Eleven responsibilities are contested.** Contested ownership, not missing
  functionality, is the estate's dominant structural problem.
- **Six responsibilities have a single clear owner** and should not be disturbed:
  gates, agent lifecycle, model routing (Agent Factory); persona, sessions,
  encryption (Laurentia); notarisation (META).
- **Reasoning has no true owner.** The vocabulary exists in three places; the
  implementation is a keyword classifier plus provider calls.

## Future RFC references

`RFC-0002` (doctrine and Brain), `RFC-0003` (runtime), `RFC-0005` (router).
""")

w("audit/OPEN-QUESTIONS.md", "Open Questions", "Questions the audited evidence cannot answer.", ARC, "Three audited repositories", "IMPLEMENTED", "IMPLEMENTATION", """
Each question is unanswerable from the audited public repositories. None is answered
speculatively here.

| ID | Question | Why unanswerable | Who can answer |
|---|---|---|---|
| Q-001 | Does a sovereign CVL Brain model exist — weights, adapters, datasets, or fine-tuning infrastructure? | No such artefact, config or training script appears in any audited tree | Founder / CVLN Group |
| Q-002 | Is Claude the primary model or a fallback for CVL Brain? | Laurentia hardcodes one Anthropic model with no fallback; Agent Factory ranks Anthropic first among four with a sovereign terminal fallback. The two repositories imply different answers | Founder |
| Q-003 | Which of the three constitutions is authoritative — META's, Agent Factory's, or the conceptual one? | All three exist; none references the others | Founder |
| Q-004 | Are the twelve registry entries live services or aspirational placeholders? | `registry_data.py` is static; discovery returned DEGRADED for all | Operations |
| Q-005 | Is `sovereign-brain/` an existing private repository or a planned one? | Referenced only by README prose | Founder |
| Q-006 | Which ADL generation is authoritative, v1 or v2? | Both are served; no deprecation marker exists | Agent Factory owner |
| Q-007 | Is any audited system currently deployed, and at which commit? | Static audit only; no runtime probed | Operations |
| Q-008 | Do the quoted test results (64 in Laurentia, 17 in META) pass at the audited commits? | Reports are committed artefacts, not re-executed here | CI |
| Q-009 | Was the canonical layering ever an implementation plan, or always a conceptual map? | No migration document, ADR or issue in the audited trees proposes it | Founder |
| Q-010 | Is `frek_id` a cross-estate identity or a Laurentia-local identifier? | Appears only in Laurentia; META has no corresponding notion | Founder |

## Standing rule

Q-001 and Q-002 must be answered before any document in this repository makes a
sovereignty claim about the Brain. Until then the required formulation is:
**NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.**

## Future RFC references

`RFC-0002`.
""")

w("audit/FOUNDER-DECISIONS.md", "Founder Decisions Required", "Decisions that only the founder can make, each blocking downstream work.", ARC, "CVLN intelligence ecosystem", "IMPLEMENTED", "SPECIFICATION", """
These are the critical path. Each entry states the decision, what it unblocks, and
the cost of deferral. No option is pre-selected.

## FD-001 — Doctrine and Brain boundary

**Decision.** Which component owns doctrine of record, and what "CVL Brain" denotes:
a service, a library, a model, or an architectural concept.

**Options.** (a) Brain-owned doctrine, Brain extracted as a service; (b) META-owned
doctrine, Brain reduced to a reasoning service; (c) formalise the current triplication
with a reconciliation protocol.

**Blocks.** `G-004`, `G-009`, `G-010`; contradictions `C-002`, `C-008`; all of
`architecture/CVLN-BRAIN.md` beyond audit findings.

**Cost of deferral.** Three doctrine stores continue diverging with no reconciliation
mechanism.

## FD-002 — Dependency direction

**Decision.** Ratify, amend, or abandon the canonical layering
`META → Agent Factory → Brain → Laurentia → Applications`.

**Options.** (a) Ratify and fund integration; (b) adopt a federated peer model with
contracts only; (c) declare the layering conceptual and stop presenting it as
architecture.

**Blocks.** `G-001`, `G-008`; contradiction `C-001`.

**Cost of deferral.** Every integration estimate remains unbounded.

## FD-003 — Open-core boundary

**Decision.** Which concerns are sovereign, and whether the documented
`open-core/` versus `sovereign-brain/` split is executed.

**Options.** (a) Execute the migration in `LAUR/ARCHITECTURE.md` steps 2–4;
(b) correct the README to the future tense and defer; (c) redefine the boundary.

**Blocks.** `G-012`; contradiction `C-003`.

**Cost of deferral.** Anti-jailbreak and persona rules remain publicly readable,
which measurably weakens them.

## FD-004 — Model router ownership

**Decision.** Where model routing lives, and whether provider-agnosticism binds the
whole estate.

**Options.** (a) Promote `provider_layer.py` to a Brain-owned shared service;
(b) leave routing in Agent Factory and require Laurentia to call it; (c) permit
per-system routing and withdraw doctrine article `DOC-ARC-04`.

**Blocks.** `G-011`; contradictions `C-004`, `C-006`.

**Cost of deferral.** Laurentia remains a single-provider single point of failure.

## FD-005 — ISA and MCL

**Decision.** Adopt, defer, or reject the proposed ISA instruction set and MCL
language.

**Options.** (a) Adopt one or both via `RFC-0007` / `RFC-0008`; (b) defer pending
integration work; (c) reject and remove the proposal directories.

**Blocks.** `G-014`, `G-015`.

**Cost of deferral.** Low. Both are `PROPOSED` and quarantined; nothing depends on
them. Deferral is a legitimate outcome.

---

## Sequencing

`FD-002` first, since it determines whether integration is funded at all. `FD-001`
and `FD-004` next. `FD-003` is independent and can proceed in parallel. `FD-005`
last.

## Future RFC references

`RFC-0001` through `RFC-0008`.
""")
print("audit set written")
