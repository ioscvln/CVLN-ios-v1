// Hand-written mirrors of the Pydantic models in backend/models/docs.py.
// Nothing infers across the boundary — change both files in the same edit.

export interface DocMeta {
  path: string;
  section: string;
  title: string;
  purpose: string;
  ownership: string;
  scope: string;
  version: string;
  status: string;
  attribution: string;
}

export interface Heading {
  level: number;
  text: string;
  slug: string;
}

export interface DocDetail extends DocMeta {
  content: string;
  headings: Heading[];
  word_count: number;
}

export interface SectionNode {
  section: string;
  label: string;
  documents: DocMeta[];
}

export interface DocTree {
  version: string;
  total_documents: number;
  sections: SectionNode[];
}

export interface SearchHit {
  path: string;
  section: string;
  title: string;
  status: string;
  hits: number;
  snippet: string;
}

export interface SearchResponse {
  query: string;
  total: number;
  results: SearchHit[];
}

export interface ComponentRow {
  component: string;
  repository: string;
  path: string;
  conceptual_responsibility: string;
  actual_implementation: string;
  evidence: string;
  status: string;
  dependencies: string;
  consumers: string;
  providers: string;
  notes: string;
}

export interface ComponentMatrix {
  source: string;
  total: number;
  rows: ComponentRow[];
}

export interface GapRow {
  id: string;
  gap: string;
  severity: string;
  current_state: string;
  desired_state: string;
  evidence: string;
  impact: string;
  depends_on: string;
  recommended_action: string;
  founder_decision: string;
}

export interface GapAnalysis {
  source: string;
  total: number;
  rows: GapRow[];
}

export interface StatusCount {
  status: string;
  count: number;
}

export interface StatusStats {
  total_documents: number;
  total_components: number;
  document_status: StatusCount[];
  component_status: StatusCount[];
  gap_severity: StatusCount[];
  contradictions: number;
}
