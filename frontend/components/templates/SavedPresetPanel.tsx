"use client";

import { useState } from "react";

type Props = {
  presets: any[];
  currentConfig: any;
  onUse: (preset: any) => void;
  onSave: (payload: any) => Promise<any>;
};

export function SavedPresetPanel({ presets, currentConfig, onUse, onSave }: Props) {
  const [name, setName] = useState("");

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Saved Presets</h2>
      <div className="mb-3 flex gap-2">
        <input
          className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
          placeholder="Preset name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm"
          onClick={() => name.trim() && onSave({ name, ...currentConfig }).then(() => setName(""))}
        >
          Save
        </button>
      </div>
      <div className="space-y-2">
        {presets.length ? presets.map((preset) => (
          <button
            key={preset.key}
            onClick={() => onUse(preset)}
            className="block w-full rounded-lg border border-slate-200 p-3 text-left text-sm hover:bg-slate-50"
          >
            <div className="font-medium text-slate-900">{preset.label}</div>
            <div className="text-xs text-slate-500">
              {preset.audience} • {preset.tone} • {preset.prompt_preset}
            </div>
          </button>
        )) : (
          <div className="rounded-lg border border-dashed border-slate-300 p-3 text-sm text-slate-500">
            No presets saved yet.
          </div>
        )}
      </div>
    </section>
  );
}
