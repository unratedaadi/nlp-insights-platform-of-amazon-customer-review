"""Stream and retain a reproducible Amazon Polarity sample."""

from __future__ import annotations

import argparse
import json
from itertools import islice
from pathlib import Path
from typing import Sequence

import pandas as pd
from datasets import load_dataset

from src.data import clean_reviews, validate_labels


DATASET_NAME = "mteb/amazon_polarity"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a cleaned Amazon review sample.")
    parser.add_argument("--sample-size", type=int, default=30_000)
    parser.add_argument("--output-path", type=Path, default=Path("data/raw/amazon_reviews_30k.parquet"))
    parser.add_argument("--report-path", type=Path, default=Path("reports/data_quality.json"))
    args = parser.parse_args(argv)
    if args.sample_size <= 0:
        parser.error("--sample-size must be greater than zero")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    source = load_dataset(DATASET_NAME, split="train", streaming=True)
    sampled = pd.DataFrame(list(islice(source, args.sample_size)))
    cleaned, quality = clean_reviews(sampled)
    validate_labels(cleaned)

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    args.report_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_parquet(args.output_path, index=False)

    report = {**quality, "dataset": DATASET_NAME, "sample_size": args.sample_size}
    args.report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
