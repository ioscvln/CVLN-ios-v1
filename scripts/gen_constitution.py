import os, sys, textwrap
sys.path.insert(0, "/app/scripts")
from gen_audit import w, PROPOSED_BANNER, MET, BRN, FAC, ARC

def simple(path, title, purpose, owner, status, attrib, lines, scope="CVLN intelligence ecosystem", rfc="`RFC-0001`"):
    body = lines + f"\n\n## Relationships\n\nSee [`audit/RESPONSIBILITY-MATRIX.md`](../audit/RESPONSIBILITY-MATRIX.md) for current ownership and [`audit/TARGET-ARCHITECTURE.md`](../audit/TARGET-ARCHITECTURE.md) for target ownership.\n\n## Future RFC references\n\n{rfc}"
    w(path, title, purpose, owner, scope, status, attrib, body)

# ================= CONSTITUTION =================
simple("constitution/CVLN-CONSTITUTION-v1.md", "CVLN Constitution v1", "Establish the binding rules of the CVLN Intelligence Operating System.", MET, "PARTIAL", "SPECIFICATION", """
## Article I — Vocabulary

`META CVLN` is the operating system and governance layer. `CVLN AGENT FACTORY` is the
nervous system and agent runtime. `CVL BRAIN` is the sovereign intelligence.
`LAURENTIA` is the cultural-industry operator. These terms are canonical and may not
be renamed by any subordinate repository.

**Sovereign** denotes control over data, keys and jurisdiction. It does **not** denote
a fallback provider. Contradiction `C-008` records the current conflation.

## Article II — Evidence

No CVLN document may present a concept as an implementation. Every architectural
claim carries an attribution level (`CONCEPT`, `SPECIFICATION`, `IMPLEMENTATION`,
`DEPLOYED RUNTIME`) and every component carries exactly one implementation status.

## Article III — Doctrine

Doctrine is the estate's binding operational rule set. Doctrine change requires human
approval and an evidence record. Automatic mutation of doctrine is prohibited.
META CVLN implements this rule today at `/learning/proposals/{id}/approve`.

**Current state:** doctrine is implemented in three components. Ownership is contested
pending `FD-001`.

## Article IV — Authority and gates

No capability executes without an authority decision. Blocked and escalated actions
are journalled append-only. Agent Factory implements this in `gate_routes.py`.

## Article V — Provider neutrality

No component may call a model provider outside a designated routing boundary. Agent
Factory doctrine article `DOC-ARC-04` and `ADR-002` state this rule; Laurentia does
not currently satisfy it (`C-004`).

## Article VI — Amendment

This constitution is amended by RFC only. Amendments are signed and recorded. Agent
Factory implements a compatible mechanism at `/amendments/{id}/sign`.

## Article VII — Ratification

**This constitution is not yet ratified.** It states rules that the estate partially
observes. Ratification is `RFC-0001`.
""", rfc="`RFC-0001` (ratification), `RFC-0002` (doctrine ownership)")

