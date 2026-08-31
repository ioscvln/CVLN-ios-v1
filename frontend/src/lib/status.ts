// Status and severity tokens. Colour never carries meaning alone: every token pairs a
// hue with its literal label, and PROPOSED additionally uses a dashed border so a
// planned capability can never read as an existing one.

export const STATUS_TOKENS: Record<string, string> = {
  IMPLEMENTED: "bg-emerald-950/70 text-emerald-300 border-emerald-800/80",
  PARTIAL: "bg-blue-950/70 text-blue-300 border-blue-800/80",
  DEFINED: "bg-violet-950/70 text-violet-300 border-violet-800/80",
  REFERENCED: "bg-cyan-950/70 text-cyan-300 border-cyan-800/80",
  "PRIVATE / NOT VISIBLE": "bg-slate-800/70 text-slate-300 border-slate-600/80",
  PROPOSED: "bg-amber-950/70 text-amber-300 border-amber-600/90 border-dashed",
  TARGET: "bg-fuchsia-950/70 text-fuchsia-300 border-fuchsia-700/90 border-dashed",
  DECIDED: "bg-sky-950/70 text-sky-300 border-sky-800/80",
  OBSERVED: "bg-teal-950/70 text-teal-300 border-teal-800/80",
  VERIFIED: "bg-green-950/70 text-green-300 border-green-700/80",
  HISTORICAL: "bg-stone-900/70 text-stone-300 border-stone-600/80 border-dotted",
  OPEN: "bg-orange-950/70 text-orange-300 border-orange-700/90 border-dashed",
  DEPRECATED: "bg-zinc-900/70 text-zinc-400 border-zinc-700/80",
  REJECTED: "bg-rose-950/70 text-rose-300 border-rose-800/80",
  UNKNOWN: "bg-neutral-900/70 text-neutral-400 border-neutral-700/80 border-dotted",
};

export const SEVERITY_TOKENS: Record<string, string> = {
  CRITICAL: "bg-rose-950/80 text-rose-300 border-rose-800",
  HIGH: "bg-orange-950/80 text-orange-300 border-orange-800",
  MEDIUM: "bg-amber-950/80 text-amber-300 border-amber-800",
  LOW: "bg-emerald-950/80 text-emerald-300 border-emerald-800",
  OPTIONAL: "bg-indigo-950/80 text-indigo-300 border-indigo-800",
};

export const STATUS_ORDER = [
  "IMPLEMENTED",
  "PARTIAL",
  "DEFINED",
  "REFERENCED",
  "PRIVATE / NOT VISIBLE",
  "PROPOSED",
  "TARGET",
  "OPEN",
  "HISTORICAL",
  "UNKNOWN",
];

export const SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "OPTIONAL"];

export const REPO_URLS: Record<string, string> = {
  META: "https://github.com/metacvln-spec/MetaCVLN",
  FACTORY: "https://github.com/frekcore/CVLNAgentfactory/tree/CVLN-AGENT-FACTORY",
  LAUR: "https://github.com/cultureconnectorg/Laurent.ia/tree/public",
};

export const REPO_LABELS: Record<string, string> = {
  META: "MetaCVLN",
  FACTORY: "CVLNAgentfactory",
  LAUR: "Laurent.ia",
};

export function statusToken(status: string): string {
  return STATUS_TOKENS[status.trim().toUpperCase()] ?? STATUS_TOKENS.UNKNOWN;
}

export function severityToken(severity: string): string {
  return SEVERITY_TOKENS[severity.trim().toUpperCase()] ?? SEVERITY_TOKENS.OPTIONAL;
}

/** Deep link an evidence path back into the audited repository, when resolvable. */
export function evidenceUrl(repository: string, path: string): string | null {
  const base = REPO_URLS[repository.trim().toUpperCase()];
  if (!base || !path || path === "none" || path.trim() === "—") return null;
  if (!path.includes("/") && !path.endsWith(".py") && !path.endsWith(".md")) return base;
  const branchless = base.replace(/\/tree\/[^/]+$/, (m) => m);
  return base.includes("/tree/")
    ? `${branchless.replace("/tree/", "/blob/")}/${path.trim()}`
    : `${base}/blob/main/${path.trim()}`;
}
