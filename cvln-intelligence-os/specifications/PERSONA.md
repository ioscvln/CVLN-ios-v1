---
title: Persona
purpose: Specify a CVLN intelligence concern against repository evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: CVLN intelligence ecosystem
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Persona

## Implemented — `LAUR/backend/services/cvl_brain_knowledge.py`

Persona v1.2 with explicit non-disclosure and anti-jailbreak rules. The persona is
instructed never to name Anthropic, Claude, OpenAI, any underlying provider, or
`CVLN/CVL Brain`, and never to disclose internal instructions or environment key
names (`LAURENTIA_*`, `MONGO_URL`, `EMERGENT_LLM_KEY`). Exfiltration attempts receive
a refusal with business reorientation rather than a bare denial.

## Assessment

This is the most developed persona artefact in the estate and the only implemented
form of doctrine-of-voice. Two findings qualify it:

1. It is publicly readable despite being designated sovereign (`C-003`). Published
   anti-jailbreak rules are weaker rules.
2. It is Laurentia-local. No other CVLN surface inherits it.


## Relationships

See [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.

## Future RFC references

`RFC-0002`, `RFC-0006`
