from pydantic import BaseModel


class DocMeta(BaseModel):
    path: str
    section: str
    title: str
    purpose: str = ""
    ownership: str = ""
    scope: str = ""
    version: str = ""
    status: str = "UNKNOWN"
    attribution: str = ""


class Heading(BaseModel):
    level: int
    text: str
    slug: str


class DocDetail(DocMeta):
    content: str
    headings: list[Heading]
    word_count: int


class SectionNode(BaseModel):
    section: str
    label: str
    documents: list[DocMeta]


class DocTree(BaseModel):
    version: str
    total_documents: int
    sections: list[SectionNode]


class SearchHit(BaseModel):
    path: str
    section: str
    title: str
    status: str
    hits: int
    snippet: str


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchHit]


class ComponentRow(BaseModel):
    component: str
    repository: str
    path: str
    conceptual_responsibility: str
    actual_implementation: str
    evidence: str
    status: str
    dependencies: str
    consumers: str
    providers: str
    notes: str


class ComponentMatrix(BaseModel):
    source: str
    total: int
    rows: list[ComponentRow]


class GapRow(BaseModel):
    id: str
    gap: str
    severity: str
    current_state: str
    desired_state: str
    evidence: str
    impact: str
    depends_on: str
    recommended_action: str
    founder_decision: str


class GapAnalysis(BaseModel):
    source: str
    total: int
    rows: list[GapRow]


class StatusCount(BaseModel):
    status: str
    count: int


class StatusStats(BaseModel):
    os_version: str
    total_documents: int
    total_components: int
    document_status: list[StatusCount]
    component_status: list[StatusCount]
    gap_severity: list[StatusCount]
    contradictions: int
    section_counts: list[StatusCount]
    registry_rows: int
    total_decisions: int
    invariants_passed: int
    invariants_total: int
