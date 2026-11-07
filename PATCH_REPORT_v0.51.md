# v0.51 consolidation and P0 repairs — change report

## Reviewed inputs

All mounted Sales Copilot ZIP overlays: v0 scaffold, OpenAI agent pack, v0.2, v0.3, v0.35, v0.4/v0.45, and v0.5. Original v0.1 complete UI skeleton was not supplied. Followed WORKING_STYLE guidelines (inspect, minimal changes, delete stale paths, focused tests, disclose remaining risk).

## Fixes and file changes

| Issue | Files | Resolution |
|---|---|---|
| Fragmented patch ZIPs | merged `frontend/`, `backend/`, `legacy-v0/`, `patch-notes/`, new `README.md` | Reconstructed single repo. Old v0 files retained under `legacy-v0/`. |
| Fake URL/upload text | `backend/app/core/intake_pipeline.py`, `backend/app/api/routes_intake.py`, `backend/app/schemas/intake.py` (retained), `frontend/app/page.tsx` | Source-backed paste, real `.eml`/text/PDF upload, DNS-pinned HTTPS curl retrieval; reject redirects/private hosts/unreadable sources. |
| UI no-op callbacks | `frontend/app/page.tsx`, `frontend/app/layout.tsx`, `frontend/app/style.css`, `frontend/package.json`, `frontend/tsconfig.json`, `frontend/next-env.d.ts` | Full active workflow wired: generate/select/revise/guardrail/edit/approve/export, plus reopen/filter/history, error/busy states. Older stubs are not active. |
| Approval bypass and export before approval | `backend/app/core/workflow.py`, `backend/app/api/routes_sessions.py`, `backend/app/api/routes_export.py`, `backend/app/api/routes_guardrail.py`, `backend/app/api/routes_safety.py`, `backend/app/api/routes_drafts.py`, `backend/app/api/routes_templates.py`, `backend/app/api/routes_revisions.py` | Validate selected ID; SHA-256-bind guardrail and human approval to exact selected text; require four confirmed checks; high risk blocks approval; edits/revisions/select invalidate approval; build pack is not export. |
| No claim trace | `backend/app/core/workflow.py`, `backend/app/api/routes_intake.py`, `backend/app/api/routes_sources.py`, `frontend/app/page.tsx` | Source quote spans for *exact text matches*; unresolved paraphrases flagged for manual review; original source stays visible. |
| SQLite migration failure | `backend/app/core/session_store.py` | Idempotent column addition, backfilled fields for old sessions, parameterized filter, DB path env var, persisted selection/revisions/approval. |
| Missing v0.1 files blocking boot | `backend/app/schemas/source.py`, `revisions.py`, `guardrail.py`, `backend/app/api/routes_health.py`, Python `__init__.py` | Restored necessary schemas/health routes/packaging. |
| SDK unconfigured prevents app starting | `backend/app/core/prompt_runner.py`, `backend/requirements.txt` | Lazy OpenAI SDK/client construction; live calls require SDK and `OPENAI_API_KEY`, offline routes/tests boot without them. |
| Stale evaluation fixtures | `backend/evals/fixtures/` | Removed incompatible old inputs, current offline evaluator now passes. |
| Regression coverage | `backend/tests/test_v051_regression.py` | Approval bypass, stale edit, selected draft validity, revision, URL validation, email attachment, DB migration and guarded HTML extraction. |
| Documentation | `README.md`, `WORKING_STYLE.md`, `PATCH_REPORT_v0.51.md` | Setup, limitations, changed files, verification. |

## Verification (current environment)

- `python -m compileall -q app`: **PASS**
- `PYTHONPATH=. python -m pytest -q tests/test_v051_regression.py`: **6 passed**
- `PYTHONPATH=. python evals/run_eval.py`: **3 fixture checks returned valid results**
- FastAPI import and route registration: **25 routes registered**
- Real supplied SINTRONES `.eml` parsing: **PASS** through upload endpoint, using mocked agents
- Next.js build/typecheck: **NOT VERIFIED**; React/Next/TypeScript type dependencies are not installed locally. Run `npm install && npm run typecheck && npm run build`.
- Live OpenAI API: **NOT VERIFIED**; no SDK or key installed for live calls.
- Live public URL retrieval: mocked DNS-pinned path test **PASS**, real external site test **not performed**.

## Remaining limitations

1. Human review still required; source exact-match is traceability aid, not certification of factual accuracy.
2. Single-user app lacks authentication, authorization and recipient-level controls. Do not expose backend publicly.
3. Gmail/CRM/LINE/LinkedIn delivery is not connected. Export/copy only; no automatic send.
4. Article HTML extraction does not work on every JavaScript-heavy or paywalled page; non-public addresses and redirects are blocked intentionally.
5. Frontend production build and live LLM integration remain release gates.
