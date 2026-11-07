type Props = {
  sessionId?: string;
  onMarkdownExport: (payload: any) => Promise<any>;
};

export function ExportFormatPanel({ sessionId, onMarkdownExport }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Export Formats</h2>
      <div className="flex gap-2">
        <button
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50"
          disabled={!sessionId}
          onClick={() => sessionId && onMarkdownExport({ session_id: sessionId })}
        >
          Markdown Export
        </button>
      </div>
    </section>
  );
}
