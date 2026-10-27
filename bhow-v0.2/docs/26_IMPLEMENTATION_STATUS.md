# 26 — Truthful implementation status and evidence

| Vertical slice | Working in delivered code | Verified in current run | Missing for public app |
|---|---|---|---|
| API setup | Yes | FastAPI imports, OpenAPI generation | Hosting/monitoring |
| Relational schema | Yes | SQLite migration up/down/check | Staging PostgreSQL rehearsal |
| Dog CRUD | Yes | HTTP integration tests | Secure mobile login, role sharing |
| Dog Today overview | Yes | Cross-account and counts HTTP tests | Frontend physical-device checks, reminders by timezone |
| Care events | Yes | Insert/read/provenance tests | Vet verification credentials, correction workflow |
| Due care tasks | Yes | CRUD/completion tests | Push delivery, smart schedule clinical review |
| Auth | OIDC JWT validation and local opt-in | Production misconfig guard + IDOR tests | Mobile OIDC PKCE login and provider integration |
| Food flags | Bounded educational text check | Hazard/unknown tests | Vet-approved KB, OCR, clinical audit |
| Breed discovery | Abstention interpreter | Domain tests | Dataset, trained ONNX model, deployed inference |
| Outdoor guidance | Offline generic advice | HTTP test | Live provider, licensed use and reviewed regional rules |
| Nearby clinics | Explicit unavailable | HTTP contract | Verified provider and consentful location search |
| Account export/deletion | MVP database only | Integration test | IDP deletion, assets/partner deletion, legal retention |
| Flet client | Four-tab Today/Passport/Check/Explore; dog switcher/forms | View-model/API tests and syntax; Flet not installed | Live Flet runtime/device and accessibility validation |
| Deploy | Docker/Compose/CI definitions | Python tests and SQLite migration | Live deployed service, production load and security tests |

## Verification notes

Executed locally in the preparation environment: `PYTHONPATH=src pytest -q` (21 passing in v0.2); Python compileall; Alembic SQLite upgrade → downgrade → upgrade; `alembic check` (no schema drift). The environment could not reach PyPI to download Ruff, so Ruff formatting/lint, MyPy, Flet UI runtime, dependency locking, PostgreSQL live migrations and actual deployment have **not** been executed. No paid providers or veterinary reviewer have been connected. This is a genuine working starter, not a fully finished or clinically approved application.

<!-- Phase 2 Functional Gate: PASSED -->
