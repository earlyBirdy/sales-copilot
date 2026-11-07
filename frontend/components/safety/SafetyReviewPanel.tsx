type Props = {
  session?: any;
  onReview: (payload: any) => Promise<any>;
};

export function SafetyReviewPanel({ session, onReview }: Props) {
  const selectedDraftId = session?.selected_draft_id;
  const riskLevel = session?.safety_review?.risk_level || session?.review_notes?.length ? "reviewed" : "not reviewed";
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-700">Safety Review</h2>
      <div className="mb-3 rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700">
        Risk: {session?.safety_review?.risk_level || "unknown"}
      </div>
      <button
        className="rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:opacity-50"
        disabled={!session?.session_id || !selectedDraftId}
        onClick={() => session?.session_id && selectedDraftId && onReview({ session_id: session.session_id, draft_id: selectedDraftId })}
      >
        Run Safety Review
      </button>
      {(session?.safety_review?.highlights || []).length ? (
        <div className="mt-3 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800">
          <div className="font-medium">Unsupported wording highlights</div>
          <ul className="mt-2 list-disc pl-5">
            {session.safety_review.highlights.map((item: any, idx: number) => <li key={idx}>{item.term}: {item.note}</li>)}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
