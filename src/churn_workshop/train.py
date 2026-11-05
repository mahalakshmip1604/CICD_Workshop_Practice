"""Train a churn model and write the model + metrics to disk.

Usage:
    python -m churn_workshop.train --out models/model.joblib --metrics metrics.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from churn_workshop.data import generate_data, validate_data
from churn_workshop.features import FEATURES, TARGET, add_features, build_preprocessor


def train_model(df: pd.DataFrame, seed: int = 42) -> tuple[Pipeline, dict]:
    df = add_features(validate_data(df))
    X_train, X_test, y_train, y_test = train_test_split(
        df[FEATURES], df[TARGET], test_size=0.25, random_state=seed, stratify=df[TARGET]
    )
    model = Pipeline(
        [
            ("prep", build_preprocessor()),
            ("clf", LogisticRegression(max_iter=1000, random_state=seed)),
        ]
    )
    model.fit(X_train, y_train)

    proba = model.predict_proba(X_test)[:, 1]
    metrics = {
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        "accuracy": round(float(accuracy_score(y_test, model.predict(X_test))), 4),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }
    return model, metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="models/model.joblib")
    parser.add_argument("--metrics", default="metrics.json")
    parser.add_argument("--rows", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    model, metrics = train_model(generate_data(args.rows, args.seed), args.seed)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.out)
    Path(args.metrics).write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
