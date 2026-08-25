import sys
sys.path.insert(0, "/app/scripts")
from gen_audit import w, PROPOSED_BANNER, MET, BRN, FAC, ARC
from gen_constitution import simple

# ================= PROTOCOLS =================
simple("protocols/README.md", "Protocols — Status Notice", "Separate protocols that exist from protocols that are proposed.", ARC, "PARTIAL", "IMPLEMENTATION", """
The initial brief named three protocols: ISA, ADL and MCL. The audit tested each
against the repositories. They are **not** equivalent in standing.

| Protocol | Found in repositories | Status | Location |
|---|---|---|---|
| **ADL** — Agent Definition Language | Yes — `FACTORY/backend/adl_schema.py` + `schemas/adl_v2_schema.json` | IMPLEMENTED (v1), DEFINED (v2) | [`ADL/`](ADL/ADL-v1.md) |
| **ISA** — Intelligence System Architecture instruction set | No | PROPOSED | [`ISA/`](ISA/ISA-SPEC.md) |
| **MCL** — MetaCVLN Language | No | PROPOSED | [`MCL/`](MCL/MCL-SPEC.md) |
| **Agent Protocol** — handshake, messages, memory, tools, reports, errors | Partially — event bus and contracts exist; no handshake | Mixed | [`AGENT-PROTOCOL/`](AGENT-PROTOCOL/HANDSHAKE.md) |

ISA and MCL are quarantined proposals introduced by this specification. Neither is
CVLN technology, and neither may be cited as one until `RFC-0007` / `RFC-0008` are
ratified. Presenting them otherwise would retroactively attribute invented
terminology to CVLN — the exact failure this repository exists to prevent.
""", rfc="`RFC-0007`, `RFC-0008`")

# ---- ADL (real) ----
simple("protocols/ADL/ADL-v1.md", "ADL v1 — Agent Definition Language", "Specify the implemented CVLN agent definition language.", FAC, "IMPLEMENTED", "IMPLEMENTATION", """
ADL is the one protocol in the initial brief that demonstrably exists. Source of
truth: `FACTORY/backend/adl_schema.py`, with a second generation at
`FACTORY/backend/schemas/adl_v2_schema.json`.

## Implemented grammar

| Rule | Regex / enum | Evidence |
|---|---|---|
| Agent identifier | `^AGT-\\d{3}$` | `AGENT_ID_RE` |
| Version | `^\\d+\\.\\d+\\.\\d+$` | `SEMVER_RE` |
| Lifecycle | Draft, Prototype, Alpha, Beta, Production, Maintenance, Archive | `LifecycleStatus` |
| Transitions | next stage, or Archive | `allowed_transitions()` |
| Brain memory binding | `scope: session | persistent`, `owner` | `BrainMemory` |
| Brain events binding | `subscribe: []`, `publish: []` | `BrainEvents` |

YAML is a first-class input format via `parse_adl_yaml()`.

## Example agent definition (v1 shape)

```yaml
agent_id: AGT-014
name: Weekly Drop Reporter
version: 1.2.0
lifecycle_status: Production
autonomy_level: 2
risk_level: medium
brain:
  memory:
    scope: persistent
    owner: AGT-014
  events:
    subscribe: ["daily.closing.completed"]
    publish: ["agent.report.ready"]
capabilities:
  - id: report.weekly_drop
    gate_level: 2
```

## Example v2 envelope

```yaml
adl_version: "2.0"
schema_uri: "https://cvln.spec/adl/v2.json"
agent:
  id: AGT-014
  name: Weekly Drop Reporter
brain:
  memory: { scope: persistent }
capabilities:
  - id: report.weekly_drop
```

## Known issue

v1 and v2 coexist with no declared authoritative version and no converter
(`G-016`). Fields not present in either schema are `PROPOSED`.
""", rfc="`RFC-0003`")

