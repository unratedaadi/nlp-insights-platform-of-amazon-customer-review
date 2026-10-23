# Project Requirements

## Purpose

Analyze real Amazon customer-review text to demonstrate sentiment classification, topic discovery, data-quality reporting, and evidence-backed business insights.

## Local software

- macOS, Windows, or Linux
- Python 3.11 or newer
- Git
- A terminal and internet connection for the initial public-dataset download

## Python packages

Install the exact project dependencies with:

```bash
python -m pip install -r requirements.txt
```

The project uses Hugging Face Datasets, pandas, PyArrow, scikit-learn, joblib, matplotlib, and pytest.

## Dataset

- Source: Amazon Polarity from Hugging Face
- Starting size: 30,000 streamed training reviews
- Labels: binary positive (`1`) and negative (`0`)
- Local format: Parquet
- The raw data is intentionally excluded from Git.

## Current capabilities

- Review cleaning and duplicate removal
- Data-quality report
- TF-IDF and Logistic Regression sentiment baseline
- Accuracy, precision, recall, F1-score, and confusion matrix

## Planned deployment requirements

- GitHub repository for source code and documentation
- Static React dashboard
- Vercel account for deployment
- No API key, database, or server is required for the first public dashboard

## Limitations

- The source data has no neutral sentiment class.
- It does not provide dates or product categories for trend analysis.
- Model metrics measure this dataset split only; they do not prove universal sentiment accuracy.
