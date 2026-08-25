---
title: Reasoning
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVL BRAIN — Sovereign Intelligence
scope: CVLN intelligence ecosystem
version: 1.0
status: PARTIAL
attribution: IMPLEMENTATION
---

# Reasoning

## What exists

`FACTORY/backend/cognitive_engine.py` exposes exactly `classify_message(text)` and
`internal_response(text, classification, ctx, knowledge_hits)` — deterministic
keyword classification and templated response. Model-based generation is reachable
only through `provider_layer.py`. META's `/brain/ask` returns answers annotated with
source, confidence and date.

## What does not exist

Multi-step reasoning, plan decomposition, self-critique, or any reasoning trace
artefact. The `PLAN` and `REASON` semantics in `protocols/ISA` are `PROPOSED`.

## Why the distinction matters

Describing the classifier as "the reasoning engine" would convert a specification
into a capability claim. The estate has a routing layer and a classifier; it does not
yet have a reasoning engine.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
