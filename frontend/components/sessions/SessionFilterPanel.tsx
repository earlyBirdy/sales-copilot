"use client";

import { useState } from "react";

type Props = {
  onApply: (filters: Record<string, string>) => Promise<any>;
};

export function SessionFilterPanel({ onApply }: Props) {
  const [company, setCompany] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [status, setStatus] = useState("");
  const [date, setDate] = useState("");

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Session Filters</h2>
      <div className="space-y-2">
        <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" placeholder="Company" value={company} onChange={(e) => setCompany(e.target.value)} />
        <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" placeholder="Source type" value={sourceType} onChange={(e) => setSourceType(e.target.value)} />
        <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" placeholder="Status" value={status} onChange={(e) => setStatus(e.target.value)} />
        <input className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" placeholder="Date contains YYYY-MM-DD" value={date} onChange={(e) => setDate(e.target.value)} />
        <button
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
          onClick={() => onApply({ company, source_type: sourceType, status, date })}
        >
          Apply Filters
        </button>
      </div>
    </section>
  );
}
