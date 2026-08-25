import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { ComponentMatrix } from "@/lib/types";
import { StatusBadge } from "@/components/StatusBadge";
import { STATUS_ORDER, REPO_LABELS, evidenceUrl } from "@/lib/status";

type SortKey = "component" | "repository" | "status";

export default function MatrixPage() {
  const [statusFilter, setStatusFilter] = useState<string | null>(null);
  const [repoFilter, setRepoFilter] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("component");
  const [asc, setAsc] = useState(true);

  const { data, isLoading } = useQuery({
    queryKey: ["docs", "matrix"],
    queryFn: () => apiGet<ComponentMatrix>("/docs/matrix"),
  });

  const repos = useMemo(
    () => Array.from(new Set((data?.rows ?? []).map((r) => r.repository))).sort(),
    [data],
  );

  const rows = useMemo(() => {
    let out = [...(data?.rows ?? [])];
    if (statusFilter) out = out.filter((r) => r.status.toUpperCase() === statusFilter);
    if (repoFilter) out = out.filter((r) => r.repository === repoFilter);
    out.sort((a, b) => {
      const cmp = a[sortKey].localeCompare(b[sortKey]);
      return asc ? cmp : -cmp;
    });
    return out;
  }, [data, statusFilter, repoFilter, sortKey, asc]);

  function toggleSort(key: SortKey) {
    if (key === sortKey) setAsc((v) => !v);
    else {
      setSortKey(key);
      setAsc(true);
    }
  }

  const th = "sticky top-0 z-10 bg-sidebar px-3 py-2 text-left font-mono text-[10px] font-semibold uppercase tracking-[0.11em] text-muted-foreground border-b border-border whitespace-nowrap";

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-12">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Phase 0 · Forensic audit
      </p>
      <h1 data-testid="matrix-title" className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
        Component Matrix
      </h1>
      <p className="mt-2 max-w-[85ch] text-[13.5px] leading-relaxed text-muted-foreground">
        One row per significant component, exactly one status per row. Rendered live from{" "}
        <Link
          to="/doc?path=audit/COMPONENT-MATRIX.md"
          data-testid="matrix-source-link"
          className="font-mono text-[12.5px] text-sky-400 hover:text-sky-300"
        >
          {data?.source ?? "audit/COMPONENT-MATRIX.md"}
        </Link>
        , which remains the canonical source of truth.
      </p>

      <div className="mt-5 flex flex-wrap items-center gap-1.5">
        <button
          data-testid="status-filter-all"
          onClick={() => setStatusFilter(null)}
          className={`rounded border px-2 py-1 font-mono text-[10px] uppercase tracking-[0.09em] transition-colors duration-150 ${
            statusFilter === null
              ? "border-primary bg-primary/20 text-sky-300"
              : "border-border text-muted-foreground hover:text-foreground"
          }`}
        >
          All ({data?.total ?? 0})
        </button>
        {STATUS_ORDER.map((s) => {
          const count = (data?.rows ?? []).filter((r) => r.status.toUpperCase() === s).length;
          if (count === 0) return null;
          return (
            <button
              key={s}
              data-testid={`status-filter-${s.replace(/[^A-Z]/g, "-").toLowerCase()}`}
              onClick={() => setStatusFilter(statusFilter === s ? null : s)}
              className={`transition-opacity duration-150 ${statusFilter && statusFilter !== s ? "opacity-40" : ""}`}
            >
              <StatusBadge value={`${s} · ${count}`} />
            </button>
          );
        })}
      </div>

      <div className="mt-2.5 flex flex-wrap items-center gap-1.5">
        <span className="font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
          Repository
        </span>
        {repos.map((r) => (
          <button
            key={r}
            data-testid={`repo-filter-${r}`}
            onClick={() => setRepoFilter(repoFilter === r ? null : r)}
            className={`rounded border px-2 py-1 font-mono text-[10px] uppercase tracking-[0.09em] transition-colors duration-150 ${
              repoFilter === r
                ? "border-primary bg-primary/20 text-sky-300"
                : "border-border text-muted-foreground hover:text-foreground"
            }`}
          >
            {REPO_LABELS[r] ?? r}
          </button>
        ))}
      </div>

      {isLoading ? (
        <p data-testid="matrix-loading" className="mt-8 font-mono text-xs text-muted-foreground">
          Loading matrix…
        </p>
      ) : (
        <>
          <p data-testid="matrix-result-count" className="mt-5 font-mono text-[11px] text-muted-foreground">
            {rows.length} of {data?.total ?? 0} components
          </p>
          <div className="mt-2 max-h-[70vh] overflow-auto rounded border border-border">
            <table data-testid="matrix-table" className="w-full border-collapse text-[12.5px]">
              <thead>
                <tr>
                  {(["component", "repository", "status"] as SortKey[]).map((k) => (
                    <th key={k} className={th}>
                      <button
                        data-testid={`matrix-sort-${k}`}
                        onClick={() => toggleSort(k)}
                        className="transition-colors duration-150 hover:text-foreground"
                      >
                        {k} {sortKey === k ? (asc ? "▴" : "▾") : ""}
                      </button>
                    </th>
                  ))}
                  <th className={th}>Path / Evidence</th>
                  <th className={th}>Conceptual responsibility</th>
                  <th className={th}>Actual implementation</th>
                  <th className={th}>Consumers</th>
                  <th className={th}>Notes</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => {
                  const link = evidenceUrl(r.repository, r.path);
                  return (
                    <tr
                      key={`${r.component}-${r.repository}`}
                      data-testid={`matrix-row-${r.component}`}
                      className="border-b border-border transition-colors duration-150 last:border-0 hover:bg-white/[0.02]"
                    >
                      <td className="px-3 py-2 align-top font-medium text-foreground">{r.component}</td>
                      <td className="px-3 py-2 align-top font-mono text-[11px] text-muted-foreground">
                        {r.repository}
                      </td>
                      <td className="px-3 py-2 align-top">
                        <StatusBadge value={r.status} testId={`matrix-status-${r.component}`} />
                      </td>
                      <td className="px-3 py-2 align-top font-mono text-[11px]">
                        {link ? (
                          <a
                            href={link}
                            target="_blank"
                            rel="noreferrer"
                            data-testid={`matrix-evidence-${r.component}`}
                            className="text-sky-400 hover:text-sky-300"
                          >
                            {r.path} ↗
                          </a>
                        ) : (
                          <span className="text-muted-foreground">{r.path}</span>
                        )}
                        <span className="mt-0.5 block text-[10.5px] text-muted-foreground/80">
                          {r.evidence}
                        </span>
                      </td>
                      <td className="px-3 py-2 align-top text-muted-foreground">
                        {r.conceptual_responsibility}
                      </td>
                      <td className="px-3 py-2 align-top text-muted-foreground">
                        {r.actual_implementation}
                      </td>
                      <td className="px-3 py-2 align-top font-mono text-[11px] text-muted-foreground">
                        {r.consumers}
                      </td>
                      <td className="px-3 py-2 align-top text-[11.5px] text-muted-foreground/90">
                        {r.notes}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
}