for p, t, body in [
 ("AGENT-SCHEMA", "ADL Agent Schema", """
Field-level schema of a CVLN agent, as validated in code.

| Field | Type | Constraint | Status |
|---|---|---|---|
| `agent_id` | string | `^AGT-\\d{3}$` | IMPLEMENTED |
| `version` | string | semver | IMPLEMENTED |
| `lifecycle_status` | enum | 7 stages | IMPLEMENTED |
| `brain.memory.scope` | enum | session / persistent | IMPLEMENTED |
| `brain.memory.owner` | string | — | IMPLEMENTED |
| `brain.events.subscribe` | list | topic prefixes | IMPLEMENTED |
| `brain.events.publish` | list | topic prefixes | IMPLEMENTED |
| `capabilities` | list | ADL v2 top-level property | DEFINED |
| `autonomy_level` | integer | route exists at `/agents/{id}/autonomy` | PARTIAL |
| `risk_level` | enum | referenced by gates | PARTIAL |
| `permissions` | list | not observed in schema | PROPOSED |
| `tools` | list | not observed in schema | PROPOSED |

Rows marked `PROPOSED` are fields the brief expects but the schema does not contain.
"""),
 ("AGENT-LIFECYCLE", "ADL Agent Lifecycle", """
Seven ordered stages, enforced by `allowed_transitions()`.

```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Prototype
  Prototype --> Alpha
  Alpha --> Beta
  Beta --> Production
  Production --> Maintenance
  Maintenance --> Archive
  Draft --> Archive
  Prototype --> Archive
  Alpha --> Archive
  Beta --> Archive
  Production --> Archive
  Archive --> [*]
```

## Rules (implemented)

1. Advance by exactly one stage, or archive.
2. Archive is terminal — no transition leaves it.
3. Skipping stages is rejected by the transition function, not by convention.

## Runtime surfaces

`/agents/{id}/lifecycle` · `/…/state` · `/…/versions` · `/…/diff` ·
`/…/checkpoint` · `/…/checkpoints` · `/…/export` · `/…/wake`. Checkpoint and diff
make lifecycle changes reversible and reviewable.
"""),
 ("CAPABILITY-CONTRACT", "ADL Capability Contract", """
An agent's capabilities are declared in its definition, not discovered at runtime.

## Implemented

ADL v2 carries `capabilities` as a top-level schema property. Agent Factory executes
declared capabilities through its gate system, so declaration and authorisation are
coupled by construction.

## Defined but unconsumed

`META/backend/contracts.py::Capability` is the estate's intended wire format for
capability advertisement. No component consumes it (`G-017`), and no component serves
`/api/capabilities` (`G-002`).

## Required contract shape

```json
{
  "id": "report.weekly_drop",
  "version": "1.0.0",
  "owner": "AGT-014",
  "inputs": { "period": "string" },
  "outputs": { "artifact_url": "string" },
  "permissions": ["report.read"],
  "gate_level": 2,
  "risk": "medium"
}
```

Fields beyond `contracts.py::Capability` are `PROPOSED`.
"""),
]:
    simple(f"protocols/ADL/{p}.md", t, "Specify part of the implemented ADL protocol.", FAC, "IMPLEMENTED", "IMPLEMENTATION", body, rfc="`RFC-0003`")

# ---- ISA (proposed) ----
simple("protocols/ISA/ISA-SPEC.md", "ISA — Intelligence System Architecture (PROPOSED)", "Propose a native execution cycle for CVLN agents.", ARC, "PROPOSED", "SPECIFICATION", PROPOSED_BANNER + """

## Why proposed and not documented

The audit searched all three repositories for instruction-set semantics. None exists.
The closest implemented artefacts are Agent Factory's autonomy cycles
(`/cycle`, `/cycles`) and META's `ExecutionStep` / `ExecutionPlan` contracts. Neither
defines instructions with ownership, permissions and error handling.

## Proposed instruction set

Eight instructions: `REASON`, `PLAN`, `MEMORY_READ`, `MEMORY_WRITE`, `EXECUTE`,
`OBSERVE`, `LEARN`, `REPORT`. Each is specified in
[`INSTRUCTION-SET.md`](INSTRUCTION-SET.md).

## Proposed invariants

1. Every instruction is journalled with actor, agent, inputs digest and outcome.
2. `EXECUTE` requires a prior gate decision — reusing Agent Factory's implemented
   gate system rather than inventing an authority model.
3. `MEMORY_WRITE` requires validation, reusing the implemented human-validation
   pattern at `/memory/entries/{id}/validate`.
4. `LEARN` may only produce proposals. It may never mutate doctrine — this preserves
   META's implemented and strongest governance property.
5. Instructions are deterministic in their effects on state, even when `REASON` is
   non-deterministic in output.

## Adoption cost

Moderate. Invariants 2, 3 and 4 map onto subsystems that already exist. Adoption is
mainly a matter of naming and journalling what Agent Factory already does.

## Decision

`RFC-0007`, gated by founder decision `FD-005`. Rejection is a legitimate outcome:
nothing in the estate depends on ISA.
""", rfc="`RFC-0007`")

