# Exercise 3: Data & model quality gates (30 min)

**Goal:** Make CI fail when **data** is bad or the **model** is not good enough, not just when code is broken.

## Part A: Understand the data contract (5 min)
Read `src/churn_workshop/data.py::validate_data` and `tests/test_data.py`.
- What does the contract enforce?
- `train_model` calls `validate_data` first. Why is validating *inside* the pipeline important, not only in tests?

**Task:** add a new rule: `support_tickets` must be `>= 0`, with a test that proves a negative value is rejected. Make sure CI is green.

## Part B: Train in CI (10 min)
Create a new workflow `.github/workflows/model.yml` that, on pull requests touching `src/**`:
1. Installs the project
2. Runs `python -m churn_workshop.train --out models/model.joblib --metrics metrics.json`
3. Writes the metrics into the **job summary** (`$GITHUB_STEP_SUMMARY`)
4. Uploads `model.joblib` + `metrics.json` as an artifact named `model-${{ github.sha }}`

> Versioning artifacts by commit SHA = you can always trace a model back to the exact code that produced it.

## Part C: The quality gate (5 min)
Add a step running:
```bash
python scripts/check_metrics.py metrics.json --min-auc 0.70
```
Place it **before** the upload step. Why?

## Part D: Sabotage the model 💥 (10 min)
Open **three** PRs (or three commits on one PR) and, for each one, predict first: *will the unit tests fail? will the gate fail?*

| # | Change in `src/churn_workshop/features.py` | Unit tests | Gate (AUC ≥ 0.70) |
|---|--------------------------------------------|-----------|-------------------|
| 1 | `< 6` → `< 60` in `add_features` | ? | ? |
| 2 | Remove `"tenure_months"` from `NUMERIC` | ? | ? |
| 3 | Set `NUMERIC = ["is_new_customer"]` | ? | ? |

<details><summary>What you should observe</summary>

1. **Unit test fails** (`test_is_new_customer_flag`). The code-level check catches it, AUC barely moves (~0.83).
2. **Everything passes**, AUC drops to ~0.78 but stays above 0.70. A *weak gate lets a real regression through*.
3. **Unit tests pass, gate fails** (AUC ~0.68). Code is "correct", the model is worse. This is the failure mode only a metric gate catches.
</details>

Takeaways: tests protect *code correctness*, gates protect *model quality*, and a fixed threshold is a blunt instrument (see #2 and the discussion below).

## Discuss
- A fixed threshold (0.70) is crude. What would a **regression check** look like (compare to the model on `main`)?
- How would you check for performance on *slices* (e.g. each contract type)?
- Where should the threshold live, and who should be allowed to change it?

## ✅ Success criteria
- [ ] New data rule + test
- [ ] Metrics visible in the run summary
- [ ] Model artifact uploaded per commit
- [ ] A PR that fails *only* because of the quality gate (sabotage #3)

**Reference:** `solutions/02-model-gate.yml`
