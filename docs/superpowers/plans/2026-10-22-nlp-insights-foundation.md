# NLP Insights Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible local pipeline that samples Amazon reviews, evaluates a baseline sentiment model, and discovers positive and negative themes.

**Architecture:** Focused Python modules own data validation, model evaluation, and topic discovery. CLI entry points compose those modules and persist inspectable outputs under `data/`, `artifacts/`, and `reports/` without modifying the raw review text.

**Tech Stack:** Python 3.11+, Hugging Face Datasets, pandas, scikit-learn, joblib, matplotlib, pytest.

**Spec:** `docs/superpowers/specs/2026-10-22-nlp-insights-foundation-design.md`

## Global Constraints

- Retain original review text and source labels; store derivations separately.
- Stream exactly 30,000 source records by default and make key limits CLI-configurable.
- Do not invent model metrics, topic names, or analysis results.
- Keep raw and generated data out of Git.
- The smoke test must use local fixtures and make no network request.

## Review Focus

- Duplicate texts differing only in surrounding whitespace should produce one retained review.
- A dataset without both sentiment labels should stop before model training.
- Empty or whitespace-only review text should be excluded with an explicit data-quality count.
- A requested topic count larger than available documents should return a clear error.
- A missing sample file should cause a helpful prerequisite error, not a traceback.

---

## File Structure

- `src/data.py` — validates and normalizes sampled review records and builds the data-quality report.
- `src/sentiment.py` — trains and evaluates the TF-IDF/Logistic Regression baseline.
- `src/topics.py` — derives NMF topics and representative reviews per sentiment.
- `src/download_sample.py`, `src/train_sentiment.py`, `src/discover_topics.py` — stage CLIs.
- `src/run_pipeline.py` — runs stages in order.
- `tests/` — local, network-free module and CLI tests.
- `requirements.txt`, `.gitignore`, `README.md` — setup, Git hygiene, and usage.

### Task 1: Project scaffold and sampled-data validation

**Files:**
- Create: `requirements.txt`, `.gitignore`, `src/__init__.py`, `src/data.py`, `src/download_sample.py`, `tests/test_data.py`

**Interfaces:**
- Produces: `clean_reviews(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]` and `validate_labels(frame: pd.DataFrame) -> None`.
- Produces: `download_sample.main(argv: Sequence[str] | None = None) -> int`.

- [ ] **Step 1: Write failing data-validation tests**

Test that missing columns fail, blank text is counted and excluded, and whitespace-equivalent duplicate texts retain the first record.

- [ ] **Step 2: Run the focused tests**

Run: `pytest tests/test_data.py -v`
Expected: FAIL because `src.data` does not exist.

- [ ] **Step 3: Implement data validation and the streaming sampler**

Implement `clean_reviews` and `validate_labels` in `src/data.py`. Implement a CLI that loads `mteb/amazon_polarity` with streaming enabled, takes `--sample-size` records (default `30000`), and writes Parquet plus a JSON quality report.

- [ ] **Step 4: Run focused tests and a local CLI fixture test**

Run: `pytest tests/test_data.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add reproducible review sampler`

### Task 2: Sentiment baseline and evaluation artifacts

**Files:**
- Create: `src/sentiment.py`, `src/train_sentiment.py`, `tests/test_sentiment.py`

**Interfaces:**
- Consumes: cleaned sample Parquet from Task 1 with `review_text` and `label` columns.
- Produces: `train_and_evaluate(frame: pd.DataFrame, test_size: float = 0.2) -> tuple[Pipeline, dict[str, object]]`.

- [ ] **Step 1: Write failing sentiment tests**

Test that training on both labels returns accuracy, precision, recall, F1, and a 2×2 confusion matrix; test that one-label input raises `ValueError`.

- [ ] **Step 2: Run the focused tests**

Run: `pytest tests/test_sentiment.py -v`
Expected: FAIL because `src.sentiment` does not exist.

- [ ] **Step 3: Implement `train_and_evaluate` and its CLI**

Use `TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2)` and `LogisticRegression(max_iter=1000, random_state=42)`. The CLI writes a joblib pipeline, JSON metrics, and a PNG confusion matrix beneath `artifacts/sentiment/`.

- [ ] **Step 4: Run focused tests**

Run: `pytest tests/test_sentiment.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add evaluated sentiment baseline`

### Task 3: Sentiment-separated NMF topic discovery

**Files:**
- Create: `src/topics.py`, `src/discover_topics.py`, `tests/test_topics.py`

**Interfaces:**
- Consumes: cleaned sample frame from Task 1.
- Produces: `discover_topics(frame: pd.DataFrame, label: int, topic_count: int = 5, top_terms: int = 10) -> list[dict[str, object]]`.

- [ ] **Step 1: Write failing topic tests**

Test that valid local reviews return topic terms and representative review text, and that a topic count larger than the available rows fails clearly.

- [ ] **Step 2: Run the focused tests**

Run: `pytest tests/test_topics.py -v`
Expected: FAIL because `src.topics` does not exist.

- [ ] **Step 3: Implement topic discovery and its CLI**

Fit TF-IDF and NMF separately for labels `0` and `1`; report each topic’s ranked terms, document count, and the three highest-weight representative reviews. Write JSON to `reports/topics.json`.

- [ ] **Step 4: Run focused tests**

Run: `pytest tests/test_topics.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add sentiment-separated topic discovery`

### Task 4: Pipeline orchestration and reproducibility guide

**Files:**
- Create: `src/run_pipeline.py`, `tests/test_run_pipeline.py`, `README.md`

**Interfaces:**
- Consumes: the three stage CLIs from Tasks 1–3.
- Produces: `run_pipeline.main(argv: Sequence[str] | None = None) -> int`.

- [ ] **Step 1: Write failing orchestration tests**

Test that absent sampled data raises an actionable prerequisite error and that a patched local stage sequence runs sampler, sentiment, then topics.

- [ ] **Step 2: Run the focused tests**

Run: `pytest tests/test_run_pipeline.py -v`
Expected: FAIL because `src.run_pipeline` does not exist.

- [ ] **Step 3: Implement the orchestrator and README**

Run stages in dependency order and stop on the first non-zero exit. Document environment setup, individual commands, output locations, limitations of binary labels and NMF, and the dataset’s source/license check.

- [ ] **Step 4: Run the complete local suite**

Run: `pytest -v`
Expected: PASS without downloading data.

- [ ] **Step 5: Commit**

Commit message: `docs: add reproducible pipeline guide`
