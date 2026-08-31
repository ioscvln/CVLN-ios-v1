import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { RegistryTable } from "@/lib/freezeTypes";
import { StatusBadge } from "@/components/StatusBadge";

const KIND_STYLES: Record<string, string> = {
  "freeze-blocker": "border-rose-700 bg-rose-950/60 text-rose-300",
  contradiction: "border-orange-700 bg-orange-950/60 text-orange-300",
  "unknown-needs-evidence": "border-neutral-600 bg-neutral-900/70 text-neutral-300",
  "risk-needs-decision": "border-amber-700 bg-amber-950/50 text-amber-300",
  "open-question": "border-sky-800 bg-sky-950/50 text-sky-300",
};

const KIND_ORDER = [
  "freeze-blocker",
  "contradiction",
  "risk-needs-decision",
  "unknown-needs-evidence",
  "open-question",
];

export default function OpenQuestionsPage() {
  const [kind, setKind] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["docs", "registry", "open-questions"],
    queryFn: () => apiGet<RegistryTable>("/docs/registry/open-questions"),
  });

  const col = (name: string) =>
    data ? data.columns.findIndex((c) => c.trim().toLowerCase() === name) : -1;
  const kindIdx = col("kind");
  const ownerIdx = col("owner");
  const dueIdx = col("due");

  const counts = useMemo(() => {
    const out: Record<string, number> = {};
    for (const row of data?.rows ?? []) {
      const k = row[kindIdx]?.trim() ?? "";
      out[k] = (out[k] ?? 0) + 1;
    }
    return out;
  }, [data, kindIdx]);

  const rows = useMemo(() => {
    let out = [...(data?.rows ?? [])];
    out.sort(
      (a, b) =>
        KIND_ORDER.indexOf(a[kindIdx]?.trim()) - KIND_ORDER.indexOf(b[kindIdx]?.trim()),
    );
    if (kind) out = out.filter((r) => r[kindIdx]?.trim() === kind);
    const needle = filter.trim().toLowerCase();
    if (needle) out = out.filter((r) => r.join(" ").toLowerCase().includes(needle));
    return out;
  }, [data, kind, filter, kindIdx]);

  const blockers = (counts["freeze-blocker"] ?? 0) + (counts["contradiction"] ?? 0);
  const unassigned =
    data?.rows.filter((r) => r[ownerIdx]?.trim().toUpperCase() === "UNASSIGNED").length ?? 0;

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Governance · {data?.source ?? "governance/OPEN-QUESTIONS.md"}
      </p>
      <h1 data-testid="questions-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Open questions
      </h1>
      <p className="mt-3 max-w-[85ch] text-[15px] leading-relaxed text-muted-foreground">
        Everything that must be answered before the next freeze can be declared, generated from
        the registries. <span className="font-mono text-[13px] text-foreground">UNASSIGNED</span>{" "}
        and <span className="font-mono text-[13px] text-foreground">TBD</span> are truthful
        values: no owner has been named and no date has been set. Both columns are edited by
        humans in the Markdown register and preserved across regenerations (D-021).
      </p>

      <div className="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        {[
          ["questions-stat-total", data?.total, "Open questions"],
          ["questions-stat-blockers", blockers, "Freeze blockers"],
          ["questions-stat-unassigned", unassigned, "Owners unassigned"],
          ["questions-stat-kinds", Object.keys(counts).length, "Kinds in use"],
        ].map(([testId, value, label]) => (
          <div key={String(testId)} data-testid={String(testId)} className="border border-border bg-card/40 p-4">
            <p className="font-mono text-2xl font-semibold text-foreground">
              {isLoading ? "—" : String(value ?? 0)}
            </p>
            <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
              {label}
            </p>
          </div>
        ))}
      </div>

      {blockers > 0 && (
        <div
          data-testid="questions-blocker-notice"
          className="mt-4 border-l-2 border-rose-600 bg-rose-950/30 px-4 py-3"
        >
          <p className="font-mono text-[10.5px] uppercase tracking-[0.14em] text-rose-300">
            Next freeze blocked
          </p>
          <p className="mt-1.5 max-w-[85ch] text-[13.5px] text-foreground">
            {blockers} freeze-blocking rows are unresolved. A freeze may not be declared while any
            of them stands (D-021, `audit/DRIFT-CONTROL.md`).
          </p>
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-2">
        <input
          data-testid="questions-filter-input"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter questions…"
          aria-label="Filter open questions"
          className="w-56 rounded border border-input bg-secondary/40 px-2.5 py-1.5 font-mono text-[11px] text-foreground outline-none transition-colors duration-150 focus:border-primary"
        />
        <button
          data-testid="questions-kind-all"
          onClick={() => setKind(null)}
          className={`rounded border px-2 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
            kind === null ? "border-primary text-sky-300" : "border-border text-muted-foreground"
          }`}
        >
          All
        </button>
        {KIND_ORDER.filter((k) => counts[k]).map((k) => (
          <button
            key={k}
            data-testid={`questions-kind-${k}`}
            onClick={() => setKind(k === kind ? null : k)}
            className={`rounded border px-2 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
              k === kind ? "border-primary text-sky-300" : "border-border text-muted-foreground hover:text-foreground"
            }`}
          >
            {k} · {counts[k]}
          </button>
        ))}
        <span data-testid="questions-row-count" className="ml-auto font-mono text-[11px] text-muted-foreground">
          {rows.length} / {data?.total ?? 0} rows
        </span>
      </div>

      <div className="mt-4 overflow-x-auto border border-border">
        <table data-testid="questions-table" className="w-full min-w-[980px] border-collapse text-left">
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
            {rows.map((row) => (
              <tr
                key={row[0]}
                data-testid={`question-row-${row[0]}`}
                className="align-top transition-colors duration-150 hover:bg-secondary/25"
              >
                {row.map((cell, ci) => (
                  <td key={ci} className="border-b border-border/60 px-3 py-2 text-[12.5px] text-muted-foreground">
                    {ci === kindIdx ? (
                      <span
                        data-testid={`question-kind-${row[0]}`}
                        className={`rounded border px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.08em] ${
                          KIND_STYLES[cell.trim()] ?? "border-border text-muted-foreground"
                        }`}
                      >
                        {cell}
                      </span>
                    ) : ci === data!.status_column ? (
                      <StatusBadge value={cell} kind="status" testId={`question-status-${row[0]}`} />
                    ) : ci === ownerIdx || ci === dueIdx ? (
                      <span
                        data-testid={ci === ownerIdx ? `question-owner-${row[0]}` : `question-due-${row[0]}`}
                        className={`font-mono text-[11px] ${
                          cell.trim().toUpperCase() === "UNASSIGNED" || cell.trim().toUpperCase() === "TBD"
                            ? "text-amber-300/90"
                            : "text-foreground"
                        }`}
                      >
                        {cell}
                      </span>
                    ) : ci === 0 ? (
                      <span className="font-mono text-[11.5px] text-foreground">{cell}</span>
                    ) : ci === 3 ? (
                      <Link
                        to={`/doc?path=${encodeURIComponent(cell.trim())}`}
                        data-testid={`question-source-${row[0]}`}
                        className="font-mono text-[11px] text-sky-400 hover:text-sky-300"
                      >
                        {cell}
                      </Link>
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
