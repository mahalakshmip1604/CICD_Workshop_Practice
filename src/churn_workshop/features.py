"""Feature engineering and preprocessing."""

from __future__ import annotations

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC = ["tenure_months", "monthly_charges", "support_tickets", "is_new_customer"]
CATEGORICAL = ["contract"]
FEATURES = NUMERIC + CATEGORICAL
TARGET = "churned"


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add derived features. Never mutates the input."""
    out = df.copy()
    out["is_new_customer"] = (out["tenure_months"] < 60).astype(int)
    return out


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        [
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ]
    )
