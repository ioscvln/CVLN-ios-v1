---
title: Contradictions Register
purpose: Record, without resolving, every conflict between the CVLN conceptual model and repository evidence.
ownership: CVLN Group — Office of the Principal Systems Architect
scope: Three audited repositories
version: 1.0
status: IMPLEMENTED
attribution: IMPLEMENTATION
---

# Contradictions Register

A contradiction is recorded when a documented or conceptual claim cannot be
reconciled with repository evidence. Contradictions are **not** silently resolved
here. Each carries a proposed resolution path and, where applicable, a founder
decision reference.

---

## C-001 — The canonical layering is not the implemented dependency direction

**Claim.** `MetaCVLN → CVLN Agent Factory → CVL Brain → Laurentia → Applications`.

**Evidence.** No audited repository imports another. Each has its own
`requirements.txt`, its own MongoDB handle, its own authentication, and its own
event bus. Laurentia reaches intelligence through its local
`backend/services/cvl_brain.py`, not through Agent Factory or META. The only
realised edge is outbound HTTP from META to `/adapters/laurentia/briefing`,
`/adapters/labelos/push_catalogue` and `/adapters/wallet/transaction` — which
inverts the stated direction, since the governance layer calls the operator rather
than the operator deriving from the governance layer.

**Assessment.** The canonical layering is a `CONCEPT` and a target. It is not a
description of the current implementation.

**Resolution path.** `RFC-0003`, `RFC-0004`. Founder decision `FD-002`.

---

## C-002 — Doctrine has three owners

**Claim.** "Brain owns intelligence. Nobody else owns doctrine."

**Evidence.**
- Agent Factory implements doctrine as a first-class subsystem —
  `backend/doctrine.py` seeds numbered articles, `backend/doctrine_registry_routes.py`
  exposes `/doctrine` and `/doctrine/check`.
- META CVLN maintains `doctrine_history` and mutates it on learning-proposal
  approval.
- Laurentia carries a persona and knowledge layer in
  `backend/services/cvl_brain_knowledge.py` which functions as doctrine of voice.

None of the three defers to a Brain-owned doctrine service.

**Assessment.** Doctrine ownership is triplicated. The rule is currently
unenforced, and the divergence risk is real: three doctrine stores can disagree with
no reconciliation mechanism.

**Resolution path.** `RFC-0002`. Founder decision `FD-001`.

---

## C-003 — The open-core split is documented as complete but has not been performed

**Claim.** Laurentia's `README.md` presents a private `sovereign-brain/` submodule
containing `cvl_brain_knowledge.py`, `fingerprint_router.py` and `pipeline_echo/`,
distinguished from a public `open-core/` tree containing `frontend-ui/`, `SDK/` and
`bridges/`.

**Evidence.** Neither `sovereign-brain/` nor `open-core/` exists in the audited
`public` branch. The tree is a conventional `backend/` + `frontend/` application.
Two of the three concerns named as sovereign are present in the public tree:
`backend/services/cvl_brain_knowledge.py` and `backend/services/fingerprint.py`.
`ARCHITECTURE.md` §4 is internally consistent with the code: it marks only
"Étape 1 — préparation documentaire" as done, with physical migration pending.

**Assessment.** The README describes the target repository layout in the present
tense. Material consequence: persona rules and anti-jailbreak instructions intended
to be sovereign are publicly readable.

**Resolution path.** Execute `ARCHITECTURE.md` steps 2–4, or restate the README in
the future tense. Founder decision `FD-003`.

---

## C-004 — Provider-agnosticism is doctrine in one repository and violated in another

**Claim.** Agent Factory doctrine article `DOC-ARC-04`: no hardcoded provider
dependency (GPT/Claude); the execution layer is provider-agnostic.

**Evidence.** Agent Factory honours this — `backend/provider_layer.py` is the sole
provider boundary with a documented `ADR-002` rule and a terminal sovereign
fallback. Laurentia does not: `backend/services/cvl_brain.py` calls
`.with_model("anthropic", DEFAULT_MODEL)` with `DEFAULT_MODEL` defaulting to
`claude-sonnet-4-5-20250929`, and `backend/routes/brain.py` returns a hardcoded
`"model": "claude-sonnet-4-5-20250929"` in its health response. No fallback provider
is present in Laurentia; `routes/social_admin.py` raises `503` when generation is
unavailable.

