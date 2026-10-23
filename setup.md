# Setup Guide

## 1. Open the project folder

```bash
cd /Users/aadityjain/Desktop/nlp-insights-platform/.worktrees/codex/nlp-insights-foundation
```

## 2. Create and activate Python environment

Python 3.11 or newer is recommended.

```bash
/opt/homebrew/bin/python3.11 -m venv .venv
source .venv/bin/activate
```

## 3. Install packages

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Download the review sample

This streams 30,000 public Amazon Polarity reviews and stores them locally.

```bash
python -m src.download_sample --sample-size 30000
```

Expected files:

```text
data/raw/amazon_reviews_30k.parquet
reports/data_quality.json
```

## 5. Train and evaluate sentiment analysis

```bash
python -m src.train_sentiment
```

Expected files:

```text
artifacts/sentiment/model.joblib
artifacts/sentiment/metrics.json
artifacts/sentiment/confusion_matrix.png
```

## 6. Run tests

```bash
python -m pytest -v
```

## Common issue

The warning about unauthenticated Hugging Face requests is safe for this public dataset. An `HF_TOKEN` is optional and only increases download limits.
