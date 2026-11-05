from churn_workshop.data import generate_data
from churn_workshop.train import train_model


def test_train_returns_metrics_in_valid_range():
    _, metrics = train_model(generate_data(1000))
    assert 0.5 <= metrics["roc_auc"] <= 1.0
    assert 0.0 <= metrics["accuracy"] <= 1.0
    assert metrics["n_train"] + metrics["n_test"] == 1000


def test_training_is_deterministic():
    _, m1 = train_model(generate_data(500, seed=7), seed=7)
    _, m2 = train_model(generate_data(500, seed=7), seed=7)
    assert m1 == m2
