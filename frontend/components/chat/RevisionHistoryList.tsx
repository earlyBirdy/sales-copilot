type Props = {
  items: { revision_id: string; draft_id: string; instruction: string; result_text: string }[];
};

export function RevisionHistoryList({ items }: Props) {
  return (
    <div className="space-y-2">
      {items.length ? (
        items.map((item) => (
          <div key={item.revision_id} className="rounded-lg border border-slate-200 p-3 text-sm text-slate-700">
            <div className="mb-1 flex items-center justify-between">
              <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                {item.draft_id}
              </div>
              <div className="text-xs text-slate-400">{item.revision_id}</div>
            </div>
            <div className="mb-2 rounded bg-slate-50 p-2 text-slate-600">
              Instruction: {item.instruction}
            </div>
            <div className="whitespace-pre-wrap">{item.result_text}</div>
          </div>
        ))
      ) : (
        <div className="rounded-lg border border-slate-200 p-3 text-sm text-slate-700">
          Revision history will appear here.
        </div>
      )}
    </div>
  );
}
