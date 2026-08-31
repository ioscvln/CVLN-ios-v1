import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";
import type { FreezeState } from "@/lib/freezeTypes";

/** Estate-wide alert: shown on every page as soon as one freeze invariant is violated. */
export function InvariantAlert() {
  const { data } = useQuery({
    queryKey: ["docs", "freeze"],
    queryFn: () => apiGet<FreezeState>("/docs/freeze"),
    refetchInterval: 60_000,
  });

  const failed = data?.invariants.filter((i) => !i.passed) ?? [];
  if (!data || failed.length === 0) return null;

  return (
    <div
      data-testid="invariant-alert-banner"
      role="alert"
      className="sticky top-0 z-50 border-b border-rose-700 bg-rose-950/95 px-6 py-2.5 backdrop-blur"
    >
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <span className="rounded border border-rose-700 bg-rose-900/80 px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.14em] text-rose-200">
          Freeze violation
        </span>
        <span data-testid="invariant-alert-count" className="font-mono text-[12px] text-rose-100">
          {failed.length} of {data.invariants.length} invariants violated:{" "}
          {failed.map((f) => f.id).join(", ")}
        </span>
        <Link
          to="/freeze"
          data-testid="invariant-alert-link"
          className="ml-auto font-mono text-[11px] uppercase tracking-[0.1em] text-rose-200 underline transition-colors duration-150 hover:text-white"
        >
          Inspect
        </Link>
      </div>
    </div>
  );
}
