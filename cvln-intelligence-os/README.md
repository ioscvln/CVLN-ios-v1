---
title: CVLN-INTELLIGENCE-OS
purpose: Root index of the CVLN Intelligence OS architecture specification and forensic audit.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: All CVLN intelligence repositories
version: OS v1.0 — TITAN FOUNDATION
status: IMPLEMENTED
attribution: SPECIFICATION
---

# CVLN-INTELLIGENCE-OS

**The sovereign architecture specification of the CVLN Intelligence Operating System.**

Version: `OS v1.0 — TITAN FOUNDATION`
License: Documentation proprietary to CVLN Group. Open-core compatible architecture documentation.

---

## What this repository is

This repository is not an application, a backend, a frontend, or a model. It is the
**technical constitution and architecture specification** of the CVLN intelligence
ecosystem, produced by a forensic audit of the repositories that actually exist.

It contains architecture, protocols, RFCs, contracts, diagrams, governance and
intelligence specifications. It contains no business logic, no product UI and no
deployment code.

## What this repository is *not*

It is not a wish list. Version 1.0 was produced under a strict evidentiary rule:

> Prefer 50 accurate lines over 300 speculative lines.

Every significant statement is bound to one of four **attribution levels** and every
component carries exactly one **implementation status**. Nothing invented in this
repository is presented as an existing CVLN capability.

### Attribution levels

| Level | Meaning |
|---|---|
| `CONCEPT` | Vocabulary and intent. No specification or code implied. |
| `SPECIFICATION` | Formally described here or in an audited repository. |
| `IMPLEMENTATION` | Executable code exists in an audited repository. |
| `DEPLOYED RUNTIME` | Observed running. **v1.0 asserts this for no component** — no audited runtime was probed. |

### Implementation status taxonomy

| Status | Meaning |
|---|---|
| `IMPLEMENTED` | Clearly implemented in executable code. |
| `PARTIAL` | Partially implemented but incomplete. |
| `DEFINED` | Architecturally or schema-defined, not demonstrably implemented. |
| `REFERENCED` | Referenced by code or documentation; implementation absent from the audited repository. |
| `PRIVATE / NOT VISIBLE` | Explicitly referenced as private, external or sovereign. |
| `PROPOSED` | A future recommendation. Never presented as existing. |
| `UNKNOWN` | Insufficient evidence. |

---

## Audited repositories

Audit scope was limited to three public repositories, at the commits reachable on
2026-08-20.

