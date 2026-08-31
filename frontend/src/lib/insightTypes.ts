// Hand-written mirrors of backend/models/insight.py.

export interface BaselineInfo {
  id: string;
  label: string;
  created: string;
  provenance: string;
  total_rows: number;
}

export interface DriftRow {
  registry: string;
  row_id: string;
  change: string;
  base_status: string;
  target_status: string;
  adr: string;
  promotion: boolean;
  promotion_without_adr: boolean;
  advisory: boolean;
}

export interface DriftReport {
  base: BaselineInfo;
  target: BaselineInfo;
  rows: DriftRow[];
  total_compared: number;
  added: number;
  removed: number;
  status_changed: number;
  promotions: number;
  promotions_without_adr: number;
  advisories: number;
  verdict: string;
}

export interface EvidenceArtefact {
  path: string;
  sha256: string;
  bytes: number;
}

export interface EvidenceClaim {
  statement: string;
  status: string;
  evidence: string;
}

export interface EvidencePackage {
  package_id: string;
  subject: string;
  baseline: string;
  generated_at: string;
  claims: EvidenceClaim[];
  artefacts: EvidenceArtefact[];
  decisions: string[];
  chain_hash: string;
  signature: string;
  signature_algorithm: string;
  public_key: string;
  anchored_at: string | null;
  anchor: AnchorRecord | null;
  anchor_proof_ots_base64: string | null;
  legal_effect: string;
  verification: string;
}

export interface AnchorRecord {
  digest: string;
  subject: string;
  provider: string;
  provider_label: string;
  status: string;
  calendar: string | null;
  created_at: string;
  upgraded_at: string | null;
  attempts: number;
  detail: string;
  proof_file: string | null;
  qualified_timestamp: boolean;
}

export interface AnchorVerification {
  digest: string;
  parsed: boolean;
  bound_to_digest: boolean;
  detail: string;
}

export interface AnchorProviders {
  providers: Record<string, string>;
  calendars: string[];
  disclaimer: string;
}

export interface SystemSummary {
  name: string;
  layer: string;
  role: string;
  status: string;
  evidence: string;
  components: number;
  vulnerabilities: number;
  decisions: number;
}

export interface SystemCard {
  name: string;
  layer: string;
  role: string;
  repository: string;
  evidence: string;
  status: string;
  owns: string;
  must_not_own: string;
  components: string[][];
  component_columns: string[];
  vulnerabilities: string[][];
  vulnerability_columns: string[];
  decisions: string[][];
  decision_columns: string[];
  relations: string[][];
  relation_columns: string[];
  documents: string[];
}
