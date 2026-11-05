# Exercise 1: Your first CI pipeline (25 min)

**Goal:** On every push and pull request, automatically lint and test the code.

## Step 0: See it run
Open `.github/workflows/ci.yml`. It only echoes a message. Push any change to `main` in your fork and open the **Actions** tab. You should see a green run.

## Step 1: Create a branch
```bash
git checkout -b feature/real-ci
```

## Step 2: Replace the `hello` job with a `test` job
Your job must:
1. Check out the code → `actions/checkout@v4`
2. Install Python 3.12 → `actions/setup-python@v5`
3. Install the project → `pip install -e ".[serve,dev]"`
4. Run `pytest`

<details><summary>Hint</summary>

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[serve,dev]"
      - run: pytest
```
</details>

## Step 3: Add a `lint` job
Add a **separate job** that runs `ruff check .` and `ruff format --check .`.
Make `test` depend on `lint` with `needs: lint` so cheap checks run first.

## Step 4: Open a pull request
Push your branch and open a PR **into your fork's `main`**. Watch the checks appear at the bottom of the PR.

## Step 5: Break it on purpose 💥
In `src/churn_workshop/features.py`, change `< 6` to `> 6`, commit and push to the PR.

- Which check fails? Read the log: which test caught it, and what did it say?
- Fix it and push again. Does the PR turn green?

Now introduce a lint error instead (e.g. add `import os` that is never used). Which job fails now?

## Step 6: Protect `main`
*Settings → Branches → Add branch ruleset* (or classic rule) for `main`:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass → select `lint` and `test`

Try to merge a failing PR. What happens?

## ✅ Success criteria
- [ ] PR shows `lint` and `test` checks
- [ ] You saw a red build caused by a test and one caused by lint
- [ ] `main` is protected

**Reference:** `solutions/01-ci.yml` (also includes Exercise 2 features, so try Exercise 2 first!)
