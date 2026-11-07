"use client";

import { useEffect, useState } from "react";
import { SectionCard } from "../shared/SectionCard";

const PROMPT_PRESETS = ["balanced", "guarded", "direct", "social"];

type Props = {
  sessionId?: string;
  onGenerate: (payload: {
    session_id: string;
    audience: string;
    tone: string;
    lengths: string[];
    prompt_preset: string;
  }) => Promise<any>;
  loading?: boolean;
  template?: any | null;
};

export function DraftControlPanel({
  sessionId,
  onGenerate,
  loading = false,
  template = null,
}: Props) {
  const [audience, setAudience] = useState("customer");
  const [tone, setTone] = useState("technical_commercial");
  const [lengths, setLengths] = useState<string[]>(["short", "medium"]);
  const [promptPreset, setPromptPreset] = useState("balanced");
  const [localError, setLocalError] = useState("");

  useEffect(() => {
    if (!template) return;
    setAudience(template.audience || "customer");
    setTone(template.tone || "technical_commercial");
    setLengths(template.lengths || ["short", "medium"]);
    setPromptPreset(template.prompt_preset || "balanced");
  }, [template]);

  const toggle = (value: string) => {
    if (lengths.includes(value)) setLengths(lengths.filter((v) => v !== value));
    else setLengths([...lengths, value]);
  };

  const submit = async () => {
    if (!sessionId) return setLocalError("Analyze a source first.");
    if (!lengths.length) return setLocalError("Choose at least one draft length.");
    setLocalError("");
    await onGenerate({ session_id: sessionId, audience, tone, lengths, prompt_preset: promptPreset });
  };

  return (
    <SectionCard title="Draft Controls">
      {localError ? (
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          {localError}
        </div>
      ) : null}
      <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" value={audience} onChange={(e) => setAudience(e.target.value)}>
        <option>customer</option>
        <option>internal</option>
        <option>prospect</option>
        <option>partner</option>
        <option>linkedin_dm</option>
        <option>linkedin_post</option>
        <option>crm_note</option>
      </select>
      <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" value={tone} onChange={(e) => setTone(e.target.value)}>
        <option>technical_commercial</option>
        <option>professional_neutral</option>
        <option>warm_consultative</option>
        <option>executive_brief</option>
        <option>social_light</option>
      </select>
      <div className="flex flex-wrap gap-2">
        {["short", "medium", "long"].map((item) => (
          <label key={item} className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm">
            <input type="checkbox" checked={lengths.includes(item)} onChange={() => toggle(item)} />
            {item}
          </label>
        ))}
      </div>
      <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" value={promptPreset} onChange={(e) => setPromptPreset(e.target.value)}>
        {PROMPT_PRESETS.map((item) => <option key={item} value={item}>{item}</option>)}
      </select>
      <button
        className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50"
        disabled={loading}
        onClick={submit}
      >
        Generate Drafts
      </button>
    </SectionCard>
  );
}
