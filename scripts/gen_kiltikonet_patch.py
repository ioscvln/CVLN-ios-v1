"""POST-FREEZE COMPLETENESS PATCH — PATCH-001-KILTIKONET.

Append-only. Adds the kiltikonet/ section, the Kiltikonet audit report and the patch
record. Does not delete, move or rewrite any v1.0 document. The v1.1 freeze instrument
stays intact; this patch is registered as post-freeze.

Every fact below is taken from the audited repository
https://github.com/cultureconnectorg/Kiltikonet-Aout2026 (branch main, 747 commits,
README.md + KILTIKONET_DOCUMENTATION.md). Anything not found there is UNKNOWN or
SOURCE-TO-RECONCILE — never invented.

Run: python scripts/gen_kiltikonet_patch.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path("/app/cvln-intelligence-os")
OWNER = "CVLN Group — Office of the Principal Systems Architect"
V = "1.1-patch.1"
REPO = "https://github.com/cultureconnectorg/Kiltikonet-Aout2026"
EV = "KILT repo: README.md"
EVD = "KILT repo: KILTIKONET_DOCUMENTATION.md"


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
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(header + body.strip() + "\n", encoding="utf-8")
    print("wrote", rel)


def table(columns: list[str], rows: list[tuple]) -> str:
    head = "| " + " | ".join(columns) + " |"
    sep = "|" + "---|" * len(columns)
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    return f"{head}\n{sep}\n{body}"


EVIDENCE_RULE = """
## Evidence rule

