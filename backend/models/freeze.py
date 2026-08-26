"""v1.1 baseline-freeze models. Mirrored by hand in frontend/src/lib/types.ts."""
from pydantic import BaseModel


class RegistryDescriptor(BaseModel):
    key: str
    title: str
    source: str
    total: int
    columns: list[str]


class RegistryTable(BaseModel):
    key: str
    title: str
    source: str
    note: str
    columns: list[str]
    rows: list[list[str]]
    total: int
    status_column: int


class RegistryList(BaseModel):
    version: str
    registries: list[RegistryDescriptor]


class Invariant(BaseModel):
    id: str
    rule: str
    passed: bool
    detail: str


class FreezeState(BaseModel):
    version: str
    label: str
    predecessor: str
    freeze_instrument: str
    freeze_report: str
    canonical_store: str
    database_as_source_of_truth: bool
    append_only: bool
    audited_repositories: list[str]
    status_vocabulary: list[str]
    sections_added: list[str]
    total_documents: int
    total_decisions: int
    total_registry_rows: int
    invariants: list[Invariant]


class GraphNode(BaseModel):
    id: str
    label: str
    kind: str
    status: str


class GraphEdge(BaseModel):
    source: str
    target: str
    kind: str


class TraceGraph(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    total_nodes: int
    total_edges: int
