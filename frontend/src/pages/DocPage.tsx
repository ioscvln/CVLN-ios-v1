import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { DocDetail } from "@/lib/types";
import { Markdown } from "@/components/Markdown";
import { StatusBadge } from "@/components/StatusBadge";

const REPO_LINKS: Array<{ label: string; url: string }> = [
  { label: "MetaCVLN", url: "https://github.com/metacvln-spec/MetaCVLN" },
  {
    label: "CVLNAgentfactory",
    url: "https://github.com/frekcore/CVLNAgentfactory/tree/CVLN-AGENT-FACTORY",
  },
  { label: "Laurent.ia", url: "https://github.com/cultureconnectorg/Laurent.ia/tree/public" },
];

function MetaField({ label, value }: { label: string; value: string }) {
  if (!value) return null;
  return (
    <div className="min-w-0">
      <dt className="font-mono text-[10px] font-semibold uppercase tracking-[0.15em] text-muted-foreground">
        {label}
      </dt>
      <dd className="mt-0.5 text-[12.5px] text-foreground/90">{value}</dd>
    </div>
  );
}

export default function DocPage() {
  const [params] = useSearchParams();
  const path = params.get("path") ?? "README.md";

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["docs", "file", path],
    queryFn: () => apiGet<DocDetail>(`/docs/file?path=${encodeURIComponent(path)}`),
  });

  if (isLoading) {
    return (
      <p data-testid="doc-loading" className="px-8 py-10 font-mono text-xs text-muted-foreground">
        Loading document…
      </p>
    );
  }

  if (isError || !data) {
    return (
      <div data-testid="doc-error" className="px-8 py-10">
        <h1 className="text-xl font-semibold text-rose-400">Document unavailable</h1>
        <p className="mt-2 font-mono text-xs text-muted-foreground">
          {path} — {error instanceof Error ? error.message : "unknown error"}
        </p>
      </div>
    );
  }

  const proposed = data.status === "PROPOSED";

  return (
    <div className="flex">
      <article className="min-w-0 flex-1 px-6 py-8 sm:px-10 lg:px-14">
        <p
          data-testid="doc-canonical-path"
          className="font-mono text-[10.5px] uppercase tracking-[0.15em] text-muted-foreground"
        >
          cvln-intelligence-os / {data.path}
        </p>

        <div
          data-testid="doc-spec-header"
          className={`mt-3 rounded border p-4 ${
            proposed ? "border-dashed border-amber-700/70 bg-amber-950/15" : "border-border bg-card/40"
          }`}
        >
          <div className="flex flex-wrap items-center gap-2">
            <StatusBadge value={data.status} testId="doc-status-badge" />
            <span
              data-testid="doc-attribution-badge"
              className="rounded border border-border bg-secondary/50 px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-[0.09em] text-muted-foreground"
            >
              {data.attribution || "UNSPECIFIED"}
            </span>
            <span className="font-mono text-[10px] uppercase tracking-[0.12em] text-muted-foreground">
              v{data.version || "—"} · {data.word_count} words
            </span>
          </div>

          <h1 data-testid="doc-title" className="mt-3 text-2xl font-semibold tracking-tight text-foreground">
            {data.title}
          </h1>
          {data.purpose && (
            <p data-testid="doc-purpose" className="mt-1.5 max-w-[80ch] text-[13.5px] text-muted-foreground">
              {data.purpose}
            </p>
          )}

          <dl className="mt-4 grid grid-cols-1 gap-3 border-t border-border pt-3 sm:grid-cols-3">
            <MetaField label="Ownership" value={data.ownership} />
            <MetaField label="Scope" value={data.scope} />
            <MetaField label="Section" value={data.section} />
          </dl>

          {proposed && (
            <p
              data-testid="doc-proposed-warning"
              className="mt-3 border-t border-dashed border-amber-700/60 pt-2.5 font-mono text-[11px] leading-relaxed text-amber-300"
            >
              TARGET SPEC — this artefact was not found in any audited repository. It is a
              proposal and must not be cited as an existing CVLN capability.
            </p>
          )}
        </div>

        <div className="mt-8">
          <Markdown content={data.content} docPath={data.path} />
        </div>
      </article>

      <aside className="sticky top-14 hidden h-[calc(100vh-3.5rem)] w-64 shrink-0 overflow-y-auto border-l border-border px-4 py-8 xl:block">
        <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
          On this page
        </p>
        <nav data-testid="doc-toc" className="mt-3 space-y-1">
          {data.headings
            .filter((h) => h.level >= 2)
            .map((h) => (
              <a
                key={`${h.slug}-${h.text}`}
                href={`#${h.slug}`}
                data-testid={`toc-link-${h.slug}`}
                className={`block truncate text-[12px] text-muted-foreground transition-colors duration-150 hover:text-foreground ${
                  h.level === 3 ? "pl-3" : ""
                }`}
              >
                {h.text}
              </a>
            ))}
        </nav>

        <div className="mt-8 border-t border-border pt-4">
          <p className="font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
            Audited repositories
          </p>
          <ul className="mt-2.5 space-y-1.5">
            {REPO_LINKS.map((repo) => (
              <li key={repo.label}>
                <a
                  href={repo.url}
                  target="_blank"
                  rel="noreferrer"
                  data-testid={`evidence-repo-${repo.label}`}
                  className="font-mono text-[11px] text-sky-400 transition-colors duration-150 hover:text-sky-300"
                >
                  {repo.label} ↗
                </a>
              </li>
            ))}
          </ul>
        </div>
      </aside>
    </div>
  );
}
