import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { SearchResponse } from "@/lib/types";
import { StatusBadge } from "@/components/StatusBadge";

export default function SearchPage() {
  const [params, setParams] = useSearchParams();
  const q = params.get("q") ?? "";
  const [draft, setDraft] = useState(q);

  const { data, isLoading, isError } = useQuery({
    queryKey: ["docs", "search", q],
    queryFn: () => apiGet<SearchResponse>(`/docs/search?q=${encodeURIComponent(q)}`),
    enabled: q.trim().length >= 2,
  });

  return (
    <div className="px-6 py-8 sm:px-10 lg:px-14">
      <p className="font-mono text-[10.5px] uppercase tracking-[0.16em] text-muted-foreground">
        Corpus query
      </p>
      <h1 data-testid="search-title" className="mt-2 text-2xl font-semibold tracking-tight text-foreground">
        Search the specification
      </h1>

      <form
        className="mt-5 flex max-w-2xl items-center gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          if (draft.trim().length >= 2) setParams({ q: draft.trim() });
        }}
      >
        <input
          data-testid="search-page-input"
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="doctrine, provider_layer, sovereign, ADL…"
          aria-label="Search the specification corpus"
          className="flex-1 rounded border border-input bg-secondary/40 px-3 py-2 font-mono text-[12.5px] text-foreground outline-none transition-colors duration-150 placeholder:text-muted-foreground focus:border-primary"
        />
        <button
          type="submit"
          data-testid="search-page-submit"
          className="rounded border border-primary bg-primary/15 px-3 py-2 font-mono text-[11px] uppercase tracking-[0.1em] text-sky-300 transition-colors duration-150 hover:bg-primary/25"
        >
          Query
        </button>
      </form>

      {q.trim().length < 2 && (
        <p data-testid="search-empty-state" className="mt-8 font-mono text-[12px] text-muted-foreground">
          Enter at least two characters. Search runs over the canonical Markdown corpus on disk.
        </p>
      )}

      {isLoading && q && (
        <p data-testid="search-loading" className="mt-8 font-mono text-xs text-muted-foreground">
          Searching corpus…
        </p>
      )}

      {isError && (
        <p data-testid="search-error" className="mt-8 font-mono text-xs text-rose-400">
          Search failed.
        </p>
      )}

      {data && (
        <>
          <p data-testid="search-result-count" className="mt-6 font-mono text-[11px] text-muted-foreground">
            {data.total} document{data.total === 1 ? "" : "s"} matching “{data.query}”
          </p>
          <ul data-testid="search-results" className="mt-3 divide-y divide-border border-y border-border">
            {data.results.map((hit) => (
              <li key={hit.path} className="py-3.5">
                <div className="flex flex-wrap items-center gap-2">
                  <Link
                    to={`/doc?path=${encodeURIComponent(hit.path)}`}
                    data-testid={`search-result-${hit.path}`}
                    className="text-[14px] font-medium text-foreground transition-colors duration-150 hover:text-sky-300"
                  >
                    {hit.title}
                  </Link>
                  <StatusBadge value={hit.status} />
                  <span className="font-mono text-[10px] text-muted-foreground">
                    {hit.hits} occurrence{hit.hits === 1 ? "" : "s"}
                  </span>
                </div>
                <p className="mt-0.5 font-mono text-[10.5px] uppercase tracking-[0.11em] text-muted-foreground">
                  {hit.path}
                </p>
                {hit.snippet && (
                  <p className="mt-1.5 max-w-[95ch] text-[12.5px] leading-relaxed text-muted-foreground">
                    …{hit.snippet}…
                  </p>
                )}
              </li>
            ))}
          </ul>
          {data.total === 0 && (
            <p data-testid="search-no-results" className="mt-6 font-mono text-[12px] text-muted-foreground">
              No document in the corpus contains that term.
            </p>
          )}
        </>
      )}
    </div>
  );
}
