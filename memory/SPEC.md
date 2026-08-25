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
