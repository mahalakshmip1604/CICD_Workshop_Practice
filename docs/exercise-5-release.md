# Exercise 5: Releases with approval gates (20 min)

**Goal:** Cut a versioned release through staging → production, with a human approval before production.

## Part A: Create environments
*Settings → Environments → New environment*
- `staging`: no rules
- `production`: ✅ **Required reviewers** → add yourself

## Part B: The release workflow
Create `.github/workflows/release.yml` triggered by tags `v*`, with jobs chained via `needs:`

1. `verify`: tests + train + quality gate (re-check everything on the exact tagged commit)
2. `deploy-staging`: `environment: staging`
3. `deploy-production`: `environment: production`, then `gh release create` with generated notes

Real deploy commands (kubectl, cloud CLI, SSH…) are replaced by `echo` here. The *structure* is the lesson.

## Part C: Ship it
```bash
git checkout main && git pull
git tag v0.1.0
git push origin v0.1.0
```
Watch the run pause at **production** and wait for your approval. Approve it, then check the **Releases** page.

## Part D: Rollback drill
Pretend v0.1.1 is broken. Describe (or implement) how you'd roll back:
- Re-deploy the previous image tag?
- Revert the commit and tag `v0.1.2`?
Which is faster? Which leaves a better audit trail?

## Discuss
- What belongs in a staging check that's *not* in CI? (real data volumes, integration with upstream systems…)
- Continuous *delivery* vs *deployment*: where does your team want the human gate?
- How would you add a **canary** or **shadow deployment** for a model?

## ✅ Success criteria
- [ ] Tag triggers the workflow
- [ ] Pipeline pauses for approval before production
- [ ] A GitHub Release exists

**Reference:** `solutions/04-release-deploy.yml`
