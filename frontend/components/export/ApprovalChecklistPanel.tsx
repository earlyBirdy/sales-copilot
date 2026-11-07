type Props = {
  reviewNotes?: string[];
  annotations?: any[];
};

const CHECKLIST = [
  "Source is relevant to target audience",
  "Claims look supported by the source",
  "CTA is appropriate and not too strong",
  "Tone matches the intended recipient",
  "Export block has been edited if needed",
];

export function ApprovalChecklistPanel({ reviewNotes = [], annotations = [] }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Approval Checklist</h2>
      <div className="space-y-2">
        {CHECKLIST.map((item) => (
          <label key={item} className="flex items-start gap-2 rounded-lg border border-slate-200 p-2 text-sm">
            <input type="checkbox" />
            <span>{item}</span>
          </label>
        ))}
      </div>
      {reviewNotes.length ? (
        <div className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
          <div className="font-medium">Guardrail notes</div>
          <ul className="mt-2 list-disc pl-5">
            {reviewNotes.map((note, idx) => <li key={idx}>{note}</li>)}
          </ul>
        </div>
      ) : null}
      {annotations.length ? (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          <div className="font-medium">Flagged phrases</div>
          <ul className="mt-2 list-disc pl-5">
            {annotations.map((a, idx) => <li key={idx}>{a.term}: {a.note}</li>)}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