simple("protocols/ISA/INSTRUCTION-SET.md", "ISA Instruction Set (PROPOSED)", "Specify each proposed instruction.", ARC, "PROPOSED", "SPECIFICATION", PROPOSED_BANNER + """

Each instruction: description, inputs, outputs, ownership, permissions, lifecycle,
error handling.

| Instruction | Description | Inputs | Outputs | Owner | Permission | Lifecycle | Error handling |
|---|---|---|---|---|---|---|---|
| `REASON` | Produce an assessment over context | context, objective | assessment, confidence | CVL BRAIN | `brain.reason` | stateless | on provider failure, terminal sovereign fallback; never silent |
| `PLAN` | Decompose an objective into steps | objective, capabilities | ordered plan | CVL BRAIN | `brain.plan` | stateless | empty plan is an error, not a no-op |
| `MEMORY_READ` | Retrieve scoped memory | scope, query | entries, provenance | CVL BRAIN | `memory.read` | read-only | missing scope is a hard error |
| `MEMORY_WRITE` | Persist memory | scope, entry, evidence | entry id, validation state | CVL BRAIN | `memory.write` | pending until validated | rejected write is journalled, never dropped |
| `EXECUTE` | Invoke a declared capability | capability id, arguments | result, receipt | AGENT FACTORY | `capability.execute` + gate decision | gated | gate denial journalled as `action_bloquee`; escalates to the single queue |
| `OBSERVE` | Record an outcome signal | subject, signal | observation | AGENT FACTORY | `runtime.observe` | append-only | loss of an observation degrades runtime mode |
| `LEARN` | Convert observations into proposals | observations, threshold | proposal | CVL BRAIN | `learning.propose` | proposal only | may never mutate doctrine directly |
| `REPORT` | Emit a signed account of a cycle | cycle id | signed event, artefact | META CVLN | `report.emit` | terminal | unsigned report is invalid |

## Ownership rationale

Cognition instructions belong to the Brain, execution and observation to Agent
Factory, reporting to META. This mirrors the target layering rather than current
implementation, which is why the whole set is `PROPOSED`.
""", rfc="`RFC-0007`")

for p, t, body in [
 ("EXECUTION-CYCLE", "ISA Execution Cycle (PROPOSED)", """
```mermaid
graph LR
  A["MEMORY_READ"] --> B["REASON"]
  B --> C["PLAN"]
  C --> D{"gate decision"}
  D -->|"denied"| J["journal · escalate"]
  D -->|"permitted"| E["EXECUTE"]
  E --> F["OBSERVE"]
  F --> G["MEMORY_WRITE"]
  G --> H["LEARN — proposal only"]
  H --> I["REPORT — signed"]
  J --> I
```

## Cycle rules

1. A cycle is atomic for reporting: every cycle ends in `REPORT`, including a denied
   one. A denied cycle that is not reported is a governance failure.
2. `LEARN` output is a proposal, never a doctrine mutation.
3. A cycle carries one trace identifier across every instruction.
4. Cycles are resumable from the last successful `MEMORY_WRITE`.

Closest existing artefact: Agent Factory `/cycle` and `/cycles/{cycle_id}`, which
lack instruction-level semantics.
"""),
 ("INTERRUPTS", "ISA Interrupts (PROPOSED)", """
An interrupt suspends a cycle before its next instruction.

| Interrupt | Trigger | Effect | Existing analogue |
|---|---|---|---|
| `GATE_DENIED` | Gate refuses `EXECUTE` | Cycle ends, journalled, escalated | `gate_routes.py` `action_bloquee` — IMPLEMENTED |
| `CRITICAL_INTENT` | Intent classifier flags a critical action | Human confirmation required | `detect_critical_intent()` — IMPLEMENTED |
| `RUNTIME_CRITICAL` | Runtime mode enters `critical` | Non-essential cycles suspended | META `/runtime/state` — IMPLEMENTED |
| `PROVIDER_EXHAUSTED` | All providers fail | Terminal sovereign fallback | `provider_layer.py` — IMPLEMENTED |
| `CIRCUIT_OPEN` | Downstream circuit breaker opens | Cycle deferred | Laurentia `circuit_breaker.py` — IMPLEMENTED |
| `DOCTRINE_CONFLICT` | Plan conflicts with doctrine | Escalated to a decision | `/doctrine/check` — PARTIAL |

## Observation

Five of six proposed interrupts already have working implementations in the estate.
ISA's interrupt model is therefore mostly a naming exercise over proven behaviour,
which is the strongest argument in its favour.
"""),
]:
    simple(f"protocols/ISA/{p}.md", t, "Specify a proposed ISA facility.", ARC, "PROPOSED", "SPECIFICATION", PROPOSED_BANNER + "\n" + body, rfc="`RFC-0007`")

