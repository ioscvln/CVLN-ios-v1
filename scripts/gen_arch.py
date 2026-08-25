import sys
sys.path.insert(0, "/app/scripts")
from gen_audit import w, PROPOSED_BANNER, MET, BRN, FAC, ARC
from gen_constitution import simple

A = "architecture"
# ================= ARCHITECTURE =================
simple(f"{A}/SYSTEM-OVERVIEW.md", "System Overview", "Single-page orientation to the CVLN Intelligence OS as audited and as targeted.", ARC, "PARTIAL", "IMPLEMENTATION", """
CVLN today is three independently deployable systems that share a vocabulary. The
five-layer OS is the target, not the current state.

| Layer | Component | Audited status |
|---|---|---|
| 0 | META CVLN | IMPLEMENTED as a governance plane; depended upon by nothing |
| 1 | CVL BRAIN | PARTIAL — interface, persona and knowledge exist; no Brain service |
| 2 | CVLN AGENT FACTORY | IMPLEMENTED — largest codebase, ADL, gates, router |
| 3 | LAURENTIA | IMPLEMENTED — standalone operator product |
| 4 | Applications | REFERENCED |

## Where the weight actually is

Agent Factory holds ~143 routes across 30 modules and the estate's only agent
definition language. META holds the estate's only cryptographic trust chain.
Laurentia holds the estate's only encryption at rest and its only external product
surface. No single system holds intelligence.

## Diagrams

Current state: [`../diagrams/ECOSYSTEM.md`](../diagrams/ECOSYSTEM.md) ·
layers: [`../diagrams/LAYERED-OS.md`](../diagrams/LAYERED-OS.md).
""", rfc="`RFC-0003`")

simple(f"{A}/CVLN-BRAIN.md", "CVL Brain", "State precisely what is and is not verifiable about CVL Brain.", BRN, "PARTIAL", "IMPLEMENTATION", """
This document is deliberately conservative. CVL Brain is the component about which
the public evidence supports the fewest conclusions, and it is the component about
which overclaiming would be most damaging.

## What the evidence establishes

| Aspect | Finding | Status |
|---|---|---|
| Brain as architectural concept | Named across all three repositories | CONCEPT |
| Brain interface | `LAUR/backend/services/cvl_brain.py` — an `LlmChat` wrapper over `emergentintegrations`, `.with_model("anthropic", DEFAULT_MODEL)` | IMPLEMENTED |
| Brain knowledge and persona | `LAUR/backend/services/cvl_brain_knowledge.py` — Persona v1.2, anti-jailbreak and non-disclosure rules | IMPLEMENTED |
| Brain agents | `LAUR/backend/services/cvl_brain_agents.py` | PARTIAL |
| Brain memory | Encrypted `laurentia_memory` in Laurentia; separate layered memory in Agent Factory; no shared Brain memory | PARTIAL |
| Brain reasoning | Only `classify_message` / `internal_response` in `FACTORY/backend/cognitive_engine.py`; model reasoning reached via provider layer | PARTIAL |
| Brain query surface | `META /brain/ask`, `/brain/history`; `FACTORY /brain/stats`; `LAUR /api/laurentia/query` | IMPLEMENTED, triplicated |
| Model provider | Anthropic model identifiers appear in Laurentia and in Agent Factory's provider table | IMPLEMENTED |
| Fallback / emergency model | Agent Factory only: terminal `sovereign` provider `cvln-internal-deterministic` | IMPLEMENTED |
| Sovereign private Brain components | `sovereign-brain/` referenced by `LAUR/README.md`; absent from the audited tree | PRIVATE / NOT VISIBLE |
| Training, weights, adapters, datasets, fine-tuning | No artefact of any kind | UNKNOWN |

## Required formulations

Regarding training and sovereignty:

> **NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.**

This specification therefore does **not** claim that CVL Brain is trained, and does
**not** claim that it is untrained. It does **not** claim Claude is the primary model,
and does **not** claim Claude is only a fallback. The two audited repositories that
call models imply different answers, which is recorded as open question `Q-002`.

## What "Claude integration ≠ CVL Brain" means concretely

A provider wrapper is a transport. The Brain concept as used across CVLN spans
persona, doctrine, memory, reasoning, routing and emergency behaviour. Of those, the
public evidence shows persona (Laurentia), routing and emergency fallback (Agent
Factory), and partial memory in two places. Equating the whole to the Anthropic
wrapper would collapse six concerns into one and would be wrong.

## Structural finding

There is no addressable Brain service. The Brain is a library in Laurentia, a route
in META and a statistics endpoint in Agent Factory. Consequently no component can own
doctrine on the Brain's behalf — the mechanical cause of contradiction `C-002`.

## Target

One Brain service owning persona, doctrine, semantic and institutional memory,
learning, reasoning, model routing and emergency behaviour, per
[`../api-contracts/BRAIN-API.md`](../api-contracts/BRAIN-API.md). `PROPOSED`, blocked
on `FD-001`.
""", rfc="`RFC-0002` (Brain boundary and sovereignty claim), `RFC-0005`")

