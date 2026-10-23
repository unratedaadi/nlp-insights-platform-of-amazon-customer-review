"""Train and persist the baseline sentiment model."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Sequence
import joblib, matplotlib.pyplot as plt, pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay
from src.sentiment import train_and_evaluate

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=Path, default=Path("data/raw/amazon_reviews_30k.parquet"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/sentiment"))
    args = parser.parse_args(argv)
    if not args.input_path.is_file():
        parser.error(f"Sample file not found: {args.input_path}. Run download_sample first.")
    model, metrics = train_and_evaluate(pd.read_parquet(args.input_path))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output_dir / "model.joblib")
    (args.output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    ConfusionMatrixDisplay(metrics["confusion_matrix"], display_labels=["negative", "positive"]).plot()
    plt.savefig(args.output_dir / "confusion_matrix.png", bbox_inches="tight")
    plt.close()
    return 0
if __name__ == "__main__": raise SystemExit(main())
