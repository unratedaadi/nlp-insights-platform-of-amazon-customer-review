# NLP Insights Foundation — Design

## Purpose

Create a local, reproducible data-science foundation for a portfolio project that turns Amazon customer-review text into evidence-backed sentiment and topic insights. The first release is for the project owner to run in VS Code; it deliberately excludes a web API and dashboard until the analytical results are validated.

## Scope

The project will stream and retain a deterministic 30,000-record sample from the Amazon Polarity training split, clean it without changing original review text, train a supervised sentiment baseline, and discover unsupervised topics. Outputs will be inspectable files rather than a UI.

## Architecture and data flow

1. `src/download_sample.py` streams Amazon Polarity, takes a fixed-size sample, validates required fields, removes null and duplicate review text, and writes a Parquet dataset plus a data-quality summary.
2. `src/train_sentiment.py` reads the retained sample, splits it stratified by label, fits a TF-IDF plus Logistic Regression pipeline, and writes model metrics, a confusion-matrix image, and the fitted model.
3. `src/discover_topics.py` reads the same sample, applies TF-IDF and NMF separately to positive and negative reviews, and writes topic keywords, coverage counts, and representative review text.
4. `src/run_pipeline.py` runs these stages in order and fails clearly when a prerequisite output is absent.

Each script accepts paths and key limits as command-line arguments, so a larger sample can be used later without source changes.

## Data handling

The original `review_text`, binary label, and source label text remain in the sample. Derived columns and results live in separate outputs. Review text is not redistributed by default; raw and processed data are ignored by Git. The dataset card and source identifiers are retained in the data-quality report.

## Error handling

Scripts give actionable messages for missing dependencies, download failures, empty samples, missing required columns, insufficient label diversity, and invalid topic counts. They do not silently substitute fabricated results or accuracy claims.

## Validation

Unit tests will cover sample validation, text de-duplication, required-column errors, label mapping, metric output structure, and topic-result structure. A lightweight smoke test will run the pipeline on a small local fixture, avoiding network access.

## Deferred work

FastAPI endpoints, upload flows, a React dashboard, advanced aspect-based sentiment analysis, and deployment are intentionally deferred until the baseline metrics and topics are available.
