# Exercise 2: Faster & more reliable (20 min)

**Goal:** Test across Python versions, speed up runs, and keep useful outputs.

## Part A: Matrix
Your library users (or your future self) may run Python 3.10, 3.11 or 3.12. Turn the `test` job into a matrix:

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```
Use `${{ matrix.python-version }}` in `setup-python`. How many test jobs appear in the PR now?

## Part B: Cache dependencies
Add `cache: pip` to `setup-python`. Run the workflow twice (re-run from the Actions UI).
- Compare install time on the first vs second run. Where do you see "Cache restored"?

## Part C: Cancel redundant runs
Push 3 commits quickly. Notice old runs keep going. Add at the top level:
```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```
Push again twice. What happens to the older run?

## Part D: Coverage artifact
1. Change the test command: `pytest --cov --cov-report=xml --cov-report=term-missing`
2. Upload `coverage.xml` using `actions/upload-artifact@v4` (only from one matrix entry).
3. Find it on the run summary page and download it.

## Part E: Least privilege
Add a top-level block:
```yaml
permissions:
  contents: read
```
Why is this a good default?

## Discuss
- What's the cost/benefit of testing 3 Python versions? When would you test only one?
- Which of these steps reduces *cost*, and which reduces *risk*?

## ✅ Success criteria
- [ ] 3 parallel test jobs
- [ ] Second run restores the pip cache
- [ ] Coverage artifact downloadable
- [ ] Older runs are cancelled on new pushes

**Reference:** `solutions/01-ci.yml`
