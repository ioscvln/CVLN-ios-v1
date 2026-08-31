"""Drift, evidence-package export and system-card models.
Mirrored by hand in frontend/src/lib/insightTypes.ts."""
from pydantic import BaseModel


class BaselineInfo(BaseModel):
    id: str
    label: str
    created: str
    provenance: str
    total_rows: int


class DriftRow(BaseModel):
    registry: str
    row_id: str
    change: str  # added | removed | status_changed | unchanged_adr_missing
    base_status: str
    target_status: str
    adr: str
    promotion: bool
    promotion_without_adr: bool
    advisory: bool


class DriftReport(BaseModel):
    base: BaselineInfo
    target: BaselineInfo
    rows: list[DriftRow]
    total_compared: int
    added: int
    removed: int
    status_changed: int
    promotions: int
    promotions_without_adr: int
    advisories: int
    verdict: str


class EvidenceArtefact(BaseModel):
    path: str
    sha256: str
    bytes: int


class EvidenceClaim(BaseModel):
    statement: str
    status: str
    evidence: str


class AnchorRecord(BaseModel):
    digest: str
    subject: str
    provider: str
    provider_label: str
    status: str  # pending | confirmed | offline | unavailable
    calendar: str | None
    created_at: str
    upgraded_at: str | None
    attempts: int
    detail: str
    proof_file: str | None
    qualified_timestamp: bool


class AnchorVerification(BaseModel):
    digest: str
    parsed: bool
    bound_to_digest: bool
    detail: str


class AnchorProviders(BaseModel):
    providers: dict[str, str]
    calendars: list[str]
    disclaimer: str


class EvidencePackage(BaseModel):
    package_id: str
    subject: str
    baseline: str
    generated_at: str
    claims: list[EvidenceClaim]
    artefacts: list[EvidenceArtefact]
    decisions: list[str]
    chain_hash: str
    signature: str
    signature_algorithm: str
    public_key: str
    anchored_at: str | None
    anchor: AnchorRecord | None
    anchor_proof_ots_base64: str | None
    legal_effect: str
    verification: str


class SystemSummary(BaseModel):
    name: str
    layer: str
    role: str
    status: str
    evidence: str
    components: int
    vulnerabilities: int
    decisions: int


class SystemCard(BaseModel):
    name: str
    layer: str
    role: str
    repository: str
    evidence: str
    status: str
    owns: str
    must_not_own: str
    components: list[list[str]]
    component_columns: list[str]
    vulnerabilities: list[list[str]]
    vulnerability_columns: list[str]
    decisions: list[list[str]]
    decision_columns: list[str]
    relations: list[list[str]]
    relation_columns: list[str]
    documents: list[str]
