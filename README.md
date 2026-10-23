# NLP Insights from Customer Reviews

A local Python project that turns Amazon product reviews into structured sentiment-analysis results.

The current implementation cleans a 30,000-review sample, trains a TF-IDF and Logistic Regression sentiment classifier, and saves model metrics plus a confusion matrix.

## What it does

- Cleans blank and duplicate review text
- Preserves the original positive or negative source label
- Trains a reproducible baseline sentiment model
- Reports accuracy, precision, recall, F1-score, and a confusion matrix
- Keeps downloaded data and model artifacts out of Git

## Dataset

This project uses Amazon Polarity, a public Amazon review dataset with binary sentiment labels. The local data files are intentionally excluded from the repository. See [about.md](about.md) for the local dataset workflow and limitations.

## Quick start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
python -m src.train_sentiment
```

Before training, make sure `data/raw/amazon_reviews_30k.parquet` exists. [setup.md](setup.md) explains how to create it from a downloaded Amazon Polarity Parquet shard.

## Output files

```text
artifacts/sentiment/model.joblib
artifacts/sentiment/metrics.json
artifacts/sentiment/confusion_matrix.png
```

## Limitations

Amazon Polarity does not include a neutral class, product categories, or review dates. This model is a baseline and its evaluation results apply to the sampled dataset split only.

## Project documents

- [about.md](about.md) — project and dataset provenance
- [setup.md](setup.md) — local setup and run steps
- [requirement.md](requirement.md) — software and data requirements

## License

This repository is available under the MIT License. Review the dataset’s own terms before redistributing review data.