| Repository | Branch | Role in the canonical model |
|---|---|---|
| [`metacvln-spec/MetaCVLN`](https://github.com/metacvln-spec/MetaCVLN) | `main` | META CVLN — operating system / governance layer |
| [`frekcore/CVLNAgentfactory`](https://github.com/frekcore/CVLNAgentfactory) | `CVLN-AGENT-FACTORY` | CVLN AGENT FACTORY — nervous system / agent runtime |
| [`cultureconnectorg/Laurent.ia`](https://github.com/cultureconnectorg/Laurent.ia) | `public` | LAURENTIA — cultural-industry operator |

FREKCORE was excluded by instruction. Repositories referenced but not audited are
marked `PRIVATE / NOT ACCESSIBLE` in [`audit/DEPENDENCY-MAP.md`](audit/DEPENDENCY-MAP.md).

---

## Canonical vocabulary

These terms are canonical and must not be renamed.

- **META CVLN** — CVLN operating system / governance layer.
- **CVLN AGENT FACTORY** — CVLN nervous system / agent factory / agent runtime.
- **CVL BRAIN** — sovereign CVLN intelligence.
- **LAURENTIA** — cultural-industry operator / agent.

The repositories, not this vocabulary, are the source of truth for what is
*implemented*. Where they contradict the conceptual model, the contradiction is
recorded rather than resolved — see [`audit/CONTRADICTIONS.md`](audit/CONTRADICTIONS.md).

---

## Reading order

The document set is sequenced as evidence → reconstruction → model → specification
→ gaps → proposals. Read it in that order.

1. **Phase 0 — Forensic audit.** [`audit/REPOSITORY-AUDIT.md`](audit/REPOSITORY-AUDIT.md),
   [`audit/COMPONENT-MATRIX.md`](audit/COMPONENT-MATRIX.md),
   [`audit/IMPLEMENTATION-STATUS.md`](audit/IMPLEMENTATION-STATUS.md),
   [`audit/ARCHITECTURE-EVIDENCE.md`](audit/ARCHITECTURE-EVIDENCE.md),
   [`audit/DEPENDENCY-MAP.md`](audit/DEPENDENCY-MAP.md),
   [`audit/CROSS-REPO-INTEGRATION.md`](audit/CROSS-REPO-INTEGRATION.md),
   [`audit/CONTRADICTIONS.md`](audit/CONTRADICTIONS.md),
   [`audit/OPEN-QUESTIONS.md`](audit/OPEN-QUESTIONS.md)
2. **Phase 1 — Reconstruction.** [`audit/CURRENT-STATE-ARCHITECTURE.md`](audit/CURRENT-STATE-ARCHITECTURE.md)
3. **Phase 2 — Responsibility map.** [`audit/RESPONSIBILITY-MATRIX.md`](audit/RESPONSIBILITY-MATRIX.md)
4. **Phase 3 — Target.** [`audit/TARGET-ARCHITECTURE.md`](audit/TARGET-ARCHITECTURE.md)
5. **Phase 4 — Gaps.** [`audit/GAP-ANALYSIS.md`](audit/GAP-ANALYSIS.md), [`audit/FOUNDER-DECISIONS.md`](audit/FOUNDER-DECISIONS.md)
6. **Phase 5 — Specification.** `constitution/`, `architecture/`, `protocols/`, `api-contracts/`, `specifications/`, `rfc/`, `diagrams/`

---

## Headline audit findings

1. **The three repositories are three independent systems, not four layers of one
   system.** No audited repository imports another. The only realised runtime edge is
   HTTP: META CVLN calls adapters aimed at other systems. See
   [`audit/CROSS-REPO-INTEGRATION.md`](audit/CROSS-REPO-INTEGRATION.md).
2. **CVLN Agent Factory is the largest implementation** — approximately 143 routes
   across 30 router modules, including an Agent Definition Language with two schema
   generations, a gate system, an event bus and a provider-fallback model router.
3. **ADL exists. ISA and MCL do not.** ADL is `IMPLEMENTED`. ISA and MCL were not
   found in any audited repository and are therefore recorded as `PROPOSED`, in
   quarantined sections. See [`protocols/README.md`](protocols/README.md).
4. **The CVL Brain question is not settled by the public evidence.** What is
   verifiable is an interface plus persona and knowledge layers, calling third-party
   models through `emergentintegrations`. Whether a sovereign trained model exists is
   **NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES**. See
   [`architecture/CVLN-BRAIN.md`](architecture/CVLN-BRAIN.md).
5. **Doctrine has three owners in code**, contradicting the rule that only the Brain
   owns doctrine. See [`audit/CONTRADICTIONS.md`](audit/CONTRADICTIONS.md) C-002.
6. **The canonical dependency direction is not implemented.** It is a target, not a
   description. See [`audit/TARGET-ARCHITECTURE.md`](audit/TARGET-ARCHITECTURE.md).

---

## Governing rule

> **DO NOT INVENT CVLN. RECONSTRUCT IT.**
> Then formalise it. Then identify what is missing. Then propose improvements.

## Future RFC references

- `RFC-0001` Constitution ratification
- `RFC-0002` CVL Brain boundary and sovereignty claim
- `RFC-0003` Agent runtime consolidation
- `RFC-0004` Laurentia as a Brain consumer
- `RFC-0005` Model Router ownership
- `RFC-0006` Multi-agent orchestration
- `RFC-0007` ISA adoption (`PROPOSED`)
- `RFC-0008` MCL adoption (`PROPOSED`)