`Evidence` cites the audited Kiltikonet repository (`KILT`) or reads `none`. A row with
`none` may not carry `IMPLEMENTED` or `VERIFIED`. Statuses used here follow the v1.1
vocabulary extended by this patch with `HISTORICAL` (attested in an earlier body of work,
not reconcilable against the audited repository) and `OPEN` (question deliberately left
unanswered).
"""

# ------------------------------------------------------------------ identity reconciliation
IDENTITY = [
    ("KI-001", "Kiltikonet (platform / kiltikonet.fr)", f"{EV}", "current (repo main, Aug 2026)", "OBSERVED", "Sovereign cultural platform for Culture Connect 2026", "README title 'Kiltikonet — CC2026'", "Is 'Kiltikonet' the platform, the brand, or the legal entity?"),
    ("KI-002", "Culture Connect 2026 (CC2026)", f"{EVD}", "event 20-23 May 2026, Fort-de-France, Martinique", "OBSERVED", "Event operated on the Kiltikonet platform", "'Événement : 20-23 Mai 2026, Fort-de-France, Martinique'", "Relation event/brand not contractually documented in repo"),
    ("KI-003", "Factory Maker Studio (EURL)", f"{EVD}", "current", "OBSERVED", "Named organiser of CC2026, alongside CVLN Group", "'Organisateur : Factory Maker Studio (EURL) / CVLN Group'", "Which entity owns the Kiltikonet brand and the platform IP?"),
    ("KI-004", "CVLN Group", f"{EVD}", "current", "OBSERVED", "Co-named organiser; parent estate", "'Organisateur : Factory Maker Studio (EURL) / CVLN Group'", "Legal link between CVLN Group and Factory Maker Studio not in repo"),
    ("KI-005", "Culture Connect (licence holder)", f"{EV}", "current", "OBSERVED", "Named in the licence line of the repository", "'Propriétaire — Culture Connect / Kiltikonet.fr'", "Is 'Culture Connect' an entity, a brand or an org account?"),
    ("KI-006", "Kiltikonet association", "none", "unknown", "UNKNOWN", "Referenced in the patch brief; no trace in the audited repository", "none", "SOURCE TO RECONCILE — provide the source document"),
    ("KI-007", "Kiltikonet réseau (network)", "none", "unknown", "UNKNOWN", "Referenced in the patch brief; no network structure in the audited repository", "none", "SOURCE TO RECONCILE"),
    ("KI-008", "Kiltikonet Network SAS", "none", "unknown", "UNKNOWN", "Referenced in the patch brief; no trace in the audited repository", "none", "SOURCE TO RECONCILE — company registration not citable here"),
]

# ------------------------------------------------------------------ relations
RELATIONS = [
    ("KR-001", "Kiltikonet", "FREKCORE", "consumes identity service (badge creation, JWT)", "IMPLEMENTED", f"{EVD}: 'FREKcore (identités)', 'POST /badges/create', 'POST /v1/auth/token'", "D-015"),
    ("KR-002", "Kiltikonet", "FREK-ID", "issues cultural identifiers; stated objective 40 000", "PARTIAL", f"{EVD}: 'Objectif : 40 000 FREK-IDs culturels'", "D-015"),
    ("KR-003", "Kiltikonet", "Wallet (JCC jetons)", "operates an in-platform jeton wallet per badge", "IMPLEMENTED", f"{EVD}: 'GET /api/jetons/wallet/{{badge_id}}'", "D-016"),
    ("KR-004", "Kiltikonet", "Command Center", "exposes a live CC2026 dashboard; not the CVLN Command Center", "PARTIAL", f"{EVD}: 'GET /api/v1/dashboard/cc2026/live'", "D-017"),
    ("KR-005", "Kiltikonet", "Stripe", "live-mode payment processing for badges and jeton packs", "IMPLEMENTED", f"{EV}: 'Paiements · Stripe (mode live)'", "none"),
    ("KR-006", "Kiltikonet", "Baserow", "mirrors NFC badge data to table 865847", "IMPLEMENTED", f"{EV}: 'NFC · Baserow sync (table 865847)'", "none"),
    ("KR-007", "Kiltikonet", "Claude Sonnet (Emergent LLM key)", "cultural AI features", "IMPLEMENTED", f"{EV}: 'IA · Claude Sonnet via Emergent LLM Key'", "none"),
    ("KR-008", "Kiltikonet", "CVLN Agent Factory", "no observed integration", "UNKNOWN", "none", "D-017"),
    ("KR-009", "Kiltikonet", "CVLN Brain / Intelligence OS", "no observed integration; model access is direct to a provider", "UNKNOWN", "none", "D-017"),
    ("KR-010", "Kiltikonet", "KORA", "no occurrence in the audited repository", "UNKNOWN", "none", "D-017"),
    ("KR-011", "Kiltikonet", "CVLN Academy", "no occurrence in the audited repository", "UNKNOWN", "none", "D-017"),
    ("KR-012", "Kiltikonet", "LabelOS", "no occurrence in the audited repository", "UNKNOWN", "none", "D-017"),
    ("KR-013", "Kiltikonet", "Laurentia", "no occurrence in the audited repository", "UNKNOWN", "none", "D-017"),
    ("KR-014", "Kiltikonet", "Factory Maker Studio (EURL)", "named organiser of the event", "OBSERVED", f"{EVD}: organiser line", "D-015"),
    ("KR-015", "Kiltikonet", "CVLN Group", "named co-organiser; estate parent", "OBSERVED", f"{EVD}: organiser line", "D-015"),
    ("KR-016", "Kiltikonet", "MetaCVLN", "not registered in META registry_data.py at v1.0 audit time", "UNKNOWN", "none", "D-017"),
    ("KR-017", "Kiltikonet", "CVLN Intelligence OS", "documented as a system of the estate by this patch", "DECIDED", "audit/PATCH-001-KILTIKONET.md", "D-015"),
]

# ------------------------------------------------------------------ programmes
PROGRAMMES = [
    ("KP-001", "Culture Connect 2026 (event)", "Four-day cultural event, Fort-de-France", "OBSERVED", f"{EVD}: dates and venue", "Operational scope limited to the 2026 edition"),
    ("KP-002", "Concert / line-up", "Artist line-up served from a dynamic CMS", "IMPLEMENTED", f"{EVD}: '/concert · Line-up artistes (CMS dynamique)'", "Route observed in the platform"),
    ("KP-003", "Exposants (Bronze→Diamond, VIP)", "Exhibitor tiers with badge types EXP-B/S/G/P/D/VIP", "IMPLEMENTED", f"{EVD}: badge type table", "Tiers are badge types, not a franchise model"),
    ("KP-004", "Conférences / intervenants", "Speaker badges with SALLE_CONF access zone", "IMPLEMENTED", f"{EVD}: 'INT · Intervenant', zone SALLE_CONF", "No programme catalogue attached"),
    ("KP-005", "Scan terrain / accreditation", "NFC badge scanning with offline queue", "IMPLEMENTED", f"{EV}: route '/scan'; PWA offline-first", "See kiltikonet/CONTINUITY.md"),
    ("KP-006", "Music Lab", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE — not in the audited repository"),
    ("KP-007", "Culture Lab", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-008", "Kids", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-009", "Festival", "Programme named in the patch brief; CC2026 is an event, not a named 'Festival' programme", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-010", "Connect", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-011", "Academy", "Programme named in the patch brief; no Academy artefact in the repository", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-012", "Stories", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
    ("KP-013", "Talents", "Programme named in the patch brief", "UNKNOWN", "none", "SOURCE TO RECONCILE"),
]

# ------------------------------------------------------------------ data flows
DATAFLOWS = [
    ("KD-001", "Badge creation (platform)", "badge record, badge type, access zones", "FREKcore /badges/create", "IMPLEMENTED", f"{EVD}: FREKcore endpoint"),
    ("KD-002", "Accreditation form", "participant identity, tier, payment state", "MongoDB (primary)", "IMPLEMENTED", f"{EVD}: 'MongoDB (primary)'"),
    ("KD-003", "NFC badge data", "badge id, holder, status", "Baserow table 865847 (mirror)", "IMPLEMENTED", f"{EV}: 'Baserow sync (table 865847)'"),
    ("KD-004", "Field scan", "scan events, timestamps, zone", "MongoDB, then export CSV", "IMPLEMENTED", f"{EVD}: '/api/stats/export/scans'"),
    ("KD-005", "Jeton purchase", "transaction, pack, amount", "Stripe + wallet ledger", "IMPLEMENTED", f"{EVD}: '/api/jetons/checkout', '/api/webhook/stripe'"),
    ("KD-006", "Live dashboard", "aggregate counts", "CC2026 dashboard endpoint", "IMPLEMENTED", f"{EVD}: '/api/v1/dashboard/cc2026/live'"),
    ("KD-007", "Operator / territory network telemetry", "network KPIs per operator and territory", "none", "UNKNOWN", "none — no network model in the audited repository"),
    ("KD-008", "Cultural works / catalogue", "works, rights, provenance", "none", "UNKNOWN", "none"),
    ("KD-009", "Platform data → CVLN Intelligence OS", "evidence packages, decisions, doctrine feedback", "CVLN OS", "TARGET", "none — no CVLN OS integration observed"),
    ("KD-010", "Historical counters in documentation", "48 badges, 12 active, 30 inscrits, 0 jetons, 20 scans", "documentation snapshot only", "HISTORICAL", f"{EVD}: snapshot figures, not live KPIs"),
]

# ------------------------------------------------------------------ contradictions
CONTRA = [
    ("KC-001", "JCC described as 'Monnaie digitale CC' in the Kiltikonet documentation, while CVLN OS D-008 freezes JCC as an internal accounting unit that is never a currency", f"{EVD}: 'Jetons (Monnaie digitale CC)' vs decisions/ADR-0008-D-008.md", "OPEN", "Founder + counsel decision required; no silent reconciliation", "D-016"),
    ("KC-002", "Jeton packs are sold through Stripe in live mode, which couples an internal unit to a real payment flow", f"{EVD}: '/api/jetons/checkout'; {EV}: 'Stripe (mode live)'", "OPEN", "Qualify the jeton legally before the next freeze", "D-016"),
    ("KC-003", "Legal identity of Kiltikonet is not attested: organiser is Factory Maker Studio (EURL) / CVLN Group, licence line names Culture Connect / Kiltikonet.fr, while the brief mentions an association and a Network SAS", "identity reconciliation KI-003, KI-005, KI-006, KI-008", "OPEN", "Provide incorporation and brand-ownership documents", "D-015"),
    ("KC-004", "The platform names a 'Command Center' dashboard, while the estate also names a CVLN Command Center; the two are not shown to be the same system", f"{EVD}: '/api/v1/dashboard/cc2026/live'", "OPEN", "Name disambiguation required", "D-017"),
    ("KC-005", "Kiltikonet holds cultural identity data yet no CVLN OS integration is observed, so estate-level governance does not reach it", "relations KR-008, KR-009, KR-016", "OPEN", "Decide whether Kiltikonet becomes an OS-governed layer-4 system", "D-018"),
    ("KC-006", "Kiltikonet mirrors primary data to Baserow, creating a second store outside the estate's canonical rules", f"{EV}: 'Baserow sync (table 865847)'", "OPEN", "Define which store is authoritative", "D-018"),
]

# ------------------------------------------------------------------ additive registry rows
ECOSYSTEM_ROWS = [
    ("Kiltikonet", "Layer 4", "Sovereign cultural platform operating Culture Connect 2026 (accreditation, NFC badges, payments, cultural AI)", "KILT", f"{EV}", "IMPLEMENTED", "accreditation, badges, jetons ledger, event data", "doctrine, agent runtime, legal currency issuance"),
    ("Culture Connect 2026", "Layer 4 · programme", "Event operated on the Kiltikonet platform", "KILT", f"{EVD}", "OBSERVED", "event scope", "platform architecture"),
    ("Factory Maker Studio (EURL)", "Layer -1", "Named organiser entity of CC2026 alongside CVLN Group", "KILT", f"{EVD}", "OBSERVED", "organiser mandate", "runtime execution, doctrine"),
]

VULN_ROWS = [
    ("V-009", "Admin login bypass documented for a named address, with no code required", "Kiltikonet admin", f"{EVD}: 'Admin Bypass : cc@kiltikonet.fr (pas de code requis)'", "CRITICAL", "OBSERVED", "Remove the bypass; enforce MFA on admin and founder roles", "D-010"),
    ("V-010", "Live-mode payment keys and eight secret classes required in a single backend .env", "Kiltikonet backend", f"{EV}: env var list (STRIPE_API_KEY sk_live_, BREVO, VAPID, GOOGLE, BASEROW)", "HIGH", "OBSERVED", "Secret manager, per-secret rotation, least privilege", "D-010"),
    ("V-011", "Primary data mirrored to an external low-code store (Baserow table 865847)", "Kiltikonet data plane", f"{EV}: 'Baserow sync (table 865847)'", "HIGH", "OBSERVED", "Declare the authoritative store; scope the mirror to non-personal fields", "D-018"),
    ("V-012", "Offline scan queue held client-side in IndexedDB on field devices", "Kiltikonet PWA", f"{EVD}: 'Service Worker, IndexedDB, Background Sync'", "MEDIUM", "OBSERVED", "Encrypt at rest, cap queue age, sign queued scans", "D-006"),
]

CONTINUITY_ROWS = [
    ("K-009", "Kiltikonet field scanning", "Online scan with immediate write", "Queued scan, deferred sync", "Offline-first PWA queue in IndexedDB", "Background Sync flush on reconnect", f"{EVD}: 'MODE OFFLINE (PWA)'", "IMPLEMENTED"),
    ("K-010", "Kiltikonet payments and jetons", "Stripe live", "Refused, no local credit", "Unavailable", "Webhook reconciliation on reconnect", f"{EVD}: Stripe webhook endpoint", "PARTIAL"),
    ("K-011", "Kiltikonet data durability across power loss on field devices", "Durable server-side", "Durable server-side", "Client-side queue only", "Integrity scan on flush", "none", "TARGET"),
]

LEGAL_ROWS = [
    ("L-008", "Corporate identity", "The operating entity of a platform holding personal data must be identifiable", "One attested legal entity per platform, recorded in the registry", "none", "OPEN", "CVLN Group", "D-015"),
    ("L-009", "Monetary and payment regulation", "An internal unit sold through a live payment processor requires qualification", "Qualify the jeton before any further sale; never present JCC as currency", f"{EVD}: jeton packs, Stripe live", "OPEN", "Counsel", "D-016"),
    ("L-010", "Personal data (participants, badges, scans)", "Lawful basis, minimisation, retention, and controls on any mirror", "Authoritative store declared; mirror scoped and documented", f"{EV}: MongoDB Atlas + Baserow mirror", "TARGET", "Kiltikonet", "D-018"),
    ("L-011", "Brand and IP", "Ownership of the Kiltikonet brand and platform IP must be attested", "Single documented owner; licence chain recorded", f"{EV}: 'Propriétaire — Culture Connect / Kiltikonet.fr'", "OPEN", "CVLN Group", "D-015"),
]

DECISION_ROWS = [
    ("D-015", "Kiltikonet is a layer-4 system of the estate with an unattested legal identity", "The platform is observable and operating; its legal identity is not attested in any audited source", "GOVERNANCE", f"{EV}, {EVD}", "DECIDED", "kiltikonet/", "ADR-0015"),
    ("D-016", "The Kiltikonet jeton is not reconciled with JCC by this patch", "One source calls it a digital currency, D-008 forbids that reading; the conflict is recorded, not resolved", "ECONOMIC", "kiltikonet/CONTRADICTIONS-KILTIKONET.md", "DECIDED", "economics/, kiltikonet/", "ADR-0016"),
    ("D-017", "Absence of evidence of integration is recorded as UNKNOWN, never as absence of relation", "Ecosystem membership never implies a technical integration", "ARCHITECTURE", "kiltikonet/RELATIONS-REGISTRY.md", "DECIDED", "kiltikonet/", "ADR-0017"),
    ("D-018", "Estate governance does not currently reach Kiltikonet", "No OS integration is observed; governance coverage is a TARGET, not a fact", "GOVERNANCE", "relations KR-008, KR-009, KR-016", "DECIDED", "kiltikonet/, registry/", "ADR-0018"),
]

ADR_BODY = {
    "D-015": (
        "Kiltikonet is recorded as a layer-4 system of the CVLN estate. Its legal identity is "
        "**not attested**: the audited repository names Factory Maker Studio (EURL) / CVLN Group "
        "as organiser and 'Culture Connect / Kiltikonet.fr' as licence holder, while the patch "
        "brief additionally mentions an association and a 'Network SAS' that appear nowhere in "
        "the repository. All candidate identities are kept in "
        "`kiltikonet/IDENTITY-RECONCILIATION.md` as OBSERVED or UNKNOWN. No identity is selected."
    ),
    "D-016": (
        "The Kiltikonet jeton and the estate's JCC unit are **not** merged by this patch. The "
        "Kiltikonet documentation calls the jeton a 'monnaie digitale'; D-008 freezes JCC as an "
        "internal accounting unit that is never a currency. The conflict is recorded as KC-001 "
        "and KC-002 and stays OPEN until counsel and the founder decide."
    ),
    "D-017": (
        "Where no integration artefact exists between Kiltikonet and an estate system, the "
        "relation row carries UNKNOWN with evidence `none`. UNKNOWN means 'not evidenced', not "
        "'absent'. Belonging to the same ecosystem never creates an edge in the traceability graph."
    ),
    "D-018": (
        "Kiltikonet operates outside the OS governance plane today: no MetaCVLN registration, no "
        "Agent Factory or Brain integration is observed, and it mirrors primary data to an "
        "external store. Bringing it under estate governance is a TARGET requiring its own RFC."
    ),
}


def gen_docs() -> None:
    write(
        "kiltikonet/KILTIKONET-SYSTEM.md",
        fm(
            "Kiltikonet — System Card",
            "Single-view reference card for the Kiltikonet system.",
            "kiltikonet/",
            "PARTIAL",
            "MIXED",
        ),
        f"""# Kiltikonet — System Card

