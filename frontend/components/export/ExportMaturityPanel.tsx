type Props = {
  session?: any;
  onExport: (payload: any) => Promise<any>;
  onMarkdown: (payload: any) => Promise<any>;
  onEmailReady: (payload: any) => Promise<any>;
};

export function ExportMaturityPanel({ session, onExport, onMarkdown, onEmailReady }: Props) {
  const sessionId = session?.session_id;
  const exportMeta = session?.final_pack?.export_meta || {};

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Export Maturity</h2>
      <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
        <div>Copy-ready blocks: {(session?.final_pack?.final_editable_blocks || []).length}</div>
        <div>CRM note: {exportMeta.crm_note ? "available" : "not built yet"}</div>
        <div>Email-ready block: {exportMeta.email_ready_block ? "available" : "not built yet"}</div>
      </div>
      <div className="flex flex-wrap gap-2">
        <button className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50" disabled={!sessionId} onClick={() => sessionId && onExport({ session_id: sessionId })}>
          Build Final Pack
        </button>
        <button className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50" disabled={!sessionId} onClick={() => sessionId && onMarkdown({ session_id: sessionId })}>
          Markdown Bundle
        </button>
        <button className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50" disabled={!sessionId} onClick={() => sessionId && onEmailReady({ session_id: sessionId })}>
          Email-ready Block
        </button>
      </div>
    </section>
  );
}