**Assessment.** Doctrine is not binding across repository boundaries, because no
mechanism exists to bind it.

**Resolution path.** `RFC-0005`. Founder decision `FD-004`.

---

## C-005 — Capability discovery expects a contract no repository implements

**Claim.** META CVLN performs capability auto-discovery across the CVLN estate.

**Evidence.** `/registry/discover-all` probes registered repositories for
`/api/capabilities`. META's own audit documentation reports the live result: twelve
of twelve entries returned `DEGRADED`, because no repository exposes the endpoint.
Neither Agent Factory nor Laurentia declares an `/api/capabilities` route.

**Assessment.** The prober is `IMPLEMENTED`; the contract is `DEFINED` and
unimplemented by every provider. This is a genuine, honestly reported gap rather
than a concealed one — the mechanism works, the counterparties do not answer.

**Resolution path.** `RFC-0003` §Capability advertisement. Gap `G-002`.

---

## C-006 — The Model Router is not where the conceptual model places it

**Claim.** The Model Router is a CVL Brain responsibility (Layer 1).

**Evidence.** The only implemented model router in the estate is
`FACTORY/backend/provider_layer.py` — Layer 2. META's `contracts.py` defines a
`RoutingDecision` contract but implements no router. Laurentia routes implicitly by
hardcoding one provider.

**Assessment.** Implementation places model routing in the nervous system, not the
brain. Either the model or the code must move; the audit does not choose.

**Resolution path.** `RFC-0005`. Founder decision `FD-004`.

---

## C-007 — Three independent event buses, one conceptual bus

**Claim.** A single CVLN event bus.

**Evidence.** `FACTORY/backend/event_bus.py` with an enforced topic namespace, a
dead letter queue and spool replay; `LAUR/backend/orchestrator/event_bus.py` with a
circuit breaker and signals; `META` `/events/emit` with Ed25519 signing and
quarantine of tampered payloads. The three use different topic conventions,
different durability guarantees and different trust models. Only META's is signed.

**Assessment.** No shared event schema exists, despite META's `contracts.py` `Event`
model being available as a candidate.

**Resolution path.** `RFC-0006`. Gap `G-003`.

---

## C-008 — "Sovereign" denotes two different things

**Evidence.** In Agent Factory, `sovereign` is a concrete provider entry —
`"sovereign": {"model": "cvln-internal-deterministic", "cost_per_1k_tokens": 0.0,
"quality_rank": 99}` — a deterministic, non-model, infallible terminal fallback. In
Laurentia's README, "souveraineté" denotes cryptographic and jurisdictional control
over data, and "noyau cognitif propriétaire" denotes a proprietary cognitive core.

**Assessment.** A deterministic fallback provider is not a sovereign trained model.
The shared word invites conflation of a fallback with a capability. This document
records the distinction and asserts neither the presence nor the absence of a
sovereign trained model — see `architecture/CVLN-BRAIN.md`.

**Resolution path.** Terminology ruling in `constitution/CVLN-CONSTITUTION-v1.md`
§Vocabulary. Founder decision `FD-001`.

---

## C-009 — Agent Factory README is empty while the repository is the largest implementation

**Evidence.** `FACTORY/README.md` contains only the placeholder line "Here are your
Instructions", yet the repository contains approximately 143 routes, 30 router
modules, and the only implemented ADL in the estate. The MetaCVLN README is likewise
a placeholder while `docs/` carries the real architecture material.

**Assessment.** Documentation quality is inversely correlated with implementation
weight. Any audit relying on READMEs alone would have inverted the estate's true
centre of gravity.

**Resolution path.** `CONTRIBUTING.md` §Documentation duty. Gap `G-007`.

---

## Summary

| ID | Subject | Severity | Founder decision |
|---|---|---|---|
| C-001 | Layering versus dependencies | CRITICAL | FD-002 |
| C-002 | Doctrine ownership triplicated | CRITICAL | FD-001 |
| C-003 | Open-core split not performed | HIGH | FD-003 |
| C-004 | Provider-agnosticism unenforced | HIGH | FD-004 |
| C-005 | Capability contract unimplemented | MEDIUM | — |
| C-006 | Model Router placement | HIGH | FD-004 |
| C-007 | Three event buses | MEDIUM | — |
| C-008 | "Sovereign" overloaded | MEDIUM | FD-001 |
| C-009 | Documentation inversion | LOW | — |
