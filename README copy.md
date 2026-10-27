# Bhow — Dog Care OS

**Python-first dog wellbeing app. Work in progress; not a clinical or production system.**

Bhow provides a caregiver-scoped dog profile, care notes, reminders, private data export, and educational food-ingredient flags. Breed inference, verified local care, real weather and Android OIDC sessions are not yet connected.

## Start

```sh
cd bhow-v0.2
python -m pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
uvicorn bhow_api.main:app --host 127.0.0.1 --reload
pytest -q
```

Never expose local header authentication outside a loopback-only development environment. See `bhow-v0.2/SECURITY.md`.

## Project structure

- `bhow-v0.2/src/bhow_api`: FastAPI endpoints / SQLAlchemy persistence
- `bhow-v0.2/src/bhow_core`: pure care rules
- `bhow-v0.2/src/bhow_kb`: educational reference content (unreviewed)
- `bhow-v0.2/client`: Flet client prototype
- `bhow-v0.2/alembic`: migrations
- `bhow-v0.2/tests`: tests
- `bhow-v0.2/docs`: PRD, architecture, design and launch gates

## Release status

Backend prototype and tests only. Android Flet runtime, live sign-in, provider revocation, remote integrations, Postgres migrations and external security review are pending. See [v0.3 fixes](bhow-v0.2/docs/30_V03_AUDIT_REMEDIATION.md).
