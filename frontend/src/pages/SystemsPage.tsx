import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { SystemSummary } from "@/lib/insightTypes";
import { StatusBadge } from "@/components/StatusBadge";

export default function SystemsPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["docs", "systems"],
    queryFn: () => apiGet<SystemSummary[]>("/docs/systems"),
  });

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Ecosystem · one card per system
      </p>
      <h1 data-testid="systems-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        System cards
      </h1>
      <p className="mt-3 max-w-[85ch] text-[15px] leading-relaxed text-muted-foreground">
        Every system of the ecosystem registry, with its components, vulnerabilities and
        decisions gathered on one page. Counts are computed from the registries at request
        time — a zero means nothing is recorded, not that nothing exists.
      </p>

      <p data-testid="systems-count" className="mt-6 font-mono text-[11px] text-muted-foreground">
        {isLoading ? "—" : data!.length} systems
      </p>

      <ul data-testid="systems-list" className="mt-4 grid gap-3 lg:grid-cols-2">
        {data?.map((s) => (
          <li key={s.name} data-testid={`system-card-${s.name}`}>
            <Link
              to={`/system/${encodeURIComponent(s.name)}`}
              data-testid={`system-link-${s.name}`}
              className="block border border-border bg-card/30 p-4 transition-colors duration-150 hover:border-foreground/30"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[15px] font-medium text-foreground">{s.name}</span>
                <StatusBadge value={s.status} kind="status" testId={`system-status-${s.name}`} />
                <span className="font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground">
                  {s.layer}
                </span>
              </div>
              <p className="mt-1.5 text-[13px] leading-relaxed text-muted-foreground">{s.role}</p>
              <div className="mt-3 flex flex-wrap gap-4 border-t border-border pt-3 font-mono text-[11px] text-muted-foreground">
                <span data-testid={`system-components-${s.name}`}>{s.components} components</span>
                <span data-testid={`system-vulns-${s.name}`}>{s.vulnerabilities} vulnerabilities</span>
                <span data-testid={`system-decisions-${s.name}`}>{s.decisions} decisions</span>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
