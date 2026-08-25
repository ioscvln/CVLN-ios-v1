---
title: Open Questions
purpose: Questions the audited evidence cannot answer.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Open Questions

Each question is unanswerable from the audited public repositories. None is answered
speculatively here.

| ID | Question | Why unanswerable | Who can answer |
|---|---|---|---|
| Q-001 | Does a sovereign CVL Brain model exist — weights, adapters, datasets, or fine-tuning infrastructure? | No such artefact, config or training script appears in any audited tree | Founder / CVLN Group |
| Q-002 | Is Claude the primary model or a fallback for CVL Brain? | Laurentia hardcodes one Anthropic model with no fallback; Agent Factory ranks Anthropic first among four with a sovereign terminal fallback. The two repositories imply different answers | Founder |
| Q-003 | Which of the three constitutions is authoritative — META's, Agent Factory's, or the conceptual one? | All three exist; none references the others | Founder |
| Q-004 | Are the twelve registry entries live services or aspirational placeholders? | `registry_data.py` is static; discovery returned DEGRADED for all | Operations |
| Q-005 | Is `sovereign-brain/` an existing private repository or a planned one? | Referenced only by README prose | Founder |
| Q-006 | Which ADL generation is authoritative, v1 or v2? | Both are served; no deprecation marker exists | Agent Factory owner |
| Q-007 | Is any audited system currently deployed, and at which commit? | Static audit only; no runtime probed | Operations |
| Q-008 | Do the quoted test results (64 in Laurentia, 17 in META) pass at the audited commits? | Reports are committed artefacts, not re-executed here | CI |
| Q-009 | Was the canonical layering ever an implementation plan, or always a conceptual map? | No migration document, ADR or issue in the audited trees proposes it | Founder |
| Q-010 | Is `frek_id` a cross-estate identity or a Laurentia-local identifier? | Appears only in Laurentia; META has no corresponding notion | Founder |

## Standing rule

Q-001 and Q-002 must be answered before any document in this repository makes a
sovereignty claim about the Brain. Until then the required formulation is:
**NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.**

## Future RFC references

`RFC-0002`.
