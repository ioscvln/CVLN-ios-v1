// Hand-written mirrors of backend/models/freeze.py.
// Nothing infers across the boundary — change both files in the same edit.

export interface RegistryDescriptor {
  key: string;
  title: string;
  source: string;
  total: number;
  columns: string[];
}

export interface RegistryTable {
  key: string;
  title: string;
  source: string;
  note: string;
  columns: string[];
  rows: string[][];
  total: number;
  status_column: number;
}

export interface RegistryList {
  version: string;
  registries: RegistryDescriptor[];
}

export interface Invariant {
  id: string;
  rule: string;
  passed: boolean;
  detail: string;
}

export interface FreezeState {
  version: string;
  label: string;
  predecessor: string;
  freeze_instrument: string;
  freeze_report: string;
  canonical_store: string;
  database_as_source_of_truth: boolean;
  append_only: boolean;
  audited_repositories: string[];
  status_vocabulary: string[];
  sections_added: string[];
  total_documents: number;
  total_decisions: number;
  total_registry_rows: number;
  invariants: Invariant[];
}

export interface GraphNode {
  id: string;
  label: string;
  kind: string;
  status: string;
}

export interface GraphEdge {
  source: string;
  target: string;
  kind: string;
}

export interface TraceGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  total_nodes: number;
  total_edges: number;
}
