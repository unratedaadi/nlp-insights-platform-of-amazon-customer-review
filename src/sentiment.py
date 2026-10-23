"""Baseline supervised sentiment classification."""
from __future__ import annotations

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


def train_and_evaluate(frame: pd.DataFrame, test_size: float = 0.2) -> tuple[Pipeline, dict[str, object]]:
    if {"review_text", "label"} - set(frame.columns):
        raise ValueError("Input requires review_text and label columns")
    if set(frame["label"].unique()) != {0, 1}:
        raise ValueError("Sentiment training requires both 0 and 1 labels")
    x_train, x_test, y_train, y_test = train_test_split(
        frame["review_text"], frame["label"], test_size=test_size, random_state=42, stratify=frame["label"]
    )
    model = Pipeline([("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2)), ("classifier", LogisticRegression(max_iter=1000, random_state=42))])
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, predictions, average="binary", zero_division=0)
    return model, {"accuracy": float(accuracy_score(y_test, predictions)), "precision": float(precision), "recall": float(recall), "f1": float(f1), "confusion_matrix": confusion_matrix(y_test, predictions, labels=[0, 1]).tolist()}
