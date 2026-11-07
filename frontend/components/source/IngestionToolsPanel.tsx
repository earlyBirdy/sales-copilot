"use client";

import { useState } from "react";

type Props = {
  onArticleFetch: (payload: { url: string; title?: string; user_goal?: string }) => Promise<any>;
  onEmailCleanup: (payload: { raw_email_text: string; title?: string; sender_company?: string; user_goal?: string }) => Promise<any>;
};

export function IngestionToolsPanel({ onArticleFetch, onEmailCleanup }: Props) {
  const [url, setUrl] = useState("");
  const [rawEmail, setRawEmail] = useState("");

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Ingestion Tools</h2>
      <div className="space-y-3">
        <div>
          <input
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            placeholder="Article URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <button
            className="mt-2 rounded-lg border border-slate-300 px-3 py-2 text-sm"
            onClick={() => url.trim() && onArticleFetch({ url })}
          >
            Fetch article
          </button>
        </div>
        <div>
          <textarea
            className="min-h-[120px] w-full rounded-lg border border-slate-300 px-3 py-2 text-sm"
            placeholder="Paste raw forwarded email / newsletter here"
            value={rawEmail}
            onChange={(e) => setRawEmail(e.target.value)}
          />
          <button
            className="mt-2 rounded-lg border border-slate-300 px-3 py-2 text-sm"
            onClick={() => rawEmail.trim() && onEmailCleanup({ raw_email_text: rawEmail })}
          >
            Clean email
          </button>
        </div>
      </div>
    </section>
  );
}
