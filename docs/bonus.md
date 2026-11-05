# Bonus challenges

Pick what's relevant for your day job.

1. **Nightly retraining**: scheduled + manual trigger, with artifacts and a gate (`solutions/05-scheduled-retrain-and-security.yml`).
2. **Dependency security**: run `pip-audit` in CI; enable Dependabot (`.github/dependabot.yml` is already included, just enable it in repo settings).
3. **Regression gate**: instead of a fixed AUC threshold, download the metrics artifact from the last `main` run and fail if AUC drops by more than 0.01. (Hint: `gh run download`, or `actions/download-artifact` with `run-id`.)
4. **Slice metrics**: report AUC per `contract` type and fail if any slice is below a floor.
5. **Data drift check**: generate a "new batch" with different distribution (`monthly_charges` mean 120) and add a test that detects the shift (e.g. KS test from `scipy.stats`).
6. **PR comment bot**: post the metrics table as a PR comment (`actions/github-script`).
7. **Reusable workflow**: extract "setup Python + install" into a reusable workflow or composite action.
8. **Type checking**: add `mypy` and make it a required check.
9. **Experiment tracking**: log metrics to MLflow in CI; compare runs.
10. **Another platform**: port `ci.yml` to GitLab CI, Azure DevOps or Jenkins. Which concepts map 1:1?
