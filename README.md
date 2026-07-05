# Financial Statement Dashboard

Extracts key financial data out of statement PDFs (starting with T. Rowe Price
Portfolio Summary statements) and turns it into a dashboard: portfolio value,
asset allocation, investment style breakdown, activity summary, retirement
income estimates, and beneficiary designations.

## Architecture

- **`backend/`** — Python/FastAPI service.
  - `app/parsers/` — pluggable statement parsers. Each parser implements
    `can_parse(pages)` / `parse(pages)` and registers itself; `find_parser`
    picks the first one that recognizes a document. `trowe_price.py` is the
    first parser; add new institutions/formats by adding another module here.
  - `app/parsers/row_parsing.py` — shared helper that pulls labeled numeric
    rows out of flattened PDF text by counting numeric columns per line,
    rather than hardcoding label strings, so it holds up across similar
    statement layouts.
  - `app/models.py` — the normalized `Statement` schema every parser maps
    into (asset allocation, investment style, activity summary, beneficiaries,
    retirement income estimate).
  - `app/storage.py` — persists each extracted `Statement` as a JSON file
    under `backend/data/extracted/` (no database).
  - `app/api/routes.py` — upload / list / get / delete statements, plus
    `/dashboard/portfolio-history` and `/dashboard/latest` for the frontend.
- **`frontend/`** — Vite + React + TypeScript dashboard that uploads a PDF to
  the API and renders the extracted data (stat tiles, an asset-allocation
  stacked bar + table, a portfolio-value trend line once 2+ statements exist,
  and tables for investment style / activity / retirement estimates /
  beneficiaries).

## Running locally

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run tests:

```bash
pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The Vite dev server proxies `/api/*` to the
backend on port 8000.

## Notes

- Extracted data is written to `backend/data/extracted/*.json`, which is
  git-ignored since it holds real personal financial data once you upload
  real statements.
- The T. Rowe Price parser reads flattened PDF text (via `pdfplumber`) and
  matches table rows by their numeric-column count (5 columns = asset
  allocation, 6 = fund activity, 7/8 = investment style). This keeps it
  reasonably resilient to label wording changes, but statements with
  multi-line rows or very different table shapes would need a parser of
  their own.
- Tests use a fabricated, sanitized page-text fixture
  (`backend/tests/fixtures/trowe_price_sample_pages.py`) that mirrors the
  real layout with fake names/numbers — no real statement data lives in this
  repo.
