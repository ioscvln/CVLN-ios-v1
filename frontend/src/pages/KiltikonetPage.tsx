import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { RegistryTable } from "@/lib/freezeTypes";
import type { DocDetail } from "@/lib/types";
import { Markdown } from "@/components/Markdown";
import { StatusBadge } from "@/components/StatusBadge";

const SYSTEM_CARD = "kiltikonet/KILTIKONET-SYSTEM.md";

function useRegistry(key: string) {
  return useQuery({
    queryKey: ["docs", "registry", key],
    queryFn: () => apiGet<RegistryTable>(`/docs/registry/${key}`),
  });
}

function Table({ table, testId }: { table?: RegistryTable; testId: string }) {
  if (!table) return <p className="font-mono text-[12px] text-muted-foreground">Loading…</p>;
  return (
    <div className="overflow-x-auto border border-border">
      <table data-testid={testId} className="w-full min-w-[760px] border-collapse text-left">
        <thead>
          <tr className="bg-secondary/50">
            {table.columns.map((c, i) => (
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
          {table.rows.map((row, ri) => (
            <tr
              key={`${row[0]}-${ri}`}
              data-testid={`${testId}-row-${row[0]}`}
              className="align-top transition-colors duration-150 hover:bg-secondary/25"
            >
              {row.map((cell, ci) => (
                <td
                  key={ci}
                  className="border-b border-border/60 px-3 py-2 text-[12.5px] text-muted-foreground"
                >
                  {ci === table.status_column ? (
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

function Section({
  title,
  note,
  children,
}: {
  title: string;
  note: string;
  children: React.ReactNode;
}) {
  return (
    <section className="mt-12">
      <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
        {title}
      </h2>
      <p className="mt-2 max-w-[85ch] text-[13px] text-muted-foreground">{note}</p>
      <div className="mt-4">{children}</div>
    </section>
  );
}

export default function KiltikonetPage() {
  const { data: card } = useQuery({
    queryKey: ["docs", "file", SYSTEM_CARD],
    queryFn: () => apiGet<DocDetail>(`/docs/file?path=${encodeURIComponent(SYSTEM_CARD)}`),
  });

  const relations = useRegistry("kiltikonet-relations");
  const programmes = useRegistry("kiltikonet-programmes");
  const identity = useRegistry("kiltikonet-identity");
  const contradictions = useRegistry("kiltikonet-contradictions");
  const flows = useRegistry("kiltikonet-data");

  const unknown =
    relations.data?.rows.filter((r) => r[relations.data!.status_column].trim().toUpperCase() === "UNKNOWN")
      .length ?? 0;

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        PATCH-001-KILTIKONET · post-freeze completeness patch
      </p>
      <h1 data-testid="kiltikonet-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Kiltikonet — system card
      </h1>
      <p className="mt-3 max-w-[85ch] text-[15px] leading-relaxed text-muted-foreground">
        Added after the v1.1 freeze, from the audited repository{" "}
        <span className="font-mono text-[13px] text-foreground">cultureconnectorg/Kiltikonet-Aout2026</span>.
        The v1.1 freeze text is unchanged. UNKNOWN means "not evidenced", never "absent"
        (D-017): {unknown} of {relations.data?.total ?? 0} declared relations are UNKNOWN.
      </p>

      <div className="mt-6 flex flex-wrap gap-2">
        <Link
          to={`/doc?path=${encodeURIComponent(SYSTEM_CARD)}`}
          data-testid="kiltikonet-open-card"
          className="rounded border border-primary bg-primary/15 px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-sky-300 transition-colors duration-150 hover:bg-primary/25"
        >
          Full system card
        </Link>
        <Link
          to="/doc?path=audit%2FKILTIKONET-AUDIT-REPORT.md"
          data-testid="kiltikonet-open-audit"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Audit report
        </Link>
        <Link
          to="/doc?path=audit%2FPATCH-001-KILTIKONET.md"
          data-testid="kiltikonet-open-patch"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Patch record
        </Link>
        <Link
          to="/registry/kiltikonet-relations"
          data-testid="kiltikonet-open-registries"
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
        >
          Kiltikonet registries
        </Link>
      </div>

      <Section
        title="Identity reconciliation"
        note="No identity is selected. Divergent formulations are preserved side by side; unattested variants stay UNKNOWN."
      >
        <Table table={identity.data} testId="kiltikonet-identity-table" />
      </Section>

      <Section
        title="Estate relations"
        note="An edge exists only where an artefact declares it. Shared ecosystem membership creates no relation."
      >
        <Table table={relations.data} testId="kiltikonet-relations-table" />
      </Section>

      <Section
        title="Programmes"
        note="One status per programme. Names supplied without a source artefact remain UNKNOWN / source to reconcile."
      >
        <Table table={programmes.data} testId="kiltikonet-programmes-table" />
      </Section>

      <Section
        title="Data flows"
        note="SOURCE → DATA → DESTINATION → STATUS → EVIDENCE. Historical snapshot counters are never rendered as live KPIs."
      >
        <Table table={flows.data} testId="kiltikonet-data-table" />
      </Section>

      <Section
        title="Contradictions"
        note="Recorded, never resolved by fiat. Every row stays OPEN until a founder or counsel decision closes it."
      >
        <Table table={contradictions.data} testId="kiltikonet-contradictions-table" />
      </Section>

      <Section title="System card (canonical text)" note={`Rendered from ${SYSTEM_CARD}.`}>
        <div data-testid="kiltikonet-card-markdown" className="max-w-[95ch]">
          {card ? <Markdown content={card.content} docPath={SYSTEM_CARD} /> : null}
        </div>
      </Section>
    </div>
  );
}
