import { statusToken, severityToken } from "@/lib/status";

interface Props {
  value: string;
  kind?: "status" | "severity";
  testId?: string;
  className?: string;
}

export function StatusBadge({ value, kind = "status", testId, className = "" }: Props) {
  const token = kind === "status" ? statusToken(value) : severityToken(value);
  return (
    <span
      data-testid={testId}
      title={value}
      className={`inline-flex shrink-0 items-center gap-1 rounded border px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase leading-none tracking-[0.09em] ${token} ${className}`}
    >
      {value}
    </span>
  );
}
