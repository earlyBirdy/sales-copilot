"use client";

import { useState } from "react";

const TEMPLATE_OPTIONS = [
  ["customer_update", "Customer Update"],
  ["warm_prospect", "Warm Prospect"],
  ["partner_note", "Partner Note"],
  ["linkedin_post", "LinkedIn Post"],
  ["internal_summary", "Internal Summary"],
];

type Props = {
  sessionId?: string;
  templates: any[];
  presets: any[];
  ctaOptions?: string[];
  onGenerate: (payload: any) => Promise<any>;
  onSavePreset: (payload: any) => Promise<any>;
};

export function TemplateDrivenDraftPanel({
  sessionId,
  templates,
  presets,
  ctaOptions = [],
  onGenerate,
  onSavePreset,
}: Props) {
  const [templateKey, setTemplateKey] = useState("customer_update");
  const [selectedCta, setSelectedCta] = useState("");
  const [presetName, setPresetName] = useState("");

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Template-driven Drafting</h2>
      <div className="space-y-2">
        <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" value={templateKey} onChange={(e) => setTemplateKey(e.target.value)}>
          {TEMPLATE_OPTIONS.map(([key, label]) => <option key={key} value={key}>{label}</option>)}
        </select>
        <select className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm" value={selectedCta} onChange={(e) => setSelectedCta(e.target.value)}>
          <option value="">Select CTA</option>
          {ctaOptions.map((cta) => <option key={cta} value={cta}>{cta}</option>)}
        </select>
        <div className="flex gap-2">
          <input
            className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
            placeholder="Save as preset name"
            value={presetName}
            onChange={(e) => setPresetName(e.target.value)}
          />
          <button
            className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
            onClick={() => presetName.trim() && onSavePreset({ name: presetName, template_key: templateKey })}
          >
            Save
          </button>
        </div>
        <button
          className="rounded-lg bg-slate-900 px-3 py-2 text-sm text-white disabled:opacity-50"
          disabled={!sessionId}
          onClick={() => sessionId && onGenerate({ session_id: sessionId, template_key: templateKey, selected_cta: selectedCta })}
        >
          Generate From Template
        </button>
      </div>
    </section>
  );
}
