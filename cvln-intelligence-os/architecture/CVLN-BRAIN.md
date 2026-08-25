---
title: CVL Brain
purpose: State precisely what is and is not verifiable about CVL Brain.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# CVL Brain

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


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002` (Brain boundary and sovereignty claim), `RFC-0005`
