import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { StatusStats } from "@/lib/types";
import { StatusBadge } from "@/components/StatusBadge";
import { SEVERITY_ORDER, STATUS_ORDER } from "@/lib/status";

function Bar({
  label,
  count,
  total,
  kind,
  testId,
}: {
  label: string;
  count: number;
  total: number;
  kind: "status" | "severity";
  testId: string;
}) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div data-testid={testId} className="flex items-center gap-3 py-1.5">
      <div className="w-52 shrink-0">
        <StatusBadge value={label} kind={kind} />
      </div>
      <div className="h-1.5 flex-1 overflow-hidden rounded-sm bg-secondary/60">
        <div
          className="h-full bg-primary/70 transition-[width] duration-500 ease-out"
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="w-14 shrink-0 text-right font-mono text-[11px] text-muted-foreground">
        {count} · {pct}%
      </span>
    </div>
  );
}

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

const FINDINGS: Array<{ id: string; text: string; doc: string }> = [
  {
    id: "F-1",
    text: "The three repositories are three independent systems, not four layers of one system. No audited repository imports another.",
    doc: "audit/CURRENT-STATE-ARCHITECTURE.md",
  },
  {
    id: "F-2",
    text: "ADL exists and is implemented. ISA and MCL were not found in any audited repository and are recorded as PROPOSED.",
    doc: "protocols/README.md",
  },
  {
    id: "F-3",
    text: "CVL Brain sovereignty and training are NOT VERIFIABLE FROM THE AUDITED PUBLIC REPOSITORIES.",
    doc: "architecture/CVLN-BRAIN.md",
  },
  {
    id: "F-4",
    text: "Doctrine has three owners in code, contradicting the rule that only the Brain owns doctrine.",
    doc: "audit/CONTRADICTIONS.md",
  },
  {
    id: "F-5",
    text: "The canonical dependency direction is a target, not a description of the current implementation.",
    doc: "audit/TARGET-ARCHITECTURE.md",
  },
];

export default function OverviewPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["docs", "stats"],
    queryFn: () => apiGet<StatusStats>("/docs/stats"),
  });

  const compTotal = data?.component_status.reduce((a, s) => a + s.count, 0) ?? 0;
  const gapTotal = data?.gap_severity.reduce((a, s) => a + s.count, 0) ?? 0;

  const orderedComp = STATUS_ORDER.map((s) => ({
    status: s,
    count: data?.component_status.find((c) => c.status.toUpperCase() === s)?.count ?? 0,
  }));
  const orderedSev = SEVERITY_ORDER.map((s) => ({
    status: s,
    count: data?.gap_severity.find((c) => c.status.toUpperCase() === s)?.count ?? 0,
  }));

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        {data?.os_version ?? "OS v1.1"} · Forensic architecture audit · baseline frozen
      </p>
      <h1 data-testid="overview-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        CVLN Intelligence OS
      </h1>
      <p className="mt-3 max-w-[80ch] text-[15px] leading-relaxed text-muted-foreground">
        The technical constitution and architecture specification of the CVLN intelligence
        ecosystem, reconstructed from three audited public repositories. Every component carries
        exactly one implementation status; every claim carries an attribution level. Nothing
        invented here is presented as an existing CVLN capability.
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <Link
          to="/doc?path=README.md"
          data-testid="overview-read-readme"
          className="rounded border border-primary bg-primary/15 px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-sky-300 transition-colors duration-150 hover:bg-primary/25"
        >
          Read the repository index
        </Link>
        <Link
          to="/doc?path=audit/REPOSITORY-AUDIT.md"
          data-testid="overview-read-audit"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Phase 0 · Repository audit
        </Link>
        <Link
          to="/doc?path=audit/FOUNDER-DECISIONS.md"
          data-testid="overview-read-decisions"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Founder decisions required
        </Link>
      </div>

      <div className="mt-10 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat value={isLoading ? "—" : data!.total_documents} label="Specification documents" testId="stat-documents" />
        <Stat value={isLoading ? "—" : data!.total_components} label="Components audited" testId="stat-components" />
        <Stat value={isLoading ? "—" : gapTotal} label="Gaps classified" testId="stat-gaps" />
        <Stat value={isLoading ? "—" : data!.contradictions} label="Contradictions recorded" testId="stat-contradictions" />
        <Stat value={isLoading ? "—" : data!.total_decisions} label="Foundational decisions" testId="stat-decisions" />
        <Stat value={isLoading ? "—" : data!.registry_rows} label="Registry rows" testId="stat-registry-rows" />
        <Stat
          value={isLoading ? "—" : `${data!.invariants_passed}/${data!.invariants_total}`}
          label="Freeze invariants holding"
          testId="stat-invariants"
        />
        <Stat
          value={isLoading ? "—" : data!.section_counts.length}
          label="Corpus sections"
          testId="stat-sections"
        />
      </div>

      <div className="mt-4 border border-dashed border-sky-800/70 bg-sky-950/20 px-4 py-3">
        <p className="font-mono text-[10.5px] uppercase tracking-[0.14em] text-sky-300">
          v1.1 — Architecture baseline frozen
        </p>
        <p className="mt-1.5 max-w-[85ch] text-[13px] leading-relaxed text-muted-foreground">
          The v1.0 corpus is preserved append-only. Governance, security, resilience,
          legal-by-design, proof and economic dimensions were added as TARGET or PROPOSED unless
          evidence exists. IMPLEMENTED never implies VERIFIED.{" "}
          <Link to="/freeze" data-testid="overview-goto-freeze" className="font-mono text-[11.5px] text-sky-400 hover:text-sky-300">
            Open the freeze report ↗
          </Link>
        </p>
      </div>

      <section className="mt-12">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Implementation status distribution
        </h2>
        <p className="mt-2 max-w-[80ch] text-[13.5px] text-muted-foreground">
          Across {compTotal} audited components. PROPOSED is rendered with a dashed border
          throughout the portal so a planned capability can never read as an existing one.
        </p>
        <div data-testid="status-distribution" className="mt-4">
          {orderedComp.map((s) => (
            <Bar
              key={s.status}
              label={s.status}
              count={s.count}
              total={compTotal}
              kind="status"
              testId={`status-bar-${s.status.replace(/[^A-Z]/g, "-")}`}
            />
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Gap severity distribution
        </h2>
        <div data-testid="severity-distribution" className="mt-4">
          {orderedSev.map((s) => (
            <Bar
              key={s.status}
              label={s.status}
              count={s.count}
              total={gapTotal}
              kind="severity"
              testId={`severity-bar-${s.status}`}
            />
          ))}
        </div>
        <Link
          to="/gaps"
          data-testid="overview-goto-gaps"
          className="mt-4 inline-block font-mono text-[11px] text-sky-400 hover:text-sky-300"
        >
          Open the full gap analysis ↗
        </Link>
      </section>

      <section className="mt-12">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Headline findings
        </h2>
        <ol data-testid="headline-findings" className="mt-4 space-y-3">
          {FINDINGS.map((f) => (
            <li key={f.id} className="flex gap-3 border-l border-border pl-4">
              <span className="shrink-0 font-mono text-[11px] text-muted-foreground">{f.id}</span>
              <span className="text-[13.5px] leading-relaxed text-muted-foreground">
                {f.text}{" "}
                <Link
                  to={`/doc?path=${encodeURIComponent(f.doc)}`}
                  data-testid={`finding-link-${f.id}`}
                  className="font-mono text-[11.5px] text-sky-400 hover:text-sky-300"
                >
                  {f.doc}
                </Link>
              </span>
            </li>
          ))}
        </ol>
      </section>
    </div>
  );
}
