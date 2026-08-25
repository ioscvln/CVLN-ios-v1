---
title: Model Router
purpose: Specify provider selection and fallback.
ownership: CVLN AGENT FACTORY — Runtime Authority
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Model Router

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


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0003`, `RFC-0005`
