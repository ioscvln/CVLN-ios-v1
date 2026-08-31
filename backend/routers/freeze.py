"""v1.1 baseline-freeze read-only endpoints. Mounted on api_router under /api."""
from fastapi import APIRouter, HTTPException

from lib import corpus, invariants
from models.freeze import (
    FreezeState,
    GraphEdge,
    GraphNode,
    Invariant,
    RegistryDescriptor,
    RegistryList,
    RegistryTable,
    TraceGraph,
)

router = APIRouter(prefix="/docs", tags=["freeze"])

OS_VERSION = "OS v1.1 — ARCHITECTURE BASELINE FROZEN"

REGISTRIES: dict[str, dict] = {
    "ecosystem": {
        "title": "Ecosystem Registry",
        "source": "registry/ECOSYSTEM-REGISTRY.md",
        "columns": 8,
        "note": "Systems of the estate. `Must Not Own` is binding.",
    },
    "component": {
        "title": "Component Registry",
        "source": "audit/COMPONENT-MATRIX.md",
        "columns": 11,
        "note": "v1.0 component matrix, preserved unchanged, governed by registry/COMPONENT-REGISTRY.md.",
    },
    "vulnerability": {
        "title": "Vulnerability Registry",
        "source": "registry/VULNERABILITY-REGISTRY.md",
        "columns": 8,
        "note": "OBSERVED weaknesses and TARGET controls. No row closes without remediation evidence.",
    },
    "continuity": {
        "title": "Continuity Matrix",
        "source": "registry/CONTINUITY-MATRIX.md",
        "columns": 8,
        "note": "Behaviour per capability across Normal, Degraded, Offline and Recovery.",
    },
    "legal": {
        "title": "Legal Matrix",
        "source": "registry/LEGAL-MATRIX.md",
        "columns": 8,
        "note": "Obligation domains mapped to design constraints. Architecture documentation, not legal advice.",
    },
    "kiltikonet-relations": {
        "title": "Kiltikonet Relations",
        "source": "kiltikonet/RELATIONS-REGISTRY.md",
        "columns": 7,
        "note": "An edge exists only where an artefact declares it. UNKNOWN means not evidenced, never absent (D-017).",
    },
    "kiltikonet-programmes": {
        "title": "Kiltikonet Programmes",
        "source": "kiltikonet/PROGRAMMES-REGISTRY.md",
        "columns": 6,
        "note": "One row per programme, one status per row. No programme inherits another's status.",
    },
    "kiltikonet-data": {
        "title": "Kiltikonet Data Flows",
        "source": "kiltikonet/DATA-FLOWS.md",
        "columns": 6,
        "note": "SOURCE to DATA to DESTINATION with status and evidence.",
    },
    "kiltikonet-identity": {
        "title": "Kiltikonet Identity Reconciliation",
        "source": "kiltikonet/IDENTITY-RECONCILIATION.md",
        "columns": 8,
        "note": "All candidate legal identities preserved side by side. None is selected by the patch.",
    },
    "kiltikonet-contradictions": {
        "title": "Kiltikonet Contradictions",
        "source": "kiltikonet/CONTRADICTIONS-KILTIKONET.md",
        "columns": 6,
        "note": "Recorded, never resolved by fiat. Every row stays OPEN until a decision closes it.",
    },
    "open-questions": {
        "title": "Open Questions",
        "source": "governance/OPEN-QUESTIONS.md",
        "columns": 9,
        "note": "Every open question, contradiction, unknown and undecided risk. Owner and Due are human-owned: UNASSIGNED and TBD mean exactly that.",
    },
    "decisions": {
        "title": "Decision Registry",
        "source": "decisions/DECISION-REGISTRY.md",
        "columns": 8,
        "note": "Foundational decisions D-001 to D-014, each with an ADR.",
    },
}

REPO_TO_SYSTEM = {
    "META": "MetaCVLN",
    "FACTORY": "CVLN Agent Factory",
    "LAUR": "Laurentia",
}


def _status_column(columns: list[str]) -> int:
    for i, c in enumerate(columns):
        if c.strip().lower() == "status":
            return i
    return -1


def _load(key: str) -> RegistryTable:
    spec = REGISTRIES.get(key)
    if spec is None:
        raise HTTPException(status_code=404, detail=f"unknown registry: {key}")
    columns, rows = corpus.parse_registry(spec["source"], min_columns=spec["columns"])
    if not columns or not rows:
        raise HTTPException(status_code=500, detail=f"registry table not parseable: {spec['source']}")
    return RegistryTable(
        key=key,
        title=spec["title"],
        source=spec["source"],
        note=spec["note"],
        columns=columns,
        rows=rows,
        total=len(rows),
        status_column=_status_column(columns),
    )


