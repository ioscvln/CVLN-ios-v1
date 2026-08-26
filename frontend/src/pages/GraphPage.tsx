import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { TraceGraph } from "@/lib/freezeTypes";
import { Mermaid } from "@/components/Mermaid";

const KINDS = ["system", "component", "decision", "vulnerability", "continuity", "legal", "gap"];

function safeId(id: string): string {
  return id.replace(/[^A-Za-z0-9]/g, "_");
}

function label(text: string): string {
  return text.replace(/["`\\[\]{}()]/g, "").slice(0, 46);
}

export default function GraphPage() {
  const [kinds, setKinds] = useState<string[]>(["system", "component", "decision", "vulnerability"]);

  const { data, isLoading } = useQuery({
    queryKey: ["docs", "graph"],
    queryFn: () => apiGet<TraceGraph>("/docs/graph"),
  });

  const code = useMemo(() => {
    if (!data) return "";
    const visible = new Set(
      data.nodes.filter((n) => kinds.includes(n.kind)).map((n) => n.id),
    );
    const lines = ["graph LR"];
    for (const n of data.nodes) {
      if (!visible.has(n.id)) continue;
      const shape =
        n.kind === "system"
          ? `[["${label(n.label)}"]]`
          : n.kind === "decision"
            ? `{{"${label(n.label)}"}}`
            : n.kind === "vulnerability"
              ? `(["${label(n.label)}"])`
              : `["${label(n.label)}"]`;
      lines.push(`  ${safeId(n.id)}${shape}`);
    }
    for (const e of data.edges) {
      if (!visible.has(e.source) || !visible.has(e.target)) continue;
      lines.push(`  ${safeId(e.source)} -->|${e.kind}| ${safeId(e.target)}`);
    }
    return lines.join("\n");
  }, [data, kinds]);

  const shown = data?.nodes.filter((n) => kinds.includes(n.kind)).length ?? 0;

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Traceability · derived from the registries at request time
      </p>
      <h1 data-testid="graph-title" className="mt-2 text-3xl font-semibold tracking-tight text-foreground">
        Traceability graph
      </h1>
      <p className="mt-3 max-w-[80ch] text-[14px] leading-relaxed text-muted-foreground">
        Every node comes from a registry row; every edge comes from a declared reference. Nothing
        here is authored by hand — if an edge is missing, the registry does not declare it.
      </p>

      <div className="mt-6 flex flex-wrap items-center gap-2">
        {KINDS.map((k) => (
          <button
            key={k}
            data-testid={`graph-kind-${k}`}
            onClick={() =>
              setKinds((prev) => (prev.includes(k) ? prev.filter((x) => x !== k) : [...prev, k]))
            }
            className={`rounded border px-2.5 py-1 font-mono text-[10.5px] uppercase tracking-[0.1em] transition-colors duration-150 ${
              kinds.includes(k)
                ? "border-primary bg-primary/15 text-sky-300"
                : "border-border text-muted-foreground hover:text-foreground"
            }`}
          >
            {k}
          </button>
        ))}
        <span data-testid="graph-counts" className="ml-auto font-mono text-[11px] text-muted-foreground">
          {shown} / {data?.total_nodes ?? 0} nodes · {data?.total_edges ?? 0} declared edges
        </span>
      </div>

      <div className="mt-6 overflow-x-auto border border-border bg-card/20 p-4">
        {isLoading || !code ? (
          <p className="font-mono text-[12px] text-muted-foreground">Building graph…</p>
        ) : (
          <div data-testid="graph-canvas">
            <Mermaid code={code} />
          </div>
        )}
      </div>
    </div>
  );
}