# ---- MCL (proposed) ----
simple("protocols/MCL/MCL-SPEC.md", "MCL — MetaCVLN Language (PROPOSED)", "Propose a declarative language for the CVLN operating system.", ARC, "PROPOSED", "SPECIFICATION", PROPOSED_BANNER + """

## Audit result

No grammar, parser, file extension, test or reference to a MetaCVLN Language was
found in any audited repository. MCL has the weakest standing of the three named
protocols: ADL exists, ISA has close analogues, MCL has neither.

## Motivation

Entities, capabilities, objectives, permissions and workflows are currently expressed
as Python — `registry_data.py`, `doctrine.py`, `GATE_LEVELS`, route handlers. They
cannot be reviewed, diffed or governed as declarations.

## Proposed scope

Entities · capabilities · objectives · permissions · workflows · policies ·
relationships. Grammar sketches: [`ENTITY-SYNTAX.md`](ENTITY-SYNTAX.md),
[`WORKFLOW-SYNTAX.md`](WORKFLOW-SYNTAX.md),
[`PERMISSION-SYNTAX.md`](PERMISSION-SYNTAX.md),
[`VALIDATION.md`](VALIDATION.md).

## Precondition

MCL must not be specified further until `FD-001` and `FD-002` settle what META owns.
A declarative language for contested ownership would encode the contradictions rather
than resolve them.

## Decision

`RFC-0008`, gated by `FD-005`. Priority: below ISA.
""", rfc="`RFC-0008`")

for p, t, body in [
 ("ENTITY-SYNTAX", "MCL Entity Syntax (PROPOSED)", """
```mcl
entity KORA {
  kind        product
  owner       cvln.group
  repository  "https://github.com/..."
  runtime     "https://kora.cvln"
  capabilities [ catalogue.read, catalogue.write ]
  relationships {
    consumes  LAURENTIA
    governed_by META_CVLN
  }
}
```

Maps to the implemented static register in `META/backend/registry_data.py`, adding
declared relationships that the current register lacks.
"""),
 ("WORKFLOW-SYNTAX", "MCL Workflow Syntax (PROPOSED)", """
```mcl
workflow weekly_drop_report {
  objective   "Publish the weekly drop report"
  trigger     schedule("weekly")
  gate        level(2)
  steps {
    execute report.weekly_drop by AGT-014
    observe  outcome
    report   signed
  }
  on_failure  escalate to decision
}
```

Compare `/api/cron/weekly-drop-report` and `/reports/weekly-drop`, which implement
this workflow imperatively today.
"""),
 ("PERMISSION-SYNTAX", "MCL Permission Syntax (PROPOSED)", """
```mcl
permission report.emit {
  roles      [ admin, ops_lead ]
  gate_level 2
  critical   false
}

permission doctrine.amend {
  roles      [ admin ]
  gate_level 4
  critical   true
  requires   human_approval + evidence
}
```

Maps to META's implemented RBAC roles and Agent Factory's `GATE_LEVELS` and
`CRITICAL_ACTIONS`, unifying two models that are currently unrelated.
"""),
 ("VALIDATION", "MCL Validation (PROPOSED)", """
Proposed validation rules for any MCL document.

| Rule | Failure mode |
|---|---|
| Every referenced entity is declared | dangling reference |
| Every capability referenced by a workflow is declared by some agent | unexecutable workflow |
| Every permission names at least one role and a gate level | unenforceable permission |
| Relationship direction is acyclic across layers | layering violation |
| Critical permissions require human approval | governance bypass |
| Version is semver | non-comparable revisions |

Validation must be a build-time gate, not a runtime warning; the estate's existing
ADL validation is the precedent to follow.
"""),
]:
    simple(f"protocols/MCL/{p}.md", t, "Sketch a proposed MCL facility.", ARC, "PROPOSED", "SPECIFICATION", PROPOSED_BANNER + "\n" + body, rfc="`RFC-0008`")

