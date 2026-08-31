import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { apiGet, apiPost } from "@/lib/api";
import type { AnchorProviders, AnchorRecord } from "@/lib/insightTypes";

const STATUS_STYLES: Record<string, string> = {
  confirmed: "border-emerald-700 bg-emerald-950/60 text-emerald-300",
  pending: "border-amber-700 bg-amber-950/50 text-amber-300",
  offline: "border-rose-800 bg-rose-950/60 text-rose-300",
  unavailable: "border-neutral-600 bg-neutral-900/70 text-neutral-300",
};

/** External anchoring panel: independent evidence of temporal existence, never a
 *  qualified/eIDAS timestamp (D-020). */
export function AnchorPanel({ baseline = "v1.1" }: { baseline?: string }) {
  const qc = useQueryClient();
  const [busy, setBusy] = useState<string | null>(null);

  const { data: providers } = useQuery({
    queryKey: ["docs", "anchor", "providers"],
    queryFn: () => apiGet<AnchorProviders>("/docs/anchor/providers"),
  });

  const { data: anchors } = useQuery({
    queryKey: ["docs", "anchors"],
    queryFn: () => apiGet<AnchorRecord[]>("/docs/anchors"),
  });

  const anchorMutation = useMutation({
    mutationFn: (provider: string) =>
      apiPost<AnchorRecord>(`/docs/anchor/${baseline}?provider=${provider}`, {}),
    onSuccess: (record) => {
      qc.invalidateQueries({ queryKey: ["docs", "anchors"] });
      toast.success(`Anchor ${record.status}`, { description: record.detail });
    },
    onError: () => toast.error("Anchoring request failed"),
  });

  const upgradeMutation = useMutation({
    mutationFn: (digest: string) =>
      apiPost<AnchorRecord>(`/docs/anchor/${digest}/upgrade`, {}),
    onSuccess: (record) => {
      qc.invalidateQueries({ queryKey: ["docs", "anchors"] });
      toast.message(`Anchor ${record.status}`, { description: record.detail });
    },
    onError: () => toast.error("Upgrade failed"),
  });

  async function run(kind: "anchor" | "upgrade", value: string) {
    setBusy(`${kind}:${value}`);
    try {
      if (kind === "anchor") await anchorMutation.mutateAsync(value);
      else await upgradeMutation.mutateAsync(value);
    } finally {
      setBusy(null);
    }
  }

  return (
    <section className="mt-12">
      <h2 className="border-b border-border pb-2 text-xl font-semibold tracking-tight text-foreground">
        External anchoring
      </h2>
      <p data-testid="anchor-disclaimer" className="mt-2 max-w-[85ch] text-[13.5px] leading-relaxed text-muted-foreground">
        {providers?.disclaimer ??
          "OpenTimestamps provides independent evidence of temporal existence and integrity."}
      </p>

      <div className="mt-4 flex flex-wrap items-center gap-2">
        <button
          data-testid="anchor-submit-ots"
          disabled={busy !== null}
          onClick={() => run("anchor", "ots")}
          className="rounded border border-primary bg-primary/15 px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-sky-300 transition-colors duration-150 hover:bg-primary/25 disabled:opacity-50"
        >
          {busy === "anchor:ots" ? "Submitting…" : `Anchor ${baseline} · OpenTimestamps`}
        </button>
        <button
          data-testid="anchor-submit-rfc3161"
          disabled={busy !== null}
          onClick={() => run("anchor", "rfc3161")}
          className="rounded border border-border px-3 py-1.5 font-mono text-[11px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:border-foreground/30 hover:text-foreground disabled:opacity-50"
        >
          Qualified RFC 3161 · reserved
        </button>
        <span className="font-mono text-[10.5px] text-muted-foreground">
          calendars: {providers?.calendars.length ?? 0}
        </span>
      </div>

      <ul data-testid="anchor-list" className="mt-4 space-y-2">
        {(anchors ?? []).length === 0 && (
          <li data-testid="anchor-empty" className="font-mono text-[11.5px] text-muted-foreground">
            No anchor recorded yet.
          </li>
        )}
        {anchors?.map((a) => (
          <li
            key={a.digest}
            data-testid={`anchor-row-${a.digest.slice(0, 12)}`}
            className="border border-border bg-card/30 p-4"
          >
            <div className="flex flex-wrap items-center gap-2">
              <span
                data-testid={`anchor-status-${a.digest.slice(0, 12)}`}
                className={`rounded border px-1.5 py-0.5 font-mono text-[9.5px] font-semibold uppercase tracking-[0.1em] ${
                  STATUS_STYLES[a.status] ?? "border-border text-muted-foreground"
                }`}
              >
                {a.status}
              </span>
              <span className="font-mono text-[11px] text-foreground">{a.provider}</span>
              <span className="font-mono text-[10.5px] text-muted-foreground">
                qualified timestamp: {String(a.qualified_timestamp)}
              </span>
              {a.status === "pending" && (
                <button
                  data-testid={`anchor-upgrade-${a.digest.slice(0, 12)}`}
                  disabled={busy !== null}
                  onClick={() => run("upgrade", a.digest)}
                  className="ml-auto rounded border border-border px-2 py-0.5 font-mono text-[10px] uppercase tracking-[0.1em] text-muted-foreground transition-colors duration-150 hover:text-foreground disabled:opacity-50"
                >
                  {busy === `upgrade:${a.digest}` ? "Upgrading…" : "Upgrade proof"}
                </button>
              )}
            </div>
            <p className="mt-2 break-all font-mono text-[10.5px] text-muted-foreground">
              digest {a.digest}
            </p>
            <p className="mt-1 font-mono text-[10.5px] text-muted-foreground">
              {a.subject} · submitted {a.created_at}
              {a.upgraded_at ? ` · last upgrade ${a.upgraded_at}` : ""}
              {a.calendar ? ` · ${a.calendar}` : ""}
            </p>
            <p className="mt-1.5 text-[12.5px] text-muted-foreground">{a.detail}</p>
            {a.proof_file && (
              <p className="mt-1 font-mono text-[10.5px] text-muted-foreground">
                proof: {a.proof_file} — verify with{" "}
                <span className="text-foreground">ots verify {a.digest.slice(0, 12)}….ots</span>
              </p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
