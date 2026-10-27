# BHOW / The Dog Care OS — v0.2

> **Know your dog. Care with confidence.** A thoughtful, Python-first foundation for canine wellbeing — and eventually a responsible animal-welfare network.

**Status: functional API + four-screen Flet implementation, NOT a verified mobile release or production-ready veterinary application.** Updated 27 Oct 2026. Working name subject to trademark clearance. This kit merges the strongest parts of Bhow (individual dog's living care profile) and PAWPRINT (broader welfare vision).

## What is actually working

**v0.2 additions:** authenticated `GET /v1/dogs/{dog_id}/overview`, live Flet Today/Passport/Check/Explore flow, dog switching, quick care tasks and observations. The backend and client state test suites run; the Flet UI itself has not been executed in this environment because Flet was unavailable for installation. See `CHANGELOG.md`.

- FastAPI `/v1` service with OpenAPI schema, typed request validation, relational dog/caregiver/care-event/care-task models.
- Record creation/listing/updating/deletion, append-only caregiver care events, task creation/completion, data export and initial account-record deletion.
- Authorization enforced on every dog-related endpoint, using external OIDC RS256 bearer-token verification in staging/production. Explicit **local-only** development identity header for local demos.
- Educational ingredient-text flags from cited **sample** hazard data; *unknown never means safe*, and the sample is **not reviewed by a veterinarian**.
- Offline outdoor-care educational advice clearly labeled **not live**.
- Alembic initial migration, SQLite local dev, PostgreSQL via psycopg for hosting, Docker and CI skeleton, integration tests, and a Python/Flet four-screen care-journal implementation (requires device testing).
- ML models, photo upload, actual push notifications, live weather, nearby vet directory, payments and rescue coordination are **contracts/planned**, not falsely claimed to work.

## Project map

```text
bhow-starter/
├── README.md                   # Entry point and exact setup
├── pyproject.toml              # Typed Python backend, quality tooling
├── .env.example                # Environment and auth configuration
├── alembic/                    # Versioned SQL migrations
├── src/
│   ├── bhow_api/               # FastAPI HTTP/auth/persistence adapters
│   ├── bhow_core/              # Pure business rules (deterministic)
│   └── bhow_kb/                # Versioned preview knowledge base
├── tests/                      # Domain + HTTP authorization tests
├── tools/                      # Smoke test
├── client/                     # Python/Flet UI preview + brand tokens
├── models/                     # ML integration/model-card requirements
├── docs/                       # PRD, UX, system design, quality, business
├── ops/                        # Docker & Compose
└── .github/workflows/ci.yml   # Lint, tests, migration rehearsal
```

## Quickstart — laptop, no paid provider required

Python 3.12+ recommended. From the archive's root:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e '.[dev]'
cp .env.example .env        # Windows: copy .env.example .env
alembic upgrade head
uvicorn bhow_api.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`. `.env.example` explicitly enables **unsafe development identity headers only for local use**. Try:

```bash
curl -X POST http://127.0.0.1:8000/v1/dogs \
  -H 'X-Dev-User: founder' -H 'Content-Type: application/json' \
  -d '{"name":"Kaju","care_context":"community","estimated_age_months":24}'
curl http://127.0.0.1:8000/v1/dogs -H 'X-Dev-User: founder'
curl -X POST http://127.0.0.1:8000/v1/food/check \
  -H 'Content-Type: application/json' -d '{"ingredients_text":"chocolate and raisins","already_eaten":true}'
pytest -q
```

Separate UI implementation: `client/README.md`. To run a four-screen UI prototype, install its own dependencies and enable the explicitly local client identity. For deployment: use a real external OIDC provider, HTTPS reverse proxy, Postgres, supported secret store and an appropriate rate limiter. **Do not copy local auth settings to production.** Compose is a starting example and requires real OIDC variables.

## Why the product should win

**Core promise:** “One reliable place to understand this individual dog, organize its care, and know what to do next.” Breed classification is acquisition; the care passport and useful record continuity are the retention hypothesis. Long-term platform: optional verified professional and animal-welfare partner workflows.

### Product experiences (some working, some planned)

1. **Meet** — beautiful, evolving dog identity, unknown data allowed, Indian indie-friendly.
2. **Today** — one next helpful action, upcoming reminders, location-aware outdoor guidance (once weather feed is licensed).
3. **Passport** — caregiver observations distinctly separated from vet-verified facts; controlled sharing.
4. **Check** — food/label safety assistance with uncertainty and emergency referral.
5. **Discover** — visual breed resemblance, abstention, no false genetic certainty.
6. **Help** — verified nearby resources and eventually a moderated welfare network.

## How to use the specifications

Start at `docs/01_PRD.md`, then `docs/03_UI_UX.md`, `docs/05_ARCHITECTURE.md`, `docs/06_DATA_MODEL.md`, `docs/07_API.md`, and `docs/12_EXECUTION.md`. `docs/19_LAUNCH_GATES.md` lists blockers before public release. `docs/29_CLIENT_MILESTONE.md` documents implemented interaction flows and open device-test gates. `docs/23_MASTER_BUILD_PROMPTS.md` contains stage-specific implementation prompts for a development agent. All referenced providers, paid integrations, veterinary signoffs and legal counsel are **not included**.

## Boundaries that protect users

This application is not veterinary diagnosis or treatment. A photo cannot establish genetic breed. A missing food hazard match cannot establish that food is safe. An unverified clinic listing does not establish 24/7 availability. Precise dog/rescue locations should never be public by default. Essential urgent-care guidance and record export are never paywalled. Sources and limitations are documented in `docs/09_VETERINARY_SAFETY.md` and `docs/10_SECURITY_PRIVACY.md`.

## Sources used to frame safety and platform design

- [WSAVA vaccination guidelines](https://wsava.org/Global-Guidelines/Vaccination-Guidelines/)
- [ASPCA foods to avoid](https://www.aspca.org/pet-care/aspca-poison-control/people-foods-avoid-feeding-your-pets)
- [MeitY DPDP Rules 2025](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025%3B)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Flet documentation](https://flet.dev/docs/)

**Ownership:** no business trademark, code license for third parties, photographic license or vendor contract is conveyed by this starter. See `LICENSE-NOTICE.md`.
