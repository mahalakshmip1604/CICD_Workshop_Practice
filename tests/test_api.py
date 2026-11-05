import joblib
import pytest
from fastapi.testclient import TestClient

from churn_workshop.data import generate_data
from churn_workshop.train import train_model


@pytest.fixture()
def client(tmp_path, monkeypatch):
    model, _ = train_model(generate_data(500))
    path = tmp_path / "model.joblib"
    joblib.dump(model, path)
    monkeypatch.setenv("MODEL_PATH", str(path))

    from churn_workshop import api

    api.get_model.cache_clear()
    return TestClient(api.app)


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_predict_returns_probability(client):
    payload = {
        "tenure_months": 3,
        "monthly_charges": 95.0,
        "support_tickets": 5,
        "contract": "month-to-month",
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    assert 0.0 <= r.json()["churn_probability"] <= 1.0


def test_predict_rejects_bad_input(client):
    r = client.post("/predict", json={"tenure_months": -1})
    assert r.status_code == 422
