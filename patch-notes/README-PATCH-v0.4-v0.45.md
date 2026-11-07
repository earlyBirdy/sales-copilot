# Sales Copilot v0.4 + v0.45 Patch

This patch combines:

## v0.35 quality/safety hardening
- eval runner scripts
- schema validation at every agent step
- prompt version tagging
- backend logs
- request tracing
- stronger export payload validation

## v0.4 reusable workflow
- saved presets
- template library
- multi-output pack generation
- CTA selector
- approval checklist

## v0.45 ingestion/export
- article fetch pipeline
- email cleanup/parser
- better export formats
- CRM-note block
- markdown export

## Merge targets

### Frontend
- `frontend/app/page.tsx`
- `frontend/lib/api.ts`
- `frontend/hooks/useSalesCopilot.ts`
- `frontend/components/templates/TemplateLibraryPanel.tsx`
- `frontend/components/templates/SavedPresetPanel.tsx`
- `frontend/components/drafts/MultiOutputPackPanel.tsx`
- `frontend/components/export/ExportFormatPanel.tsx`
- `frontend/components/export/ApprovalChecklistPanel.tsx`
- `frontend/components/source/IngestionToolsPanel.tsx`

### Backend
- `backend/app/main.py`
- `backend/app/api/routes_templates.py`
- `backend/app/api/routes_ingestion.py`
- `backend/app/api/routes_export.py`
- `backend/app/core/preset_store.py`
- `backend/app/core/ingestion.py`
- `backend/app/core/validators.py`
- `backend/app/schemas/templates.py`
- `backend/app/schemas/ingestion.py`
- `backend/app/schemas/export.py`

### Evals
- `backend/evals/run_eval.py`
- `backend/evals/fixtures/*.json`

## Notes
This patch assumes:
- your OpenAI-backed agents are already merged
- your v0.35 logger/request-tracing pieces already exist or will be merged together
