import { StatusChip } from "../shared/StatusChip";

type Props = {
  sessions: any[];
  currentSessionId?: string;
  onOpen: (sessionId: string) => void;
  loading?: boolean;
};

export function SessionHistoryPanel({ sessions, currentSessionId, onOpen, loading = false }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-700">Session History</h2>
        {loading ? <StatusChip label="refreshing" tone="info" /> : null}
      </div>
      <div className="space-y-2">
        {sessions.length ? sessions.map((session) => (
          <button
            key={session.session_id}
            onClick={() => onOpen(session.session_id)}
            className="block w-full rounded-lg border border-slate-200 p-3 text-left text-sm hover:bg-slate-50"
          >
            <div className="flex items-center justify-between gap-2">
              <div className="font-medium text-slate-900">
                {session.source?.title || session.session_id}
                {session.session_id === currentSessionId ? " • current" : ""}
              </div>
              <div className="flex gap-1">
                <StatusChip label={session.status || "unknown"} tone="info" />
                <StatusChip
                  label={session.approval_state || "drafted"}
                  tone={(session.approval_state || "") === "approved" ? "success" : "warn"}
                />
              </div>
            </div>
            <div className="mt-1 text-xs text-slate-500">{session.session_id}</div>
          </button>
        )) : (
          <div className="rounded-lg border border-dashed border-slate-300 p-3 text-sm text-slate-500">
            No saved sessions yet.
          </div>
        )}
      </div>
    </section>
  );
}
