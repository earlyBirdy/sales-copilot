type Props = {
  sessionId?: string;
  finalBlocks: { label: string; text: string }[];
  onExport: (payload: { session_id: string; draft_ids?: string[] }) => Promise<any>;
  loading?: boolean;
};

export function ExportPanel({ sessionId, finalBlocks, onExport, loading = false }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold tracking-wide text-slate-700 uppercase">Export</h2>
      <div className="mb-3 flex gap-2">
        <button
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm disabled:opacity-50"
          onClick={() => sessionId && onExport({ session_id: sessionId })}
          disabled={!sessionId || loading}
        >
          Build Final Pack
        </button>
      </div>
      <div className="space-y-4">
        {finalBlocks.length ? (
          finalBlocks.map((block) => (
            <div key={block.label} className="rounded-lg border border-slate-200 p-3">
              <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">{block.label}</div>
              <div className="whitespace-pre-wrap text-sm text-slate-800">{block.text}</div>
            </div>
          ))
        ) : (
          <div className="rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
            Build the final pack to see exportable blocks.
          </div>
        )}
      </div>
    </section>
  );
}
