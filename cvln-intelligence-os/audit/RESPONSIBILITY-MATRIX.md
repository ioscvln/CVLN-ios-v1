---
title: Responsibility Matrix
purpose: Record which component owns each responsibility today, without reassigning any.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Responsibility Matrix

This is a Phase 2 document: it documents reality. Responsibilities are **not** moved
here. Target ownership is proposed only in
[`TARGET-ARCHITECTURE.md`](TARGET-ARCHITECTURE.md).

`✔` owns it in code · `~` partial · `·` no implementation · `!` contested ownership

| Responsibility | META | FACTORY | LAUR | Current owner of record | Status |
|---|---|---|---|---|---|
| Identity | ✔ | ✔ | ✔ | contested — three systems | ! |
| Entities | ✔ | ✔ | · | contested | ! |
| Governance | ✔ | ✔ | · | contested | ! |
| Constitution | ✔ | ✔ | · | contested | ! |
| Permissions | ✔ | ~ | ~ | META (RBAC) | IMPLEMENTED |
| Capabilities | ~ | ✔ | · | Agent Factory | PARTIAL |
| Agents | ✔ | ✔ | ~ | Agent Factory (ADL) | IMPLEMENTED |
| Agent lifecycle | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Orchestration | · | ✔ | ✔ | contested | ! |
| Cognition | ~ | ~ | ✔ | Laurentia | PARTIAL |
| Reasoning | · | ~ | ~ | none — classifier only | PARTIAL |
| Memory | ~ | ✔ | ✔ | contested — three stores | ! |
| Doctrine | ✔ | ✔ | ✔ | contested — see C-002 | ! |
| Persona | · | · | ✔ | Laurentia | IMPLEMENTED |
| Model selection | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Model fallback | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Learning | ✔ | ~ | · | META | PARTIAL |
| Execution | · | ✔ | ✔ | contested | ! |
| Tools | · | ✔ | ✔ | contested | ! |
| Events | ✔ | ✔ | ✔ | contested — three buses | ! |
| Sessions | · | · | ✔ | Laurentia | IMPLEMENTED |
| Workflows | ~ | ✔ | ✔ | contested | ! |
| Observability | ✔ | ~ | ~ | META (runtime state) | PARTIAL |
| Security | ~ | ~ | ✔ | Laurentia (crypto, RGPD) | PARTIAL |
| Persistence | ✔ | ✔ | ✔ | per-system, no sharing | IMPLEMENTED |
| Gates | · | ✔ | · | Agent Factory | IMPLEMENTED |
| Trust chain / notarisation | ✔ | · | ~ | META | IMPLEMENTED |
| Autonomy | · | ✔ | · | Agent Factory | PARTIAL |
| Continuity / backup | · | ✔ | · | Agent Factory | IMPLEMENTED |

## Findings

- **Eleven responsibilities are contested.** Contested ownership, not missing
  functionality, is the estate's dominant structural problem.
- **Six responsibilities have a single clear owner** and should not be disturbed:
  gates, agent lifecycle, model routing (Agent Factory); persona, sessions,
  encryption (Laurentia); notarisation (META).
- **Reasoning has no true owner.** The vocabulary exists in three places; the
  implementation is a keyword classifier plus provider calls.

## Future RFC references

`RFC-0002` (doctrine and Brain), `RFC-0003` (runtime), `RFC-0005` (router).
