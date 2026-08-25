---
title: Gap Analysis
purpose: Classify the distance between the current state and the target architecture.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: SPECIFICATION
---

# Gap Analysis

Gaps are derived from evidence. No gap is listed to make the audit appear thorough:
the estate's implemented governance loop, gate system and ADL are deliberately
**not** restated as gaps.

Severity scale: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, `OPTIONAL`.

| ID | Gap | Severity | Current state | Desired state | Evidence | Impact | Depends on | Recommended action | Founder decision |
|---|---|---|---|---|---|---|---|---|---|
| G-001 | No inter-system dependency exists | CRITICAL | Three isolated systems; zero cross-imports; one outbound adapter | Layered dependency per target architecture | No cross-repo imports in any audited tree | The OS claim is unsupported; each system evolves independently and will diverge | FD-002 | Ratify the target direction, then implement in the order given in TARGET-ARCHITECTURE §4 | Required |
| G-002 | Capability advertisement unimplemented by providers | CRITICAL | META probes /api/capabilities; 12/12 DEGRADED | Every CVLN service advertises capabilities per contracts.py::Capability | META audit doc; no such route in FACTORY or LAUR | Registry, routing and orchestration are all blind | none | Implement GET /api/capabilities in Agent Factory and Laurentia. Cheapest high-value fix in the estate | Not required |
| G-003 | Three event buses, no shared envelope | HIGH | FACTORY topics + DLQ; LAUR orchestrator bus; META signed events | One signed envelope, one topic namespace | event_bus.py x2, /events/emit | No estate-wide causality or replay; only META events are tamper-evident | none | Adopt contracts.py::Event as the envelope; make Ed25519 signing mandatory | Not required |
| G-004 | No addressable Brain service | CRITICAL | Brain is an in-process wrapper in Laurentia and a route in META | One Brain service owning persona, doctrine, memory, reasoning, routing | cvl_brain.py; /brain/ask | Doctrine cannot be centrally owned while the Brain is a library | FD-001 | Extract the Brain behind api-contracts/BRAIN-API.md | Required |
| G-005 | Notary private key stored unencrypted | HIGH | db.system_keys.private_b64 in plaintext | Key wrapped by an env-derived secret, or an external KMS | META repository's own gap list | Compromise of the database forfeits the entire trust chain | none | Wrap the key at rest; rotate afterwards | Not required |
| G-006 | No encryption at rest outside Laurentia | HIGH | AES-256-GCM in LAUR only | Encryption at rest across the estate | crypto.py present only in LAUR | Governance and agent data are less protected than conversational data | none | Port the Laurentia crypto service pattern to META and Agent Factory | Not required |
| G-007 | Documentation inverted relative to implementation | LOW | Largest codebase has a placeholder README | Every repository documents its own architecture | FACTORY/README.md | New engineers misjudge the estate's centre of gravity | none | Require an ARCHITECTURE.md per repository, derived from this specification | Not required |
| G-008 | No shared identity | HIGH | Three independent auth systems, no SSO | One identity plane owned by META | Three distinct auth mechanisms | Permissions cannot be governed centrally; audit trails cannot be joined | FD-002 | Define META as the identity authority; issue tokens the other systems verify | Required |
| G-009 | Reasoning is a keyword classifier | MEDIUM | cognitive_engine.py exposes classify_message and internal_response | Model-backed reasoning behind the provider boundary | cognitive_engine.py | Autonomy cycles reason deterministically; capability is narrower than the vocabulary implies | FD-001 | Route cognition through the Brain; retain the classifier as a cheap pre-filter | Not required |
| G-010 | No unified memory | MEDIUM | Three unrelated stores, no shared schema | One semantic and institutional memory | FACTORY /memory, laurentia_memory, META evidence | Learning cannot generalise across the estate | G-004 | Specify the memory graph, implement after the Brain is extracted | Required |
| G-011 | Laurentia has no model fallback | HIGH | One hardcoded provider; 503 on failure | Terminal fallback as in provider_layer.py | cvl_brain.py; social_admin.py 503 | Single provider outage stops the operator product | FD-004 | Route Laurentia through the shared router | Required |
| G-012 | Open-core split documented but not performed | MEDIUM | Persona and fingerprint logic public | Sovereign concerns in a private module | LAUR ARCHITECTURE.md §4; C-003 | Anti-jailbreak rules are publicly readable, weakening them | FD-003 | Execute the migration, or correct the README tense | Required |
| G-013 | No cross-repository observability | MEDIUM | Per-system logs and journals; no distributed tracing | Estate-wide correlated tracing | META's own gap list | Cross-system incidents cannot be reconstructed | G-003 | Adopt one trace identifier propagated in the event envelope | Not required |
| G-014 | ISA does not exist | MEDIUM | No instruction-set semantics anywhere | Ratified execution model, or explicit rejection | absence across all repos | Agents execute with ad-hoc step semantics; autonomy is unauditable at instruction level | none | Decide RFC-0007. Do not present ISA as CVLN technology until ratified | Required |
| G-015 | MCL does not exist | LOW | No grammar, parser or file extension | Declarative OS language, or explicit rejection | absence across all repos | Entities, workflows and permissions are defined in code, not declaratively | G-014 | Decide RFC-0008. Lower priority than ISA | Required |
| G-016 | ADL v1 and v2 coexist without a migration path | MEDIUM | Pydantic v1 models and a v2 JSON Schema both served | One authoritative ADL version with a documented migration | adl_schema.py, adl_v2_schema.json | Agent definitions may validate against one generation and not the other | none | Declare the authoritative version and write the converter | Not required |
| G-017 | Contracts have no consumers | MEDIUM | Five contracts defined in META, consumed by nothing | Contracts imported or mirrored by every participant | contracts.py | Versioned contracts provide no compatibility guarantee while unused | G-002 | Publish contracts as a versioned artefact and consume them | Not required |
| G-018 | Wallet adapter fails upstream | LOW | POST /adapters/wallet/transaction receives 404 | Round-trip success | META's own gap list | One estate actuation path is broken | none | Ship the missing endpoint on the wallet service | Not required |
| G-019 | Strict multi-tenant isolation absent in META | MEDIUM | Isolation not enforced per tenant_id | Enforced tenant scoping on every query | META's own gap list | Cross-tenant data exposure risk as the estate grows | none | Add tenant scoping at the data-access layer | Not required |
| G-020 | Red-team scenarios unexecuted | OPTIONAL | Seven scenarios named, not run | Executed with a published maturity matrix | META's own next-action list | Security posture is asserted rather than measured | G-005 | Execute registry, context and memory poisoning scenarios first | Not required |

---

## Distribution

| Severity | Count |
|---|---|
| CRITICAL | 3 |
| HIGH | 6 |
| MEDIUM | 8 |
| LOW | 2 |
| OPTIONAL | 1 |

## Sequencing note

`G-002`, `G-003`, `G-005` and `G-006` require no founder ruling and can proceed
immediately. Every `CRITICAL` gap except `G-002` is blocked on a founder decision,
which makes [`FOUNDER-DECISIONS.md`](FOUNDER-DECISIONS.md) the critical path for the
entire programme.

## Future RFC references

`RFC-0002` through `RFC-0008`.
