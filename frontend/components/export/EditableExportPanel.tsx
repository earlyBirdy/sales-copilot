"use client";

import { useState } from "react";
import { StatusChip } from "../shared/StatusChip";

type Props = {
  sessionId?: string;
  finalBlocks: { label: string; text: string }[];
  onSave: (sessionId: string, label: string, text: string) => Promise<any>;
  onApprove: (sessionId: string, state: string) => Promise<any>;
  loading?: boolean;
  approvalState?: string;
};

export function EditableExportPanel({
  sessionId,
  finalBlocks,
  onSave,
  onApprove,
  loading = false,
  approvalState = "drafted",
}: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-700">Editable Export Blocks</h2>
        <StatusChip label={approvalState} tone={approvalState === "approved" ? "success" : "warn"} />
      </div>
      <div className="mb-3 flex flex-wrap gap-2">
        {["drafted", "reviewed", "approved", "exported"].map((state) => (
          <button
            key={state}
            className={`rounded-lg px-3 py-1.5 text-sm ${approvalState === state ? "bg-slate-900 text-white" : "border border-slate-300"}`}
            onClick={() => sessionId && onApprove(sessionId, state)}
            disabled={!sessionId || loading}
          >
            {state}
          </button>
        ))}
      </div>
      <div className="space-y-4">
        {finalBlocks.length ? finalBlocks.map((block) => (
          <EditableBlockRow
            key={block.label}
            sessionId={sessionId}
            label={block.label}
            text={block.text}
            onSave={onSave}
            loading={loading}
          />
        )) : (
          <div className="rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
            Build final pack first.
          </div>
        )}
      </div>
    </section>
  );
}

function EditableBlockRow({
  sessionId,
  label,
  text,
  onSave,
  loading,
}: {
  sessionId?: string;
  label: string;
  text: string;
  onSave: (sessionId: string, label: string, text: string) => Promise<any>;
  loading: boolean;
}) {
  const [value, setValue] = useState(text);
  const dirty = value !== text;

  return (
    <div className="rounded-lg border border-slate-200 p-3">
      <div className="mb-2 flex items-center justify-between">
        <div className="text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</div>
        {dirty ? <StatusChip label="edited" tone="info" /> : null}
      </div>
      <textarea
        className="min-h-[100px] w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
      <div className="mt-2">
        <button
          className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm disabled:opacity-50"
          onClick={() => sessionId && onSave(sessionId, label, value)}
          disabled={!sessionId || loading || !dirty}
        >
          Save Edit
        </button>
      </div>
    </div>
  );
}