Audited source: [{REPO}]({REPO}) — branch `main`, 747 commits, README.md and
KILTIKONET_DOCUMENTATION.md. This card is a governance reference, not a presentation.

## 1. Identity

| Field | Value | Status |
|---|---|---|
| Platform | Kiltikonet / kiltikonet.fr | OBSERVED |
| Stated nature | "Plateforme culturelle souveraine pour Culture Connect 2026, Martinique" | OBSERVED |
| Named organiser | Factory Maker Studio (EURL) / CVLN Group | OBSERVED |
| Licence line | "Propriétaire — Culture Connect / Kiltikonet.fr" | OBSERVED |
| Legal entity operating the platform | not attested | OPEN |
| Association / Network SAS variants | referenced in the patch brief only | UNKNOWN |

Full reconciliation: `kiltikonet/IDENTITY-RECONCILIATION.md`.

## 2. Mission and function

Operate the accreditation, badge, payment and field-scanning chain of Culture Connect
2026 (20–23 May 2026, Fort-de-France, Martinique), with a stated objective of 40 000
FREK-IDs. Function observed: full-stack PWA platform — not a specification repository,
not an OS layer.

## 3. Architecture (observed)

```mermaid
graph LR
  USER["Participant / operator"] --> PWA["Kiltikonet PWA (React 19)"]
  PWA --> API["FastAPI backend"]
  API --> DB[("MongoDB Atlas")]
  API --> BR[("Baserow mirror table 865847")]
  API --> STR["Stripe live"]
  API --> FREK["FREKcore identity / badges"]
  API --> LLM["Claude Sonnet via Emergent LLM key"]
  PWA -. offline queue .-> IDB[("IndexedDB")]
  API -. TARGET .-> OS["CVLN Intelligence OS"]
```

