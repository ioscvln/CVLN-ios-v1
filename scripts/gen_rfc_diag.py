import sys
sys.path.insert(0, "/app/scripts")
from gen_audit import w, PROPOSED_BANNER, ARC, MET, BRN, FAC
from gen_constitution import simple

def rfc(num, title, status, context, problem, proposal, alts, sec, mig, compat):
    body = f"""
| Field | Value |
|---|---|
| RFC | {num} |
| Status | **{status}** |
| Author | Office of the Principal Systems Architect |
| Supersedes | — |

## Context

{context}

## Problem

{problem}

## Proposal

{proposal}

## Alternatives considered

{alts}

## Security impact

{sec}

## Migration

{mig}

## Compatibility

{compat}

## Status

**{status}.** Ratification requires a founder decision — see
[`../audit/FOUNDER-DECISIONS.md`](../audit/FOUNDER-DECISIONS.md).
"""
    simple(f"rfc/{num}-{title.upper().replace(' ','-')}.md", f"{num} — {title}",
           f"RFC: {title}.", ARC, "PROPOSED", "SPECIFICATION", body, rfc="this document")

simple("rfc/RFC-TEMPLATE.md", "RFC Template", "Canonical template for every CVLN RFC.", ARC, "IMPLEMENTED", "SPECIFICATION", """
Every CVLN RFC contains exactly these sections, in this order.

```markdown
---
title: RFC-NNNN — <Title>
version: 1.0
status: DRAFT | PROPOSED | ACCEPTED | REJECTED | SUPERSEDED
attribution: SPECIFICATION
---

# RFC-NNNN — <Title>

| Field | Value |
|---|---|
| RFC | RFC-NNNN |
| Status | DRAFT |
| Author | |
| Supersedes | |

## Context
## Problem
## Proposal
## Alternatives considered
## Security impact
## Migration
## Compatibility
## Status
```

## Rules

1. An RFC states evidence before proposal. Claims cite a repository path.
2. An RFC that changes a component's status must say which status, from what, to what.
3. `Alternatives considered` may not be empty. "Do nothing" is always an alternative.
4. An RFC is not ratified by being written.
""", rfc="`RFC-0001`")

rfc("RFC-0001", "Constitution", "PROPOSED",
 "The estate has three constitutional artefacts: the conceptual model, META's governance plane, and Agent Factory's constitution and amendment service. None references the others.",
 "There is no ratified constitution. Rules are observed inconsistently and no document is authoritative, so no rule can be enforced across repository boundaries.",
 "Ratify `constitution/CVLN-CONSTITUTION-v1.md` as authoritative, with amendment via Agent Factory's implemented `/amendments/{id}/sign` mechanism and ratification recorded as a META decision of record.",
 "(a) Do nothing — divergence continues. (b) Adopt META's governance plane as the constitution — rejected: it implements decisions, not rules. (c) Adopt Agent Factory's constitution service — rejected: Layer 2 cannot bind Layer 0.",
 "Positive. A ratified constitution makes the provider-neutrality and human-approval rules enforceable rather than advisory.",
 "No code change. Record ratification as a decision; publish the constitution version in every repository README.",
 "Backwards compatible. No existing behaviour changes.")

rfc("RFC-0002", "Brain", "PROPOSED",
 "CVL Brain exists as a provider wrapper in Laurentia, a route in META and a statistics endpoint in Agent Factory. Doctrine is implemented in all three.",
 "Because there is no addressable Brain, no component can own doctrine on the Brain's behalf. Sovereignty claims about the Brain are also unverifiable from public evidence (`Q-001`, `Q-002`).",
 "Define the Brain boundary and extract one Brain service per `api-contracts/BRAIN-API.md`, owning persona, doctrine, memory, learning, reasoning, routing and emergency behaviour. Until ratified, every document states: NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.",
 "(a) Do nothing — three doctrine stores continue diverging. (b) META owns doctrine and the Brain is reduced to reasoning. (c) Formalise triplication with a reconciliation protocol — highest long-term cost.",
 "Significant and positive. One doctrine of record removes the possibility of contradictory rules being enforced by different components.",
 "Extract behind the Brain API; migrate Laurentia's in-process wrapper to a client; freeze doctrine writes in Agent Factory and META during cutover.",
 "Breaking for Laurentia's internal call path. No external contract changes.")

