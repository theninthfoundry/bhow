# Bhow v0.3.1 — Audit Fix Release Notes

**Repository:** `theninthfoundry/bhow` on `main`.

This release integrates and documents the audit remediation updates for Bhow v0.3.1, incorporating root-level CI, PostgreSQL migration verification, database-backed idempotency, CORS preflight compatibility, and proxy-boundary authentication hardening.

## Audit Fixes & Enhancements

- **CI Workflow & PostgreSQL Container Job:** Root-level GitHub Actions workflow (`.github/workflows/ci.yml`) executes:
  - SQLite unit and API test suites.
  - PostgreSQL container job with automated migration cycles (`upgrade head -> downgrade base -> upgrade head`).
  - PostgreSQL schema readiness check (`/readyz`) and unauthenticated denial assertions.
- **CORS Configuration:** Added `Idempotency-Key` (and `idempotency-key`) to allowed CORS headers to guarantee browser client preflight compatibility for retry-safe operations.
- **Development Authentication Boundary:** Hardened `security.py` to reject reverse-proxy forwarding headers (`X-Forwarded-For`, `X-Forwarded-Host`, `X-Real-IP`, `Forwarded`) on development authentication, preventing external spoofing when running behind loopback proxies.
- **Cursor Pagination:** Complete cursor-paginated dog, care-event and task APIs with status filtering.
- **Database-Backed Idempotency:** Added migration `0002_idempotency.py` and idempotency tracking for event/task creation.
- **Database Readiness:** `/readyz` probe validates current migration schema (`0002`) and core tables.
- **Client Reliability:** Client supplies repeat-stable idempotency keys and supports incremental history pagination.
- **Documentation Reconciliation:** Synchronized root `README.md`, `31_STAGING_AND_CI.md`, and release documentation with the live repository commit history.

## Local Run & Verification

```bash
cd bhow-v0.2
python -m pip install -e '.[dev]'
cp .env.example .env
alembic upgrade head
uvicorn bhow_api.main:app --host 127.0.0.1 --reload
pytest -q
```

## Production Launch Blockers (Not Ready for Public Rollout)

As documented in [19_LAUNCH_GATES.md](bhow-v0.2/docs/19_LAUNCH_GATES.md) and [31_STAGING_AND_CI.md](bhow-v0.2/docs/31_STAGING_AND_CI.md), the following gates remain required before public deployment:
1. **Mobile PKCE & Credential Storage:** Full OIDC authorization code flow with PKCE, token refresh, revocation, and secure hardware storage on Android.
2. **Managed PostgreSQL Staging:** Live persistent PostgreSQL deployment with verified automated backups and disaster-recovery restoration rehearsals.
3. **Veterinary Content Review:** Formal clinical review of food ingredient hazards and emergency medical guidance by licensed veterinary professionals.
4. **Security & Operations:** Rate limiting, production reverse-proxy TLS termination, security scanning, privacy policy review, and end-to-end data export/deletion workflows.
