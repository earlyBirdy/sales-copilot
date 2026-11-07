"use client";

import { useState } from "react";

type Props = {
  onSubmit: (payload: any) => Promise<any>;
  onGmailPlaceholder: (payload: any) => Promise<any>;
  loading?: boolean;
};

export function UnifiedIntakePanel({ onSubmit, onGmailPlaceholder, loading = false }: Props) {
  const [mode, setMode] = useState("paste");
  const [title, setTitle] = useState("");
  const [rawText, setRawText] = useState("");
  const [url, setUrl] = useState("");
  const [senderCompany, setSenderCompany] = useState("");
  const [goal, setGoal] = useState("");
  const [uploadName, setUploadName] = useState("");
  const [localError, setLocalError] = useState("");

  const submit = async () => {
    if (mode === "paste" && !rawText.trim()) return setLocalError("Paste text is required.");
    if (mode === "url_fetch" && !url.trim()) return setLocalError("URL is required.");
    if (mode === "upload" && !uploadName.trim()) return setLocalError("Upload placeholder name is required.");
    setLocalError("");
    await onSubmit({
      intake_mode: mode,
      source_type: mode === "url_fetch" ? "article" : "email",
      title,
      raw_text: rawText,
      url,
      sender_company: senderCompany,
      user_goal: goal,
      upload_name: uploadName,
    });
  };

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Unified Intake</h2>
      {localError ? <div className="mb-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">{localError}</div> : null}

      <div className="mb-3 flex gap-2">
        {[
          ["paste", "Paste"],
          ["upload", "Upload"],
          ["url_fetch", "URL Fetch"],
          ["gmail_later", "Gmail Later"],
        ].map(([key, label]) => (
          <button
            key={key}
            className={`rounded-lg px-3 py-2 text-sm ${mode === key ? "bg-slate-900 text-white" : "border border-slate-300"}`}
            onClick={() => setMode(key)}
          >
            {label}
          </button>
        ))}
      </div>

      <input
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Sender / company"
        value={senderCompany}
        onChange={(e) => setSenderCompany(e.target.value)}
      />
      <input
        className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
        placeholder="Goal"
        value={goal}
        onChange={(e) => setGoal(e.target.value)}
      />

      {mode === "paste" ? (
        <textarea
          className="mb-3 min-h-[160px] w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Paste source text"
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
        />
      ) : null}

      {mode === "upload" ? (
        <input
          className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Upload placeholder filename"
          value={uploadName}
          onChange={(e) => setUploadName(e.target.value)}
        />
      ) : null}

      {mode === "url_fetch" ? (
        <input
          className="mb-3 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Article URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
      ) : null}

      {mode === "gmail_later" ? (
        <div className="mb-3 rounded-lg border border-blue-200 bg-blue-50 p-3 text-sm text-blue-700">
          Gmail ingestion is a later connector path. Use the placeholder button to record the intent.
        </div>
      ) : null}

      <div className="flex gap-2">
        <button
          className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50"
          onClick={submit}
          disabled={loading || mode === "gmail_later"}
        >
          Intake Source
        </button>
        {mode === "gmail_later" ? (
          <button
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
            onClick={() => onGmailPlaceholder({ title, sender_company: senderCompany, user_goal: goal })}
          >
            Save Gmail Placeholder
          </button>
        ) : null}
      </div>
    </section>
  );
}
