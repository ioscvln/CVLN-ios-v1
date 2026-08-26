"""Generate the CVLN Intelligence OS v1.1 baseline-freeze corpus (append-only).

Nothing from the v1.0 corpus is deleted or rewritten by this script. It only writes new
documents and registries. Run: python scripts/gen_v11_freeze.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/app/cvln-intelligence-os")
OWNER = "CVLN Group — Office of the Principal Systems Architect"
V = "1.1"


def fm(title: str, purpose: str, scope: str, status: str, attribution: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"purpose: {purpose}\n"
        f"ownership: {OWNER}\n"
        f"scope: {scope}\n"
        f"version: {V}\n"
        f"status: {status}\n"
        f"attribution: {attribution}\n"
        "---\n\n"
    )


def write(rel: str, header: str, body: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + body.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


STATUS_LEGEND = """
## Status vocabulary (canonical, v1.1)

`OBSERVED` · `DECIDED` · `IMPLEMENTED` · `VERIFIED` · `PROPOSED` · `TARGET` ·
`UNKNOWN` · `DEPRECATED` · `REJECTED`

Two rules bind every reader and every generator:

- `IMPLEMENTED` never implies `VERIFIED`.
- `CURRENT` never implies `TARGET`.

A status may only be promoted by an ADR that cites evidence. Silent promotion is a
freeze violation.
"""

# ---------------------------------------------------------------- decisions D-001..D-014
DECISIONS: list[tuple[str, str, str, str, str, str, str, str]] = [
    ("D-001", "Evidence first", "No statement enters the corpus without a citable artefact or an explicit UNKNOWN", "PRINCIPLE", "audit/REPOSITORY-AUDIT.md", "DECIDED", "whole corpus", "ADR-0001"),
    ("D-002", "CURRENT is not TARGET", "Observed state and intended state are separate namespaces and never merge", "PRINCIPLE", "audit/COMPONENT-MATRIX.md", "DECIDED", "whole corpus", "ADR-0002"),
    ("D-003", "Human authority is final", "Autonomy is bounded by gates; a human decision of record outranks any agent output", "PRINCIPLE", "FACTORY backend/gate_routes.py", "DECIDED", "runtime, agents", "ADR-0003"),
    ("D-004", "Markdown is the only canonical store", "The portal renders; no database replicates canonical truth", "ARCHITECTURE", "backend/lib/corpus.py", "DECIDED", "portal", "ADR-0004"),
    ("D-005", "Append-only baseline", "v1.0 documents are preserved; corrections require a traced ADR reference", "GOVERNANCE", "constitution/FREEZE-001.md", "DECIDED", "whole corpus", "ADR-0005"),
    ("D-006", "Resilience is a first-class dimension", "Degradation, offline operation and recovery are specified, not improvised", "ARCHITECTURE", "META backend/server.py runtime state", "DECIDED", "resilience/", "ADR-0006"),
    ("D-007", "Proof layer is digital evidence only", "The OS produces evidence packages; it does not produce legal attestation", "ARCHITECTURE", "META backend/server.py notarizations", "DECIDED", "proof/", "ADR-0007"),
    ("D-008", "JCC is an internal accounting unit", "JCC is never described, priced or exchanged as legal currency", "ECONOMIC", "none — no monetary implementation observed", "DECIDED", "economics/", "ADR-0008"),
    ("D-009", "Legal-by-design bounds the design space", "A capability outside the lawful design space is REJECTED at specification time", "GOVERNANCE", "legal/LAWFUL-DESIGN-SPACE.md", "DECIDED", "legal/", "ADR-0009"),
    ("D-010", "Zero-trust between layers", "Layer-to-layer calls authenticate; internal position grants no privilege", "SECURITY", "META backend/server.py JWT", "DECIDED", "security/", "ADR-0010"),
    ("D-011", "Doctrine ownership is contested and frozen as a contradiction", "C-002 is not resolved by fiat; it stays an open contradiction until an ADR closes it", "GOVERNANCE", "audit/CONTRADICTIONS.md", "DECIDED", "architecture/", "ADR-0011"),
    ("D-012", "One status per row", "Every registry row carries exactly one status and one evidence cell", "GOVERNANCE", "registry/", "DECIDED", "registries", "ADR-0012"),
    ("D-013", "Traceability is mandatory", "Every gap, decision and vulnerability links to at least one component or system node", "GOVERNANCE", "registry/", "DECIDED", "whole corpus", "ADR-0013"),
    ("D-014", "Freeze is verifiable by machine", "Invariants are executable assertions over the corpus, not prose", "GOVERNANCE", "scripts/check_freeze_invariants.py", "DECIDED", "whole corpus", "ADR-0014"),
]

ECOSYSTEM = [
    ("FREKCORE", "Layer -1", "Holding and industrial origin of the estate", "—", "none in audited repositories", "UNKNOWN", "capital, mandate", "runtime execution, doctrine"),
    ("MetaCVLN", "Layer 0", "OS kernel: governance, registry, permissions, runtime state", "META", "backend/server.py", "IMPLEMENTED", "governance, registry, decisions", "cultural production, agent execution"),
    ("CVLN Brain", "Layer 1", "Sovereign intelligence engine", "—", "no dedicated repository audited", "TARGET", "doctrine, reasoning, memory", "workflow execution"),
    ("CVLN Agent Factory", "Layer 2", "Nervous system: ADL, runtime, gates, event bus", "FACTORY", "backend/adl_schema.py, gate_routes.py", "IMPLEMENTED", "agent execution, gates", "doctrine of record"),
    ("Laurentia", "Layer 3", "Cultural industry operator", "LAUR", "public branch application code", "PARTIAL", "sessions, artifacts, reports", "doctrine, agent runtime internals"),
    ("KORA", "Layer 4", "Application on the estate contracts", "—", "referenced in META registry_data.py", "REFERENCED", "product surface", "OS primitives"),
    ("LabelOS", "Layer 4", "Application on the estate contracts", "—", "META adapter target", "REFERENCED", "product surface", "OS primitives"),
    ("Wallet", "Layer 4", "Value and accounting surface", "—", "META adapter returns upstream 404", "REFERENCED", "accounting surface", "legal currency issuance"),
    ("CVLN Academy", "Layer 4", "Learning surface", "—", "no evidence in audited repositories", "UNKNOWN", "unknown", "unknown"),
    ("Proof Layer", "Cross-cutting", "Digital evidence packaging and verification", "META", "notarizations, signed event bus", "PARTIAL", "digital evidence", "legal attestation"),
]

VULNS = [
    ("V-001", "Notary private key stored unencrypted at rest", "META notary", "backend/server.py", "CRITICAL", "OBSERVED", "KMS or sealed secret; rotation policy", "D-010"),
    ("V-002", "Single monolithic governance module (~1611 lines, ~50 paths)", "META API", "backend/server.py", "HIGH", "OBSERVED", "Module split with per-router authorisation tests", "D-010"),
    ("V-003", "No observed mutual authentication between layers", "inter-layer calls", "adapters in META", "HIGH", "OBSERVED", "mTLS or signed service tokens", "D-010"),
    ("V-004", "Capability discovery probes remote repos that expose nothing", "registry discovery", "/registry/discover-all — 12/12 DEGRADED", "MEDIUM", "OBSERVED", "Contract-first capability endpoint per repo", "D-002"),
    ("V-005", "Provider credentials handled inside a single provider layer with journalling", "FACTORY model router", "backend/provider_layer.py", "MEDIUM", "OBSERVED", "Verify journal redaction of secrets", "D-010"),
    ("V-006", "No observed rate limiting or abuse control on public read surfaces", "META public endpoints", "/public/notarizations", "MEDIUM", "OBSERVED", "Edge rate limiting", "D-010"),
    ("V-007", "Threat model for offline and degraded modes not specified", "resilience", "none", "HIGH", "TARGET", "Adopt resilience/CONTINUITY-MODEL.md threat annex", "D-006"),
    ("V-008", "Evidence package integrity chain not end-to-end verified", "proof layer", "notarizations verify endpoint only", "HIGH", "TARGET", "Chain manifest + external anchoring", "D-007"),
]

CONTINUITY = [
    ("K-001", "Human decision of record", "Available", "Available", "Queued locally, replayed on reconnect", "Replay with conflict report", "META decisions endpoints", "TARGET"),
    ("K-002", "Agent execution", "Available", "Reduced concurrency", "Deterministic sovereign provider only", "Checkpoint resume", "FACTORY provider_layer.py sovereign fallback", "PARTIAL"),
    ("K-003", "Event bus delivery", "Available", "Spool + DLQ", "Local spool, no external fan-out", "Spool replay in order", "FACTORY event_bus.py", "IMPLEMENTED"),
    ("K-004", "Model routing", "Full provider table", "Fallback chain", "Sovereign deterministic provider", "Re-probe providers", "FACTORY provider_layer.py", "IMPLEMENTED"),
    ("K-005", "Runtime state signalling", "normal", "degraded", "critical / offline", "Hysteresis-guarded return to normal", "META /runtime/state", "IMPLEMENTED"),
    ("K-006", "Evidence packaging", "Available", "Available", "Local hashing only, no anchoring", "Anchor backlog flush", "none", "TARGET"),
    ("K-007", "Power-loss durability of journals", "Durable", "Durable", "Durable append-only spool", "Integrity scan on boot", "none", "TARGET"),
    ("K-008", "Documentation portal", "Available", "Available", "Static corpus read from disk", "No recovery step required", "backend/lib/corpus.py", "IMPLEMENTED"),
]

LEGAL = [
    ("L-001", "Personal data", "Lawful basis, minimisation, retention limits for memory stores", "Memory writes carry purpose and retention metadata", "none", "TARGET", "MetaCVLN", "D-009"),
    ("L-002", "Automated decision-making", "Human review of consequential decisions", "Gate system blocks critical actions pending human decision", "FACTORY gate_routes.py", "PARTIAL", "Agent Factory", "D-003"),
    ("L-003", "Evidence and records", "Records must be attributable, tamper-evident and time-anchored", "Signed events + notarisation", "META /events/verify", "PARTIAL", "MetaCVLN", "D-007"),
    ("L-004", "Legal attestation", "Only a competent authority attests legal effect", "OS emits evidence packages; attestation is external", "none", "TARGET", "Legal counsel", "D-007"),
    ("L-005", "Monetary and payment regulation", "Internal units must not be presented as currency or payment instrument", "JCC constrained as internal accounting unit", "none", "TARGET", "FREKCORE", "D-008"),
    ("L-006", "Intellectual property of cultural artifacts", "Rights chain per artifact", "Artifact records carry rights provenance", "none", "TARGET", "Laurentia", "D-009"),
    ("L-007", "Cross-border transfer", "Transfer conditions per jurisdiction", "Provider routing constrained by jurisdiction tag", "none", "TARGET", "MetaCVLN", "D-009"),
]


def gen_decisions() -> None:
    hdr = fm(
        "Decision Registry",
        "Canonical register of foundational decisions D-001 to D-014.",
        "Whole corpus",
        "DECIDED",
        "GOVERNANCE",
    )
    rows = "\n".join(
        "| " + " | ".join(d) + " |" for d in DECISIONS
    )
    body = f"""# Decision Registry

