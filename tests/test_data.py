import pandas as pd
import pytest

from src.data import clean_reviews, validate_labels
from src import download_sample


def test_clean_reviews_excludes_blank_text_and_collapses_whitespace_duplicates():
    frame = pd.DataFrame(
        {
            "text": ["  Great product  ", "Great product", "   ", None, "Slow delivery"],
            "label": [1, 1, 0, 0, 0],
            "label_text": ["positive", "positive", "negative", "negative", "negative"],
        }
    )

    cleaned, quality = clean_reviews(frame)

    assert cleaned["review_text"].tolist() == ["Great product", "Slow delivery"]
    assert cleaned["label"].tolist() == [1, 0]
    assert quality == {
        "input_rows": 5,
        "blank_text_rows": 2,
        "duplicate_text_rows": 1,
        "retained_rows": 2,
    }


def test_clean_reviews_rejects_missing_required_columns():
    frame = pd.DataFrame({"text": ["Great product"], "label": [1]})

    with pytest.raises(ValueError, match="label_text"):
        clean_reviews(frame)


def test_validate_labels_requires_both_binary_classes():
    frame = pd.DataFrame(
        {
            "review_text": ["Great product", "Also great"],
            "label": [1, 1],
            "label_text": ["positive", "positive"],
        }
    )

    with pytest.raises(ValueError, match="both 0 and 1"):
        validate_labels(frame)


def test_sampler_writes_cleaned_parquet_and_quality_report(tmp_path, monkeypatch):
    rows = [
        {"text": "Excellent quality", "label": 1, "label_text": "positive"},
        {"text": "  Excellent quality ", "label": 1, "label_text": "positive"},
        {"text": "Arrived late", "label": 0, "label_text": "negative"},
        {"text": "", "label": 0, "label_text": "negative"},
    ]
    output_path = tmp_path / "reviews.parquet"
    report_path = tmp_path / "quality.json"

    monkeypatch.setattr(download_sample, "load_dataset", lambda *_, **__: rows)

    exit_code = download_sample.main(
        [
            "--sample-size",
            "4",
            "--output-path",
            str(output_path),
            "--report-path",
            str(report_path),
        ]
    )

    saved = pd.read_parquet(output_path)
    assert exit_code == 0
    assert saved["review_text"].tolist() == ["Excellent quality", "Arrived late"]
    assert report_path.read_text(encoding="utf-8") == (
        '{\n'
        '  "blank_text_rows": 1,\n'
        '  "dataset": "mteb/amazon_polarity",\n'
        '  "duplicate_text_rows": 1,\n'
        '  "input_rows": 4,\n'
        '  "retained_rows": 2,\n'
        '  "sample_size": 4\n'
        '}\n'
    )
