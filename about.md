# About this project

This project analyses Amazon product reviews with a local NLP pipeline. It prepares review text, trains a sentiment classifier, and saves evaluation results for a portfolio dashboard.

## Dataset source

The dataset is Amazon Polarity, a public Amazon review dataset with binary sentiment labels: `0` for negative and `1` for positive.

The downloaded shard was originally saved at:

```text
/Users/aadityjain/Downloads/train-00000-of-00004.parquet
```

It contains 899,999 reviews with `label`, `text`, and `label_text` columns. It was copied into this project at:

```text
data/raw/train-00000-of-00004.parquet
```

The project creates a 30,000-review working sample here:

```text
data/raw/amazon_reviews_30k.parquet
```

The raw shard and working sample are ignored by Git and remain local.

## Analysis steps

The data-cleaning step removes blank reviews, normalizes whitespace, and removes duplicate text. Its report is stored in `reports/data_quality.json`.

Run the sentiment model with:

```bash
python -m src.train_sentiment
```

It writes model metrics and a confusion matrix to `artifacts/sentiment/`.

## Current limits

The dataset has only positive and negative labels. It does not include neutral sentiment, dates, or product categories. The model is a baseline and its metrics apply to this sample split only.