Each row is a foundational decision of the v1.1 baseline freeze. A decision is binding
until superseded by a later ADR. `Evidence` cites the artefact that motivated the
decision, or the literal string `none` where the decision is normative rather than
observed.

| ID | Decision | Rationale | Type | Evidence | Status | Scope | ADR |
|---|---|---|---|---|---|---|---|
{rows}

{STATUS_LEGEND}

## Relationships

- Frozen by `constitution/FREEZE-001.md`.
- Reported in `audit/FREEZE-REPORT-v1.1.md`.
- Enforced by `scripts/check_freeze_invariants.py`.
"""
    write("decisions/DECISION-REGISTRY.md", hdr, body)

    tmpl = fm(
        "ADR Template",
        "Required shape of every architecture decision record.",
        "decisions/",
        "DECIDED",
        "GOVERNANCE",
    )
    write(
        "decisions/ADR-TEMPLATE.md",
        tmpl,
        """# ADR Template

## Context
## Decision
## Evidence
## Status
## Consequences
## Alternatives considered
## Security impact
## Legal impact
## Continuity impact
## Supersedes / Superseded by
""",
    )

    for d in DECISIONS:
        did, title, rationale, dtype, evidence, status, scope, adr = d
        hdr = fm(
            f"{adr} — {title}",
            f"Architecture decision record for {did}.",
            scope,
            "DECIDED",
            "GOVERNANCE",
        )
        body = f"""# {adr} — {title}

