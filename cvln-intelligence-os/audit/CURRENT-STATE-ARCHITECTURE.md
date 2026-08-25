---
title: Current State Architecture
purpose: Reconstruct, from repository evidence only, the architecture that exists today.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Current State Architecture

This document describes only what repository evidence establishes. Connections that
evidence does not confirm are labelled `UNVERIFIED`. No component is asserted at the
`DEPLOYED RUNTIME` level, because no audited service was executed.

---

## 1. The finding that governs the rest

CVLN today is **three independently deployable systems that share a vocabulary**, not
one operating system with four layers. Each audited repository:

- has its own `requirements.txt` and FastAPI application;
- opens its own MongoDB connection;
- implements its own authentication;
- implements its own event bus;
- and imports nothing from the other two.

The estate is therefore best described as a federation with one partially wired
governance observer.

---

## 2. Component boundaries

```mermaid
graph TB
  subgraph META["META CVLN — governance plane · IMPLEMENTED"]
    MAUTH["Identity & RBAC<br/>JWT + bcrypt · 6 roles"]
    MREG["Entity Registry<br/>static registry_data.py"]
    MDISC["Capability Discovery<br/>PARTIAL"]
    MEV["Signed Event Bus<br/>Ed25519 + notary DID"]
    MDEC["Decision System"]
    MRUN["Adaptive Runtime State"]
    MLEARN["Learning Proposals<br/>PARTIAL"]
    MNOT["Notary & Public Audit"]
    MCON["contracts.py<br/>5 contracts · DEFINED"]
    MADP["Outbound Adapters<br/>PARTIAL"]
  end

  subgraph FACTORY["CVLN AGENT FACTORY — agent runtime · IMPLEMENTED"]
    ADL1["ADL v1<br/>adl_schema.py"]
    ADL2["ADL v2<br/>JSON Schema · DEFINED"]
    ALIFE["Agent Lifecycle<br/>7 stages"]
    GATE["Gate System<br/>GATE_LEVELS"]
    FEV["Factory Event Bus<br/>topics + DLQ"]
    MROUTER["Model Router<br/>provider_layer.py"]
    SOV["Sovereign Provider<br/>deterministic fallback"]
    DOCT["Doctrine Engine"]
    CONST["Constitution Service"]
    AUTON["Autonomy Controller<br/>PARTIAL"]
    FMEM["Layered Memory<br/>PARTIAL"]
    COG["Cognitive Engine<br/>classifier · PARTIAL"]
  end

  subgraph LAUR["LAURENTIA — cultural-industry operator · IMPLEMENTED"]
    LGW["Gateway<br/>/api/laurentia/query SSE"]
    LBRAIN["Brain Interface<br/>cvl_brain.py"]
    LPERS["Persona & Knowledge<br/>cvl_brain_knowledge.py"]
    LORCH["Orchestrator<br/>+ circuit breaker"]
    LGHOST["Ghost Persistence<br/>HMAC-SHA256"]
    LCRYPT["AES-256-GCM at rest"]
    LECHO["Echo Pipeline"]
    LBILL["Billing · Stripe"]
    LBRIDGE["Bridges<br/>Kiltikonet · LabelOS · FREKCORE"]
  end

  EXT["Third-party model providers<br/>via emergentintegrations"]
  SOCIAL["Instagram · LinkedIn · X"]
  PRIV["sovereign-brain/<br/>PRIVATE / NOT VISIBLE"]

  MREG --> MDISC
  MDISC -. "probes /api/capabilities<br/>returns DEGRADED 12/12" .-> FACTORY
  MDISC -. "probes /api/capabilities<br/>returns DEGRADED 12/12" .-> LAUR
  MADP -->|"HTTP · /adapters/laurentia/briefing"| LAUR
  MEV --> MNOT
  MEV --> MDEC
  MLEARN --> MDEC

  ADL1 --> ALIFE
  ALIFE --> GATE
  AUTON --> GATE
  COG --> MROUTER
  MROUTER --> SOV
  MROUTER --> EXT
  DOCT --> GATE

  LGW --> LBRAIN
  LPERS --> LBRAIN
  LBRAIN --> EXT
  LORCH --> LECHO
  LECHO --> SOCIAL
  LBRAIN -.->|"README claim only"| PRIV

  MCON -. "no consumer found" .-> FACTORY
  MCON -. "no consumer found" .-> LAUR
```

Dotted edges are `UNVERIFIED` or documented-but-unrealised. Note the absence of any
edge from Laurentia to Agent Factory, and any edge from Agent Factory to META.

---

## 3. Data flows

### 3.1 Laurentia query flow — `IMPLEMENTED`

```mermaid
sequenceDiagram
  participant U as Client
  participant GW as laurentia_gateway.py
  participant FP as fingerprint.py
  participant RL as rate_limit_mongo.py
  participant K as cvl_brain_knowledge.py
  participant B as cvl_brain.py
  participant P as Provider (anthropic)
  participant DB as MongoDB (AES-256-GCM)

  U->>GW: POST /api/laurentia/query
  GW->>FP: derive device_id (HMAC-SHA256, cookieless)
  GW->>RL: sliding-window check (TTL, no Redis)
  GW->>K: load persona v1.2 + anti-jailbreak system message
  GW->>B: LlmChat(system_message).with_model("anthropic", DEFAULT_MODEL)
  B->>P: send_message
  P-->>B: completion
  B-->>GW: text
  GW-->>U: SSE token stream
  GW->>DB: persist encrypted interaction + memory
```

