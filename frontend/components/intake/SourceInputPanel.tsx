"use client";

import { useState } from "react";
import { SectionCard } from "../shared/SectionCard";

type Props = {
  onAnalyze: (payload: {
    source_type: string;
    title: string;
    raw_text: string;
    sender_company?: string;
    url?: string;
    user_goal?: string;
  }) => Promise<any>;
  loading?: boolean;
};

export function SourceInputPanel({ onAnalyze, loading = false }: Props) {
  const [sourceType, setSourceType] = useState("email");
  const [title, setTitle] = useState("");
  const [rawText, setRawText] = useState("");
  const [senderCompany, setSenderCompany] = useState("");
  const [url, setUrl] = useState("");
  const [goal, setGoal] = useState("");
  const [localError, setLocalError] = useState("");

  const submit = async () => {
    if (!rawText.trim()) return setLocalError("Source text is required.");
    if (!title.trim()) return setLocalError("Title is required.");
    setLocalError("");
    await onAnalyze({
      source_type: sourceType,
      title,
      raw_text: rawText,
      sender_company: senderCompany,
      url,
      user_goal: goal,
    });
  };

  return (
    <SectionCard title="Source Intake">
      {localError ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {localError}
        </div>
      ) : null}
      <input
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <select
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        value={sourceType}
        onChange={(e) => setSourceType(e.target.value)}
      >
        <option value="email">Email</option>
        <option value="article">Article</option>
        <option value="press_release">Press release</option>
        <option value="announcement">Announcement</option>
        <option value="note">Note</option>
      </select>
      <input
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Sender / company"
        value={senderCompany}
        onChange={(e) => setSenderCompany(e.target.value)}
      />
      <textarea
        className="min-h-[160px] w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Paste email, article, or announcement text here..."
        value={rawText}
        onChange={(e) => setRawText(e.target.value)}
      />
      <input
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Goal, e.g. Create customer and LinkedIn drafts"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      />
      <div className="flex items-center gap-2">
        <input
          className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Optional URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button
          className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50"
          onClick={submit}
          disabled={loading}
        >
          Analyze Source
        </button>
      </div>
    </SectionCard>
  );
}
