import { DraftCard } from "./DraftCard";

type DraftOutput = {
  draft_set_id: string;
  audience: string;
  tone: string;
  prompt_preset?: string;
  drafts: { draft_id: string; length: string; text: string }[];
};

type Props = {
  draftOutputs: DraftOutput[];
  selectedDraftId?: string;
  sessionId?: string;
  onSelect: (sessionId: string, draftId: string) => Promise<any>;
  loading?: boolean;
};

export function DraftTabs({ draftOutputs, selectedDraftId, sessionId, onSelect, loading = false }: Props) {
  if (!draftOutputs.length) {
    return (
      <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Draft Studio</h2>
        <div className="rounded-lg border border-dashed border-slate-300 p-4 text-sm text-slate-500">
          Generate drafts to compare variants here.
        </div>
      </section>
    );
  }

  return (
    <div className="space-y-4">
      {draftOutputs.map((set) => (
        <section key={set.draft_set_id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="mb-3 text-xs text-slate-500">
            {set.audience} • {set.tone} • {set.prompt_preset || "balanced"}
          </div>
          <div className="space-y-4">
            {set.drafts.map((draft) => (
              <DraftCard
                key={draft.draft_id}
                draft={draft}
                selected={draft.draft_id === selectedDraftId}
                onSelect={() => sessionId && onSelect(sessionId, draft.draft_id)}
                disabled={loading || !sessionId}
              />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
