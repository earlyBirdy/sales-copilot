# Sales Copilot v0.35 Patch — UX/state + quality/safety

This patch combines:
- v0.3 UX/state polish
- v0.35 quality/safety improvements

## UX/state focus
- session history UI
- reopen session
- selected draft persistence
- revision history viewer
- editable final text blocks
- status chips
- validation
- loading polish

## quality/safety focus
- eval runner scripts
- schema validation at every agent step
- prompt version tagging
- backend logs
- request tracing
- stronger export payload validation

## Merge targets

### Frontend
- `frontend/app/page.tsx`
- `frontend/lib/api.ts`
- `frontend/hooks/useSalesCopilot.ts`
- `frontend/components/sessions/SessionHistoryPanel.tsx`
- `frontend/components/export/EditableExportPanel.tsx`
- `frontend/components/chat/RevisionHistoryList.tsx`
- `frontend/components/shared/StatusChip.tsx`
- `frontend/components/shared/LoadingState.tsx`
- `frontend/components/shared/ErrorState.tsx`
- `frontend/components/intake/SourceInputPanel.tsx`
- `frontend/components/drafts/DraftControlPanel.tsx`

### Backend
- `backend/app/main.py`
- `backend/app/api/routes_export.py`
- `backend/app/api/routes_sources.py`
- `backend/app/api/routes_drafts.py`
- `backend/app/api/routes_revisions.py`
- `backend/app/api/routes_guardrail.py`
- `backend/app/api/routes_sessions.py`
- `backend/app/core/session_store.py`
- `backend/app/core/logger.py`
- `backend/app/core/request_context.py`
- `backend/app/core/validators.py`
- `backend/app/schemas/*.py`
- `backend/app/prompts/VERSIONS.json`

### Evals
- `backend/evals/run_eval.py`
- `backend/evals/fixtures/*.json`

## Notes
This patch is designed to sit on top of the OpenAI-backed agent runtime and the v0.3 session/template/approval patch.
