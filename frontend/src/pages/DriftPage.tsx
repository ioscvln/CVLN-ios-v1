import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { BaselineInfo, DriftReport } from "@/lib/insightTypes";
import { StatusBadge } from "@/components/StatusBadge";

type Lens = "all" | "violations" | "advisories" | "added";

export default function DriftPage() {
  const [base, setBase] = useState("v1.1");
  const [target, setTarget] = useState("current");
  const [lens, setLens] = useState<Lens>("all");

  const { data: list } = useQuery({
    queryKey: ["docs", "baselines"],
    queryFn: () => apiGet<BaselineInfo[]>("/docs/baselines"),
  });

  const { data, isLoading } = useQuery({
    queryKey: ["docs", "drift", base, target],
    queryFn: () => apiGet<DriftReport>(`/docs/drift?base=${base}&target=${target}`),
  });

  const rows = useMemo(() => {
    const all = data?.rows ?? [];
    if (lens === "violations") return all.filter((r) => r.promotion_without_adr);
    if (lens === "advisories") return all.filter((r) => r.advisory);
    if (lens === "added") return all.filter((r) => r.change === "added");
    return all;
  }, [data, lens]);

  const violation = (data?.promotions_without_adr ?? 0) > 0;

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Governance · drift control
      </p>
      <h1 data-testid="drift-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Baseline drift
      </h1>
      <p className="mt-3 max-w-[85ch] text-[15px] leading-relaxed text-muted-foreground">
        Compares the registry rows of two baselines and reports every status promotion. A
        promotion without an ADR reference is a freeze violation. A newly recorded row is not a
        promotion: it is reported as an advisory when it carries a strong status with no decision
        reference.
      </p>

      <div className="mt-6 flex flex-wrap items-end gap-4">
        {[
          { label: "Base", value: base, set: setBase, testId: "drift-select-base" },
          { label: "Target", value: target, set: setTarget, testId: "drift-select-target" },
        ].map((sel) => (
          <label key={sel.label} className="flex flex-col gap-1">
            <span className="font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
              {sel.label}
            </span>
            <select
              data-testid={sel.testId}
              value={sel.value}
              onChange={(e) => sel.set(e.target.value)}
              className="rounded border border-input bg-secondary/40 px-2.5 py-1.5 font-mono text-[11.5px] text-foreground outline-none transition-colors duration-150 focus:border-primary"
            >
              {list?.map((b) => (
                <option key={b.id} value={b.id} label={`${b.id} — ${b.total_rows} rows`} />
              ))}
            </select>
          </label>
        ))}
      </div>

      <div
        data-testid="drift-verdict"
        className={`mt-6 border-l-2 px-4 py-3 ${
          violation ? "border-rose-600 bg-rose-950/30" : "border-emerald-700 bg-emerald-950/20"
        }`}
      >
        <p
          className={`font-mono text-[10.5px] uppercase tracking-[0.14em] ${
            violation ? "text-rose-300" : "text-emerald-300"
          }`}
        >
          {violation ? "Freeze violation" : "No untraced promotion"}
        </p>
        <p className="mt-1.5 text-[13.5px] text-foreground">{data?.verdict ?? "…"}</p>
        <p className="mt-1 font-mono text-[11px] text-muted-foreground">
          {data?.base.label} → {data?.target.label} · {data?.target.provenance}
        </p>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-5">
        {[
          ["drift-stat-compared", data?.total_compared, "Rows compared"],
          ["drift-stat-added", data?.added, "Rows added"],
          ["drift-stat-changed", data?.status_changed, "Statuses changed"],
          ["drift-stat-promotions", data?.promotions, "Promotions"],
          ["drift-stat-violations", data?.promotions_without_adr, "Promotions without ADR"],
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

      <div className="mt-6 flex flex-wrap items-center gap-2">
        {(["all", "violations", "advisories", "added"] as Lens[]).map((l) => (
          <button
            key={l}
            data-testid={`drift-lens-${l}`}
            onClick={() => setLens(l)}
            className={`rounded border px-2.5 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
              lens === l ? "border-primary bg-primary/15 text-sky-300" : "border-border text-muted-foreground hover:text-foreground"
            }`}
          >
            {l}
          </button>
        ))}
        <span data-testid="drift-row-count" className="ml-auto font-mono text-[11px] text-muted-foreground">
          {rows.length} rows
        </span>
      </div>

      <div className="mt-4 overflow-x-auto border border-border">
        <table data-testid="drift-table" className="w-full min-w-[860px] border-collapse text-left">
          <thead>
            <tr className="bg-secondary/50">
              {["Registry", "Row", "Change", "Base status", "Target status", "ADR", "Verdict"].map((c) => (
                <th
                  key={c}
                  className="border-b border-border px-3 py-2 font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground"
                >
                  {c}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr
                key={`${r.registry}-${r.row_id}`}
                data-testid={`drift-row-${r.registry}-${r.row_id}`}
                className="align-top transition-colors duration-150 hover:bg-secondary/25"
              >
                <td className="border-b border-border/60 px-3 py-2 font-mono text-[11px] text-muted-foreground">
                  {r.registry}
                </td>
                <td className="border-b border-border/60 px-3 py-2 font-mono text-[11.5px] text-foreground">
                  {r.row_id}
                </td>
                <td className="border-b border-border/60 px-3 py-2 font-mono text-[11px] text-muted-foreground">
                  {r.change}
                </td>
                <td className="border-b border-border/60 px-3 py-2">
                  {r.base_status ? <StatusBadge value={r.base_status} kind="status" testId={`drift-base-${r.row_id}`} /> : "—"}
                </td>
                <td className="border-b border-border/60 px-3 py-2">
                  {r.target_status ? <StatusBadge value={r.target_status} kind="status" testId={`drift-target-${r.row_id}`} /> : "—"}
                </td>
                <td className="border-b border-border/60 px-3 py-2 font-mono text-[11px] text-muted-foreground">
                  {r.adr || "—"}
                </td>
                <td className="border-b border-border/60 px-3 py-2">
                  {r.promotion_without_adr ? (
                    <span
                      data-testid={`drift-verdict-${r.row_id}`}
                      className="rounded border border-rose-800 bg-rose-950/70 px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-rose-300"
                    >
                      Promotion without ADR
                    </span>
                  ) : r.advisory ? (
                    <span
                      data-testid={`drift-verdict-${r.row_id}`}
                      className="rounded border border-dashed border-amber-600/80 bg-amber-950/40 px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-amber-300"
                    >
                      Advisory · no decision ref
                    </span>
                  ) : (
                    <span className="font-mono text-[10.5px] text-muted-foreground">traced</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
