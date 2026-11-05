from churn_workshop.data import generate_data
from churn_workshop.features import add_features


def test_add_features_does_not_mutate_input():
    df = generate_data(20)
    before = df.copy()
    add_features(df)
    assert df.equals(before)


def test_is_new_customer_flag():
    df = generate_data(100)
    out = add_features(df)
    assert (out["is_new_customer"] == (df["tenure_months"] < 6).astype(int)).all()
