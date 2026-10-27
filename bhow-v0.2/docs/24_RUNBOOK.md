# 24 — Developer runbook (local, CI, staging)

## Local backend

Create virtual environment, install `pip install -e '.[dev]'`, copy `.env.example` to `.env`, run `alembic upgrade head`, `uvicorn bhow_api.main:app --reload`, then `pytest -q`. The local SQLite file is ignored in Git. `curl` with `X-Dev-User` works ONLY after opting into local demo auth. Run `python tools/smoke.py` with server active.

## SQLite → hosted PostgreSQL

Obtain a managed PostgreSQL instance and restricted credentials. Set `BH_APP_ENV=staging`, PostgreSQL `BH_DATABASE_URL=postgresql+psycopg://...`, nonwildcard HTTPS origins and real OIDC issuer/audience/JWKS. Explicitly keep `BH_ALLOW_DEV_AUTH=false`. Run migrations as a deployment step **before** routing real traffic, not at import time. Test backup restoration and policy before shipping. Docker Compose is a starting topology, not a fully configured production deployment.

## Manual DB migration rehearsal

- SQLite demo: `alembic upgrade head`, `alembic current`, `alembic downgrade base`, `alembic upgrade head`.
- Postgres staging: same commands using staging env; only run downgrade on disposable database. In production use forward fixes and backups rather than casually downgrading destructive schemas.
- Autogenerate changes only after careful review: `alembic revision --autogenerate -m 'description'`; check nullable transitions and duplicate names.

## Client preview

`cd client && python -m pip install -e .` and in a local shell set `BH_CLIENT_DEV_AUTH=true`, then `python main.py`. `client/README.md` distinguishes preview from production Android app. Bundle camera/location extension only after verifying the exact Flet version and Android permission lifecycle.

## Versioning and source integrity

Pin dependencies with a resolved lock (e.g., `uv lock`), commit after CI validation and review upgrades. Python environment/toolchain tested for full deployment should be fixed by container digest and vendor patches. Do not force lock regeneration in a package repository without connectivity and then claim all resolutions succeeded.