for p, t, pu, own, st, body in [
 ("META-CVLN", "META CVLN", "Specify the governance layer as audited.", MET, "IMPLEMENTED", """
Layer 0. Purpose: operating system kernel — constitution, governance, registry,
permissions, runtime state, workflows, entities, objectives, capabilities.

## Implemented subsystems

Identity and RBAC (6 roles) · entity and repository registry · capability discovery
(`PARTIAL`) · signed event bus (Ed25519, notary DID) · decision system (6 verbs) ·
adaptive runtime state (`normal|degraded|critical`, 7 signals, hysteresis) · learning
proposals with human approval · notarisation with public verification · domain
overviews and loop maps · outbound adapters · scheduled registry pings.

## Architectural notes

The backend is a single 1,611-line FastAPI module. The frontend is JavaScript CRA,
diverging from the estate's TypeScript direction. Neither prevents operation, but both
raise the cost of the target integrations.

## Not implemented

Kernel status. Nothing in the estate depends on META. It observes and actuates; it
does not govern by dependency.
"""),
 ("AGENT-FACTORY", "CVLN Agent Factory", "Specify the agent runtime as audited.", FAC, "IMPLEMENTED", """
Layer 2. Purpose: nervous system — ADL, runtime, scheduler, event bus, autonomy,
capability execution, lifecycle, evolution, journal, gates.

## Implemented subsystems

ADL v1 (Pydantic, `AGT-nnn`, semver, 7-stage lifecycle with computed transitions) ·
ADL v2 (JSON Schema, `DEFINED`) · agent lifecycle, versions, diffs, checkpoints,
export, wake · gate system with levels, critical actions and an append-only journal ·
event bus with an enforced topic namespace, dead letter queue and spool replay ·
model router with four providers and a guaranteed terminal fallback · doctrine engine ·
constitution and amendment service · autonomy modes and cycles (`PARTIAL`) · layered
memory with human entry validation (`PARTIAL`) · continuity, backup and daily closing.

## Precise statement about cognition

`backend/cognitive_engine.py` provides `classify_message()` and
`internal_response()`. This is deterministic classification and templated response.
Model-based reasoning is reachable only through `provider_layer.py`. The repository's
own doctrine (`DOC-ARC-04`) is consistent with this separation.

## Not implemented

Any dependency on META, and any consumer relationship with Laurentia. Agent Factory
executes, but nothing outside it currently asks it to.
"""),
 ("LAURENTIA", "Laurentia", "Specify the cultural-industry operator as audited.", ARC, "IMPLEMENTED", """
Layer 3. Purpose: cultural-industry operator — conversations, workflows, reports,
artefacts, sessions, jobs.

## Implemented subsystems

Gateway with SSE token streaming · Brain interface and persona · local orchestrator
with circuit breaker and signals · cookieless HMAC-SHA256 ghost persistence ·
AES-256-GCM encryption at rest · MongoDB TTL sliding-window rate limiting without
Redis · RGPD D+90 purge of the identity mapping · omnichannel echo pipeline
(Instagram, LinkedIn, X) · signed PDF export with QR · file parsing · Stripe billing ·
multi-tenant instance factory and API keys · bridges to Kiltikonet, LabelOS, FREKCORE.

## Distinctive properties

Laurentia is the only audited system with encryption at rest, bounded retention and a
paying commercial surface. Its privacy engineering is the estate's strongest.

## Rule violations recorded

It owns a persona-level doctrine (`C-002`), hardcodes a single provider with no
fallback (`C-004`, `G-011`), and its README describes an open-core split that has not
been performed (`C-003`).

## Not implemented

Any consumption of Agent Factory or META. Laurentia is a complete product that is not
yet a layer.
"""),
 ("RUNTIME", "Runtime", "Specify runtime state and degradation behaviour.", MET, "IMPLEMENTED", """
## Implemented

META CVLN computes runtime mode automatically over seven signals — `total_pings`,
`up_pings`, `error_rate`, `avg_ms`, `p95_ms`, `active_incidents`, `window` — producing
`normal`, `degraded` or `critical` with hysteresis to prevent flapping, plus an
explicit administrative override. Agent Factory independently implements autonomy
modes and execution cycles.

## Degradation policy

Mode is derived, not declared. A policy document accompanies the computed mode, so a
reader can see why the system considers itself degraded. Hysteresis is the detail that
makes the signal trustworthy in operation.

## Gap

Runtime mode is not propagated. Agent Factory and Laurentia do not observe META's
mode, and META does not observe theirs. Estate-wide degradation is therefore not a
controllable state.
"""),
 ("EVENT-BUS", "Event Bus", "Specify eventing across the estate.", FAC, "PARTIAL", """
Three independent buses exist (`C-007`).

| Bus | Guarantees | Trust |
|---|---|---|
| Agent Factory `event_bus.py` | Topic namespace, dead letter queue, spool replay | unsigned |
| Laurentia `orchestrator/event_bus.py` | Circuit breaker, signals | unsigned |
| META `/events/emit` | Ed25519 signature over canonical payload, quarantine on tamper | signed |

## Topic namespace (Agent Factory, implemented)

`agent.` · `factory.` · `monitoring.` · `memory.` · `identity.` · `daily.` ·
`system.` — enforced by prefix validation.

## Target envelope

`META/backend/contracts.py::Event`, signed, with a propagated trace identifier. The
contract already exists and has no consumers (`G-017`); adoption is the whole task.
"""),
 ("MODEL-ROUTER", "Model Router", "Specify provider selection and fallback.", FAC, "IMPLEMENTED", """
## Implemented — `FACTORY/backend/provider_layer.py`

| Provider | Model | Rank |
|---|---|---|
| anthropic | claude-sonnet-4-6 | 1 |
| openai | gpt-5.4 | 2 |
| gemini | — | 3 |
| sovereign | cvln-internal-deterministic | 99 (terminal) |

Strategies: `quality`, `cost`, `sovereign_only`. Every call is journalled. The
sovereign provider is a deterministic non-model fallback that cannot fail, which makes
total routing failure structurally impossible.

## Governing rule

`ADR-002`, restated in the module docstring: no direct provider call may occur outside
this layer. Doctrine article `DOC-ARC-04` codifies it.

## Findings

1. The only implemented router sits in Layer 2, not in the Brain (`C-006`).
2. Laurentia bypasses it entirely and has no fallback (`C-004`, `G-011`).
3. `sovereign` here means "deterministic terminal fallback", not "sovereign trained
   model" (`C-008`).
""", ),
 ("MEMORY", "Memory", "Specify memory as audited.", BRN, "PARTIAL", """
Three unrelated stores, no shared schema, no cross-system retrieval.

| Store | Owner | Properties |
|---|---|---|
| Layered memory | Agent Factory | `/memory`, `/memory-layers/summary`, human validation of entries |
| `laurentia_memory` | Laurentia | per-tenant, AES-256-GCM encrypted |
| Evidence and event history | META | signed events, notarisations, `doctrine_history` |

## Notable property

Agent Factory requires human validation of memory entries
(`/memory/entries/{id}/validate`). Memory poisoning is therefore gated rather than
assumed away — a defensible design that the target should preserve.

## Not implemented

Any graph structure, shared identifier space, or semantic retrieval across systems. A
"CVLN Memory Graph" is `PROPOSED` — see
[`../specifications/MEMORY-GRAPH.md`](../specifications/MEMORY-GRAPH.md).
"""),
 ("OBSERVABILITY", "Observability", "Specify what can currently be observed.", MET, "PARTIAL", """
## Implemented

META: registry pings with history, runtime signals, timeline, evidence store, public
audit surface. Agent Factory: append-only activity journal, gate journal, per-call
provider journalling, dead letter queue. Laurentia: activity log, circuit-breaker
signals.

## Not implemented

Distributed tracing, correlated identifiers, or any estate-wide view. A cross-system
incident cannot currently be reconstructed (`G-013`). META documents this gap itself.

## Minimum target

One trace identifier, generated at the entry edge and propagated in the shared event
envelope. This requires the envelope decision (`G-003`) and nothing else.
"""),
 ("SECURITY", "Security", "Specify the security posture as audited.", ARC, "PARTIAL", """
## Implemented controls

| Control | Location | Note |
|---|---|---|
| Ed25519 signed events with quarantine | META | estate's only tamper-evident path |
| Notarisation with public verification | META | externally checkable |
| JWT + bcrypt + RBAC | META | 6 roles |
| Gate levels and critical-action escalation | Agent Factory | denial journalled |
| Append-only journals | Agent Factory | non-repudiation |
| AES-256-GCM at rest | Laurentia | only system with it |
| HMAC-SHA256 cookieless identity | Laurentia | irreversible 64-hex device id |
| Distributed rate limiting via MongoDB TTL | Laurentia | no Redis dependency |
| RGPD D+90 purge | Laurentia | bounded retention |
| Anti-jailbreak persona rules | Laurentia | publicly readable — see `C-003` |

## Weaknesses recorded

`G-005` notary private key stored unencrypted at rest · `G-006` no encryption at rest
outside Laurentia · `G-008` no shared identity · `G-019` no strict tenant isolation in
META · `G-020` red-team scenarios named but unexecuted · `C-003` sovereign persona
rules published.

## Assessment

Individual controls are above average for the estate's maturity. The weakness is
compositional: strong controls in one system do not protect the others, and the single
unencrypted notary key can invalidate the whole trust chain.
"""),
]:
    simple(f"{A}/{p}.md", t, pu, own, st, "IMPLEMENTATION", body, rfc="`RFC-0003`, `RFC-0005`")
print("architecture written")
