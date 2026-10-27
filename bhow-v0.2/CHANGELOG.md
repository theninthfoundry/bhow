# Changelog

## 0.2.0 — functional care-journal vertical slice

- Add a membership-scoped read-only per-dog overview endpoint with counts and bounded recent records.
- Add four Flet screens with a dog switcher, welcome/create-dog sheet, reminders and completion actions, and add-observation sheet.
- Add clear emergency information and honest, provider-free Explore and Check experiences.
- Refactor client transport with explicit localhost-only preview authentication and safe errors; remote token requests require HTTPS.
- Add UI-independent controller and view model, integration tests for dashboard and client transport.
- Add honest manual test/production gate: `docs/29_CLIENT_MILESTONE.md`.
- Not included: deployed mobile build, veterinary medical validation, trained breed model, real-time weather or nearby places, OIDC PKCE login.

## 0.1.0 — foundation

- Initial FastAPI, core/KB, DB schema, developer auth, OIDC JWT verifier, CRUD, migrations, CI, and project specifications.

### [0.2.1] - 2026-10-27
- Enhanced core domain activity validation and schema documentation.