for p, t, pu, st, body in [
 ("GOVERNANCE", "Governance", "Define how CVLN decisions are made and recorded.", "PARTIAL", """
Governance is exercised through decisions of record. META CVLN implements the
decision system at `/decisions/{id}/action` with six verbs: approve, reject, edit,
escalate, pause, rollback. Every decision is retained and linked to evidence.

## Bodies

| Body | Authority | Implementation |
|---|---|---|
| Founder | Final authority on constitution, doctrine ownership, sovereignty claims | `FACTORY/backend/founder_council.py`, `founder_routes.py` — IMPLEMENTED |
| Governance plane | Decisions of record, notarisation, learning approval | META `/decisions`, `/notarizations` — IMPLEMENTED |
| Runtime authority | Gate decisions, lifecycle transitions | Agent Factory `gate_routes.py` — IMPLEMENTED |

## Escalation

Gate denial escalates to a single queue rather than a per-domain queue — an
implemented Agent Factory property that prevents authority fragmentation.

## Contested ownership

Governance and constitution are implemented in both META and Agent Factory with no
cross-reference. See `audit/CONTRADICTIONS.md` C-002 and founder decision `FD-002`.
"""),
 ("PERMISSIONS", "Permissions", "Define the CVLN permission model.", "PARTIAL", """
## Implemented models

| System | Model | Subjects |
|---|---|---|
| META CVLN | Role-based access control | admin, cfo, hr_lead, ops_lead, legal_lead, employee |
| Agent Factory | Actor + gate level | `get_current_actor`, `GATE_LEVELS`, `CRITICAL_ACTIONS` |
| Laurentia | API key + commercial tier | Free, Creator, Infinite, Enterprise |

Three permission models exist with no shared subject. An actor in one system has no
identity in another — gap `G-008`.

## Principles

1. Permission is checked before execution, never after.
2. Denial is journalled with actor, action and reason.
3. Critical actions require escalation regardless of role.
4. Tier is a commercial control and must not be used as a security boundary.

## Target

A single identity plane owned by META CVLN issuing tokens that Agent Factory and
Laurentia verify. `PROPOSED`, blocked on `FD-002`.
"""),
 ("ENTITY-MODEL", "Entity Model", "Define what a CVLN entity is and how entities are registered.", "PARTIAL", """
An entity is an organisational or product unit of the CVLN estate — for example KORA,
Academy, Wallet, LabelOS, Good Mood, Laurentia.

## Implemented

META CVLN maintains the register at `/entities` and a static estate list in
`backend/registry_data.py` carrying, per entry, an identifier, a GitHub URL and a
preview URL. Agent Factory independently implements `/entities` and
`/dashboard/{entity_id}`.

## Properties observed

| Property | Source |
|---|---|
| identifier | registry entry key |
| repository URL | `github_url` |
| runtime URL | `preview_url` |
| lifecycle status | discovery result: HEALTHY / DEGRADED / UNAVAILABLE / UNKNOWN |
| capabilities | discovery result — currently empty for all entries |

## Limitations

The register is static and hand-maintained; entities do not self-register. Capability
fields are empty estate-wide because no entity implements `/api/capabilities`
(`G-002`). Entity ownership is contested between META and Agent Factory.
"""),
 ("CAPABILITY-MODEL", "Capability Model", "Define capabilities as the unit of executable competence.", "PARTIAL", """
A capability is a named, versioned, permission-scoped competence that a CVLN
component can execute on request.

## Defined contract

META CVLN defines `Capability` in `backend/contracts.py` as one of five versioned
inter-system contracts. Status: `DEFINED` — the model exists; no component consumes
it.

## Implemented execution

Agent Factory executes capabilities through ADL-declared agents. The ADL v2 schema
carries a top-level `capabilities` property, making capability declaration part of
agent identity rather than an afterthought.

## Required advertisement

Every CVLN service is required to expose `GET /api/capabilities` returning
contract-conformant descriptors. **No service currently does**, which is why estate
discovery returns `DEGRADED` for all twelve registry entries. This is the single
cheapest high-value fix available (`G-002`).

## Capability descriptor fields

`id`, `version`, `owner`, `inputs`, `outputs`, `permissions`, `risk`, `gate_level`.
Fields beyond those present in `contracts.py::Capability` are `PROPOSED`.
"""),
 ("OBJECTIVE-MODEL", "Objective Model", "Define objectives as the link between doctrine and execution.", "PARTIAL", """
An objective is a stated, measurable intent that agents and operators are directed to
advance.

## Implemented

Agent Factory implements `backend/objectives_routes.py` and `mission_os_routes.py`
with `/missions`, `/briefing` and `/objectives` surfaces. META CVLN implements domain
loop maps — `/finance/loop` (9 stages) and `/people/loop` (11 stages) — where each
stage reports `OK` or `DATA_NOT_AVAILABLE`.

## The DATA_NOT_AVAILABLE property

META's loop maps return an explicit unavailability marker rather than a fabricated
value. Of nine finance stages, six report `OK` and three report `DATA_NOT_AVAILABLE`;
of eleven people stages, five and six respectively. This is a governance property
worth preserving estate-wide: an objective system that cannot lie about its inputs.

## Gap

Objectives are not linked to capabilities or gates. An objective cannot currently be
traced to the agent actions taken to advance it.
"""),
 ("DECISION-MODEL", "Decision Model", "Define the anatomy of a CVLN decision.", "IMPLEMENTED", """
## Verbs

META CVLN implements six decision verbs at `/decisions/{decision_id}/action`:
`approve`, `reject`, `edit`, `escalate`, `pause`, `rollback`. `rollback` is
significant: it makes decisions reversible rather than merely recorded.

## Anatomy

| Field | Meaning |
|---|---|
| subject | what is being decided |
| actor | authenticated human, by RBAC role |
| verb | one of the six |
| evidence | linked records supporting the decision |
| timestamp | server-anchored |
| signature | Ed25519 where emitted as a signed event |

## Properties

1. Decisions are human acts. No implemented path auto-approves.
2. Decisions are evidenced — `/evidence` links supporting records.
3. Decisions are notarisable and publicly verifiable via `/public/notarizations`.
4. Doctrine changes to `doctrine_history` occur only through an approved decision.

This is the most complete governance subsystem in the audited estate.
"""),
]:
    simple(f"constitution/{p}.md", t, pu, MET, st, "IMPLEMENTATION" if st!="PROPOSED" else "SPECIFICATION", body, rfc="`RFC-0001`, `RFC-0002`")
print("constitution written")
