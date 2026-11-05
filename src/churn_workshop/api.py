"""Tiny FastAPI service that serves the trained model.

Run locally:  uvicorn churn_workshop.api:app --reload
"""

from __future__ import annotations

import os
from functools import lru_cache

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from churn_workshop import __version__
from churn_workshop.data import CONTRACTS
from churn_workshop.features import FEATURES, add_features

app = FastAPI(title="Churn API", version=__version__)


class Customer(BaseModel):
    tenure_months: int = Field(ge=0, le=120)
    monthly_charges: float = Field(gt=0)
    support_tickets: int = Field(ge=0)
    contract: str = Field(description=f"One of {CONTRACTS}")


@lru_cache(maxsize=1)
def get_model():
    return joblib.load(os.environ.get("MODEL_PATH", "models/model.joblib"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/predict")
def predict(customer: Customer) -> dict:
    frame = add_features(pd.DataFrame([customer.model_dump()]))
    proba = float(get_model().predict_proba(frame[FEATURES])[0, 1])
    return {"churn_probability": round(proba, 4)}
