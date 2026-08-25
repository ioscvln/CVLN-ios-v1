import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { DocDetail } from "@/lib/types";
import { Mermaid } from "@/components/Mermaid";
import { StatusBadge } from "@/components/StatusBadge";

const CURRENT_DIAGRAM = `graph TB
  META["META CVLN<br/>governance plane"]
  FACT["CVLN AGENT FACTORY<br/>agent runtime"]
  LAUR["LAURENTIA<br/>operator product"]
  PROV["Model providers"]
  META -->|"HTTP adapter"| LAUR
  META -.->|"capabilities · DEGRADED"| FACT
  META -.->|"capabilities · DEGRADED"| LAUR
  FACT --> PROV
  LAUR --> PROV
  META --> PROV
  FACT -.->|"absent"| META
  LAUR -.->|"absent"| FACT`;

const TARGET_DIAGRAM = `graph TB
  APP["Layer 4 · Applications"]
  LAUR["Layer 3 · LAURENTIA"]
  FACT["Layer 2 · CVLN AGENT FACTORY"]
  BRAIN["Layer 1 · CVL BRAIN"]
  META["Layer 0 · META CVLN"]
  APP -->|"contracts only"| LAUR
  LAUR -->|"capability execution"| FACT
  LAUR -->|"cognition"| BRAIN
  FACT -->|"doctrine + reasoning"| BRAIN
  BRAIN -->|"constitution"| META
  FACT -->|"registry + gates"| META`;

const EDGES: Array<{ edge: string; current: string; target: string; delta: string }> = [
  { edge: "Applications → Laurentia", current: "UNVERIFIED", target: "Contract-only", delta: "Publish official contracts" },
  { edge: "Laurentia → Agent Factory", current: "absent", target: "Capability execution", delta: "New integration (G-001)" },
  { edge: "Laurentia → Brain", current: "in-process wrapper", target: "Remote Brain service", delta: "Extract Brain (G-004)" },
  { edge: "Agent Factory → Brain", current: "local provider_layer", target: "Brain-owned routing", delta: "Move router (C-006, FD-004)" },
  { edge: "Brain → META", current: "absent", target: "Constitution + permissions", delta: "New integration" },
  { edge: "Agent Factory → META", current: "absent", target: "Registry + gate authority", delta: "New integration (G-001)" },
  { edge: "META → Laurentia", current: "HTTP adapter, implemented", target: "Retained for actuation", delta: "Keep, no longer the only edge" },
  { edge: "Any → /api/capabilities", current: "12/12 DEGRADED", target: "All systems advertise", delta: "Implement provider side (G-002)" },
];

export default function ArchitecturePage() {
  const { data: target } = useQuery({
    queryKey: ["docs", "file", "audit/TARGET-ARCHITECTURE.md"],
    queryFn: () => apiGet<DocDetail>("/docs/file?path=audit/TARGET-ARCHITECTURE.md"),
  });

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Phase 1 versus Phase 3
      </p>
      <h1 data-testid="architecture-title" className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
        Current versus Target Architecture
      </h1>
      <p className="mt-2 max-w-[80ch] text-[13.5px] leading-relaxed text-muted-foreground">
        Left is what repository evidence establishes. Right is the ratification target. Dotted
        edges are UNVERIFIED, unanswered, or absent. Not one target edge is implemented today.
      </p>

      <div className="mt-8 grid grid-cols-1 gap-5 xl:grid-cols-2">
        <section data-testid="current-state-panel" className="border border-border bg-card/30 p-4">
          <div className="flex items-center gap-2">
            <h2 className="text-[15px] font-semibold text-foreground">Current state</h2>
            <StatusBadge value="IMPLEMENTED" testId="current-state-status" />
          </div>
          <p className="mt-1.5 text-[12.5px] text-muted-foreground">
            Three independent systems sharing a vocabulary. One realised runtime edge, and it runs
            opposite to the canonical direction.
          </p>
          <Mermaid code={CURRENT_DIAGRAM} />
          <Link
            to="/doc?path=audit/CURRENT-STATE-ARCHITECTURE.md"
            data-testid="architecture-current-link"
            className="font-mono text-[11px] text-sky-400 hover:text-sky-300"
          >
            audit/CURRENT-STATE-ARCHITECTURE.md ↗
          </Link>
        </section>

        <section
          data-testid="target-state-panel"
          className="border border-dashed border-amber-700/70 bg-amber-950/10 p-4"
        >
          <div className="flex items-center gap-2">
            <h2 className="text-[15px] font-semibold text-foreground">Target state</h2>
            <StatusBadge value={target?.status ?? "PROPOSED"} testId="target-state-status" />
          </div>
          <p className="mt-1.5 text-[12.5px] text-muted-foreground">
            The canonical five-layer model. Every edge below is PROPOSED and describes no existing
            capability.
          </p>
          <Mermaid code={TARGET_DIAGRAM} />
          <Link
            to="/doc?path=audit/TARGET-ARCHITECTURE.md"
            data-testid="architecture-target-link"
            className="font-mono text-[11px] text-sky-400 hover:text-sky-300"
          >
            audit/TARGET-ARCHITECTURE.md ↗
          </Link>
        </section>
      </div>

      <section className="mt-12">
        <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
          Edge-by-edge delta
        </h2>
        <div className="mt-4 overflow-x-auto rounded border border-border">
          <table data-testid="edge-delta-table" className="w-full border-collapse text-[12.5px]">
            <thead>
              <tr>
                {["Edge", "Current", "Target", "Delta"].map((h) => (
                  <th
                    key={h}
                    className="border-b border-border bg-sidebar px-3 py-2 text-left font-mono text-[10px] font-semibold uppercase tracking-[0.11em] text-muted-foreground"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {EDGES.map((row) => (
                <tr
                  key={row.edge}
                  data-testid={`edge-row-${row.edge}`}
                  className="border-b border-border transition-colors duration-150 last:border-0 hover:bg-white/[0.02]"
                >
                  <td className="px-3 py-2 font-mono text-[11.5px] text-foreground">{row.edge}</td>
                  <td className="px-3 py-2 text-muted-foreground">{row.current}</td>
                  <td className="px-3 py-2 text-muted-foreground">{row.target}</td>
                  <td className="px-3 py-2 text-muted-foreground">{row.delta}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