rfc("RFC-0003", "Agent Runtime", "PROPOSED",
 "Agent Factory is the largest implementation in the estate — ADL, gates, event bus, lifecycle, router — and nothing depends on it.",
 "The nervous system has no consumers. Laurentia executes its own workflows; META actuates by HTTP adapter.",
 "Establish Agent Factory as the estate's capability execution runtime. Implement `GET /api/capabilities` first (`G-002`), then wire Laurentia to it for capability execution, then bind gate and registry authority to META.",
 "(a) Do nothing. (b) Move execution into Laurentia — rejected: discards the gate system and ADL. (c) Federated peers with contracts only — viable and cheaper; ranks second.",
 "Positive. Routing execution through gates makes every capability invocation authorised and journalled.",
 "Three steps in the order above. Step one is non-breaking and independently valuable.",
 "Additive. Existing Agent Factory routes are unchanged.")

rfc("RFC-0004", "Laurentia", "PROPOSED",
 "Laurentia is a complete standalone product with the estate's strongest privacy engineering and its only paying surface.",
 "It owns doctrine of voice, hardcodes one model provider without fallback, and consumes neither Brain nor runtime — so it is a product, not a layer.",
 "Reposition Laurentia as a Layer 3 consumer: read doctrine from the Brain, execute capabilities via Agent Factory, route models through the shared router, and advertise capabilities.",
 "(a) Do nothing — accept Laurentia as an independent product and drop the layering claim; a legitimate outcome. (b) Partial adoption: router and capabilities only, retaining local persona.",
 "Positive. It removes the single-provider failure mode (`G-011`) and brings the persona under governance.",
 "Adopt the shared router first — it is the only change that reduces risk immediately. Doctrine migration follows RFC-0002.",
 "Breaking for internal Laurentia modules. No change to the public gateway contract.")

rfc("RFC-0005", "Model Router", "PROPOSED",
 "The only implemented router is `FACTORY/backend/provider_layer.py`, with four providers, named strategies, per-call journalling and a guaranteed terminal sovereign fallback under `ADR-002`.",
 "The conceptual model places the router in the Brain (Layer 1), the implementation places it in the nervous system (Layer 2), and Laurentia bypasses it entirely — violating doctrine article `DOC-ARC-04`.",
 "Promote the existing provider layer to a shared, Brain-owned routing service without redesigning it, and require every model call in the estate to pass through it.",
 "(a) Leave routing in Agent Factory and require Laurentia to call it — lower cost, retains the layering contradiction. (b) Permit per-system routing and withdraw `DOC-ARC-04` — honest but forfeits fallback guarantees.",
 "Positive. One audited provider boundary, one journal of model calls, and a fallback that cannot fail.",
 "Expose the provider layer over HTTP; migrate Laurentia's `cvl_brain.py` to a client; keep the sovereign fallback terminal.",
 "Additive for Agent Footprint; breaking for Laurentia's internal path only.")

rfc("RFC-0006", "Multiagent", "PROPOSED",
 "Three event buses exist with three trust models; only META signs events. META's `contracts.py::Event` is defined and unconsumed.",
 "Multi-agent orchestration across systems is impossible: no shared envelope, no shared topic namespace, no correlated trace, no handshake.",
 "Adopt `contracts.py::Event` as the estate envelope with mandatory Ed25519 signing, the Agent Factory topic namespace, a propagated `trace_id`, and the capability handshake in `protocols/AGENT-PROTOCOL/HANDSHAKE.md`.",
 "(a) Do nothing. (b) Adopt the envelope without signing — cheaper, forfeits tamper evidence. (c) Introduce a message broker — premature before the envelope is agreed.",
 "Positive. Signed, correlated events make cross-system causality reconstructible and tampering detectable.",
 "Envelope and signing first (no founder decision needed), then trace propagation, then handshake.",
 "Breaking at the bus level for Agent Factory and Laurentia; META is already conformant.")

