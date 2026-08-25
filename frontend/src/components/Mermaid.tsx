import { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";

let initialised = false;

function init() {
  if (initialised) return;
  mermaid.initialize({
    startOnLoad: false,
    theme: "dark",
    securityLevel: "loose",
    fontFamily: "'IBM Plex Sans', sans-serif",
    themeVariables: {
      background: "#0B1120",
      primaryColor: "#111827",
      primaryTextColor: "#E2E8F0",
      primaryBorderColor: "#334155",
      lineColor: "#64748B",
      secondaryColor: "#0E131F",
      tertiaryColor: "#0B1120",
      fontSize: "13px",
    },
  });
  initialised = true;
}

let seq = 0;

export function Mermaid({ code }: { code: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    init();
    seq += 1;
    const id = `cvln-mermaid-${seq}`;
    mermaid
      .render(id, code)
      .then(({ svg }) => {
        if (!cancelled && ref.current) {
          ref.current.innerHTML = svg;
          setError(null);
        }
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "diagram failed to render");
      });
    return () => {
      cancelled = true;
    };
  }, [code]);

  if (error) {
    return (
      <div
        data-testid="mermaid-error"
        className="cvln-mermaid font-mono text-xs text-amber-400"
      >
        Diagram could not be rendered. Source:
        <pre className="mt-2 whitespace-pre-wrap text-[11px] text-slate-400">{code}</pre>
      </div>
    );
  }

  return <div data-testid="mermaid-diagram" ref={ref} className="cvln-mermaid cvln-grid" />;
}
