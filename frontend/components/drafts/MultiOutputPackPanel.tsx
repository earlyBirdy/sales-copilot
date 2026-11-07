const DEFAULT_PACKS = [
  { key: "customer_social_partner", label: "Customer + LinkedIn + Partner", outputs: ["customer", "linkedin_post", "partner"] },
  { key: "internal_customer_crm", label: "Internal + Customer + CRM", outputs: ["internal", "customer", "crm_note"] },
];

type Props = {
  sessionId?: string;
  ctaOptions?: string[];
  onGenerate: (payload: any) => Promise<any>;
};

export function MultiOutputPackPanel({ sessionId, ctaOptions = [], onGenerate }: Props) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Multi-output Packs</h2>
      <div className="mb-3 text-xs text-slate-500">CTA selector is passed into the generated pack payload.</div>
      <div className="space-y-2">
        {DEFAULT_PACKS.map((pack) => (
          <button
            key={pack.key}
            className="block w-full rounded-lg border border-slate-200 p-3 text-left text-sm hover:bg-slate-50 disabled:opacity-50"
            disabled={!sessionId}
            onClick={() =>
              sessionId &&
              onGenerate({
                session_id: sessionId,
                outputs: pack.outputs,
                tone: "professional_neutral",
                lengths: ["short", "medium"],
                prompt_preset: "balanced",
                selected_cta: ctaOptions[0] || "",
              })
            }
          >
            <div className="font-medium text-slate-900">{pack.label}</div>
            <div className="text-xs text-slate-500">{pack.outputs.join(" • ")}</div>
          </button>
        ))}
      </div>
    </section>
  );
}
