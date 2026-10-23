"""Validation and normalization for Amazon Polarity review samples."""

from __future__ import annotations

import pandas as pd


REQUIRED_COLUMNS = {"text", "label", "label_text"}


def clean_reviews(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Return usable reviews and counts describing discarded source rows."""
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    source = frame.copy()
    source["_normalized_text"] = source["text"].map(
        lambda value: "" if pd.isna(value) else " ".join(str(value).split())
    )
    blank = source["_normalized_text"].eq("")
    usable = source.loc[~blank].copy()
    duplicates = usable.duplicated(subset="_normalized_text", keep="first")
    retained = usable.loc[~duplicates, ["_normalized_text", "label", "label_text"]].rename(
        columns={"_normalized_text": "review_text"}
    )

    quality = {
        "input_rows": len(source),
        "blank_text_rows": int(blank.sum()),
        "duplicate_text_rows": int(duplicates.sum()),
        "retained_rows": len(retained),
    }
    return retained.reset_index(drop=True), quality


def validate_labels(frame: pd.DataFrame) -> None:
    """Ensure a cleaned review frame contains the binary source labels."""
    if "label" not in frame.columns:
        raise ValueError("Missing required column: label")

    labels = set(frame["label"].dropna().unique())
    if labels != {0, 1}:
        raise ValueError("Sentiment training requires both 0 and 1 labels")