@router.get("/registries", response_model=RegistryList)
async def list_registries() -> RegistryList:
    out = []
    for key in REGISTRIES:
        table = _load(key)
        out.append(
            RegistryDescriptor(
                key=key,
                title=table.title,
                source=table.source,
                total=table.total,
                columns=table.columns,
            )
        )
    return RegistryList(version=OS_VERSION, registries=out)


@router.get("/registry/{key}", response_model=RegistryTable)
async def get_registry(key: str) -> RegistryTable:
    return _load(key)


@router.get("/freeze", response_model=FreezeState)
async def get_freeze() -> FreezeState:
    manifest = corpus.read_manifest()
    total_rows = 0
    for key in REGISTRIES:
        total_rows += _load(key).total
    decisions = _load("decisions").total
    return FreezeState(
        version=str(manifest.get("version", "1.1")),
        label=str(manifest.get("label", OS_VERSION)),
        predecessor=str(manifest.get("predecessor", "")),
        freeze_instrument=str(manifest.get("freeze_instrument", "")),
        freeze_report=str(manifest.get("freeze_report", "")),
        canonical_store=str(manifest.get("canonical_store", "markdown")),
        database_as_source_of_truth=bool(manifest.get("database_as_source_of_truth", False)),
        append_only=bool(manifest.get("append_only", True)),
        audited_repositories=list(manifest.get("audited_repositories", [])),
        status_vocabulary=list(manifest.get("status_vocabulary", [])),
        sections_added=list(manifest.get("sections_added", [])),
        total_documents=len(corpus.corpus_index()),
        total_decisions=decisions,
        total_registry_rows=total_rows,
        invariants=[Invariant(**i) for i in invariants.run_all()],
    )


@router.get("/graph", response_model=TraceGraph)
async def get_graph() -> TraceGraph:
    """Traceability graph derived from the registries at request time."""
    nodes: dict[str, GraphNode] = {}
    edges: list[GraphEdge] = []

    def add(node_id: str, label: str, kind: str, status: str) -> str:
        nodes.setdefault(node_id, GraphNode(id=node_id, label=label, kind=kind, status=status))
        return node_id

    eco = _load("ecosystem")
    for row in eco.rows:
        add(f"sys:{row[0]}", row[0], "system", row[eco.status_column])

    comp = _load("component")
    comp_names: list[str] = []
    for row in comp.rows:
        cid = add(f"comp:{row[0]}", row[0], "component", row[comp.status_column])
        comp_names.append(row[0])
        system = REPO_TO_SYSTEM.get(row[1].strip().upper())
        if system and f"sys:{system}" in nodes:
            edges.append(GraphEdge(source=cid, target=f"sys:{system}", kind="owned_by"))

    dec = _load("decisions")
    for row in dec.rows:
        add(f"dec:{row[0]}", f"{row[0]} {row[1]}", "decision", row[dec.status_column])

    vul = _load("vulnerability")
    for row in vul.rows:
        vid = add(f"vul:{row[0]}", f"{row[0]} {row[1][:48]}", "vulnerability", row[vul.status_column])
        ref = row[7].strip()
        if f"dec:{ref}" in nodes:
            edges.append(GraphEdge(source=vid, target=f"dec:{ref}", kind="governed_by"))

    cont = _load("continuity")
    for row in cont.rows:
        add(f"con:{row[0]}", f"{row[0]} {row[1]}", "continuity", row[cont.status_column])

    leg = _load("legal")
    for row in leg.rows:
        lid = add(f"leg:{row[0]}", f"{row[0]} {row[1]}", "legal", row[leg.status_column])
        ref = row[7].strip()
        if f"dec:{ref}" in nodes:
            edges.append(GraphEdge(source=lid, target=f"dec:{ref}", kind="governed_by"))

    kil = _load("kiltikonet-relations")
    for row in kil.rows:
        src = add(f"sys:{row[1]}", row[1], "system", "IMPLEMENTED")
        tgt_id = f"sys:{row[2]}"
        if tgt_id not in nodes:
            add(tgt_id, row[2], "kiltikonet-relation", row[kil.status_column])
        edges.append(
            GraphEdge(source=src, target=tgt_id, kind=f"{row[0]} {row[kil.status_column]}")
        )
        ref = row[6].strip()
        if f"dec:{ref}" in nodes:
            edges.append(GraphEdge(source=f"sys:{row[1]}", target=f"dec:{ref}", kind="governed_by"))

    gap_cols, gap_rows = corpus.parse_registry("audit/GAP-ANALYSIS.md", min_columns=10)
    for row in gap_rows:
        gid = add(f"gap:{row[0]}", f"{row[0]} {row[1][:48]}", "gap", row[2])
        for name in comp_names:
            if len(name) > 4 and name.lower() in row[1].lower():
                edges.append(GraphEdge(source=gid, target=f"comp:{name}", kind="affects"))
                break

    node_list = list(nodes.values())
    return TraceGraph(
        nodes=node_list,
        edges=edges,
        total_nodes=len(node_list),
        total_edges=len(edges),
    )
