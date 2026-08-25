---
title: ISA Instruction Set (PROPOSED)
purpose: Specify each proposed instruction.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: PROPOSED
attribution: SPECIFICATION
---

# ISA Instruction Set (PROPOSED)

> **Status: `PROPOSED`.** This artefact was not found in any audited CVLN
> repository. It is a proposal introduced by this specification and must never be
> cited as an existing CVLN capability until its RFC is ratified.


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


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0007`
