---
title: Dependency Map
purpose: Map every declared and referenced dependency, including inaccessible ones.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Audited repositories and their named counterparties
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Dependency Map

## Inter-repository dependencies (audited scope)

| From | To | Kind | Status |
|---|---|---|---|
| META CVLN | LAURENTIA | HTTP adapter `/adapters/laurentia/briefing` | IMPLEMENTED |
| META CVLN | LabelOS | HTTP adapter `/adapters/labelos/push_catalogue` | PARTIAL |
| META CVLN | Wallet | HTTP adapter `/adapters/wallet/transaction` | PARTIAL — upstream 404 |
| META CVLN | all registered repos | capability probe | PARTIAL — 12/12 DEGRADED |
| LAURENTIA | Agent Factory | — | absent |
| Agent Factory | META CVLN | — | absent |

**Import-level dependencies between audited repositories: none.**

## Referenced but not audited

Named in code or registry data, outside audit scope, contents not inspected. Marked
`PRIVATE / NOT ACCESSIBLE` where no public tree was reachable.

| Counterparty | Referenced from | Status |
|---|---|---|
| Kiltikonet | `LAUR/backend/services/kiltikonet_bridge.py` | REFERENCED |
| LabelOS | `LAUR/services/labelos_bridge.py`, META adapter | REFERENCED |
| FREKCORE | `LAUR/services/frekcore_bridge.py`, META registry | Excluded by instruction |
| KORA | META `registry_data.py` | REFERENCED |
| CVL Academy | META `registry_data.py` | REFERENCED |
| Wallet | META adapter | REFERENCED |
| Good Mood, Gala Cook, FMS, Blockchain | META `registry_data.py` | REFERENCED |
| `sovereign-brain/` | `LAUR/README.md` | PRIVATE / NOT ACCESSIBLE |

No speculation is offered about the contents of any entry above.

## External service dependencies

| Service | Consumer | Evidence |
|---|---|---|
| Model providers via `emergentintegrations` | LAUR, FACTORY, META | `cvl_brain.py`, `provider_layer.py` |
| Stripe | LAUR | `routes/billing.py` |
| OVH SMS + OVH S3 | LAUR | `orchestrator/sms_ovh.py`, `jobs/corpus_pipeline.py` |
| Instagram Graph, LinkedIn, X | LAUR | `jobs/social_agent.py` |
| Telegram | FACTORY | `backend/notifier.py` |
| MongoDB | all three | per-repository `database.py` / `lib` |

## Future RFC references

`RFC-0003`, `RFC-0006`.
