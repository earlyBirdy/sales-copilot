type Props = {
  templates: any[];
  onSelect: (template: any) => void;
};

export function TemplateLibraryPanel({ templates, onSelect }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Template Library</h2>
      <div className="space-y-2">
        {templates.length ? templates.map((template) => (
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
        )) : (
          <div className="rounded-lg border border-dashed border-slate-300 p-3 text-sm text-slate-500">
            No templates loaded.
          </div>
        )}
      </div>
    </section>
  );
}
