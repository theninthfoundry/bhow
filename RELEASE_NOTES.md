# Bhow v0.3 — audit-fix release notes

**Base repository:** `theninthfoundry/bhow` main @ `4d0d476791a7df6e7584bb79d7ab779f3bce3031`.

This is an updated source package, **not an update pushed to GitHub**. The GitHub connector has read access but no push permission. The working project is intentionally kept in the existing `bhow-v0.2/` directory to avoid breaking current import and build paths; application metadata identifies v0.3.

## Changes

- Development auth requests from non-loopback ASGI peers now fail HTTP 403 (don't expose loopback through public proxies).
- CI workflow moved to repository root; working directory set to nested package.
- Complete cursor-paginated dog, care-event and task APIs; task status filters.
- Database-backed idempotency on event/task creates, including conflict detection.
- Client passes repeat-stable idempotency keys and offers Load more on passport history.
- Name normalization, E-967 additive variant, corrected date formatting.
- Migration 0002, Compose migration job, database/schema readiness endpoint.
- Root README, updated API documentation, regression tests.

## Run locally

```bash
cd bhow-v0.2
python -m pip install -e '.[dev]'
cp .env.example .env
alembic upgrade head
uvicorn bhow_api.main:app --host 127.0.0.1 --reload
pytest -q
```

## Verification

- Pytest: 30 passed; 0 failed.
- Python compileall: passed.
- SQLite upgrade/downgrade/upgrade: passed.
- SQLite `/readyz` and `/healthz`: HTTP 200 after migration.
- Ruff/mypy: not run (unavailable in sandbox, installation unavailable). Tests need green CI after upload.
- Physical Flet app / Android, Docker, PostgreSQL and real OIDC: not tested.

## Still not ready for public rollout

OIDC PKCE + Android secure token storage/revocation; complete deletion workflows; async Flet UI; clinically reviewed food reference; real provider integrations; live Postgres staging, production privacy/security review. See `bhow-v0.2/docs/30_V03_AUDIT_REMEDIATION.md`.

## Applying to your repository

1. On your computer clone `https://github.com/theninthfoundry/bhow`.
2. Create a new branch from `main`: `git switch -c fix/v03-reliability`.
3. Copy this package's root `.github/` and README, and replace the `bhow-v0.2/` project directory.
4. Run `pytest -q`, `alembic upgrade head`, and CI lint/type checks.
5. Commit and open a PR, check Actions and approve only after staging testing.

Do not overwrite any later changes you have independently made without reviewing a diff.