# ---- AGENT PROTOCOL ----
AP = [
 ("HANDSHAKE", "Agent Handshake", "PROPOSED", """
No handshake exists in any audited repository. The closest artefact is META's
capability probe, which currently receives no answer from any provider (`C-005`).

## Proposed handshake

1. Caller requests `GET /api/capabilities`.
2. Provider answers with `contracts.py::Capability` descriptors and an
   `adl_version`.
3. Caller verifies the provider identity — Agent Factory already implements service
   identities and rotation at `/identity/service/{agent_id}/rotate`.
4. Caller and provider agree the lowest common contract version.
5. The handshake result is emitted as a signed event.

Implementing step 2 alone resolves gap `G-002` and makes the existing prober useful.
"""),
 ("MESSAGE-FORMAT", "Agent Message Format", "DEFINED", """
`META/backend/contracts.py::Event` is the estate's defined envelope. It has no
consumers (`G-017`).

## Required envelope fields

`event_id` · `type` · `source` · `subject` · `occurred_at` · `payload` ·
`signature` · `key_id`.

## Rules

1. Signature is mandatory. META already quarantines tampered payloads on verify.
2. `type` uses the implemented Agent Factory namespace: `agent.`, `factory.`,
   `monitoring.`, `memory.`, `identity.`, `daily.`, `system.`.
3. A trace identifier is propagated unchanged across every hop (`G-013`).

Today three buses use three incompatible formats (`C-007`).
"""),
 ("MEMORY-PROTOCOL", "Agent Memory Protocol", "PARTIAL", """
## Implemented

Agent Factory: `/memory`, `/memory-layers/summary`, and human validation at
`/memory/entries/{entry_id}/validate`. Laurentia: encrypted per-tenant memory. ADL
binds an agent to a memory scope (`session` or `persistent`) and an owner.

## Rules derived from implementation

1. Every entry has an owning agent — ADL `BrainMemory.owner`.
2. Scope is declared, not inferred.
3. Entries are validated before they influence behaviour. Memory poisoning is gated
   rather than assumed away.

## Not implemented

Cross-system read, shared identifiers, provenance chains, or graph traversal
(`G-010`).
"""),
 ("TOOL-PROTOCOL", "Agent Tool Protocol", "PARTIAL", """
## Implemented

Tool invocation exists as capability execution in Agent Factory, gated by
`gate_routes.py`, and as bridges in Laurentia
(`kiltikonet_bridge.py`, `labelos_bridge.py`, `frekcore_bridge.py`).

## Rules

1. A tool call is a capability execution and requires a gate decision.
2. Tool failure is an `OBSERVE` result, never a silent retry — Laurentia's echo
   pipeline retries three times then skips and records the skip.
3. External tool credentials never leave the calling service.

## Not implemented

A declared `tools` field in ADL. Tools are bound in code, not in agent definitions.
"""),
 ("REPORT-PROTOCOL", "Agent Report Protocol", "PARTIAL", """
## Implemented

META: notarisations with verification and export, public verification surface,
weekly drop reports. Agent Factory: activity journal, daily closings, briefings.
Laurentia: signed PDF export with QR, reports and timelines.

## Rules

1. A report is signed. META's Ed25519 notarisation is the reference implementation.
2. A report is verifiable by a third party without privileged access —
   `/public/notarizations/{id}` implements this.
3. Absent data is reported as absent. META's loop maps return
   `DATA_NOT_AVAILABLE` rather than a fabricated value. This rule is binding on all
   future CVLN reporting.
"""),
 ("ERROR-PROTOCOL", "Agent Error Protocol", "PARTIAL", """
## Implemented behaviours

| Failure | Response | Location |
|---|---|---|
| Provider failure | Next provider, then terminal sovereign fallback | `provider_layer.py` |
| Event delivery failure | Dead letter queue, replayable from spool | `event_bus.py` |
| Downstream instability | Circuit breaker opens | Laurentia `circuit_breaker.py` |
| Gate denial | Journalled and escalated | `gate_routes.py` |
| Tampered event | Quarantined | META `/events/verify` |
| Model unavailable in Laurentia | `503`, no fallback | `social_admin.py` — `G-011` |
| Missing upstream endpoint | Upstream `404` surfaced, not masked | wallet adapter — `G-018` |

## Rules

1. Failures are journalled, never swallowed.
2. Every execution path terminates in a defined outcome; Agent Factory guarantees
   this via an infallible terminal provider.
3. Absence of data is reported as absence.

The estate's error handling is materially better than its integration; the single
exception is Laurentia's missing fallback.
"""),
]
for p, t, st, body in AP:
    simple(f"protocols/AGENT-PROTOCOL/{p}.md", t, "Specify an agent-protocol facility against repository evidence.", FAC, st,
           "SPECIFICATION" if st == "PROPOSED" else "IMPLEMENTATION",
           (PROPOSED_BANNER + "\n" if st == "PROPOSED" else "") + body, rfc="`RFC-0006`")
print("protocols written")
