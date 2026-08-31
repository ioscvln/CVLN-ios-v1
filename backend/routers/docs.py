from collections import Counter

from fastapi import APIRouter, HTTPException, Query

from lib import corpus, invariants
from routers.freeze import REGISTRIES, _load
from models.docs import (
    ComponentMatrix,
    ComponentRow,
    DocDetail,
    DocMeta,
    DocTree,
    GapAnalysis,
    GapRow,
    SearchResponse,
    SectionNode,
    StatusCount,
    StatusStats,
)

router = APIRouter(prefix="/docs", tags=["docs"])

OS_VERSION = "OS v1.1 — ARCHITECTURE BASELINE FROZEN"

SECTION_LABELS = {
    "root": "Repository",
    "decisions": "Decisions · ADR",
    "registry": "Registries",
    "kiltikonet": "Kiltikonet",
    "security": "Security",
    "resilience": "Resilience & Continuity",
    "legal": "Legal-by-Design",
    "proof": "Intelligent Proof",
    "economics": "Economic Intelligence",
    "audit": "Phase 0–4 · Forensic Audit",
    "constitution": "Constitution",
    "architecture": "Architecture",
    "protocols": "Protocols",
    "api-contracts": "API Contracts",
    "specifications": "Specifications",
    "rfc": "RFC",
    "diagrams": "Diagrams",
}

MATRIX_PATH = "audit/COMPONENT-MATRIX.md"
GAP_PATH = "audit/GAP-ANALYSIS.md"
CONTRADICTIONS_PATH = "audit/CONTRADICTIONS.md"


@router.get("/tree", response_model=DocTree)
async def get_tree() -> DocTree:
    index = corpus.corpus_index()
    grouped: dict[str, list[DocMeta]] = {}
    for entry in index:
        grouped.setdefault(entry["section"], []).append(DocMeta(**entry))
    order = ["root"] + corpus.SECTION_ORDER
    sections = [
        SectionNode(
            section=name,
            label=SECTION_LABELS.get(name, name),
            documents=grouped[name],
        )
        for name in order
        if name in grouped
    ]
    return DocTree(version=OS_VERSION, total_documents=len(index), sections=sections)


@router.get("/file", response_model=DocDetail)
async def get_file(path: str = Query(..., min_length=3)) -> DocDetail:
    try:
        data = corpus.read_doc(path)
    except ValueError:
        raise HTTPException(status_code=400, detail="invalid corpus path")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"document not found: {path}")
    return DocDetail(**data)


@router.get("/search", response_model=SearchResponse)
async def search_docs(q: str = Query(..., min_length=2)) -> SearchResponse:
    results = corpus.search(q)
    return SearchResponse(query=q, total=len(results), results=results)


@router.get("/matrix", response_model=ComponentMatrix)
async def get_matrix() -> ComponentMatrix:
    rows = corpus.parse_table(MATRIX_PATH, min_columns=11)
    if len(rows) < 2:
        raise HTTPException(status_code=500, detail="component matrix table not parseable")
    parsed = [
        ComponentRow(
            component=r[0],
            repository=r[1],
            path=r[2],
            conceptual_responsibility=r[3],
            actual_implementation=r[4],
            evidence=r[5],
            status=r[6],
            dependencies=r[7],
            consumers=r[8],
            providers=r[9],
            notes=r[10],
        )
        for r in rows[1:]
    ]
    return ComponentMatrix(source=MATRIX_PATH, total=len(parsed), rows=parsed)


@router.get("/gaps", response_model=GapAnalysis)
async def get_gaps() -> GapAnalysis:
    rows = corpus.parse_table(GAP_PATH, min_columns=10)
    if len(rows) < 2:
        raise HTTPException(status_code=500, detail="gap table not parseable")
    parsed = [
        GapRow(
            id=r[0],
            gap=r[1],
            severity=r[2],
            current_state=r[3],
            desired_state=r[4],
            evidence=r[5],
            impact=r[6],
            depends_on=r[7],
            recommended_action=r[8],
            founder_decision=r[9],
        )
        for r in rows[1:]
    ]
    return GapAnalysis(source=GAP_PATH, total=len(parsed), rows=parsed)


@router.get("/stats", response_model=StatusStats)
async def get_stats() -> StatusStats:
    index = corpus.corpus_index()
    doc_counter = Counter(e["status"] for e in index)

    matrix = await get_matrix()
    comp_counter = Counter(r.status for r in matrix.rows)

    gaps = await get_gaps()
    sev_counter = Counter(r.severity for r in gaps.rows)

    contradictions = sum(
        1
        for line in (corpus.CORPUS_ROOT / CONTRADICTIONS_PATH)
        .read_text(encoding="utf-8")
        .splitlines()
        if line.startswith("## C-")
    )

    def to_counts(counter: Counter) -> list[StatusCount]:
        return [
            StatusCount(status=k, count=v)
            for k, v in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ]

    section_counter = Counter(e["section"] for e in index)
    inv = invariants.run_all()
    registry_rows = sum(_load(key).total for key in REGISTRIES)

    return StatusStats(
        os_version=OS_VERSION,
        total_documents=len(index),
        total_components=matrix.total,
        document_status=to_counts(doc_counter),
        component_status=to_counts(comp_counter),
        gap_severity=to_counts(sev_counter),
        contradictions=contradictions,
        section_counts=to_counts(section_counter),
        registry_rows=registry_rows,
        total_decisions=_load("decisions").total,
        invariants_passed=sum(1 for i in inv if i["passed"]),
        invariants_total=len(inv),
    )
