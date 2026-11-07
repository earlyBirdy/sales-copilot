# Sales Copilot v0.5 Patch — intake, persistence, export, safety

This patch upgrades the repo toward a more durable internal product.

## Scope covered

### 1. Inbox/article intake
- paste
- upload-ready UI slot
- URL fetch
- optional Gmail ingestion placeholder

### 2. Template-driven drafting
- customer update
- warm prospect
- partner note
- LinkedIn post
- internal summary

### 3. Approval workflow
- draft selected
- revised
- guardrail checked
- approved
- exported

### 4. Better persistence
- session reopen
- filter by company / source type / status / date
- saved prompt/template versions

### 5. Export maturity
- copy-ready blocks
- markdown bundle
- CRM note
- email-ready block

### 6. Safety/quality
- highlight unsupported wording
- show risk level clearly
- keep source traceability visible

## Main merge targets

### Frontend
- `frontend/app/page.tsx`
- `frontend/lib/api.ts`
- `frontend/hooks/useSalesCopilot.ts`
- `frontend/components/intake/UnifiedIntakePanel.tsx`
- `frontend/components/sessions/SessionFilterPanel.tsx`
- `frontend/components/templates/TemplateDrivenDraftPanel.tsx`
- `frontend/components/export/ExportMaturityPanel.tsx`
- `frontend/components/source/TraceabilityPanel.tsx`
- `frontend/components/safety/SafetyReviewPanel.tsx`

### Backend
- `backend/app/main.py`
- `backend/app/api/routes_intake.py`
- `backend/app/api/routes_templates.py`
- `backend/app/api/routes_sessions.py`
- `backend/app/api/routes_export.py`
- `backend/app/api/routes_safety.py`
- `backend/app/core/session_store.py`
- `backend/app/core/preset_store.py`
- `backend/app/core/intake_pipeline.py`
- `backend/app/core/export_builder.py`
- `backend/app/schemas/intake.py`
- `backend/app/schemas/templates.py`
- `backend/app/schemas/export.py`
- `backend/app/schemas/safety.py`

## Notes
- Gmail ingestion is represented as a placeholder endpoint and UI hook, not a live Gmail connector.
- Upload support is UI + request schema ready; actual file extraction should be added in a later connector/parser patch.
- This patch assumes the OpenAI-backed agent runtime remains the draft/revision/guardrail engine.
