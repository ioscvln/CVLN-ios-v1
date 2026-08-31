import { useMemo, useState } from "react";
import { Link, NavLink, useLocation, useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import { InvariantAlert } from "@/components/InvariantAlert";
import type { DocTree } from "@/lib/types";
import { StatusBadge } from "./StatusBadge";

const NAV = [
  { to: "/", label: "Overview", testId: "nav-overview" },
  { to: "/matrix", label: "Component Matrix", testId: "nav-matrix" },
  { to: "/gaps", label: "Gap Analysis", testId: "nav-gaps" },
  { to: "/freeze", label: "Freeze v1.1", testId: "nav-freeze" },
  { to: "/decisions", label: "Decisions", testId: "nav-decisions" },
  { to: "/registry/ecosystem", label: "Registries", testId: "nav-registries" },
  { to: "/graph", label: "Traceability", testId: "nav-graph" },
  { to: "/kiltikonet", label: "Kiltikonet", testId: "nav-kiltikonet" },
  { to: "/systems", label: "System Cards", testId: "nav-systems" },
  { to: "/drift", label: "Drift Control", testId: "nav-drift" },
  { to: "/architecture", label: "Current vs Target", testId: "nav-architecture" },
  { to: "/search", label: "Search", testId: "nav-search" },
];

function fileLabel(path: string): string {
  const name = path.split("/").pop() ?? path;
  return name.replace(/\.md$/, "");
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [params] = useSearchParams();
  const activePath = params.get("path") ?? "";
  const [query, setQuery] = useState("");
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  const { data: tree } = useQuery({
    queryKey: ["docs", "tree"],
    queryFn: () => apiGet<DocTree>("/docs/tree"),
  });

  const activeSection = useMemo(
    () => tree?.sections.find((s) => s.documents.some((d) => d.path === activePath))?.section,
    [tree, activePath],
  );

  function submitSearch(e: React.FormEvent) {
    e.preventDefault();
    if (query.trim().length >= 2) navigate(`/search?q=${encodeURIComponent(query.trim())}`);
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <InvariantAlert />
      <header className="sticky top-0 z-50 flex h-14 w-full items-center gap-4 border-b border-border bg-background/95 px-4 backdrop-blur">
        <Link to="/" data-testid="brand-home-link" className="flex items-baseline gap-2.5">
          <span className="font-mono text-[13px] font-semibold tracking-[0.16em] text-foreground">
            CVLN-INTELLIGENCE-OS
          </span>
          <span className="hidden font-mono text-[10px] uppercase tracking-[0.14em] text-muted-foreground sm:inline">
            {tree?.version ?? "OS v1.1"}
          </span>
        </Link>

        <nav className="ml-4 hidden items-center gap-1 lg:flex">
          {NAV.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              data-testid={item.testId}
              end={item.to === "/"}
              className={({ isActive }) =>
                `rounded px-2.5 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] transition-colors duration-150 ${
                  isActive
                    ? "bg-secondary text-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <form onSubmit={submitSearch} className="ml-auto flex items-center">
          <input
            data-testid="global-search-input"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search specification…"
            aria-label="Search specification"
            className="w-40 rounded border border-input bg-secondary/40 px-2.5 py-1.5 font-mono text-[11px] text-foreground outline-none transition-colors duration-150 placeholder:text-muted-foreground focus:border-primary sm:w-56"
          />
          <button
            type="submit"
            data-testid="global-search-submit"
            className="ml-1.5 rounded border border-border px-2.5 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground"
          >
            Query
          </button>
        </form>
      </header>

      <div className="flex">
        <aside
          data-testid="doc-tree-sidebar"
          className="sticky top-14 hidden h-[calc(100vh-3.5rem)] w-72 shrink-0 overflow-y-auto border-r border-border bg-sidebar px-3 py-4 md:block"
        >
          <p className="mb-3 px-1 font-mono text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
            Canonical corpus · {tree?.total_documents ?? "—"} documents
          </p>

          {tree?.sections.map((section) => {
            const open = !(collapsed[section.section] ?? section.section !== (activeSection ?? "root"));
            return (
              <div key={section.section} className="mb-1">
                <button
                  data-testid={`tree-section-${section.section}`}
                  onClick={() =>
                    setCollapsed((prev) => ({ ...prev, [section.section]: open }))
                  }
                  className="flex w-full items-center gap-1.5 rounded px-1 py-1.5 text-left font-mono text-[10.5px] uppercase tracking-[0.13em] text-muted-foreground transition-colors duration-150 hover:text-foreground"
                >
                  <span className="w-2 text-[9px]">{open ? "▾" : "▸"}</span>
                  {section.label}
                  <span className="ml-auto text-[9.5px] text-muted-foreground/60">
                    {section.documents.length}
                  </span>
                </button>

                {open && (
                  <ul className="mb-2 ml-3 border-l border-border pl-2">
                    {section.documents.map((doc) => (
                      <li key={doc.path}>
                        <Link
                          to={`/doc?path=${encodeURIComponent(doc.path)}`}
                          data-testid={`tree-doc-${doc.path}`}
                          className={`flex items-center gap-1.5 rounded px-1.5 py-1 text-[12px] transition-colors duration-150 ${
                            doc.path === activePath
                              ? "bg-secondary text-foreground"
                              : "text-muted-foreground hover:text-foreground"
                          }`}
                        >
                          <span className="truncate font-mono text-[11px]">
                            {fileLabel(doc.path)}
                          </span>
                          {doc.status === "PROPOSED" && (
                            <span
                              title="PROPOSED"
                              className="ml-auto shrink-0 rounded border border-dashed border-amber-600/80 px-1 font-mono text-[8.5px] text-amber-400"
                            >
                              PROP
                            </span>
                          )}
                        </Link>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            );
          })}
        </aside>

        <main key={location.key} className="min-w-0 flex-1 cvln-reveal">
          {children}
        </main>
      </div>
    </div>
  );
}

export { StatusBadge };
