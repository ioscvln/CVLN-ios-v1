import { Link, useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { SystemCard } from "@/lib/insightTypes";
import { StatusBadge } from "@/components/StatusBadge";

function Grid({
  columns,
  rows,
  testId,
  emptyNote,
}: {
  columns: string[];
  rows: string[][];
  testId: string;
  emptyNote: string;
}) {
  if (!rows.length)
    return (
      <p data-testid={`${testId}-empty`} className="font-mono text-[11.5px] text-muted-foreground">
        {emptyNote}
      </p>
    );
  const statusIndex = columns.findIndex((c) => c.trim().toLowerCase() === "status");
  return (
    <div className="overflow-x-auto border border-border">
      <table data-testid={testId} className="w-full min-w-[720px] border-collapse text-left">
        <thead>
          <tr className="bg-secondary/50">
            {columns.map((c, i) => (
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
          {rows.map((row, ri) => (
            <tr key={`${row[0]}-${ri}`} data-testid={`${testId}-row-${row[0]}`} className="align-top">
              {row.map((cell, ci) => (
                <td
                  key={ci}
                  className="border-b border-border/60 px-3 py-2 text-[12.5px] text-muted-foreground"
                >
                  {ci === statusIndex ? (
                    <StatusBadge value={cell} kind="status" testId={`${testId}-status-${row[0]}`} />
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
  );
}

export default function SystemCardPage() {
  const { name = "" } = useParams<{ name: string }>();
  const { data, isError } = useQuery({
    queryKey: ["docs", "system", name],
    queryFn: () => apiGet<SystemCard>(`/docs/system/${encodeURIComponent(name)}`),
  });

  if (isError)
    return (
      <div className="px-6 py-8 sm:px-10 lg:px-14">
        <p data-testid="system-error" className="font-mono text-[12px] text-rose-300">
          Unknown system: {name}
        </p>
        <Link to="/systems" className="mt-3 inline-block font-mono text-[11.5px] text-sky-400">
          Back to system cards
        </Link>
      </div>
    );

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <Link to="/systems" data-testid="system-back" className="font-mono text-[11px] text-sky-400">
        ← System cards
      </Link>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <h1 data-testid="system-title" className="text-3xl font-semibold tracking-tight text-foreground">
          {data?.name ?? name}
        </h1>
        {data && <StatusBadge value={data.status} kind="status" testId="system-header-status" />}
      </div>
      <p className="mt-3 max-w-[85ch] text-[15px] leading-relaxed text-muted-foreground">
        {data?.role}
      </p>

      <dl data-testid="system-identity" className="mt-6 grid gap-2 font-mono text-[12px] lg:grid-cols-2">
        {[
          ["layer", data?.layer],
          ["repository", data?.repository],
          ["evidence", data?.evidence],
          ["owns", data?.owns],
          ["must not own", data?.must_not_own],
        ].map(([k, v]) => (
          <div key={String(k)} className="flex gap-2 border-b border-border/60 pb-1.5">
            <dt className="w-40 shrink-0 uppercase tracking-[0.1em] text-muted-foreground">{k}</dt>
            <dd className="text-foreground">{v || "—"}</dd>
          </div>
        ))}
      </dl>

      {[
        {
          title: "Components",
          note: "Rows of the component matrix attributed to this system's repository.",
          columns: data?.component_columns ?? [],
          rows: data?.components ?? [],
          testId: "system-components-table",
          empty: "No component row is attributed to this system.",
        },
        {
          title: "Vulnerabilities",
          note: "Registered weaknesses citing this system. Nothing is inferred.",
          columns: data?.vulnerability_columns ?? [],
          rows: data?.vulnerabilities ?? [],
          testId: "system-vulnerabilities-table",
          empty: "No vulnerability is registered against this system.",
        },
        {
          title: "Decisions",
          note: "Foundational decisions whose text references this system.",
          columns: data?.decision_columns ?? [],
          rows: data?.decisions ?? [],
          testId: "system-decisions-table",
          empty: "No decision references this system.",
        },
        {
          title: "Declared relations",
          note: "Relations declared by an artefact. UNKNOWN means not evidenced, never absent.",
          columns: data?.relation_columns ?? [],
          rows: data?.relations ?? [],
          testId: "system-relations-table",
          empty: "No relation registry declares an edge for this system.",
        },
      ].map((s) => (
        <section key={s.title} className="mt-10">
          <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
            {s.title}
          </h2>
          <p className="mt-2 max-w-[85ch] text-[13px] text-muted-foreground">{s.note}</p>
          <div className="mt-4">
            <Grid columns={s.columns} rows={s.rows} testId={s.testId} emptyNote={s.empty} />
          </div>
        </section>
      ))}

      <section className="mt-10">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Documents
        </h2>
        <ul data-testid="system-documents" className="mt-4 space-y-1.5">
          {(data?.documents ?? []).map((p) => (
            <li key={p}>
              <Link
                to={`/doc?path=${encodeURIComponent(p)}`}
                data-testid={`system-doc-${p}`}
                className="font-mono text-[11.5px] text-sky-400 transition-colors duration-150 hover:text-sky-300"
              >
                {p}
              </Link>
            </li>
          ))}
          {data && data.documents.length === 0 && (
            <li className="font-mono text-[11.5px] text-muted-foreground">
              No document title or path names this system.
            </li>
          )}
        </ul>
      </section>
    </div>
  );
}
