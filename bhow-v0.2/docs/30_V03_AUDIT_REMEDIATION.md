# v0.3 — Security and record-integrity repair

**Reviewed base:** `theninthfoundry/bhow` main `4d0d476791a7df6e7584bb79d7ab779f3bce3031`.

## Changes in this package

- A-01: local-only header identity now checks ASGI peer loopback. **This is not sufficient if an untrusted reverse proxy forwards public requests over loopback. Never expose development identity on a network.**
- A-02: GitHub workflow is now at repository-root `.github/workflows/ci.yml` and uses `working-directory: bhow-v0.2`.
- A-04: new `/v1/dogs/{id}/events/page`  , `/tasks/page`, and `/dogs/page` APIs return `items` + `next_cursor`, with deterministic keyset pagination and task status filter; legacy list endpoints remain for compatibility. The Flet passport supports loading more pages.
- A-05: optional `Idempotency-Key` on event/task creation, unique persisted ledger and payload conflict handling. Client uses a stable key per open form; repeated submissions use the same key.
- A-06 (partial): E-number codes like `E-967` now match `e967` alias. Veterinary review, negation-aware evidence handling, broader ingredient testing remain outstanding.
- A-09: history dates have a separate formatter from overdue task due dates.
- A-10: dog name is stripped/rejected if blank at the server.
- A-11: Compose migration job and `/readyz` schema/DB check; Postgres execution still needs live test.
- A-12: root README and clearer setup.

## Still blocking public launch

- A-03 real OIDC authorization-code + PKCE and Android keystore/keychain token lifecycle.
- A-07 complete account deletion and identity-provider revocation orchestration; backend data deletion is not full account deletion.
- A-08 Flet UI still uses sync network requests. Need async task scheduling, loading, accessibility and Android device validation.
- No signed/approved veterinary knowledge base. No clinically validated food verdict.
- PostgreSQL/live Docker, cross-process concurrency, provider integration and security penetration tests.
- Root CI still must be activated and pass on actual GitHub pull requests; this is a local archive, not a pushed commit.

## Pagination contracts

- `GET /v1/dogs/page?limit=50[&cursor=...]` (most recently created first)
- `GET /v1/dogs/<uuid>/events/page?limit=50[&cursor=...]` (most recent first)
- `GET /v1/dogs/<uuid>/tasks/page?status=all&limit=50[&cursor=...]` (earliest due first)
- Body: `{"items": [...], "next_cursor": null | "opaque-string"}`.
- Cursor does not authorize access and is not a security secret; ownership checked on every request.
- Pagination is stable for a static dataset. Concurrent inserts may move between pages; clients should refresh for a new snapshot.

## Testing

From `bhow-v0.2`: `pytest -q`, `alembic upgrade head`, `python -m compileall -q src client tests`. Root CI additionally expects `ruff`, `mypy`.
