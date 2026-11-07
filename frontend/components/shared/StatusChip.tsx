type Props = {
  label: string;
  tone?: "neutral" | "success" | "warn" | "info";
};

export function StatusChip({ label, tone = "neutral" }: Props) {
  const cls =
    tone === "success"
      ? "border-green-200 bg-green-50 text-green-700"
      : tone === "warn"
      ? "border-amber-200 bg-amber-50 text-amber-700"
      : tone === "info"
      ? "border-blue-200 bg-blue-50 text-blue-700"
      : "border-slate-300 bg-white text-slate-700";

  return (
    <span className={`inline-flex rounded-full border px-2 py-1 text-xs ${cls}`}>
      {label}
    </span>
  );
}
