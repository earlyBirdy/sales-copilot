# Sales Copilot v0.51 — consolidated and repaired

Human-in-the-loop sales drafting from *actual* email text, document uploads, or public HTTPS article text. The app prepares edits/approvals and **does not send messages**.

## Setup

Backend (Python 3.11+, with access to an OpenAI API key):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY='your-key'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend (Node 20+):

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev
```

Open http://localhost:3000. SQLite database defaults to `backend/sales_copilot.db`; override with `SALES_COPILOT_DB_PATH`. Back up an existing DB before first launch; schema migration adds missing session columns without deleting rows. Use only for single-user local deployment until authentication and multi-user isolation are implemented.

## Workflow

1. **Paste, upload (.txt, .md, .eml, text-based .pdf), or fetch public HTTPS URL.** No invented placeholder source content. URLs use a DNS-pinned HTTPS request with redirects blocked; some sites forbid direct extraction. Gmail is not connected.
2. Analyze actual source via the OpenAI-backed Intake/Extractor agents. Source claims receive exact-quote match flags; unmatched/paraphrased claims require human checking.
3. Generate audience-template drafts (customer, prospect, partner, LinkedIn, internal).
4. Select one draft. Revise if needed. Optionally prepare and edit the final block.
5. Run guardrail against **the current edited or revised text**. Explicitly confirm all four checklist fields and approve. High-risk reviews are blocked.
6. Export Markdown, email-ready text, or copy approved text. No sending endpoints are exposed.

Approval is invalidated whenever draft selection, text revision, or final block edits change the approved version. The server links guardrail and approval records to SHA-256 hashes of the selected text. The *prepare final pack* endpoint does not export or auto-approve.

## Tests

```bash
cd backend
PYTHONPATH=. python -m pytest -q tests/test_v051_regression.py
PYTHONPATH=. python evals/run_eval.py
python -m compileall -q app
```

The pytest suite mocks the LLM calls and does not require an API key; live OpenAI API behavior remains unverified. A real `.eml` file mounted in the development environment was used for the attachment test; if not available, that specific test is skipped. For launch readiness, also verify frontend typecheck/build, actual API responses, and manual UI flows with live credentials.

## Environment

`OPENAI_API_KEY` required for live agent calls. Optional: `SALES_COPILOT_MODEL_FAST`, `SALES_COPILOT_MODEL_REASONING`, `SALES_COPILOT_ENABLE_WEB_SEARCH`, `SALES_COPILOT_DB_PATH`, `SALES_COPILOT_CORS_ORIGINS` (comma-separated origins).

## Limits and risks

- Source exact-match annotations are **not** factual verification or semantic citations. The user must verify vendor claims and unsupported language before approving.
- Public-URL HTML extraction is best-effort. Redirects, private addresses, HTTP sites, scanned PDFs, huge files, and sites requiring JavaScript or authentication are rejected instead of returning synthetic content.
- Auth, customer/recipient management, CRM or Gmail sending, rate limits, and production-grade observability are not implemented.
- The original v0.1 full UI skeleton was not available; the working page was reconstructed from successive patch overlays, and older optional component stubs remain for reference.
- Live OpenAI and Next.js build verification were not performed in this environment because dependencies/credentials are unavailable.

See `PATCH_REPORT_v0.51.md` for a concise audit trail and test results.