## Context

The v1.1 baseline freeze requires that every binding rule of the CVLN Intelligence OS
exists as a decision record rather than as tribal convention. {did} is one of the
fourteen foundational decisions listed in `decisions/DECISION-REGISTRY.md`.

## Decision

{rationale}.

Type: `{dtype}`. Scope: `{scope}`.

## Evidence

`{evidence}`

Where the evidence cell reads `none`, this decision is **normative** — it constrains
future work and asserts nothing about current implementation.

## Status

`DECIDED`. `DECIDED` does not imply `IMPLEMENTED`, and `IMPLEMENTED` never implies
`VERIFIED`.

## Consequences

- Any specification, registry row or portal view that contradicts this decision is a
  freeze violation and must be raised as a contradiction, not silently corrected.
- Reversal requires a superseding ADR that cites new evidence.

## Alternatives considered

Leaving the rule implicit. Rejected: an implicit rule cannot be tested, and
`scripts/check_freeze_invariants.py` can only assert what is written.

## Security impact

None beyond the decision's own scope unless the type is `SECURITY`.

## Legal impact

None unless the type is `GOVERNANCE`, `ECONOMIC` or the decision is referenced from
`registry/LEGAL-MATRIX.md`.

## Continuity impact

None unless referenced from `registry/CONTINUITY-MATRIX.md`.

## Supersedes / Superseded by

Supersedes: none. Superseded by: none.
"""
        write(f"decisions/{adr}-{did}.md", hdr, body)


def gen_freeze() -> None:
    hdr = fm(
        "FREEZE-001 — Architecture Baseline Freeze",
        "Constitutional instrument that freezes the v1.1 architecture baseline.",
        "Whole corpus",
        "DECIDED",
        "GOVERNANCE",
    )
    body = f"""# FREEZE-001 — Architecture Baseline Freeze

Version: **OS v1.1 — ARCHITECTURE BASELINE FROZEN**
Predecessor: **OS v1.0 — TITAN FOUNDATION** (preserved, not superseded)

## 1. Purpose

FREEZE-001 declares the v1.1 corpus a **frozen baseline**: a known, citable state of
the architecture from which every later change must be a traced delta.

## 2. What freeze means

1. The v1.0 corpus is preserved in place. No document is deleted, moved or rewritten.
2. New dimensions are **added** as new sections: `decisions/`, `security/`,
   `resilience/`, `legal/`, `proof/`, `economics/`, `registry/`.
3. A v1.0 document may only be edited when the edit is documented, traced and
   referenced by an ADR or RFC (D-005).
4. Markdown on disk remains the sole canonical store (D-004). The portal renders it.

## 3. What freeze forbids

- Promoting any status without evidence and an ADR (D-001, D-012).
- Merging `CURRENT` and `TARGET` namespaces (D-002).
- Describing a `TARGET` capability in the present tense.
- Closing contradiction `C-002` (doctrine ownership) by fiat (D-011).
- Presenting JCC as legal currency: forbidden, JCC is never a currency (D-008).
- Presenting a digital evidence package as legal attestation (D-007).

