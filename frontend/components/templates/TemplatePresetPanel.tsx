const TEMPLATES = [
  {
    key: "customer_launch",
    label: "Customer Launch Note",
    audience: "customer",
    tone: "technical_commercial",
    lengths: ["short", "medium"],
    prompt_preset: "balanced",
  },
  {
    key: "partner_update",
    label: "Partner Update",
    audience: "partner",
    tone: "professional_neutral",
    lengths: ["short", "medium"],
    prompt_preset: "guarded",
  },
  {
    key: "linkedin_dm",
    label: "LinkedIn DM",
    audience: "linkedin_dm",
    tone: "social_light",
    lengths: ["short"],
    prompt_preset: "social",
  },
];

type Props = {
  onSelect: (template: any) => void;
};

export function TemplatePresetPanel({ onSelect }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Template Presets</h2>
      <div className="space-y-2">
        {TEMPLATES.map((template) => (
          <button
            key={template.key}
            onClick={() => onSelect(template)}
            className="block w-full rounded-lg border border-slate-200 p-3 text-left text-sm hover:bg-slate-50"
          >
            <div className="font-medium text-slate-900">{template.label}</div>
            <div className="text-xs text-slate-500">
              {template.audience} • {template.tone} • {template.prompt_preset}
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}
