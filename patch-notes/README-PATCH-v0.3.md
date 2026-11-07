# Sales Copilot v0.3 Patch — session + template + approval

This patch upgrades the v0.2 scaffold with:

- session history + reopen UI
- template presets
- prompt preset selector
- selected draft persistence in backend session state
- approval state machine
- editable export blocks
- eval runner scripts
- stronger guardrail annotations

## Merge targets

### Frontend
- `frontend/app/page.tsx`
- `frontend/components/layout/LeftSidebar.tsx`
- `frontend/components/sessions/SessionHistoryPanel.tsx`
- `frontend/components/templates/TemplatePresetPanel.tsx`
- `frontend/components/drafts/DraftControlPanel.tsx`
- `frontend/components/drafts/DraftTabs.tsx`
- `frontend/components/export/EditableExportPanel.tsx`
- `frontend/hooks/useSalesCopilot.ts`
- `frontend/lib/api.ts`

### Backend
- `backend/app/api/routes_sessions.py`
- `backend/app/api/routes_guardrail.py`
- `backend/app/api/routes_export.py`
- `backend/app/core/session_store.py`
- `backend/app/schemas/drafts.py`
- `backend/app/schemas/session.py`

### Evals
- `backend/evals/run_eval.py`
- `backend/evals/fixtures/*.json`

## Notes

This patch keeps your OpenAI-backed agents, but improves workflow and operator control around them.
