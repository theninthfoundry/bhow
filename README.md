# Bhow — The Dog Care OS

**Python-first care records for dogs.** A well-being companion for owners, foster carers and, eventually, responsible community-dog support.

> **Status:** v0.3.1 backend preview. Not a veterinary diagnostic product, production service, or tested Android release.

## Verified capabilities

- Authorized dog profiles, care tasks and observations
- Paginated history and retry-safe event/task creation
- Care overview, private JSON export and account-data deletion (identity-provider deletion is separate)
- Basic ingredient hazard *education* with conservative unknown results, not food safety certification
- SQLAlchemy models, Alembic migrations and regression tests
- Flet Python UI prototype (device runtime validation outstanding)

**Not active:** real mobile sign-in, breed AI, veterinary verification, weather feeds, clinic availability, push messaging, reliable medical triage, or public deployment.

## Quick start (localhost-only demo)

```bash
cd bhow-v0.2
python -m venv .venv
# Activate .venv using your operating system's activation command
python -m pip install -e '.[dev]'
cp .env.example .env  # On Windows, use: copy .env.example .env
alembic upgrade head
python -m uvicorn bhow_api.main:app --host 127.0.0.1 --reload
```

Open <http://127.0.0.1:8000/docs> and run `pytest -q` in another terminal. `.env.example` allows **local-only development identity**; never expose that environment on a public interface.

## Staging with persistent PostgreSQL

See [`bhow-v0.2/docs/31_STAGING_AND_CI.md`](bhow-v0.2/docs/31_STAGING_AND_CI.md). Requires actual HTTPS endpoints, identity provider, database credentials, and a reverse proxy for public access. The supplied Docker Compose setup binds the API to loopback and does **not** create a public deployment.

For deployment scope and verification steps, see [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md). GitHub Pages in this repository publishes a static landing page only and does not deploy the backend service.

## Architecture

```text
bhow-v0.2/
├── src/bhow_api/        FastAPI, authorization, SQLAlchemy
├── src/bhow_core/       deterministic rules
├── src/bhow_kb/         educational sample data (unreviewed)
├── client/              Flet UI prototype
├── alembic/             database migration history
├── tests/               API, domain and security tests
├── docs/                requirements, UX, architecture, launch gates
└── ops/                 local staging Compose and Dockerfile
.github/workflows/ci.yml  root-level GitHub CI
```

[Detailed development README](bhow-v0.2/README.md) · [Security guidelines](bhow-v0.2/SECURITY.md) · [Release notes](RELEASE_NOTES.md)

## Safety and release policy

Dog-health information is **education, not diagnosis**. Food ingredient matches are incomplete; a missing match is not evidence that food is safe. An animal with suspected poisoning, breathing difficulty or collapse needs prompt veterinary assistance. Real health content must be reviewed by a qualified veterinarian before launch.

### What remains for real users

OIDC authorization-code + PKCE in the mobile client, encrypted device credential storage, token refresh/logout, managed PostgreSQL with backup/restore, HTTPS reverse proxy, production rate limits, location privacy, commercial data licensing, professional content review, and target-device QA.