# ================= DIAGRAMS =================
D = [
 ("ECOSYSTEM", "Ecosystem", "IMPLEMENTED", """
Current state. Dotted edges are `UNVERIFIED` or unanswered.

```mermaid
graph LR
  META["META CVLN<br/>governance"] -->|adapter| LAUR["LAURENTIA"]
  META -.->|"capabilities · DEGRADED"| FACT["AGENT FACTORY"]
  META -.->|"capabilities · DEGRADED"| LAUR
  META -.->|"404"| WAL["Wallet"]
  LAUR --> PROV["Model providers"]
  FACT --> PROV
  META --> PROV
  LAUR --> KILT["Kiltikonet · LabelOS · FREKCORE"]
  FACT -.-> META
  LAUR -.-> FACT
```

The two dotted edges at the bottom do not exist. They are drawn to make their absence
legible.
"""),
 ("LAYERED-OS", "Layered OS", "PROPOSED", PROPOSED_BANNER + """

```mermaid
graph TB
  L4["Layer 4 · Applications"] --> L3["Layer 3 · LAURENTIA"]
  L3 --> L2["Layer 2 · CVLN AGENT FACTORY"]
  L3 --> L1["Layer 1 · CVL BRAIN"]
  L2 --> L1
  L1 --> L0["Layer 0 · META CVLN"]
  L2 --> L0
```

No edge above is implemented today.
"""),
 ("BRAIN-INTERNALS", "Brain Internals", "PARTIAL", """
Solid = implemented somewhere in the estate. Dashed = `PROPOSED`.

```mermaid
graph TB
  Q["Query surface<br/>3 separate entry points"] --> P["Persona Engine<br/>LAUR · IMPLEMENTED"]
  P --> R["Reasoning<br/>classifier only · PARTIAL"]
  R --> MR["Model Router<br/>FACTORY · IMPLEMENTED"]
  MR --> SOV["Sovereign fallback<br/>deterministic"]
  MR --> EXT["External providers"]
  R -.-> D["Doctrine Engine<br/>3 owners · CONTESTED"]
  R -.-> SM["Semantic Memory<br/>PROPOSED"]
  R -.-> IM["Institutional Memory<br/>PROPOSED"]
  R -.-> LE["Learning Engine<br/>META · PARTIAL"]
  R -.-> EM["Emergency Engine<br/>PROPOSED"]
```
"""),
 ("RUNTIME", "Runtime", "IMPLEMENTED", """
Agent Factory execution with gate authority.

```mermaid
graph TB
  REQ["Request"] --> GATE{"Gate check<br/>GATE_LEVELS"}
  GATE -->|denied| J["Journal · action_bloquee"] --> ESC["Single escalation queue"]
  GATE -->|permitted| LC["Lifecycle check<br/>7 stages"]
  LC --> COG["classify_message"]
  COG --> MR["provider_layer"]
  MR --> EV["event_bus · agent.*"]
  EV -->|failure| DLQ["Dead letter queue"] --> SPOOL["Replay spool"]
```
"""),
 ("MEMORY-GRAPH", "Memory Graph", "PROPOSED", PROPOSED_BANNER + """

```mermaid
graph LR
  E["Entity"] --> A["Agent · ADL"]
  A --> C["Capability"]
  C --> DEC["Decision"]
  DEC --> EVD["Evidence"]
  A --> M["Memory entry"]
  M --> V["Validation · human"]
  DOC["Doctrine article"] --> DEC
```

Today three unrelated stores exist and none of these edges is materialised.
"""),
 ("MODEL-ROUTER", "Model Router", "IMPLEMENTED", """
```mermaid
graph LR
  CALL["Cognition request"] --> S{"strategy"}
  S -->|quality| A1["anthropic"]
  S -->|cost| G1["gemini"]
  S -->|sovereign_only| SV["sovereign"]
  A1 -->|fail| O1["openai"]
  O1 -->|fail| G1
  G1 -->|fail| SV["sovereign<br/>cvln-internal-deterministic<br/>cannot fail"]
  A1 --> JR["Journal every call"]
  SV --> JR
```

Laurentia does not participate in this graph — gap `G-011`.
"""),
 ("EVENT-BUS", "Event Bus", "PARTIAL", """
```mermaid
graph TB
  subgraph F["AGENT FACTORY · unsigned"]
    FT["topic prefixes"] --> FD["DLQ"] --> FS["spool replay"]
  end
  subgraph L["LAURENTIA · unsigned"]
    LO["orchestrator"] --> LC["circuit breaker"]
  end
  subgraph M["META · signed"]
    ME["/events/emit"] --> MS["Ed25519"] --> MV["/events/verify"] --> MQ["quarantine on tamper"]
  end
  F -.->|"no shared envelope"| M
  L -.->|"no shared envelope"| M
```
"""),
 ("ORCHESTRATION", "Multi-agent Orchestration", "PROPOSED", PROPOSED_BANNER + """

```mermaid
sequenceDiagram
  participant O as Operator
  participant B as CVL BRAIN
  participant F as AGENT FACTORY
  participant A1 as AGT-014
  participant M as META
  O->>B: objective
  B->>B: REASON, PLAN
  B->>F: execute plan steps
  F->>F: gate check per step
  F->>A1: EXECUTE capability
  A1-->>F: result
  F->>M: signed REPORT with trace_id
  M-->>O: decision of record
```

No implemented path performs this sequence.
"""),
]
for p, t, st, body in D:
    simple(f"diagrams/{p}.md", t, "Mermaid architecture diagram bound to audit evidence.", ARC, st,
           "SPECIFICATION" if st == "PROPOSED" else "IMPLEMENTATION", body, rfc="`RFC-0006`")