## 4. Instruments of the freeze

| Instrument | Path |
|---|---|
| Decision registry | `decisions/DECISION-REGISTRY.md` |
| Architecture decision records | `decisions/ADR-*.md` |
| Freeze manifest | `audit/freeze-manifest.yaml` |
| Freeze report | `audit/FREEZE-REPORT-v1.1.md` |
| Executable invariants | `scripts/check_freeze_invariants.py` |
| Registries | `registry/*.md` |

{STATUS_LEGEND}

## 5. Amendment procedure

`AUDIT → MAP → PRESERVE → GOVERN`. Reuse what exists; create only against a real gap;
classify anything unimplemented as `TARGET` or `PROPOSED`; never alter the core
responsibilities of MetaCVLN, CVLN Brain, Agent Factory, Laurentia or FREKCORE without
an ADR.
"""
    write("constitution/FREEZE-001.md", hdr, body)

    hdr = fm(
        "RFC-0007 — Baseline Freeze Procedure",
        "Procedure by which a baseline is frozen, reported and re-opened.",
        "Governance",
        "DECIDED",
        "GOVERNANCE",
    )
    write(
        "rfc/RFC-0007-BASELINE-FREEZE.md",
        hdr,
        """# RFC-0007 — Baseline Freeze Procedure

## Context

v1.0 established an evidence-based map of the estate. Nothing prevented a later editor
from promoting a `TARGET` row to `IMPLEMENTED` silently.

## Problem

Architecture drift is invisible without a frozen reference point and executable rules.

## Proposal

1. Declare a freeze instrument (`constitution/FREEZE-001.md`).
2. Enumerate foundational decisions as ADRs.
3. Emit a machine-readable manifest (`audit/freeze-manifest.yaml`).
4. Emit a human freeze report (`audit/FREEZE-REPORT-v1.1.md`).
5. Enforce invariants with an executable checker.

## Alternatives

Convention-only governance (rejected: untestable). Git tags alone (rejected: a tag does
not express which claims are unverified).

## Security impact

The freeze adds `registry/VULNERABILITY-REGISTRY.md`, making known weaknesses citable.

## Migration

Additive. No v1.0 path changes.

## Compatibility

Portal endpoints of v1.0 keep their contracts; v1.1 adds endpoints.

## Status

`DECIDED`.
""",
    )


def gen_security() -> None:
    write(
        "security/SECURITY-BASELINE.md",
        fm("Security Baseline", "Frozen security posture of the estate.", "security/", "PARTIAL", "MIXED"),
        """# Security Baseline

## Observed (evidence-backed)

- JWT authentication with bcrypt password hashing and six roles (META `backend/server.py`).
- Ed25519 signing of events with verification and quarantine of tampered payloads.
- Notarisation with a verify endpoint and a public read surface.
- Gate system blocking critical agent actions, with an append-only journal (FACTORY).
- Provider access confined to one model-router layer (FACTORY `provider_layer.py`).

## Not observed — TARGET

- Key management: the notary private key is stored unencrypted at rest (V-001).
- Mutual authentication between layers (V-003).
- Rate limiting on public surfaces (V-006).
- Secret redaction verification in provider journals (V-005).

## Rule

Anything in the second list is `TARGET`. It must not be described elsewhere in this
corpus as an existing control.

Register: `registry/VULNERABILITY-REGISTRY.md`. Decision: D-010 / `ADR-0010`.
""",
    )
    write(
        "security/ZERO-TRUST.md",
        fm("Zero Trust Model", "Layer-to-layer trust rules.", "security/", "TARGET", "SPECIFICATION"),
        """# Zero Trust Model — TARGET

> This document specifies intent. No mutual-authentication implementation was observed
> in the audited repositories.

## Principles

1. Network position grants no privilege. Layer 3 calling Layer 0 authenticates exactly
   as an external caller would.
2. Every call carries a verifiable caller identity and an authorisation scope.
3. Every privileged action is journalled with the caller identity.
4. Deny by default: an unknown capability request fails closed, not open.

## Trust boundaries

| Boundary | Current control | Target control |
|---|---|---|
| Client → MetaCVLN | JWT | JWT + short TTL + audience scoping |
| MetaCVLN → Laurentia | HTTP adapter, no observed auth | Signed service token or mTLS |
| Agent Factory → provider | Provider layer credentials | Scoped credentials per agent risk level |
| External verifier → notary | Public read surface | Signed, rate-limited read surface |

Decision: D-010.
""",
    )
    write(
        "security/THREAT-MODEL.md",
        fm("Threat Model", "Adversaries, assets and abuse cases.", "security/", "TARGET", "SPECIFICATION"),
        """# Threat Model — TARGET

## Assets

Doctrine of record · decision journal · notary keys · agent definitions · memory graph ·
evidence packages.

## Adversaries

| Adversary | Capability | Primary target |
|---|---|---|
| External attacker | Public endpoints | Notary keys, public audit surface |
| Compromised provider | Model responses | Reasoning integrity, prompt exfiltration |
| Malicious agent definition | ADL authoring | Gate bypass, capability escalation |
| Insider with role | Governance API | Silent doctrine mutation |
| Physical/power event | Availability | Journal durability (see `resilience/POWER-LOSS.md`) |

