"use client";

import { useState } from "react";
import { SectionCard } from "../shared/SectionCard";
import { ActiveDraftBadge } from "./ActiveDraftBadge";
import { ChatMessageList } from "./ChatMessageList";
import { ChatComposer } from "./ChatComposer";
import { RevisionHistoryList } from "./RevisionHistoryList";

type Props = {
  sessionId?: string;
  selectedDraft?: { draft_id: string; text: string; length: string } | null;
  revisionHistory: any[];
  reviewNotes: string[];
  onRevise: (payload: { session_id: string; draft_id: string; instruction: string }) => Promise<any>;
  onGuardrail: (payload: { session_id: string; draft_id: string }) => Promise<any>;
  loadingRevise?: boolean;
  loadingGuardrail?: boolean;
};

export function RevisionChatPanel({
  sessionId,
  selectedDraft,
  revisionHistory,
  reviewNotes,
  onRevise,
  onGuardrail,
  loadingRevise = false,
  loadingGuardrail = false,
}: Props) {
  const [instruction, setInstruction] = useState("");

  return (
    <SectionCard title="Revision Chat">
      <ActiveDraftBadge label={selectedDraft ? `Active draft: ${selectedDraft.length}` : "No draft selected"} />
      <ChatMessageList />
      <ChatComposer
        value={instruction}
        onChange={setInstruction}
        onSend={() =>
          sessionId &&
          selectedDraft &&
          instruction.trim() &&
          onRevise({
            session_id: sessionId,
            draft_id: selectedDraft.draft_id,
            instruction,
          }).then(() => setInstruction(""))
        }
        disabled={!sessionId || !selectedDraft || loadingRevise}
      />
      <button
        className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50"
        onClick={() => sessionId && selectedDraft && onGuardrail({ session_id: sessionId, draft_id: selectedDraft.draft_id })}
        disabled={!sessionId || !selectedDraft || loadingGuardrail}
      >
        Run Guardrail Review
      </button>
      <RevisionHistoryList items={revisionHistory} />
      <div className="space-y-2">
        {reviewNotes.map((note, idx) => (
          <div key={idx} className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
            {note}
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