# ================= ROOT =================
for p, t, body in [
 ("MANIFESTO", "Manifesto", """
## Specification is separate from implementation

CVLN's architecture is written down so that it can be argued with. A repository that
cannot be contradicted by evidence is marketing.

## Evidence precedes architecture

The sequence is fixed: evidence → reconstruction → model → specification → gaps →
proposals. The inverse sequence — assumption → architecture → asserted capability —
is prohibited.

## Four levels, never conflated

`CONCEPT`, `SPECIFICATION`, `IMPLEMENTATION`, `DEPLOYED RUNTIME`. A specification is
not a capability. A filename is not a subsystem. A README is not a runtime.

## Absence is reported

Where evidence is missing, the required statement is
**NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES** — not a plausible guess. The
audited estate already practises this: META's loop maps return
`DATA_NOT_AVAILABLE` rather than inventing a number. That standard is inherited here.

## Nothing invented is presented as existing

ISA and MCL are proposals introduced by this repository. They are quarantined and
labelled `PROPOSED`. Retroactively attributing new terminology to CVLN would corrupt
the record this repository exists to protect.

## Precision over volume

Fifty accurate lines outrank three hundred speculative ones.
"""),
 ("ROADMAP", "Roadmap", """
Sequenced by dependency, from [`audit/GAP-ANALYSIS.md`](audit/GAP-ANALYSIS.md).

## Now — no founder decision required

1. `G-002` Implement `GET /api/capabilities` in Agent Factory and Laurentia.
2. `G-005` Encrypt the notary private key at rest, then rotate.
3. `G-003` Adopt `contracts.py::Event` as the shared envelope, signing mandatory.
4. `G-007` Add an `ARCHITECTURE.md` to every repository.

## Next — blocked on founder decisions

5. `FD-002` Ratify or abandon the canonical dependency direction.
6. `FD-001` Settle doctrine ownership and the Brain boundary.
7. `FD-004` Settle model router ownership; remove Laurentia's single point of failure.
8. `FD-003` Execute or restate the open-core split.

## Later

9. `G-004` Extract the Brain service.
10. `G-001` Wire Laurentia to the agent runtime.
11. `G-013` Propagate a trace identifier estate-wide.
12. `G-010` Specify and implement the memory graph.

## Undecided

13. `FD-005` ISA and MCL adoption. Rejection is an acceptable outcome.
"""),
 ("CHANGELOG", "Changelog", """
## OS v1.0 — TITAN FOUNDATION — 2026-08-20

Initial release. Forensic audit of three public repositories, architecture
reconstruction, and the first formal specification set.

### Added
- `audit/` — repository audit, component matrix, implementation status, dependency
  map, architecture evidence, cross-repository integration, contradictions, open
  questions, current-state architecture, responsibility matrix, target architecture,
  gap analysis, founder decisions.
- `constitution/`, `architecture/`, `protocols/`, `api-contracts/`,
  `specifications/`, `rfc/`, `diagrams/`.
- `RFC-0001` to `RFC-0006`, all `PROPOSED`. RFC template.

### Findings of record
- 9 contradictions (`C-001`–`C-009`), 20 gaps (`G-001`–`G-020`), 10 open questions,
  5 founder decisions.
- ADL recorded as `IMPLEMENTED`. ISA and MCL recorded as `PROPOSED` — not found in any
  audited repository.
- CVL Brain sovereignty and training: **NOT VERIFIABLE FROM THE AUDITED PUBLIC
  REPOSITORIES**.

### Explicitly not asserted
- No component is claimed at `DEPLOYED RUNTIME`.
"""),
 ("CONTRIBUTING", "Contributing", """
## Evidence rules

1. Every claim about an existing capability cites a repository path.
2. A directory name is not evidence. A README is evidence of intent only.
3. Absence of evidence is recorded as `PROPOSED` or `UNKNOWN`, never inferred.
4. Where evidence is unobtainable, write **NOT VERIFIABLE FROM THE AUDITED PUBLIC
   REPOSITORIES**.

## Document rules

Every Markdown file carries front matter with `title`, `purpose`, `ownership`,
`scope`, `version`, `status`, `attribution`, and ends with future RFC references.
Status changes require an RFC. Canonical vocabulary may not be renamed.

## Language

Professional technical English. No marketing language. The words "revolutionary",
"world-changing", "AGI" and "superintelligence" are prohibited unless directly
supported by audited evidence.

## Documentation duty

Every CVLN repository maintains its own `ARCHITECTURE.md` derived from this
specification. The current inversion — the largest codebase carrying a placeholder
README — is gap `G-007`.
"""),
 ("VERSIONING", "Versioning", """
## Scheme

`OS vMAJOR.MINOR — CODENAME`. Current: `OS v1.0 — TITAN FOUNDATION`.

- **MAJOR** — a change to the layer model, the canonical vocabulary, or the status
  taxonomy.
- **MINOR** — new specifications, ratified RFCs, or status transitions.
- Documents carry an independent `version` in front matter.

## Independent version lines

| Artefact | Line | Current |
|---|---|---|
| This specification | `OS vX.Y` | 1.0 |
| Inter-system contracts | semver | 1.0 stable (`contracts.py`) |
| ADL | semver | v1 implemented, v2 defined — authority undeclared (`G-016`) |
| Agent definitions | semver, enforced | per agent |

## Rules

1. A status transition is a version change and cites its ratifying RFC.
2. Contracts are versioned independently; consumers negotiate the lowest common
   version.
3. Two coexisting generations require a declared authoritative version and a
   converter.
""")]:
    simple(f"{p}.md", t, f"{t} of the CVLN Intelligence OS specification.", ARC,
           "IMPLEMENTED", "SPECIFICATION", body, rfc="`RFC-0001`")
print("rfc + diagrams + root written")