## Abuse cases

1. Forged event accepted as signed → mitigated by Ed25519 verification (observed).
2. Notary key exfiltration → **not mitigated** (V-001).
3. Agent escalating past its gate level → mitigated by gate check (observed), unverified.
4. Evidence package altered after emission → **not mitigated end-to-end** (V-008).

Nothing in this document may be read as a deployed control.
""",
    )


def gen_resilience() -> None:
    write(
        "resilience/CONTINUITY-MODEL.md",
        fm("Continuity Model", "Normal, degraded, offline and recovery states.", "resilience/", "PARTIAL", "MIXED"),
        """# Continuity Model

## State machine

```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Degraded: signal loss / provider failure
    Degraded --> Offline: connectivity or power loss
    Degraded --> Normal: signals recovered (hysteresis)
    Offline --> Recovery: connectivity restored
    Recovery --> Normal: replay complete + integrity scan passed
    Recovery --> Degraded: replay conflicts outstanding
```

## State definitions

| State | Definition | Observed control |
|---|---|---|
| Normal | All signals nominal | META `/runtime/state` = normal |
| Degraded | Reduced capability, service preserved | META degraded/critical states with hysteresis |
| Offline | No external connectivity or provider access | FACTORY sovereign deterministic provider |
| Recovery | Reconnected, replaying spooled work | FACTORY event-bus spool replay |

## Rule

Recovery is complete only when replay finished **and** an integrity scan passed. A
partially replayed system remains `Degraded`.

Matrix: `registry/CONTINUITY-MATRIX.md`. Decision: D-006.
""",
    )
    write(
        "resilience/OFFLINE-PROFILES.md",
        fm("Offline Capability Profiles", "What each layer may promise offline.", "resilience/", "TARGET", "SPECIFICATION"),
        """# Offline Capability Profiles — TARGET

| Profile | Definition | Layers | Evidence |
|---|---|---|---|
| O0 — None | Requires connectivity to function | Layer 4 applications | none |
| O1 — Read-only | Serves last known state, refuses writes | Documentation portal | `backend/lib/corpus.py` reads local disk |
| O2 — Queued write | Accepts writes into a local durable spool | Agent Factory event bus | `event_bus.py` spool |
| O3 — Deterministic execution | Executes without any external model | Model router sovereign provider | `provider_layer.py` |
| O4 — Full autonomy | Full capability offline | none | none — no layer claims O4 |

No layer is classified O4. Any future O4 claim requires evidence and an ADR.
""",
    )
    write(
        "resilience/POWER-LOSS.md",
        fm("Power Loss Model", "Durability expectations across abrupt loss.", "resilience/", "TARGET", "SPECIFICATION"),
        """# Power Loss Model — TARGET

## Requirements

1. Journals and spools are append-only and flushed before acknowledgement.
2. A record is acknowledged only once durable; an unacknowledged record may be lost.
3. On boot, an integrity scan classifies each journal as `intact`, `truncated` or
   `corrupt`; a `corrupt` journal blocks promotion out of `Recovery`.
4. No in-memory-only state is authoritative.

## Current position

No power-loss test evidence exists in the audited repositories. Status is `TARGET`
(V-007, K-007).
""",
    )
    write(
        "resilience/RECOVERY.md",
        fm("Recovery Procedure", "Ordered return to Normal.", "resilience/", "TARGET", "SPECIFICATION"),
        """# Recovery Procedure — TARGET

1. Boot in `Recovery`; refuse new autonomous actions.
2. Integrity scan of journals and spools.
3. Ordered replay of spooled events; conflicts written to a conflict report.
4. Re-probe providers; rebuild the routing table.
5. Human review of the conflict report — a human decision of record is required to
   promote to `Normal` when conflicts existed (D-003).
6. Emit an evidence package describing the recovery (`proof/EVIDENCE-PACKAGE.md`).
""",
    )


def gen_legal() -> None:
    write(
        "legal/LEGAL-BY-DESIGN.md",
        fm("Legal-by-Design Framework", "Legal constraints as design inputs.", "legal/", "TARGET", "SPECIFICATION"),
        """# Legal-by-Design Framework — TARGET

Legal constraints are **design inputs**, not post-hoc review. A specification that
cannot be built lawfully is `REJECTED` at specification time, before implementation.

## Method

1. Identify the obligation domain (`registry/LEGAL-MATRIX.md`).
2. Express each obligation as a **design constraint** in machine-checkable terms.
3. Attach the constraint to the components it binds.
4. Classify: inside the lawful design space, outside it, or `UNKNOWN` pending counsel.

## Boundary

This corpus is architecture documentation. It is **not** legal advice and does not
substitute for counsel in any jurisdiction. Decision: D-009.
""",
    )
    write(
        "legal/LAWFUL-DESIGN-SPACE.md",
        fm("Lawful Design Space", "The bounded region in which CVLN may design.", "legal/", "TARGET", "SPECIFICATION"),
        """# Lawful Design Space — TARGET

## Definition

The lawful design space is the intersection of technically feasible designs and designs
permitted by applicable obligations. CVLN designs only inside it.

## Explicit exclusions (frozen)

