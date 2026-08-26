import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { RegistryTable } from "@/lib/freezeTypes";
import { StatusBadge } from "@/components/StatusBadge";

/** Decision registry rendered as ADR cards. Columns:
 *  ID | Decision | Rationale | Type | Evidence | Status | Scope | ADR */
export default function DecisionsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["docs", "registry", "decisions"],
    queryFn: () => apiGet<RegistryTable>("/docs/registry/decisions"),
  });

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Governance · {data?.source ?? "decisions/DECISION-REGISTRY.md"}
      </p>
      <h1 data-testid="decisions-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Foundational decisions
      </h1>
      <p className="mt-3 max-w-[80ch] text-[14px] leading-relaxed text-muted-foreground">
        Each decision is binding until superseded by a later ADR. A decision whose evidence cell
        reads <span className="font-mono text-foreground">none</span> is normative: it constrains
        future work and asserts nothing about current implementation.
      </p>

      <p data-testid="decisions-count" className="mt-6 font-mono text-[11px] text-muted-foreground">
        {isLoading ? "—" : data!.total} decisions · D-001 … D-014
      </p>

      <ul data-testid="decisions-list" className="mt-4 grid gap-3 lg:grid-cols-2">
        {data?.rows.map((row) => {
          const [id, decision, rationale, type, evidence, status, scope, adr] = row;
          const normative = evidence.trim().toLowerCase().startsWith("none");
          return (
            <li
              key={id}
              data-testid={`decision-card-${id}`}
              className="border border-border bg-card/30 p-4 transition-colors duration-150 hover:border-foreground/25"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="font-mono text-[11px] font-semibold text-foreground">{id}</span>
                <StatusBadge value={status} kind="status" testId={`decision-status-${id}`} />
                <span className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
                  {type}
                </span>
                {normative && (
                  <span
                    data-testid={`decision-normative-${id}`}
                    className="rounded border border-dashed border-amber-600/80 bg-amber-950/40 px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] text-amber-300"
                  >
                    Normative · no implementation claimed
                  </span>
                )}
              </div>
              <p className="mt-2 text-[14px] font-medium text-foreground">{decision}</p>
              <p className="mt-1.5 text-[12.5px] leading-relaxed text-muted-foreground">{rationale}</p>
              <div className="mt-3 border-t border-border pt-3 font-mono text-[11px] text-muted-foreground">
                <p>evidence: {evidence}</p>
                <p className="mt-0.5">scope: {scope}</p>
              </div>
              <Link
                to={`/doc?path=${encodeURIComponent(`decisions/${adr}-${id}.md`)}`}
                data-testid={`decision-adr-link-${id}`}
                className="mt-3 inline-block font-mono text-[11px] text-sky-400 transition-colors duration-150 hover:text-sky-300"
              >
                Open {adr} ↗
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
