# Sales Copilot v0.2 Patch

This patch upgrades the prior UI + Agent skeleton with:

- frontend wiring to real backend APIs
- backend `routes_export.py`
- SQLite-backed session persistence
- frontend loading and error states
- evaluation fixtures for agent outputs

## What to merge

### Frontend
- `frontend/app/page.tsx`
- `frontend/lib/api.ts`
- `frontend/hooks/useSalesCopilot.ts`
- `frontend/components/shared/LoadingState.tsx`
- `frontend/components/shared/ErrorState.tsx`
- `frontend/components/intake/SourceInputPanel.tsx`
- `frontend/components/drafts/DraftControlPanel.tsx`
- `frontend/components/drafts/DraftTabs.tsx`
- `frontend/components/chat/RevisionChatPanel.tsx`
- `frontend/components/export/ExportPanel.tsx`

### Backend
- `backend/app/main.py`
- `backend/app/api/routes_export.py`
- `backend/app/core/session_store.py`

### Evaluation
- `backend/evals/*.json`

## Environment

Frontend:
- `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`

Backend:
- `OPENAI_API_KEY=...`
- `SALES_COPILOT_MODEL_FAST=gpt-5-mini`
- `SALES_COPILOT_MODEL_REASONING=gpt-5`
- `SALES_COPILOT_ENABLE_WEB_SEARCH=true`

## Notes

- The frontend now calls the backend instead of using hardcoded mock state.
- SQLite is used for session persistence with a JSON payload column.
- Export route builds a `final_pack` from selected or requested drafts.
- Evaluation fixtures give you repeatable source/expected-shape samples for regression checks.
