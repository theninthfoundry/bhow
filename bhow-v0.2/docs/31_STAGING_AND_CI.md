# Bhow v0.3.1 — staging and CI operations

## Not a public deployment

This release supports **local/closed staging evaluation only**. No public instance has been deployed or verified. Do not make it public with temporary identity headers, unreviewed food guidance, or a file-backed SQLite production DB.

## Local verification

From `bhow-v0.2/` on Python 3.12+:

```sh
python -m pip install -e '.[dev]'
ruff check src tests client
mypy --strict src/bhow_core
pytest -q
python -m compileall -q src client tests
BH_APP_ENV=test BH_DATABASE_URL=sqlite:///./migration_test.db BH_ALLOW_DEV_AUTH=false alembic upgrade head
BH_APP_ENV=test BH_DATABASE_URL=sqlite:///./migration_test.db BH_ALLOW_DEV_AUTH=false alembic downgrade base
BH_APP_ENV=test BH_DATABASE_URL=sqlite:///./migration_test.db BH_ALLOW_DEV_AUTH=false alembic upgrade head
```

CI lives in `/.github/workflows/ci.yml` (repository root). The workflow includes a second, disposable PostgreSQL 16 container job that rehearses migrations (upgrade -> downgrade -> upgrade), checks `/healthz` and `/readyz`, and verifies unauthenticated denial. This job runs and verifies cleanly in GitHub Actions (though automated CI verification is not a substitute for complete staging launch approval). All checks must remain green on pull requests before merge.

## Secure staging configuration

Provision a **private** Postgres database and a real OIDC provider with RS256 access-token support. Copy `.env.example` **as a local guide only**, then set the following in protected deployment secret settings:

```text
BH_APP_ENV=staging
BH_ALLOW_DEV_AUTH=false
BH_DATABASE_URL=postgresql+psycopg://<username>:<urlencoded-password>@<db-host>:5432/<database>
BH_OIDC_ISSUER=https://<idp-host>/
BH_OIDC_AUDIENCE=<api-audience>
BH_OIDC_JWKS_URL=https://<idp-host>/.well-known/jwks.json
BH_ALLOWED_ORIGINS=https://<your-staging-app-host>
```

The database password above is a placeholder. Do not commit actual credentials. Use provider secret storage and URL-encode reserved characters in DSNs. Configure DNS/certificates and ingress separately; the Compose sample binds to `127.0.0.1` only. Restrict database ingress by IP/network and least privilege, with automated encrypted backups and a tested restore.

Run `python tools/preflight.py` for settings validation, and `python tools/preflight.py --check-db` after `alembic upgrade head`. `GET /readyz` checks database schema connectivity; it does *not* test the identity provider, external network, or full app.

## Compose staging sample

From `bhow-v0.2/ops/`, set `POSTGRES_PASSWORD` and real OIDC/HTTPS CORS variables then run `docker compose up --build`. This runs a local PostgreSQL service with a persistent named volume, schema migration job, and API on `127.0.0.1:8000`. This is a staging example, not a resilient managed database, verified backup, or secure HTTPS reverse proxy.

## Launch blockers and tests

1. Real PKCE sign-in on Android with session refresh/logout/revocation; hardware-backed keychain storage where supported.
2. OIDC issuer/JWKS/AUD configuration validated against an actual provider; expired/wrong-audience tokens denied.
3. Run Postgres migration-up/down test against a disposable Postgres instance, not production.
4. Account export/delete end-to-end; verify IdP subject deletion separately and cover private records.
5. Restore a backup into a new database; document recovery time and retention policy.
6. Network failure and repeat-submit Android tests; screen reader/text scaling; crash/analytics consent.
7. Rate limits, incident alerts, dependency/secret scanning, explicit data retention, veterinary review, content versioning.
8. Product and privacy/security sign-off before any outside beta.
