# Portfolio Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a GitHub-ready NLP portfolio repository and static Vercel dashboard backed by generated analysis summaries.

**Architecture:** Python owns topic discovery and the public summary contract. A standalone Vite/React dashboard reads that static summary without exposing raw data, while GitHub Actions validates Python tests and the production frontend build.

**Tech Stack:** Python, scikit-learn NMF, React, Vite, Recharts, GitHub Actions, Vercel static hosting.

**Spec:** `docs/superpowers/specs/2026-10-22-portfolio-dashboard-design.md`

## Global Constraints

- Never commit raw review data, trained models, virtual environments, or credentials.
- The public summary has aggregate results and at most three short excerpts per topic.
- The static dashboard has no API routes, secrets, uploads, or live model execution.
- Cite the source dataset and clearly disclose binary-label and topic-model limitations.

## Review Focus

- Missing local analysis artifacts must produce an actionable summary-generation error.
- A public summary must never include source labels outside its aggregate contract or the full dataset.
- Dashboard loading failure must show an understandable empty/error state.
- The production dashboard build must work from the tracked example summary alone.
- CI must run without downloading the dataset.

---

## File Structure

- `src/topics.py`, `src/discover_topics.py` — NMF topics and JSON report.
- `src/public_summary.py`, `src/export_summary.py` — safe public dashboard data contract.
- `dashboard/` — Vite React application and tracked example summary.
- `.github/workflows/verify.yml` — Python and frontend validation.
- `README.md`, `LICENSE`, `vercel.json` — repository and deployment readiness.

### Task 1: Topic discovery

**Files:** Create `src/topics.py`, `src/discover_topics.py`, `tests/test_topics.py`.

**Interfaces:** Produces `discover_topics(frame: pd.DataFrame, label: int, topic_count: int = 5, top_terms: int = 10) -> list[dict[str, object]]` and `reports/topics.json`.

- [ ] Write local-fixture tests for returned topic terms/excerpts and topic counts larger than the available documents.
- [ ] Run `python -m pytest tests/test_topics.py -v`; expect missing-module failure.
- [ ] Implement sentiment-separated TF-IDF/NMF topics, with three representative excerpts per topic and clear invalid-count errors.
- [ ] Run `python -m pytest tests/test_topics.py -v`; expect pass.
- [ ] Commit `feat: add topic discovery`.

### Task 2: Public summary export

**Files:** Create `src/public_summary.py`, `src/export_summary.py`, `tests/test_public_summary.py`.

**Interfaces:** Consumes data quality, metrics, and topic reports; produces `build_public_summary(...) -> dict[str, object]` and `dashboard/public/analysis-summary.json`.

- [ ] Write fixture tests that reject missing reports and assert no raw-review collection appears in the export.
- [ ] Run `python -m pytest tests/test_public_summary.py -v`; expect missing-module failure.
- [ ] Implement the versioned aggregate schema and safe excerpts, with actionable missing-artifact errors.
- [ ] Run `python -m pytest tests/test_public_summary.py -v`; expect pass.
- [ ] Commit `feat: export public analysis summary`.

### Task 3: Static dashboard

**Files:** Create `dashboard/package.json`, `dashboard/src/*`, `dashboard/public/analysis-summary.json`, `dashboard/README.md`.

**Interfaces:** Consumes the public-summary JSON schema from Task 2; produces a static Vite build.

- [ ] Write frontend tests for metrics, topic rendering, and summary-load error state.
- [ ] Run the frontend test command; expect a missing-app failure.
- [ ] Implement responsive Overview, Sentiment, Topics, and Methodology views with charts and source/limitation copy.
- [ ] Run frontend tests and `npm run build`; expect pass.
- [ ] Commit `feat: add static portfolio dashboard`.

### Task 4: Repository and deployment readiness

**Files:** Create `.github/workflows/verify.yml`, `README.md`, `LICENSE`, `vercel.json`; update `setup.md`, `requirement.md`.

**Interfaces:** Consumes all project commands and dashboard build; produces documented GitHub and Vercel setup.

- [ ] Write a CI configuration test or local validation script that verifies tracked commands and dashboard build path.
- [ ] Run its focused check; expect failure until configuration exists.
- [ ] Add CI, a concise README with setup and deployment instructions, an MIT license, and Vercel static-build configuration rooted at `dashboard/`.
- [ ] Run Python tests and `npm run build` in `dashboard/`; expect pass with no network dataset download.
- [ ] Commit `docs: prepare GitHub and Vercel deployment`.