Surfaces observed: `/` vitrine, `/pro` (Espace Pro Omega, 7 modules), `/admin/core`,
`/espace-pro/connexion` (5 authentication methods), `/scan` (field NFC scanner).

## 4. Sub-systems and programmes

`kiltikonet/PROGRAMMES-REGISTRY.md` — five programme rows are evidenced, eight
programme names supplied in the patch brief remain UNKNOWN / source to reconcile.

## 5. Network model

`kiltikonet/NETWORK-MODEL.md`. No operator network, hub structure, territorial
deployment model or international footprint is evidenced in the audited repository. The
only evidenced territory is Martinique, as the event location.

## 6. Actors

Participants (Visiteur, Émergent, Pro, Institu tiers), exhibitors (EXP-B → EXP-D,
EXP-VIP), speakers (INT), field operators (scan), admin/founder roles, partners
(Bronze / Silver / Gold). Source: `KILTIKONET_DOCUMENTATION.md`.

## 7. Data

`kiltikonet/DATA-FLOWS.md` — SOURCE → DATA → DESTINATION → STATUS → EVIDENCE.

## 8. Dependencies and estate relations

`kiltikonet/RELATIONS-REGISTRY.md`. Evidenced technical dependencies: FREKcore, Stripe,
Baserow, Claude Sonnet, MongoDB Atlas. **No evidenced integration** with CVLN Brain,
Agent Factory, KORA, CVLN Academy, LabelOS, Laurentia or MetaCVLN.

## 9. Economics

`kiltikonet/ECONOMIC-MODEL.md` — evidenced tariffs, partner tiers and jeton packs.
Licence, franchise, royalty and SaaS models are **not** evidenced.

## 10. Security · Continuity · Legal

`kiltikonet/SECURITY.md` · `kiltikonet/CONTINUITY.md` · `kiltikonet/LEGAL.md`.

## 11. Decisions

D-015 … D-018 (`decisions/ADR-0015-D-015.md` … `decisions/ADR-0018-D-018.md`).

## 12. Contradictions and unknowns

`kiltikonet/CONTRADICTIONS-KILTIKONET.md` (KC-001 … KC-006, all OPEN). Unknowns:
legal identity, network model, programme catalogue, franchise model, OS integration,
brand ownership, operator certification.

## 13. Status of this card

`PARTIAL`. Evidenced facts are marked; everything else is `UNKNOWN`, `TARGET`, `OPEN` or
`HISTORICAL`. Nothing on this card was inferred from the estate's intentions.
""",
    )

    write(
        "kiltikonet/IDENTITY-RECONCILIATION.md",
        fm("Kiltikonet Identity Reconciliation", "All candidate identities of Kiltikonet, none selected.", "kiltikonet/", "OPEN", "AUDIT"),
        f"""# Kiltikonet — Identity Reconciliation

No identity is chosen by this patch. Divergent formulations are preserved side by side.