| Excluded design | Reason | Status |
|---|---|---|
| Presenting JCC as legal currency or a payment instrument | Monetary regulation (L-005) | REJECTED |
| Emitting legal attestation from the OS | Attestation is an authority function (L-004) | REJECTED |
| Fully autonomous consequential decisions without human review | L-002, D-003 | REJECTED |
| Unbounded retention of personal data in memory stores | L-001 | REJECTED |

An excluded design may not reappear as a `TARGET` without an ADR that records counsel
input.
""",
    )


def gen_proof() -> None:
    write(
        "proof/PROOF-LAYER.md",
        fm("Intelligent Proof Layer", "How the OS produces verifiable digital evidence.", "proof/", "PARTIAL", "MIXED"),
        """# Intelligent Proof Layer

## Purpose

Make what the system did reconstructible and tamper-evident.

## Observed

- Ed25519-signed events with a verify endpoint; tampered payloads quarantined (META).
- Notarisations with verify and export, plus a public read surface (META).
- Append-only gate journal (FACTORY).

## Not observed — TARGET

- End-to-end integrity chain across a whole evidence package (V-008).
- External time anchoring.
- Package-level export format with a stable schema.

## Hard boundary

The proof layer produces **digital evidence**. It does not produce **legal
attestation**. See `proof/NOTARIAL-BOUNDARY.md` and D-007.
""",
    )
    write(
        "proof/EVIDENCE-PACKAGE.md",
        fm("EvidencePackage Model", "Specification of the evidence package artefact.", "proof/", "TARGET", "SPECIFICATION"),
        """# EvidencePackage — TARGET

> Specification only. No implementation of this artefact was observed.

## Fields

| Field | Type | Meaning |
|---|---|---|
| `package_id` | string | Stable identifier |
| `subject` | string | What the package proves something about |
| `claims` | list | Each claim: statement, status, evidence reference |
| `artefacts` | list | Content-addressed items with hash and algorithm |
| `events` | list | Signed event identifiers included in the chain |
| `decisions` | list | Human decisions of record referenced |
| `chain_hash` | string | Hash over the ordered artefact and event hashes |
| `signature` | string | Signature over `chain_hash` by the emitting notary key |
| `anchored_at` | string \\| null | External anchor time, `null` when unanchored |
| `legal_effect` | literal | Always `"none"` — see the notarial boundary |

## Verification

Recompute artefact hashes → recompute `chain_hash` → verify `signature` → report each
step independently. A package that fails any step is `REJECTED`, never partially valid.
""",
    )
    write(
        "proof/NOTARIAL-BOUNDARY.md",
        fm("Notarial Boundary", "Separation of digital evidence from legal attestation.", "proof/", "DECIDED", "GOVERNANCE"),
        """# Notarial Boundary

| Dimension | Digital evidence (in scope) | Legal attestation (out of scope) |
|---|---|---|
| Producer | CVLN Intelligence OS | Competent authority or notary |
| Object | Integrity and attribution of records | Legal effect of an act |
| Verification | Cryptographic recomputation | Legal procedure |
| Failure mode | Chain breaks, verification fails | Instrument void |
| Status in corpus | `PARTIAL` / `TARGET` | Permanently out of scope |

The word "notary" in the audited MetaCVLN code names a **signing key role**. It does not
denote a legal notary. Decision: D-007.
""",
    )


def gen_economics() -> None:
    write(
        "economics/CVE-v1.2.md",
        fm("CVE v1.2 — CVLN Value Engine", "Value accounting model of the estate.", "economics/", "TARGET", "SPECIFICATION"),
        """# CVE v1.2 — CVLN Value Engine — TARGET

> No economic engine implementation was observed in the audited repositories. This
> document is a specification.

## Model

Value is recognised from **verified contribution**, not from activity volume.

| Concept | Definition | Unit |
|---|---|---|
| Contribution | An artefact or decision attributable to an actor | count |
| Verification | An evidence package supporting the contribution | boolean |
| Recognised value | Contribution weighted by verification and scope | JCC (internal) |
| Settlement | Any conversion to external value | out of scope |

## Rules

1. Unverified contribution accrues no recognised value.
2. JCC never leaves internal accounting (see `economics/JCC-UNIT-CONSTRAINTS.md`).
3. Value recognition events are journalled and reconstructible from evidence.
""",
    )
    write(
        "economics/JCC-UNIT-CONSTRAINTS.md",
        fm("JCC Internal Unit Constraints", "Hard constraints on the JCC accounting unit.", "economics/", "DECIDED", "GOVERNANCE"),
        """# JCC — Internal Accounting Unit Constraints

JCC is an **internal accounting unit**. It is not a currency, not a payment instrument,
not a security and not a token.

## Constraints (frozen)

1. JCC is not exchangeable for legal tender inside any CVLN system.
2. JCC carries no price, no market and no redemption promise.
3. No CVLN interface may present JCC in a currency position or with a currency symbol.
4. JCC balances are accounting records, not claims.
5. Any change to these constraints requires an ADR with counsel input (D-008, L-005).

Violating any constraint is a freeze violation and is asserted by
`scripts/check_freeze_invariants.py`.
""",
    )
    write(
        "economics/VALUE-CENTRIC-ECONOMICS.md",
        fm("Value-Centric Economics", "Why the estate accounts value rather than activity.", "economics/", "TARGET", "SPECIFICATION"),
        """# Value-Centric Economics — TARGET

## Position

