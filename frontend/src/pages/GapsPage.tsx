import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { GapAnalysis, GapRow } from "@/lib/types";
import { StatusBadge } from "@/components/StatusBadge";
import { SEVERITY_ORDER } from "@/lib/status";

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="font-mono text-[9.5px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
        {label}
      </p>
      <p className="mt-0.5 text-[12.5px] leading-relaxed text-muted-foreground">{value}</p>
    </div>
  );
}

function GapCard({ row }: { row: GapRow }) {
  const founder = row.founder_decision.toLowerCase().startsWith("required");
  return (
    <li
      data-testid={`gap-card-${row.id}`}
      className="border border-border bg-card/30 p-4 transition-colors duration-150 hover:border-foreground/25"
    >
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-mono text-[11px] font-semibold text-foreground">{row.id}</span>
        <StatusBadge value={row.severity} kind="severity" testId={`gap-severity-${row.id}`} />
        {founder && (
          <span
            data-testid={`gap-founder-flag-${row.id}`}
            className="rounded border border-dashed border-amber-600/80 bg-amber-950/40 px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-amber-300"
          >
            Founder decision required
          </span>
        )}
        {row.depends_on !== "none" && (
          <span className="font-mono text-[10px] text-muted-foreground">
            depends on {row.depends_on}
          </span>
        )}
      </div>

      <p className="mt-2 text-[14px] font-medium text-foreground">{row.gap}</p>

      <div className="mt-3 grid grid-cols-1 gap-3 border-t border-border pt-3 sm:grid-cols-2">
        <Field label="Current state" value={row.current_state} />
        <Field label="Desired state" value={row.desired_state} />
        <Field label="Evidence" value={row.evidence} />
        <Field label="Impact" value={row.impact} />
      </div>

      <div className="mt-3 border-t border-border pt-3">
        <Field label="Recommended action" value={row.recommended_action} />
      </div>
    </li>
  );
}

export default function GapsPage() {
  const [severity, setSeverity] = useState<string | null>(null);
  const [founderOnly, setFounderOnly] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ["docs", "gaps"],
    queryFn: () => apiGet<GapAnalysis>("/docs/gaps"),
  });

  const rows = useMemo(() => {
    let out = [...(data?.rows ?? [])];
    if (severity) out = out.filter((r) => r.severity.toUpperCase() === severity);
    if (founderOnly)
      out = out.filter((r) => r.founder_decision.toLowerCase().startsWith("required"));
    out.sort(
      (a, b) =>
        SEVERITY_ORDER.indexOf(a.severity.toUpperCase()) -
        SEVERITY_ORDER.indexOf(b.severity.toUpperCase()),
    );
    return out;
  }, [data, severity, founderOnly]);

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Phase 4 · Gap analysis
      </p>
      <h1 data-testid="gaps-title" className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
        Gap Analysis
      </h1>
      <p className="mt-2 max-w-[80ch] text-[13.5px] leading-relaxed text-muted-foreground">
        The distance between the current state and the target architecture. No gap is listed to
        make the audit appear thorough. Canonical source:{" "}
        <Link
          to="/doc?path=audit/GAP-ANALYSIS.md"
          data-testid="gaps-source-link"
          className="font-mono text-[12.5px] text-sky-400 hover:text-sky-300"
        >
          {data?.source ?? "audit/GAP-ANALYSIS.md"}
        </Link>
        .
      </p>

      <div className="mt-5 flex flex-wrap items-center gap-1.5">
        <button
          data-testid="severity-filter-all"
          onClick={() => setSeverity(null)}
          className={`rounded border px-2 py-1 font-mono text-[10px] uppercase tracking-[0.09em] transition-colors duration-150 ${
            severity === null
              ? "border-primary bg-primary/20 text-sky-300"
              : "border-border text-muted-foreground hover:text-foreground"
          }`}
        >
          All ({data?.total ?? 0})
        </button>
        {SEVERITY_ORDER.map((s) => {
          const count = (data?.rows ?? []).filter((r) => r.severity.toUpperCase() === s).length;
          if (count === 0) return null;
          return (
            <button
              key={s}
              data-testid={`severity-filter-${s.toLowerCase()}`}
              onClick={() => setSeverity(severity === s ? null : s)}
              className={`transition-opacity duration-150 ${severity && severity !== s ? "opacity-40" : ""}`}
            >
              <StatusBadge value={`${s} · ${count}`} kind="severity" />
            </button>
          );
        })}
        <button
          data-testid="founder-only-toggle"
          onClick={() => setFounderOnly((v) => !v)}
          className={`ml-2 rounded border px-2 py-1 font-mono text-[10px] uppercase tracking-[0.09em] transition-colors duration-150 ${
            founderOnly
              ? "border-amber-600 bg-amber-950/50 text-amber-300"
              : "border-border text-muted-foreground hover:text-foreground"
          }`}
        >
          Founder decision only
        </button>
      </div>

      {isLoading ? (
        <p data-testid="gaps-loading" className="mt-8 font-mono text-xs text-muted-foreground">
          Loading gap analysis…
        </p>
      ) : (
        <>
          <p data-testid="gaps-result-count" className="mt-5 font-mono text-[11px] text-muted-foreground">
            {rows.length} of {data?.total ?? 0} gaps
          </p>
          <ul data-testid="gaps-list" className="mt-3 grid grid-cols-1 gap-3 xl:grid-cols-2">
            {rows.map((row) => (
              <GapCard key={row.id} row={row} />
            ))}
          </ul>
          <Link
            to="/doc?path=audit/FOUNDER-DECISIONS.md"
            data-testid="gaps-goto-founder-decisions"
            className="mt-6 inline-block font-mono text-[11px] text-sky-400 hover:text-sky-300"
          >
            Open the five founder decisions ↗
          </Link>
        </>
      )}
    </div>
  );
}