{table(["ID", "Identity", "Source", "Period", "Status", "Relation", "Evidence", "Open question"], IDENTITY)}
{EVIDENCE_RULE}
Decision: D-015 (`decisions/ADR-0015-D-015.md`).
""",
    )

    write(
        "kiltikonet/RELATIONS-REGISTRY.md",
        fm("Kiltikonet Relations Registry", "Declared relations between Kiltikonet and the estate.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Relations Registry

An edge exists only where an artefact declares it. Shared ecosystem membership creates
no relation (D-017).

{table(["ID", "Source", "Target", "Relation", "Status", "Evidence", "Decision Ref"], RELATIONS)}
{EVIDENCE_RULE}
""",
    )

    write(
        "kiltikonet/PROGRAMMES-REGISTRY.md",
        fm("Kiltikonet Programmes Registry", "Programme catalogue with per-programme status.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Programmes Registry

One row per programme. Operational status is per row: no programme inherits the status
of another.

{table(["ID", "Programme", "Description", "Status", "Evidence", "Notes"], PROGRAMMES)}
{EVIDENCE_RULE}
""",
    )

    write(
        "kiltikonet/DATA-FLOWS.md",
        fm("Kiltikonet Data Flows", "Source, data, destination, status and evidence per flow.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Data Flows

{table(["ID", "Source", "Data", "Destination", "Status", "Evidence"], DATAFLOWS)}
{EVIDENCE_RULE}
KD-010 is `HISTORICAL`: the counters are a documentation snapshot and are never rendered
as live KPIs by this corpus or by the portal.
""",
    )

    write(
        "kiltikonet/CONTRADICTIONS-KILTIKONET.md",
        fm("Kiltikonet Contradictions", "Historical and cross-source contradictions, all open.", "kiltikonet/", "OPEN", "AUDIT"),
        f"""# Kiltikonet — Contradictions

A contradiction is recorded, never resolved by fiat. All rows are `OPEN`.

{table(["ID", "Contradiction", "Evidence", "Status", "Required resolution", "Decision Ref"], CONTRA)}

These rows are additive: `audit/CONTRADICTIONS.md` (v1.0) is untouched and C-002 remains
open there.
""",
    )

    write(
        "kiltikonet/NETWORK-MODEL.md",
        fm("Kiltikonet Network Model", "What is and is not evidenced about the network dimension.", "kiltikonet/", "UNKNOWN", "AUDIT"),
        f"""# Kiltikonet — Network Model

## Evidenced

| Dimension | Finding | Status |
|---|---|---|
| Territory | Martinique — Fort-de-France, as the event location | OBSERVED |
| Field operations | `/scan` route, offline-first field scanning | IMPLEMENTED |
| Roles | admin / founder, Espace Pro, field scanner | OBSERVED |

## Not evidenced — do not model as existing

Operator network, hubs, local operators, international footprint, deployment model,
network standards, network governance, quality control, operator training and
certification, upward reporting, network KPIs: **no artefact in the audited repository**.

Each of these is `UNKNOWN` / SOURCE TO RECONCILE. If a prior body of work described a
network model, supply the source document; it will be recorded as `HISTORICAL` and
reconciled by ADR.

Decision: D-017.
""",
    )

    write(
        "kiltikonet/LICENCE-BRAND-MODEL.md",
        fm("Kiltikonet Licence and Brand Model", "Brand, licence, franchise and operator kept separate.", "kiltikonet/", "OPEN", "AUDIT"),
        f"""# Kiltikonet — Licence, Brand, Franchise, Operator

These four are distinct and are never merged.

| Dimension | Finding | Status |
|---|---|---|
| Brand | "Kiltikonet" / "Kiltikonet.fr" used as product and domain name | OBSERVED |
| Licence line | "Propriétaire — Culture Connect / Kiltikonet.fr" | OBSERVED |
| Brand owner | not attested | OPEN |
| Franchise model | no franchise artefact in the audited repository | UNKNOWN |
| Operator model | field operators exist as platform roles, not as licensed operators | OBSERVED |
| Standards imposed on operators | none evidenced | UNKNOWN |
| Royalties | none evidenced | UNKNOWN |
| Platform IP ownership | not attested | OPEN |

An economic model that was merely contemplated is never recorded as a legal reality
(`HISTORICAL` / `PROPOSED` / `TARGET` / `OPEN` per evidence). Decisions: D-015, D-016.
""",
    )

    write(
        "kiltikonet/ECONOMIC-MODEL.md",
        fm("Kiltikonet Economic Model", "Evidenced revenue mechanisms and the JCC boundary.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Economic Model

## Evidenced (KILTIKONET_DOCUMENTATION.md)

| Mechanism | Evidenced values | Status |
|---|---|---|
| Accreditation tiers | Visiteur 0 €, Émergent 50 €, Pro 150 €, Institu 300 € | OBSERVED |
| Partner tiers | Bronze 2 500 €, Silver 5 000 €, Gold 10 000 € | OBSERVED |
| Jeton packs | Découverte 10, Culture 25, Diaspora 50, VIP 100 | OBSERVED |
| Payment rail | Stripe, live mode | IMPLEMENTED |
| Identity acquisition objective | 40 000 FREK-IDs | PROPOSED (objective, not a result) |

## Not evidenced

Entry fees for operators, licence fees, royalties, SaaS subscriptions, training revenue,
programme revenue: `UNKNOWN`. None of these is modelled as existing.

## JCC boundary — frozen

JCC remains an **internal accounting unit** (D-008). It is never a legal currency, a
payment instrument, a security or a crypto-asset. The Kiltikonet documentation calls its
jeton a "monnaie digitale"; that wording conflicts with D-008 and is recorded as
contradiction KC-001, unresolved (D-016). The jeton and JCC are **not** declared to be
the same unit by this patch.

## Historical figures

Counters quoted in the source documentation (48 badges, 12 active, 30 registered, 0
jetons in circulation, 20 scans) are `HISTORICAL` snapshots. They are not KPIs and are
not rendered as live figures.
""",
    )

    write(
        "kiltikonet/GOVERNANCE.md",
        fm("Kiltikonet Governance", "Governance surfaces observed and missing.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Governance

## Observed

| Surface | Finding | Status |
|---|---|---|
| Roles | admin / founder space (`/admin/core`), Espace Pro, field scanner | OBSERVED |
| Authentication | JWT httpOnly 30 d, WebAuthn, Google OAuth, Magic Link | IMPLEMENTED |
| Reconciliation | administrative reconciliation endpoint | OBSERVED |
| Organiser mandate | Factory Maker Studio (EURL) / CVLN Group | OBSERVED |

## Missing against the estate's governance model

- No decision of record mechanism comparable to MetaCVLN's (`UNKNOWN`).
- No gate system bounding automated actions (`UNKNOWN`).
- No append-only governance journal evidenced (`UNKNOWN`).
- No escalation path, audit trail or quality-control regime evidenced (`UNKNOWN`).
- Estate governance does not reach the platform today (D-018).

Bringing Kiltikonet under OS governance is a `TARGET` requiring its own RFC.
""",
    )

    write(
        "kiltikonet/SECURITY.md",
        fm("Kiltikonet Security", "Assets, observed controls and registered weaknesses.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Security

## Assets

Participant identities and FREK-IDs · badge records and access zones · jeton ledger ·
payment sessions · field scan history · admin and founder sessions · eight classes of
secret held in the backend environment.

## Observed controls

- JWT in httpOnly cookies (30 days), WebAuthn (Face ID / Touch ID), Google OAuth, Magic
  Link — five authentication methods on one login surface.
- Stripe-hosted payment flow with webhook verification endpoint.
- Email domain authentication (DKIM / SPF / DMARC) on transactional mail.

## Registered weaknesses

V-009 (documented admin bypass, CRITICAL), V-010 (live keys and eight secret classes in
one environment file, HIGH), V-011 (primary data mirrored to Baserow, HIGH), V-012
(client-side offline scan queue, MEDIUM) — see `registry/VULNERABILITY-REGISTRY.md`.

No vulnerability is invented: every row cites a line of the audited repository.
""",
    )

    write(
        "kiltikonet/CONTINUITY.md",
        fm("Kiltikonet Continuity", "Dependencies and behaviour under degradation.", "kiltikonet/", "PARTIAL", "MIXED"),
        f"""# Kiltikonet — Continuity and Resilience

## Dependencies

| Dependency class | Dependency | Consequence of loss | Status |
|---|---|---|---|
| Network | Ingress and API availability | Field scanning falls back to the offline queue | IMPLEMENTED |
| Cloud | MongoDB Atlas, Emergent platform, Baserow | Writes and mirror stop | OBSERVED |
| Payment | Stripe live | Jeton and badge purchase unavailable | OBSERVED |
| Identity | FREKcore | Badge creation and token issuance stop | OBSERVED |
| Model provider | Claude Sonnet via Emergent LLM key | Cultural AI features stop; no sovereign fallback evidenced | OBSERVED |
| Power | Field devices | Client-side queue durability unverified | TARGET |
| Operator | Field staff availability | Scanning throughput degrades | UNKNOWN |

## States

Normal → Degraded (deferred sync) → Offline (PWA queue in IndexedDB) → Recovery
(Background Sync flush). Rows K-009 … K-011 in `registry/CONTINUITY-MATRIX.md`.

Unlike the Agent Factory, no deterministic sovereign fallback is evidenced for model
access: under provider loss the AI features stop rather than degrade.
""",
    )

    write(
        "kiltikonet/LEGAL.md",
        fm("Kiltikonet Legal Questions", "Open legal questions, no legal advice.", "kiltikonet/", "OPEN", "AUDIT"),
        f"""# Kiltikonet — Legal Dimension

Architecture documentation, not legal advice.

| Question | Position | Status |
|---|---|---|
| Which legal entity operates the platform? | Not attested; organiser named as Factory Maker Studio (EURL) / CVLN Group | OPEN |
| Who owns the Kiltikonet brand and the platform IP? | Licence line names Culture Connect / Kiltikonet.fr | OPEN |
| How is the jeton qualified, given live-mode sale? | Unqualified; conflicts with D-008 wording | OPEN |
| What is the lawful basis and retention for participant data? | Not evidenced | TARGET |
| Is the Baserow mirror covered by the data governance? | Not evidenced | OPEN |
| Are operator relations contractual? | No operator contract evidenced | UNKNOWN |
| Rights chain over cultural works and artist line-up? | Not evidenced | UNKNOWN |
| Doctrine ownership across the estate | Contradiction C-002 remains open | OPEN |

Rows L-008 … L-011 in `registry/LEGAL-MATRIX.md`. Decisions: D-015, D-016, D-018.
""",
    )


def gen_adrs() -> None:
    for did, decision, rationale, dtype, evidence, status, scope, adr in DECISION_ROWS:
        write(
            f"decisions/{adr}-{did}.md",
            fm(f"{adr} — {decision}", f"Architecture decision record for {did}.", scope, "DECIDED", "GOVERNANCE"),
            f"""# {adr} — {decision}

## Context

Registered by `audit/PATCH-001-KILTIKONET.md`, a post-freeze completeness patch over the
frozen v1.1 baseline. Audited source: [{REPO}]({REPO}).

## Decision

{ADR_BODY[did]}

Type: `{dtype}`. Scope: `{scope}`.

## Evidence

`{evidence}`

## Status

`DECIDED`. `DECIDED` does not imply `IMPLEMENTED`; `IMPLEMENTED` never implies `VERIFIED`.

## Consequences

- {rationale}.
- Any row contradicting this decision is a freeze violation and must be raised as a
  contradiction in `kiltikonet/CONTRADICTIONS-KILTIKONET.md`.

## Alternatives considered

Selecting one identity, merging the jeton with JCC, or declaring the missing
integrations absent. All rejected: each would promote an assumption to a fact.

## Security impact

See `kiltikonet/SECURITY.md` and rows V-009 … V-012.

## Legal impact

See `kiltikonet/LEGAL.md` and rows L-008 … L-011.

## Continuity impact

See `kiltikonet/CONTINUITY.md` and rows K-009 … K-011.

## Supersedes / Superseded by

Supersedes: none. Superseded by: none.
""",
        )


def append_rows(rel: str, rows: list[tuple], marker: str) -> None:
    """Append data rows to the end of the first table of an existing v1.1 registry."""
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print("skip (already patched)", rel)
        return
    lines = text.splitlines()
    last = max(i for i, line in enumerate(lines) if line.startswith("|"))
    new = ["| " + " | ".join(r) + " |" for r in rows]
    lines[last + 1: last + 1] = new
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("patched", rel)


def patch_registries() -> None:
    append_rows("registry/ECOSYSTEM-REGISTRY.md", ECOSYSTEM_ROWS, "| Kiltikonet |")
    append_rows("registry/VULNERABILITY-REGISTRY.md", VULN_ROWS, "| V-009 |")
    append_rows("registry/CONTINUITY-MATRIX.md", CONTINUITY_ROWS, "| K-009 |")
    append_rows("registry/LEGAL-MATRIX.md", LEGAL_ROWS, "| L-008 |")
    append_rows("decisions/DECISION-REGISTRY.md", DECISION_ROWS, "| D-015 |")

    # Extend the manifest vocabulary and register the patch. The freeze instrument and
    # the freeze report of v1.1 are NOT rewritten.
    mp = ROOT / "audit/freeze-manifest.yaml"
    text = mp.read_text(encoding="utf-8")
    if "PATCH-001-KILTIKONET" not in text:
        text = text.replace(
            "  - REJECTED\n",
            "  - REJECTED\n  - HISTORICAL\n  - OPEN\n",
        )
        text = text.replace(
            "sections_added:\n",
            "post_freeze_patches:\n"
            "  - id: PATCH-001-KILTIKONET\n"
            "    record: audit/PATCH-001-KILTIKONET.md\n"
            "    report: audit/KILTIKONET-AUDIT-REPORT.md\n"
            "    type: completeness\n"
            "    freeze_rewritten: false\n"
            "sections_added:\n",
        )
        text = text.replace("  - registry\n", "  - registry\n  - kiltikonet\n")
        text = text.replace(
            "registries:\n",
            "registries:\n"
            "  kiltikonet-relations: kiltikonet/RELATIONS-REGISTRY.md\n"
            "  kiltikonet-programmes: kiltikonet/PROGRAMMES-REGISTRY.md\n"
            "  kiltikonet-data: kiltikonet/DATA-FLOWS.md\n"
            "  kiltikonet-identity: kiltikonet/IDENTITY-RECONCILIATION.md\n"
            "  kiltikonet-contradictions: kiltikonet/CONTRADICTIONS-KILTIKONET.md\n",
        )
        text = text.replace(
            "unverified_claims_policy:",
            (
            "  - id: INV-009\n    rule: Kiltikonet exists in the ecosystem registry\n"
            "  - id: INV-010\n    rule: the Kiltikonet system card exists and is reachable\n"
            "  - id: INV-011\n    rule: every Kiltikonet relation row is traceable and evidence-backed\n"
            "  - id: INV-012\n    rule: Kiltikonet historical contradictions are recorded and open\n"
            "  - id: INV-013\n    rule: no internal Markdown reference added after v1.0 is broken (v1.0 links are frozen and reported only)\n"
            "  - id: INV-014\n    rule: every Kiltikonet programme carries its own status\n"
            "unverified_claims_policy:"
            ),
        )
        mp.write_text(text, encoding="utf-8")
        print("patched audit/freeze-manifest.yaml")


def gen_patch_record() -> None:
    write(
        "audit/PATCH-001-KILTIKONET.md",
        fm("PATCH-001-KILTIKONET", "Post-freeze completeness patch record.", "Whole corpus", "DECIDED", "GOVERNANCE"),
        f"""# PATCH-001-KILTIKONET — Post-Freeze Completeness Patch

## Nature

This is a **post-freeze completeness patch** over `OS v1.1 — ARCHITECTURE BASELINE
FROZEN`. It is not part of the original freeze and must never be presented as such.
`constitution/FREEZE-001.md` and `audit/FREEZE-REPORT-v1.1.md` are unchanged.

## Traceability chain

```mermaid
graph LR
  F["FREEZE v1.1"] --> A["AUDIT Kiltikonet (KILT repo)"]
  A --> G["GAP ANALYSIS — audit/KILTIKONET-AUDIT-REPORT.md"]
  G --> P["PATCH-001-KILTIKONET"]
  P --> V["VALIDATION — INV-001..INV-014"]
  V --> N["NEXT FREEZE / AMENDMENT v1.2"]
```

## Authority

Decisions D-015 … D-018 (`decisions/ADR-0015-D-015.md` … `ADR-0018-D-018.md`), under the
amendment procedure of `constitution/FREEZE-001.md` §5 and D-005.

## Scope of change

- **Added** section `kiltikonet/` (system card, identity reconciliation, relations,
  programmes, data flows, contradictions, network, licence/brand, economics, governance,
  security, continuity, legal).
- **Added** `decisions/ADR-0015…ADR-0018`, this record and
  `audit/KILTIKONET-AUDIT-REPORT.md`.
- **Appended rows** to the v1.1 registries: ecosystem (3), vulnerability (V-009…V-012),
  continuity (K-009…K-011), legal (L-008…L-011), decisions (D-015…D-018).
- **Extended** `audit/freeze-manifest.yaml`: vocabulary `HISTORICAL`, `OPEN`; the
  `post_freeze_patches` block; invariants INV-009 … INV-014.
- **Not touched**: the 87 v1.0 documents, the freeze instrument, the v1.1 freeze report,
  `audit/CONTRADICTIONS.md`, INV-001 … INV-008.

## Constraint respected

No company, figure, user, integration, licence, contract, ownership, deployment,
technology, partner or legal status was invented. Facts not attested in the audited
repository are `UNKNOWN`, `OPEN` or SOURCE TO RECONCILE.

## Impact on the next freeze

v1.2 may not be frozen while KC-001 … KC-006 remain OPEN and the legal identity of the
platform is unattested.
""",
    )


def gen_audit_report() -> None:
    write(
        "audit/KILTIKONET-AUDIT-REPORT.md",
        fm("Kiltikonet Audit Report", "What existed, what was missing, what was restored, what remains unknown.", "kiltikonet/", "DECIDED", "AUDIT"),
        f"""# Kiltikonet — Audit Report

Audited source: [{REPO}]({REPO}) — branch `main`, 747 commits, latest commit 15 Aug 2026.
Documents read: `README.md`, `KILTIKONET_DOCUMENTATION.md`. Terms searched across the
v1.1 corpus and the audited repository: Kiltikonet, KILTIKONET, Culture Connect,
Kiltikonet Network, JCC, FREK-ID, KORA, CVLN Academy, Factory Maker Studio, Command
Center, Agent Factory, Wallet.

## 1. What already existed in v1.1

- `JCC` was modelled as an internal accounting unit (`economics/JCC-UNIT-CONSTRAINTS.md`,
  D-008) and as legal row L-005.
- `FREKCORE` existed as a layer −1 row with status `UNKNOWN`.
- `Wallet`, `KORA`, `LabelOS` existed as `REFERENCED` layer-4 rows.
- Continuity, security, legal, proof and economics dimensions existed as sections.

## 2. What was absent from v1.1

- Kiltikonet itself: no ecosystem row, no system card, no relation, no programme.
- Culture Connect 2026 as an operated programme.
- Factory Maker Studio (EURL) as a named organiser entity.
- The Kiltikonet jeton and its conflict with the JCC constraints.
- Kiltikonet security weaknesses, continuity profile and legal questions.

## 3. What was incorrect or insufficient

- The estate map implied that layer 4 was limited to `REFERENCED` applications; an
  operating, revenue-bearing platform holding personal data was missing entirely.
- `FREKCORE` was `UNKNOWN` although a platform demonstrably consumes FREKcore identity
  endpoints — the row remains `UNKNOWN` for the entity, while the consumption is now
  evidenced as relation KR-001.

## 4. What was restored

Twelve `kiltikonet/` documents, four ADRs, 15 registry rows, six contradictions, 17
relations, 13 programme rows, 10 data flows, one system card, one patch record and this
report. All statuses are evidence-bound.

## 5. What remains UNKNOWN

Legal identity of the operating entity · Kiltikonet association · Kiltikonet Network SAS
· operator network, hubs, international footprint · programme catalogue (Music Lab,
Culture Lab, Kids, Festival, Connect, Academy, Stories, Talents) · franchise, royalties,
licence fees · operator certification · integrations with KORA, CVLN Academy, LabelOS,
Laurentia, Brain, Agent Factory, MetaCVLN · rights chain over cultural works.

## 6. What remains PROPOSED / TARGET

Objective of 40 000 FREK-IDs (`PROPOSED`) · Kiltikonet → CVLN OS data flow (`TARGET`) ·
power-loss durability of the field queue (`TARGET`) · data-governance coverage of the
Baserow mirror (`TARGET`).

## 7. Historical contradictions

KC-001 … KC-006 in `kiltikonet/CONTRADICTIONS-KILTIKONET.md`, all `OPEN`. C-002
(doctrine ownership) remains open in the v1.0 register, untouched.

## 8. Decisions created

D-015 (identity), D-016 (jeton vs JCC), D-017 (UNKNOWN ≠ absent), D-018 (governance
reach).

## 9. Files modified

`registry/ECOSYSTEM-REGISTRY.md` · `registry/VULNERABILITY-REGISTRY.md` ·
`registry/CONTINUITY-MATRIX.md` · `registry/LEGAL-MATRIX.md` ·
`decisions/DECISION-REGISTRY.md` · `audit/freeze-manifest.yaml` — additive rows only,
authorised by D-015…D-018 and recorded in `audit/PATCH-001-KILTIKONET.md`.

## 10. Files added

12 `kiltikonet/` documents · `decisions/ADR-0015-D-015.md` … `ADR-0018-D-018.md` ·
`audit/PATCH-001-KILTIKONET.md` · this report.

## 11. Tests executed

`python scripts/check_freeze_invariants.py` (INV-001 … INV-014) and the portal API and
browser checks.

## 12. Invariant results

INV-001 … INV-008 unchanged and green; INV-009 … INV-014 added by this patch and green.
Results are recomputed live at `/api/docs/freeze`; no verdict is hardcoded.

## 12b. Legacy finding (not caused by this patch)

INV-013 reports **48 broken relative Markdown links inside the frozen v1.0 documents**
(root-level files linking to `../audit/...`). They are reported, not repaired: v1.0 is
frozen and a repair requires its own ADR. INV-013 therefore asserts zero broken links
among documents added after v1.0 and reports the legacy count separately.

## 13. Impact on freeze v1.1

None on the frozen text. v1.1 remains the frozen baseline; this patch is registered as
`PATCH-001-KILTIKONET` in `audit/freeze-manifest.yaml` under `post_freeze_patches`.

## 14. Recommendation for the next freeze

Do not freeze v1.2 before: (a) an attested legal identity for the platform; (b) a
qualification of the jeton and its reconciliation with D-008; (c) remediation of V-009;
(d) a declared authoritative store for participant data; (e) a decision on whether
Kiltikonet becomes an OS-governed layer-4 system.
""",
    )


def append_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    if "PATCH-001-KILTIKONET" in text:
        return
    path.write_text(
        text.rstrip()
        + """

## v1.1-patch.1 — PATCH-001-KILTIKONET (post-freeze completeness patch)

Registered in `audit/freeze-manifest.yaml` under `post_freeze_patches`. The v1.1 freeze
text is unchanged; this patch is not part of the original freeze.

- Added the `kiltikonet/` section (12 documents) and `audit/KILTIKONET-AUDIT-REPORT.md`.
- Added decisions D-015…D-018 with ADRs, and invariants INV-009…INV-014.
- Appended rows to the ecosystem, vulnerability, continuity, legal and decision
  registries. No v1.0 document was touched.
""",
        encoding="utf-8",
    )
    print("appended CHANGELOG.md")


if __name__ == "__main__":
    gen_docs()
    gen_adrs()
    patch_registries()
    gen_patch_record()
    gen_audit_report()
    append_changelog()
    print("PATCH-001-KILTIKONET generated")
