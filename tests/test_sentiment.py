import pandas as pd
import pytest

from src.sentiment import train_and_evaluate


def test_train_and_evaluate_returns_binary_metrics_and_confusion_matrix():
    frame = pd.DataFrame(
        {
            "review_text": [
                "excellent durable product", "great quality and value", "love this item", "works perfectly",
                "terrible build quality", "arrived broken", "poor value and service", "very disappointing",
                "excellent quality again", "great durable item",
            ],
            "label": [1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
        }
    )

    _, metrics = train_and_evaluate(frame, test_size=0.4)

    assert set(metrics) == {"accuracy", "precision", "recall", "f1", "confusion_matrix"}
    assert all(0.0 <= metrics[key] <= 1.0 for key in ("accuracy", "precision", "recall", "f1"))
    assert len(metrics["confusion_matrix"]) == 2
    assert all(len(row) == 2 for row in metrics["confusion_matrix"])


def test_train_and_evaluate_rejects_single_label_input():
    frame = pd.DataFrame({"review_text": ["excellent", "great"], "label": [1, 1]})

    with pytest.raises(ValueError, match="both 0 and 1"):
        train_and_evaluate(frame)
