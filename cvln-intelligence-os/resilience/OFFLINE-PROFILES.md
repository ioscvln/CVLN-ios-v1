---
title: Offline Capability Profiles
purpose: What each layer may promise offline.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: resilience/
version: 1.1
status: TARGET
attribution: SPECIFICATION
---

# Offline Capability Profiles — TARGET

| Profile | Definition | Layers | Evidence |
|---|---|---|---|
| O0 — None | Requires connectivity to function | Layer 4 applications | none |
| O1 — Read-only | Serves last known state, refuses writes | Documentation portal | `backend/lib/corpus.py` reads local disk |
| O2 — Queued write | Accepts writes into a local durable spool | Agent Factory event bus | `event_bus.py` spool |
| O3 — Deterministic execution | Executes without any external model | Model router sovereign provider | `provider_layer.py` |
| O4 — Full autonomy | Full capability offline | none | none — no layer claims O4 |

No layer is classified O4. Any future O4 claim requires evidence and an ADR.
