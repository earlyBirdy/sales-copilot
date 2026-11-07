type Props = {
  session?: any;
};

export function TraceabilityPanel({ session }: Props) {
  const source = session?.source || {};
  const summary = session?.normalized_source?.summary_bullets || [];
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Source Traceability</h2>
      <div className="space-y-2 text-sm text-slate-700">
        <div><strong>Title:</strong> {source.title || "-"}</div>
        <div><strong>Source type:</strong> {source.source_type || "-"}</div>
        <div><strong>Company:</strong> {source.sender_company || "-"}</div>
        <div><strong>URL:</strong> {source.url || "-"}</div>
        <div><strong>Input mode:</strong> {source.intake_mode || "-"}</div>
      </div>
      <div className="mt-3 rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
        <div className="font-medium">Source-grounded summary</div>
        <ul className="mt-2 list-disc pl-5">
          {summary.map((item: string) => <li key={item}>{item}</li>)}
        </ul>
      </div>
    </section>
  );
}
