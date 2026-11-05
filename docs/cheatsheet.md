# GitHub Actions cheat sheet

```yaml
name: My workflow
on:
  push:
    branches: [main]
    tags: ["v*"]
    paths: ["src/**"]          # only when these files change
  pull_request:
  schedule:
    - cron: "0 3 * * *"        # min hour day month weekday (UTC)
  workflow_dispatch:           # manual button

env:                           # workflow-level env vars
  FOO: bar

permissions:
  contents: read

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    needs: [other_job]                 # ordering
    if: github.ref == 'refs/heads/main'
    environment: production            # protection rules / secrets scope
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: |
          multi-line
          script
        env:
          API_KEY: ${{ secrets.API_KEY }}
      - uses: actions/upload-artifact@v4
        with: { name: out, path: out/ }
```

## Handy contexts
| Expression | Meaning |
|-----------|---------|
| `${{ github.sha }}` | commit SHA |
| `${{ github.ref_name }}` | branch or tag name |
| `${{ github.event_name }}` | `push`, `pull_request`, … |
| `${{ github.actor }}` | who triggered it |
| `${{ secrets.X }}` | secret value (masked in logs) |
| `${{ matrix.x }}` | current matrix value |
| `$GITHUB_STEP_SUMMARY` | file; append Markdown to show it on the run page |
| `$GITHUB_OUTPUT` | file; `echo "key=value" >> $GITHUB_OUTPUT` to pass step outputs |

## Debugging tips
- Read the **first red step**, not the last log line.
- Reproduce locally: `make all`. CI should run the *same commands*.
- Re-run with debug logging: "Re-run jobs → Enable debug logging".
- YAML is whitespace-sensitive. Use an editor with YAML linting.
- `uses:` pin to a major version (`@v4`); for high-security setups pin to a commit SHA.