There is no fallback provider in this path. On provider failure the estate has no
recovery route for Laurentia; `routes/social_admin.py` returns `503`.

### 3.2 Agent Factory execution flow — `IMPLEMENTED` with a `PARTIAL` cognition step

```mermaid
sequenceDiagram
  participant OP as Operator
  participant A as /agents · lifecycle
  participant G as gate_routes.py
  participant J as activity_journal.py
  participant C as cognitive_engine.py
  participant R as provider_layer.py
  participant S as SovereignProvider
  participant E as event_bus.py

  OP->>A: request action on AGT-nnn
  A->>G: /check(level, action)
  alt not permitted
    G->>J: journal "action_bloquee"
    G-->>OP: blocked / escalated to single queue
  else permitted
    A->>C: classify_message(text)
    C->>R: route(strategy)
    R->>R: try providers in strategy order, journal each call
    R->>S: terminal fallback (guaranteed)
    A->>E: publish agent.* event
    E->>E: on failure → DLQ, replayable from spool
  end
```

Cognition here is `classify_message` plus `internal_response` — deterministic
classification, not model reasoning. Model reasoning is reachable only through
`provider_layer.py`.

### 3.3 META governance and trust flow — `IMPLEMENTED`

```mermaid
sequenceDiagram
  participant P as Operator
  participant API as META /api
  participant EV as /events/emit
  participant NT as Notary (Ed25519)
  participant D as /decisions/{id}/action
  participant L as /learning/proposals
  participant H as doctrine_history

  P->>API: authenticate (JWT + bcrypt, RBAC)
  API->>EV: emit event
  EV->>NT: sign canonical payload (key_id = notary DID)
  NT-->>EV: signature
  Note over EV: tampered payload → quarantined on verify
  P->>D: approve / reject / edit / escalate / pause / rollback
  P->>L: approve proposal above threshold
  L->>H: append doctrine_history record with evidence
```

Doctrine is never mutated automatically. Every doctrine change is a human act with an
evidence record — the strongest governance property found in the estate.

---

## 4. Authentication and authorisation

| System | Mechanism | Roles | Evidence |
|---|---|---|---|
| META | JWT + bcrypt, RBAC | admin, cfo, hr_lead, ops_lead, legal_lead, employee | `/auth/login`, `/auth/me` |
| FACTORY | `auth_utils.get_current_actor` dependency | actor-based, gate levels | `backend/auth_utils.py`, `gate_routes.py` |
| LAUR | API keys, tiers, Emergent OAuth session endpoint | tier-based (Free/Creator/Infinite/Enterprise) | `services/api_keys.py`, `routes/auth.py` |

There is no single sign-on and no shared identity. An actor in Agent Factory has no
identity in META, and vice versa. `UNVERIFIED`: whether any human account is
intentionally mirrored across systems.

---

## 5. Persistence

Each system owns a separate MongoDB database. Observed collection families:

- **META** — repositories, entities, agents, capabilities, decisions, events,
  evidence, notarizations, `doctrine_history`, `system_keys`.
- **FACTORY** — agents, versions, checkpoints, memory entries, gate journal, events,
  DLQ, doctrine, amendments, closings, backups.
- **LAUR** — `laurentia_instances`, `laurentia_memory`, `laurentia_interactions`,
  `laurentia_activity_log`, sessions, echoes.

Only Laurentia encrypts at rest. Only META stores an asymmetric signing key, and it
stores `system_keys.private_b64` unencrypted — recorded as gap `G-005`.

---

## 6. Memory

Three unrelated stores with no shared schema: Agent Factory's layered memory with
human validation of entries; Laurentia's encrypted `laurentia_memory` per tenant;
META's evidence and event history. No graph structure, no shared identifiers, no
cross-system retrieval. A "CVLN Memory Graph" does not exist today; it is `PROPOSED`.

---

## 7. Model calls

| Path | Boundary | Fallback | Status |
|---|---|---|---|
| FACTORY → `provider_layer.py` | Single enforced boundary (ADR-002) | anthropic → openai → gemini → sovereign | IMPLEMENTED |
| LAUR → `cvl_brain.py` | Single module, one provider | none | IMPLEMENTED, no fallback |
| META → `/brain/ask` | Direct model call | UNVERIFIED | IMPLEMENTED |

Three model call sites, two provider tables, one enforced provider-agnostic layer.

---

## 8. Cross-repository dependencies

Import-level dependencies between audited repositories: **none**.
Runtime edges: META outbound adapters to Laurentia, LabelOS and Wallet, of which the
Wallet edge fails upstream with `404`. Named-but-not-audited counterparties include
Kiltikonet, LabelOS, FREKCORE, KORA, Academy, Wallet and Good Mood — see
`DEPENDENCY-MAP.md`.

---

## 9. What this reconstruction does not establish

- Whether any system is currently deployed, and at what version.
- Whether a sovereign Brain model, weights, adapters or datasets exist.
- Whether the twelve registry entries correspond to live services.
- Whether Laurentia's declared 64 passing tests and META's 17 pass today.

## Future RFC references

`RFC-0003` (runtime consolidation), `RFC-0004` (Laurentia as consumer),
`RFC-0006` (multi-agent orchestration).
