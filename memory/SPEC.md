# CVLN Intelligence OS — Documentation Portal

## What this app is

A read-only documentation portal over the canonical Markdown repository at
`/app/cvln-intelligence-os` (87 documents). The Markdown files on disk are the
**single source of truth**. Nothing is duplicated into MongoDB; the backend parses the
files on request.

## Data model

No MongoDB collections are used by this feature. The corpus is the datastore.

- `backend/lib/corpus.py` — corpus reader. Path traversal is refused
  (`safe_path` restricts to `CVLN_CORPUS_ROOT`, default `/app/cvln-intelligence-os`,
  `.md` only). Front matter is parsed into metadata; the front-matter index is
  `lru_cache`d (call `reset_cache()` after editing the corpus, or restart the backend).
- `backend/models/docs.py` — Pydantic v2 models.
- `frontend/src/lib/types.ts` — hand-written TS mirrors. **Change both in one edit.**

## API (all on `api_router`, prefix `/api`)

| Endpoint | Returns |
|---|---|
| `GET /api/docs/tree` | Section-grouped document index + `total_documents` |
| `GET /api/docs/file?path=<rel>` | Document metadata, raw Markdown, headings. 400 on traversal, 404 on missing |
| `GET /api/docs/search?q=<term>` | Full-text hits with snippets (min 2 chars) |
| `GET /api/docs/matrix` | 45 component rows parsed from `audit/COMPONENT-MATRIX.md` |
| `GET /api/docs/gaps` | 20 gap rows parsed from `audit/GAP-ANALYSIS.md` |
| `GET /api/docs/stats` | Status/severity distributions, contradiction count |

The matrix and gap endpoints parse the first Markdown pipe table with ≥11 / ≥10
columns. **If those tables' column counts change, the parsers break** — keep the
column count stable.

## Key flows

1. **Browse** — `/` overview → sidebar tree → `/doc?path=<rel>`. Relative `.md` links
   inside documents are resolved against the current document's directory and routed
   client-side.
2. **Search** — header input or `/search?q=`.
3. **Component matrix** — `/matrix`, filter by status and repository, sort by
   component/repository/status, evidence paths deep-link to GitHub.
4. **Gap analysis** — `/gaps`, filter by severity and "founder decision required".
5. **Current vs target** — `/architecture`, two Mermaid diagrams plus an edge delta table.

## Auth

None. The portal is entirely public and read-only. No accounts, no PIN, no gated area.

## Content rules the UI enforces

- `PROPOSED` always renders with a **dashed** border plus a "TARGET SPEC" warning
  block on the document header, so a proposal can never read as an existing capability.
- Status colour never carries meaning alone — the literal status label is always shown.
- ISA and MCL are `PROPOSED`; ADL is `IMPLEMENTED`. Do not change these without an RFC.

## Stack notes

- Fonts: IBM Plex Sans / IBM Plex Mono via `@fontsource`, imported at the top of
  `src/index.css`. Bespoke keyframes `cvln-reveal` and `cvln-scan` are declared there.
- Markdown: `react-markdown` + `remark-gfm`; ```mermaid fences render through
  `src/components/Mermaid.tsx` (mermaid v11, `startOnLoad: false`, dark theme).
- Corpus generators live in `/app/scripts/gen_*.py`. They **overwrite** corpus files;
  edit the generator, or the Markdown, but do not re-run generators after hand-editing
  Markdown.

---

## v1.1 — ARCHITECTURE BASELINE FROZEN (append-only upgrade)

Corpus: 126 Markdown documents (87 v1.0 preserved verbatim + 39 added). Markdown remains
the sole canonical store; no MongoDB collection mirrors it.

### Added corpus sections
`decisions/` (D-001…D-014 registry, 14 ADRs + template), `registry/` (ecosystem,
component wrapper, vulnerability, continuity, legal), `security/`, `resilience/`,
`legal/`, `proof/`, `economics/`, plus `constitution/FREEZE-001.md`,
`audit/freeze-manifest.yaml`, `audit/FREEZE-REPORT-v1.1.md`, `audit/v10-inventory.txt`,
`rfc/RFC-0007-BASELINE-FREEZE.md`, and an appended `CHANGELOG.md` entry.

### Generators / checkers
- `scripts/gen_v11_freeze.py` — regenerates the v1.1 documents (never touches v1.0).
- `scripts/check_freeze_invariants.py` — runs INV-001…INV-008, exit 1 on violation.
- `backend/lib/invariants.py` — the invariant implementations (shared with the API).

### New API (all on `api_router`, prefix `/api`)
| Endpoint | Returns |
|---|---|
| `GET /api/docs/registries` | Descriptor per registry (key, title, source, row count, columns) |
| `GET /api/docs/registry/{key}` | Registry table: columns, rows, status column index. 404 on unknown key |
| `GET /api/docs/freeze` | Freeze manifest + live counts + INV-001…INV-008 verdicts |
| `GET /api/docs/graph` | Traceability nodes/edges derived from registries at request time |
| `GET /api/docs/stats` | Extended: `os_version`, `section_counts`, `registry_rows`, `total_decisions`, `invariants_passed/total` |

Registry keys: `ecosystem`, `component`, `vulnerability`, `continuity`, `legal`, `decisions`.
Models `backend/models/freeze.py` ↔ TS `frontend/src/lib/freezeTypes.ts` (hand-mirrored).

### New portal views
`/freeze` (freeze report + invariant verdicts), `/decisions` (D-001…D-014 cards → ADR),
`/registry/:key` (tabbed registries, status + text filters), `/graph` (Mermaid
traceability graph with node-kind filters). Nav entries: Freeze v1.1, Decisions,
Registries, Traceability.

### Frozen rules enforced by the UI and the checker
- `IMPLEMENTED` never implies `VERIFIED`; `CURRENT` never implies `TARGET`.
- New dimensions ship as `TARGET`/`PROPOSED`/`UNKNOWN` — never `IMPLEMENTED`.
- JCC is an internal accounting unit only (INV-006 rejects any currency affirmation).
- Contradiction C-002 (doctrine ownership) stays open (INV-004).
- v1.0 inventory of 87 paths must remain present (INV-007).
- Status vocabulary: OBSERVED, DECIDED, IMPLEMENTED, VERIFIED, PROPOSED, TARGET,
  UNKNOWN, DEPRECATED, REJECTED (+ legacy v1.0 tokens PARTIAL, DEFINED, REFERENCED,
  PRIVATE / NOT VISIBLE).

No auth, no credentials: the portal stays public and read-only.
