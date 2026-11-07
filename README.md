# Sales Copilot v0.51 — consolidated and repaired

Human-in-the-loop sales drafting from *actual* email text, document uploads, or public HTTPS article text. The app prepares edits/approvals and **does not send messages**.

## Setup

Backend (Python 3.11+, with access to an OpenAI API key):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY='REPLACE_WITH_YOUR_REAL_API_KEY'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend (Node 20+):

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

Open http://localhost:3000. SQLite database defaults to `backend/sales_copilot.db`; override with `SALES_COPILOT_DB_PATH`. Back up an existing DB before first launch; schema migration adds missing session columns without deleting rows. Use only for single-user local deployment until authentication and multi-user isolation are implemented.

## Local startup & troubleshooting (macOS / Safari)

The app has **two separate local servers**: FastAPI at `http://127.0.0.1:8000` (API only) and Next.js at `http://localhost:3000` (sales workspace). Keep each process running in its own terminal.

### 1. Backend — terminal A

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# Supply a REAL API key, not the literal text 'your-key'. Do not commit secrets.
export OPENAI_API_KEY='REPLACE_WITH_YOUR_REAL_API_KEY'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Check in Safari:

- **API docs:** http://127.0.0.1:8000/docs
- **Health:** http://127.0.0.1:8000/health (expected `{"status":"ok"}`)
- **API root:** http://127.0.0.1:8000/ returns `{"detail":"Not Found"}` (HTTP 404) **by design**: no `/` route is defined. This does **not** mean that startup failed.
- `/favicon.ico` may also return 404; that is harmless.

A successful Uvicorn start prints `Application startup complete.` A successful `GET /` still returns 404; use `/docs` and `/health` to verify the API instead.

### 2. Frontend — terminal B

From the repository root in a **new** terminal:

```bash
cd frontend
npm install
```

Create `frontend/.env.local` with:

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

Then run:

```bash
npm run dev
```

Open **http://localhost:3000** to use Sales Copilot. Do not expect the frontend at port 8000. You can alternatively set the API URL for one command:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

### 3. Browser connectivity / CORS

`backend/app/main.py` already configures `CORSMiddleware`; no CORS code patch is required for the standard `http://localhost:3000` frontend origin. To also allow `http://127.0.0.1:3000` (a **different** browser origin), restart the backend with:

```bash
export SALES_COPILOT_CORS_ORIGINS='http://localhost:3000,http://127.0.0.1:3000'
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

If browser API requests fail, confirm the backend is running and the frontend's `NEXT_PUBLIC_API_BASE_URL` points to `http://127.0.0.1:8000`. Check Safari's Network/Console panels and the backend request logs. The API key is **only** for the backend and must never be stored in `frontend/.env.local` or frontend source.

### 4. Smoke test

1. Open `/health` and `/docs` on port 8000.
2. Open `http://localhost:3000` on port 3000.
3. Paste a real promotional email (or use a supported upload), analyze it, and generate customer/partner drafts.
4. Select a draft, revise or edit it, run the guardrail, confirm the approval checklist, and explicitly approve.
5. Export approved text. Confirm that **no message is automatically sent**.

`OPENAI_API_KEY` must contain a valid key for live analysis and generation. A literal placeholder will cause authentication errors once an agent calls the API.

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