Activity metrics (messages, runs, tokens) measure cost, not value. The estate accounts
**verified outcomes**: an artefact delivered, a decision taken, a risk avoided.

## Consequences for architecture

- Every recognised value event references an evidence package (`proof/`).
- Agent autonomy is priced by risk level, not by throughput.
- Reporting surfaces show recognised value and its verification state side by side;
  unverified value is displayed as unverified.

Status `TARGET`: no implementation observed.
""",
    )


def registry_doc(rel: str, title: str, purpose: str, columns: list[str], rows: list[tuple], note: str, status: str) -> None:
    hdr = fm(title, purpose, "registry/", status, "MIXED")
    head = "| " + " | ".join(columns) + " |"
    sep = "|" + "---|" * len(columns)
    body_rows = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    write(rel, hdr, f"# {title}\n\n{note}\n\n{head}\n{sep}\n{body_rows}\n{STATUS_LEGEND}")


def gen_registries() -> None:
    registry_doc(
        "registry/ECOSYSTEM-REGISTRY.md",
        "Ecosystem Registry",
        "Canonical register of ecosystem systems, layers and ownership boundaries.",
        ["System", "Layer", "Role", "Repository", "Evidence", "Status", "Owns", "Must Not Own"],
        ECOSYSTEM,
        "One row per system of the estate. `Must Not Own` is binding: a system found "
        "owning a forbidden responsibility is a contradiction, not a feature. Core "
        "responsibilities may not change without an ADR.",
        "PARTIAL",
    )
    registry_doc(
        "registry/VULNERABILITY-REGISTRY.md",
        "Vulnerability Registry",
        "Register of observed and anticipated security weaknesses.",
        ["ID", "Finding", "Surface", "Evidence", "Severity", "Status", "Mitigation", "Decision Ref"],
        VULNS,
        "`OBSERVED` means the weakness is visible in an audited repository. `TARGET` "
        "means the control is specified but absent. No row is closed without evidence "
        "of remediation.",
        "OBSERVED",
    )
    registry_doc(
        "registry/CONTINUITY-MATRIX.md",
        "Continuity Matrix",
        "Per-capability behaviour across Normal, Degraded, Offline and Recovery.",
        ["ID", "Capability", "Normal", "Degraded", "Offline", "Recovery", "Evidence", "Status"],
        CONTINUITY,
        "One row per continuity-relevant capability. A cell describes intended behaviour; "
        "the `Status` column states whether that behaviour is implemented.",
        "PARTIAL",
    )
    registry_doc(
        "registry/LEGAL-MATRIX.md",
        "Legal Matrix",
        "Obligation domains mapped to design constraints and owners.",
        ["ID", "Obligation Domain", "Requirement", "Design Constraint", "Evidence", "Status", "Owner", "Decision Ref"],
        LEGAL,
        "Architecture documentation, not legal advice. `TARGET` rows state constraints "
        "that no observed implementation satisfies.",
        "TARGET",
    )
    write(
        "registry/COMPONENT-REGISTRY.md",
        fm(
            "Component Registry",
            "Governance wrapper over the v1.0 component matrix.",
            "registry/",
            "IMPLEMENTED",
            "GOVERNANCE",
        ),
        """# Component Registry

The canonical per-component evidence table remains `audit/COMPONENT-MATRIX.md` (v1.0,
preserved unchanged under D-005). This registry adds the governance rules that now bind
every row, and the portal renders both from the same source.

## Rules bound to each row

1. Exactly one status per row (D-012).
2. Exactly one evidence cell; `none` is a valid, explicit value (D-001).
3. A row without an evidence path may not carry `IMPLEMENTED` or `VERIFIED`.
4. `IMPLEMENTED` never implies `VERIFIED`; verification requires a test artefact.
5. Promotion of a row's status requires an ADR reference.

## Related registries

`registry/ECOSYSTEM-REGISTRY.md` · `registry/VULNERABILITY-REGISTRY.md` ·
`registry/CONTINUITY-MATRIX.md` · `registry/LEGAL-MATRIX.md` ·
`decisions/DECISION-REGISTRY.md`
""",
    )


def gen_manifest_and_report() -> None:
    (ROOT / "audit").mkdir(parents=True, exist_ok=True)
    manifest = """# CVLN Intelligence OS — Freeze Manifest
# Machine-readable companion to constitution/FREEZE-001.md.
version: "1.1"
label: "OS v1.1 - ARCHITECTURE BASELINE FROZEN"
predecessor: "OS v1.0 - TITAN FOUNDATION"
freeze_instrument: constitution/FREEZE-001.md
freeze_report: audit/FREEZE-REPORT-v1.1.md
canonical_store: markdown
database_as_source_of_truth: false
append_only: true
audited_repositories:
  - https://github.com/metacvln-spec/MetaCVLN
  - https://github.com/frekcore/CVLNAgentfactory/tree/CVLN-AGENT-FACTORY
  - https://github.com/cultureconnectorg/Laurent.ia/tree/public
status_vocabulary:
  - OBSERVED
  - DECIDED
  - IMPLEMENTED
  - VERIFIED
  - PROPOSED
  - TARGET
  - UNKNOWN
  - DEPRECATED
  - REJECTED
sections_added:
  - decisions
  - security
  - resilience
  - legal
  - proof
  - economics
  - registry
