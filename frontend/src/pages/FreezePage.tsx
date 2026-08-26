import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { FreezeState } from "@/lib/freezeTypes";
import { StatusBadge } from "@/components/StatusBadge";

function Stat({ value, label, testId }: { value: string | number; label: string; testId: string }) {
  return (
    <div data-testid={testId} className="border border-border bg-card/40 p-4">
      <p className="font-mono text-2xl font-semibold text-foreground">{value}</p>
      <p className="mt-1 font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground">
        {label}
      </p>
    </div>
  );
}

export default function FreezePage() {
  const { data, isLoading } = useQuery({
    queryKey: ["docs", "freeze"],
    queryFn: () => apiGet<FreezeState>("/docs/freeze"),
  });

  const passed = data?.invariants.filter((i) => i.passed).length ?? 0;
  const total = data?.invariants.length ?? 0;

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        {data?.label ?? "OS v1.1"} · governance
      </p>
      <h1 data-testid="freeze-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Architecture Baseline Freeze
      </h1>
      <p className="mt-3 max-w-[80ch] text-[15px] leading-relaxed text-muted-foreground">
        v1.1 freezes the baseline established by {data?.predecessor ?? "v1.0"}. The freeze is
        append-only: no v1.0 document was deleted, moved or rewritten. Markdown on disk remains
        the sole canonical store; every figure on this page is recomputed from the corpus at
        request time.
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <Link
          to="/doc?path=constitution%2FFREEZE-001.md"
          data-testid="freeze-open-instrument"
          className="rounded border border-primary bg-primary/15 px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-sky-300 transition-colors duration-150 hover:bg-primary/25"
        >
          FREEZE-001 instrument
        </Link>
        <Link
          to="/doc?path=audit%2FFREEZE-REPORT-v1.1.md"
          data-testid="freeze-open-report"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Freeze report v1.1
        </Link>
        <Link
          to="/decisions"
          data-testid="freeze-open-decisions"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Decisions D-001…D-014
        </Link>
      </div>

      <div className="mt-10 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat value={isLoading ? "—" : data!.total_documents} label="Documents in corpus" testId="freeze-stat-documents" />
        <Stat value={isLoading ? "—" : data!.total_decisions} label="Foundational decisions" testId="freeze-stat-decisions" />
        <Stat value={isLoading ? "—" : data!.total_registry_rows} label="Registry rows" testId="freeze-stat-rows" />
        <Stat value={isLoading ? "—" : `${passed}/${total}`} label="Invariants holding" testId="freeze-stat-invariants" />
      </div>

      <section className="mt-12">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Freeze invariants
        </h2>
        <p className="mt-2 max-w-[80ch] text-[13.5px] text-muted-foreground">
          Executable assertions over the Markdown corpus. A failing invariant is a freeze
          violation, not a warning.
        </p>
        <ul data-testid="freeze-invariants" className="mt-4 space-y-2">
          {data?.invariants.map((inv) => (
            <li
              key={inv.id}
              data-testid={`invariant-${inv.id}`}
              className={`border-l-2 bg-card/30 px-4 py-3 ${
                inv.passed ? "border-emerald-700" : "border-rose-700"
              }`}
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-mono text-[11px] font-semibold text-foreground">{inv.id}</span>
                <span
                  data-testid={`invariant-verdict-${inv.id}`}
                  className={`rounded border px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] ${
                    inv.passed
                      ? "border-emerald-800 bg-emerald-950/70 text-emerald-300"
                      : "border-rose-800 bg-rose-950/70 text-rose-300"
                  }`}
                >
                  {inv.passed ? "HOLDS" : "VIOLATED"}
                </span>
              </div>
              <p className="mt-1.5 text-[13.5px] text-foreground">{inv.rule}</p>
              <p className="mt-1 font-mono text-[11px] leading-relaxed text-muted-foreground">
                {inv.detail}
              </p>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-12 grid gap-8 lg:grid-cols-2">
        <div>
          <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
            Manifest
          </h2>
          <dl data-testid="freeze-manifest" className="mt-4 space-y-2 font-mono text-[12px]">
            {[
              ["canonical store", data?.canonical_store ?? "—"],
              ["database as source of truth", String(data?.database_as_source_of_truth ?? false)],
              ["append only", String(data?.append_only ?? true)],
              ["sections added", (data?.sections_added ?? []).join(", ")],
            ].map(([k, v]) => (
              <div key={k} className="flex flex-wrap gap-2 border-b border-border/60 pb-1.5">
                <dt className="w-56 shrink-0 uppercase tracking-[0.1em] text-muted-foreground">{k}</dt>
                <dd className="text-foreground">{v}</dd>
              </div>
            ))}
          </dl>
        </div>
        <div>
          <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
            Status vocabulary
          </h2>
          <p className="mt-2 text-[13px] text-muted-foreground">
            IMPLEMENTED never implies VERIFIED. CURRENT never implies TARGET.
          </p>
          <div data-testid="freeze-vocabulary" className="mt-3 flex flex-wrap gap-2">
            {data?.status_vocabulary.map((s) => (
              <StatusBadge key={s} value={s} kind="status" testId={`vocab-${s}`} />
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
