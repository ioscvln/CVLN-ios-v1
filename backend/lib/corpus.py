"""Read-only Markdown corpus reader.

The Markdown repository at CORPUS_ROOT is the canonical source of truth. Nothing here
writes to it and nothing is duplicated into MongoDB — the portal is a renderer only.
"""
from __future__ import annotations

import os
import re
from functools import lru_cache
from pathlib import Path

CORPUS_ROOT = Path(os.environ.get("CVLN_CORPUS_ROOT", "/app/cvln-intelligence-os")).resolve()

SECTION_ORDER = [
    "audit",
    "constitution",
    "decisions",
    "registry",
    "kiltikonet",
    "security",
    "resilience",
    "legal",
    "proof",
    "economics",
    "architecture",
    "protocols",
    "api-contracts",
    "specifications",
    "rfc",
    "diagrams",
]

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$", re.MULTILINE)
FENCE_RE = re.compile(r"```.*?```", re.DOTALL)


def safe_path(rel: str) -> Path:
    """Resolve a corpus-relative path, refusing traversal outside CORPUS_ROOT."""
    target = (CORPUS_ROOT / rel).resolve()
    if not str(target).startswith(str(CORPUS_ROOT)) or target.suffix != ".md":
        raise ValueError("path outside corpus")
    return target


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def slugify(heading: str) -> str:
    slug = re.sub(r"[^a-z0-9\s-]", "", heading.lower()).strip()
    return re.sub(r"\s+", "-", slug)


def all_docs() -> list[Path]:
    return sorted(CORPUS_ROOT.rglob("*.md"))


def rel(path: Path) -> str:
    return str(path.relative_to(CORPUS_ROOT))


def section_of(rel_path: str) -> str:
    head = rel_path.split("/")[0]
    return head if head in SECTION_ORDER else "root"


def _order(rel_path: str) -> tuple[int, str]:
    sec = section_of(rel_path)
    idx = SECTION_ORDER.index(sec) if sec in SECTION_ORDER else -1
    return (idx, rel_path)


@lru_cache(maxsize=1)
def corpus_index() -> list[dict[str, str]]:
    """Front matter for every document. Cached; call reset_cache() after a corpus edit."""
    entries: list[dict[str, str]] = []
    for path in all_docs():
        meta, _ = parse_front_matter(path.read_text(encoding="utf-8"))
        rel_path = rel(path)
        entries.append(
            {
                "path": rel_path,
                "section": section_of(rel_path),
                "title": meta.get("title") or path.stem,
                "purpose": meta.get("purpose", ""),
                "ownership": meta.get("ownership", ""),
                "scope": meta.get("scope", ""),
                "version": meta.get("version", ""),
                "status": meta.get("status", "UNKNOWN"),
                "attribution": meta.get("attribution", ""),
            }
        )
    entries.sort(key=lambda e: _order(e["path"]))
    return entries


def reset_cache() -> None:
    corpus_index.cache_clear()


def read_doc(rel_path: str) -> dict:
    path = safe_path(rel_path)
    raw = path.read_text(encoding="utf-8")
    meta, content = parse_front_matter(raw)
    stripped = FENCE_RE.sub("", content)
    headings = [
        {"level": len(h.group(1)), "text": h.group(2), "slug": slugify(h.group(2))}
        for h in HEADING_RE.finditer(stripped)
    ]
    return {
        "path": rel_path,
        "section": section_of(rel_path),
        "title": meta.get("title") or path.stem,
        "purpose": meta.get("purpose", ""),
        "ownership": meta.get("ownership", ""),
        "scope": meta.get("scope", ""),
        "version": meta.get("version", ""),
        "status": meta.get("status", "UNKNOWN"),
        "attribution": meta.get("attribution", ""),
        "content": content,
        "headings": headings,
        "word_count": len(content.split()),
    }


def search(query: str, limit: int = 60) -> list[dict]:
    needle = query.strip().lower()
    if len(needle) < 2:
        return []
    results: list[dict] = []
    for entry in corpus_index():
        text = (CORPUS_ROOT / entry["path"]).read_text(encoding="utf-8")
        lowered = text.lower()
        hits = lowered.count(needle)
        title_hit = needle in entry["title"].lower()
        if not hits and not title_hit:
            continue
        pos = lowered.find(needle)
        snippet = ""
        if pos >= 0:
            start = max(0, pos - 90)
            snippet = " ".join(text[start:pos + 160].split())
        results.append(
            {
                "path": entry["path"],
                "section": entry["section"],
                "title": entry["title"],
                "status": entry["status"],
                "hits": hits,
                "snippet": snippet,
            }
        )
    results.sort(key=lambda r: (r["hits"], r["title"]), reverse=True)
    return results[:limit]


def parse_table(rel_path: str, min_columns: int) -> list[list[str]]:
    """Extract the first Markdown pipe table with at least min_columns columns."""
    text = (CORPUS_ROOT / rel_path).read_text(encoding="utf-8")
    rows: list[list[str]] = []
    started = False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < min_columns:
                if started:
                    break
                continue
            if set("".join(cells)) <= set("-: "):
                continue
            rows.append(cells)
            started = True
        elif started:
            break
    return rows


# --- v1.1 baseline freeze -------------------------------------------------------------

FREEZE_MANIFEST = "audit/freeze-manifest.yaml"


def parse_registry(rel_path: str, min_columns: int = 6) -> tuple[list[str], list[list[str]]]:
    """First pipe table of a registry document: (header cells, data rows)."""
    rows = parse_table(rel_path, min_columns=min_columns)
    if not rows:
        return [], []
    return rows[0], rows[1:]


def read_manifest() -> dict:
    """Parse the machine-readable freeze manifest. Read-only, never written."""
    import yaml  # pyyaml ships with the backend venv

    text = (CORPUS_ROOT / FREEZE_MANIFEST).read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}