registries:
  ecosystem: registry/ECOSYSTEM-REGISTRY.md
  component: audit/COMPONENT-MATRIX.md
  vulnerability: registry/VULNERABILITY-REGISTRY.md
  continuity: registry/CONTINUITY-MATRIX.md
  legal: registry/LEGAL-MATRIX.md
  decisions: decisions/DECISION-REGISTRY.md
invariants:
  - id: INV-001
    rule: no row may carry IMPLEMENTED or VERIFIED without an evidence path
  - id: INV-002
    rule: every decision D-001..D-014 has an ADR document
  - id: INV-003
    rule: markdown remains the canonical store; no database mirrors the corpus
  - id: INV-004
    rule: the contradictions register is non-empty and C-002 remains open
  - id: INV-005
    rule: every document declares a status from the canonical vocabulary
  - id: INV-006
    rule: JCC is never described as currency or a payment instrument
  - id: INV-007
    rule: no v1.0 document was deleted
  - id: INV-008
    rule: every registry row has exactly one status cell
unverified_claims_policy: "IMPLEMENTED never implies VERIFIED"
"""
    (ROOT / "audit" / "freeze-manifest.yaml").write_text(manifest, encoding="utf-8")
    print("wrote audit/freeze-manifest.yaml")

    write(
        "audit/FREEZE-REPORT-v1.1.md",
        fm(
            "Freeze Report v1.1",
            "What v1.1 preserves, adds, freezes, verifies and leaves unverified.",
            "Whole corpus",
            "DECIDED",
            "GOVERNANCE",
        ),
        """# Freeze Report — OS v1.1 ARCHITECTURE BASELINE FROZEN

## 1. Preserved

The whole v1.0 corpus, unchanged: the forensic audit, component matrix, gap analysis,
contradictions register, constitution, architecture, protocols, API contracts,
specifications, RFCs and diagrams. Append-only rule D-005. No document was deleted,
moved or rewritten by the v1.1 operation.

## 2. Added

| Section | Content |
|---|---|
| `decisions/` | D-001…D-014 registry, one ADR per decision, ADR template |
| `constitution/FREEZE-001.md` | The freeze instrument |
| `security/` | Security baseline, zero-trust model, threat model |
| `resilience/` | Continuity model, offline profiles, power loss, recovery |
| `legal/` | Legal-by-design framework, lawful design space |
| `proof/` | Proof layer, EvidencePackage model, notarial boundary |
| `economics/` | CVE v1.2, JCC unit constraints, value-centric economics |
| `registry/` | Ecosystem, component, vulnerability, continuity and legal registries |
| `audit/` | This report and `freeze-manifest.yaml` |
| `rfc/` | RFC-0007 baseline freeze procedure |

## 3. Frozen

- Status vocabulary and the two non-implication rules (`IMPLEMENTED` ≠ `VERIFIED`,
  `CURRENT` ≠ `TARGET`).
- Layer responsibilities and the `Must Not Own` column of the ecosystem registry.
- The notarial boundary: digital evidence is in scope, legal attestation is not.
- JCC as an internal accounting unit only.
- Markdown as the sole canonical store.

## 4. Verified

Verification here means **asserted by an executable check**, not "believed correct".
`scripts/check_freeze_invariants.py` asserts INV-001…INV-008 over the corpus on demand,
and the portal recomputes every statistic from the files at request time — no dashboard
number is hardcoded.

## 5. Not verified — explicitly

| Claim | Why unverified |
|---|---|
| Gate enforcement actually blocks every critical action | No test artefact observed |
| Signed event verification rejects all tampering classes | No test corpus observed |
| Journals survive abrupt power loss | No test evidence (K-007, V-007) |
| Evidence package integrity end to end | Artefact not implemented (V-008) |
| Doctrine ownership | Contradiction C-002 remains open (D-011) |
| Any `TARGET` document in `security/`, `resilience/`, `legal/`, `proof/`, `economics/` | Specification only, no implementation |

## 6. Governance position

CVLN Brain remains `TARGET`: no dedicated repository was audited. FREKCORE remains
`UNKNOWN` in the technical corpus. Neither may be described as implemented.
""",
    )


def append_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    marker = "## v1.1"
    if marker in text:
        return
    entry = """
## v1.1 — ARCHITECTURE BASELINE FROZEN

Append-only upgrade of the v1.0 baseline, authorised by `constitution/FREEZE-001.md`
and `rfc/RFC-0007-BASELINE-FREEZE.md` (decision D-005).

- Added `decisions/` (D-001…D-014 with one ADR each), `security/`, `resilience/`,
  `legal/`, `proof/`, `economics/`, `registry/`.
- Added `audit/freeze-manifest.yaml` and `audit/FREEZE-REPORT-v1.1.md`.
- No v1.0 document deleted, moved or rewritten. This CHANGELOG entry is an append.
"""
    path.write_text(text.rstrip() + "\n" + entry, encoding="utf-8")
    print("appended CHANGELOG.md")


if __name__ == "__main__":
    gen_decisions()
    gen_freeze()
    gen_security()
    gen_resilience()
    gen_legal()
    gen_proof()
    gen_economics()
    gen_registries()
    gen_manifest_and_report()
    append_changelog()
    print("v1.1 corpus generated")
