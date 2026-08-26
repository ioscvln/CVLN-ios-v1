import { useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { RegistryList, RegistryTable } from "@/lib/freezeTypes";
import { StatusBadge } from "@/components/StatusBadge";

const SEVERITY_COLUMN = "severity";

export default function RegistryPage() {
  const { key = "ecosystem" } = useParams<{ key: string }>();
  const [status, setStatus] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const { data: list } = useQuery({
    queryKey: ["docs", "registries"],
    queryFn: () => apiGet<RegistryList>("/docs/registries"),
  });

  const { data, isLoading, isError } = useQuery({
    queryKey: ["docs", "registry", key],
    queryFn: () => apiGet<RegistryTable>(`/docs/registry/${key}`),
  });

  const severityIndex = data
    ? data.columns.findIndex((c) => c.trim().toLowerCase() === SEVERITY_COLUMN)
    : -1;

  const statuses = useMemo(() => {
    if (!data || data.status_column < 0) return [];
    return [...new Set(data.rows.map((r) => r[data.status_column].trim().toUpperCase()))].sort();
  }, [data]);

  const rows = useMemo(() => {
    let out = data?.rows ?? [];
    if (status && data && data.status_column >= 0)
      out = out.filter((r) => r[data.status_column].trim().toUpperCase() === status);
    const needle = filter.trim().toLowerCase();
    if (needle) out = out.filter((r) => r.join(" ").toLowerCase().includes(needle));
    return out;
  }, [data, status, filter]);

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Registries · canonical source {data?.source ?? "—"}
      </p>
      <h1 data-testid="registry-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        {data?.title ?? "Registry"}
      </h1>
      <p className="mt-3 max-w-[80ch] text-[14px] leading-relaxed text-muted-foreground">
        {data?.note ?? ""}
      </p>

      <nav data-testid="registry-tabs" className="mt-6 flex flex-wrap gap-1.5">
        {list?.registries.map((r) => (
          <Link
            key={r.key}
            to={`/registry/${r.key}`}
            data-testid={`registry-tab-${r.key}`}
            className={`rounded border px-2.5 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] transition-colors duration-150 ${
              r.key === key
                ? "border-primary bg-primary/15 text-sky-300"
                : "border-border text-muted-foreground hover:border-foreground/30 hover:text-foreground"
            }`}
          >
            {r.title} · {r.total}
          </Link>
        ))}
      </nav>

      <div className="mt-6 flex flex-wrap items-center gap-2">
        <input
          data-testid="registry-filter-input"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter rows…"
          aria-label="Filter registry rows"
          className="w-56 rounded border border-input bg-secondary/40 px-2.5 py-1.5 font-mono text-[11px] text-foreground outline-none transition-colors duration-150 focus:border-primary"
        />
        <button
          data-testid="registry-status-all"
          onClick={() => setStatus(null)}
          className={`rounded border px-2 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
            status === null ? "border-primary text-sky-300" : "border-border text-muted-foreground"
          }`}
        >
          All
        </button>
        {statuses.map((s) => (
          <button
            key={s}
            data-testid={`registry-status-${s.replace(/[^A-Z]/g, "-")}`}
            onClick={() => setStatus(s === status ? null : s)}
            className={`rounded border px-2 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
              s === status ? "border-primary text-sky-300" : "border-border text-muted-foreground"
            }`}
          >
            {s}
          </button>
        ))}
        <span data-testid="registry-row-count" className="ml-auto font-mono text-[11px] text-muted-foreground">
          {rows.length} / {data?.total ?? 0} rows
        </span>
      </div>

      {isError && (
        <p data-testid="registry-error" className="mt-8 font-mono text-[12px] text-rose-300">
          Registry not available.
        </p>
      )}

      <div className="mt-4 overflow-x-auto border border-border">
        <table data-testid="registry-table" className="w-full min-w-[900px] border-collapse text-left">
          <thead>
            <tr className="bg-secondary/50">
              {data?.columns.map((c, i) => (
                <th
                  key={`${c}-${i}`}
                  className="border-b border-border px-3 py-2 font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground"
                >
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td className="px-3 py-4 font-mono text-[12px] text-muted-foreground">Loading…</td>
              </tr>
            )}
            {rows.map((row, ri) => (
              <tr
                key={`${row[0]}-${ri}`}
                data-testid={`registry-row-${row[0]}`}
                className="align-top transition-colors duration-150 hover:bg-secondary/25"
              >
                {row.map((cell, ci) => (
                  <td
                    key={ci}
                    className="border-b border-border/60 px-3 py-2 text-[12.5px] text-muted-foreground"
                  >
                    {ci === data?.status_column || ci === severityIndex ? (
                      <StatusBadge
                        value={cell}
                        kind={ci === severityIndex ? "severity" : "status"}
                        testId={`registry-cell-status-${row[0]}-${ci}`}
                      />
                    ) : ci === 0 ? (
                      <span className="font-mono text-[11.5px] text-foreground">{cell}</span>
                    ) : (
                      cell
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
