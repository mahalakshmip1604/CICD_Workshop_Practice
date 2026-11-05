# Exercise 4: Containers & continuous delivery (30 min)

**Goal:** Package the model service as a Docker image, verify it in CI, and publish it to GitHub Container Registry (GHCR) on every merge to `main`.

## Part A: Run it locally (optional, if you have Docker)
```bash
make docker-build
make docker-run
curl localhost:8000/health
curl -X POST localhost:8000/predict -H 'content-type: application/json' \
  -d '{"tenure_months":3,"monthly_charges":95,"support_tickets":5,"contract":"month-to-month"}'
```

## Part B: Build the image in CI (10 min)
Create `.github/workflows/docker.yml`:
- Trigger: `pull_request` and `push` to `main`
- Steps: checkout → `docker/setup-buildx-action@v3` → `docker/build-push-action@v6` with `push: false`

Open a PR. Breaking the `Dockerfile` should now break the PR *before* merge. Try it. (e.g. typo in a `COPY` path)

## Part C: Smoke test the container (10 min)
A built image isn't necessarily a *working* image. After building (with `load: true`), start it and poll `/health`:
```bash
docker run -d --name api -p 8000:8000 <image>
for i in $(seq 1 20); do curl -fs localhost:8000/health && exit 0; sleep 1; done
docker logs api; exit 1
```

## Part D: Publish on merge (10 min)
Only on pushes to `main`/tags:
1. Add `permissions: packages: write`
2. Log in with `docker/login-action@v3` (registry `ghcr.io`, password `${{ secrets.GITHUB_TOKEN }}`). No personal secrets needed.
3. Tag images with `docker/metadata-action@v5` → short SHA + branch/version
4. Set `push: true` when the event isn't a PR

After merging, find your image under your profile/repo → **Packages**.

## Discuss
- Why tag with the git SHA instead of only `latest`?
- Our image trains the model at build time. What are the pros and cons vs. downloading a versioned model from a registry?
- What would you add: vulnerability scanning of the image? SBOM? Image signing?

## ✅ Success criteria
- [ ] PR builds the image and smoke-tests it
- [ ] Merge to `main` publishes `ghcr.io/<you>/<repo>:sha-xxxxxxx`
- [ ] You can explain how to roll back to a previous version

**Reference:** `solutions/03-docker-publish.yml`
