# Bhow v0.3.2 — Phase 1 & Audit Release Notes

**Repository:** `theninthfoundry/bhow` on `main`.

This release implements Phase 1 of the Bhow Master Build Plan: Care Passport extensions, audit-preserving care event corrections, suspected-ingestion emergency escalation, dual-database disaster recovery rehearsal, and schema migration `0003`.

## Phase 1 Deliverables (v0.3.2)

- **Dog Care Passport Data Model & Schemas:**
  - Extended `Dog` entity and API schemas with optional passport fields: `allergies_reported`, `conditions_reported`, `medications_reported`, `microchip_id`, and `veterinarian_contact`.
  - Normalized validation accepting unknown or blank fields safely without breaking queries.
- **Event History Integrity & Correction Workflow:**
  - Added `POST /v1/dogs/{id}/events/{event_id}/correct` endpoint.
  - Linked corrections via `supersedes_event_id` and audit metadata `correction_reason` without overwriting or deleting historical event records.
  - Idempotency-safe correction submissions via `Idempotency-Key`.
- **Ingestion Emergency Triage Workflow:**
  - Enhanced food safety API (`/v1/food/check`) to detect when substances were already eaten (`already_eaten=True`).
  - Added structured `emergency_escalation` instructions directing owners to immediate veterinary poison intervention without delaying triage.
  - Reaffirmed boundary: Bhow provides educational references only and does not diagnose poisoning or compute chemical dosages.
- **Production Dual-Database Backup & Restoration Rehearsal:**
  - Upgraded `tools/backup_restore.py` from superficial single-connection tests to a genuine dual-database recovery engine (`--source-url` and `--target-url`).
  - Performs complete schema and tabular snapshotting, cross-database restore, row count verification, foreign-key relationship verification, and RTO/RPO metric logging.
- **Schema Migration `0003_passport_and_corrections.py`:**
  - Forward and rollback migrations for passport fields and event correction audit pointers.
  - Updated `/readyz` operational health probe to validate schema `0003`.
- **Automated Test Suite:**
  - Added `tests/test_audit_phase1.py` with 100% pass rate covering passport CRUD, event correction audit trails, cross-user IDOR denial, ingestion emergency escalation, and dual-database backup rehearsal.

---

## Prior Audit Fixes (v0.3.1)

- **CI Workflow & PostgreSQL Container Job:** Root-level GitHub Actions workflow (`.github/workflows/ci.yml`) executing SQLite tests, PostgreSQL container migrations, and readiness probes.
- **CORS Configuration:** Added `Idempotency-Key` to allowed headers for browser preflight compliance.
- **Dev-Auth Hardening:** Restricted development identity strictly to direct loopback peers without forwarding headers (`X-Forwarded-For`, `X-Real-IP`).
- **Cursor Pagination:** Keyset cursor-paginated endpoints for dogs, care events, and care tasks.
- **Database-Backed Idempotency:** Persisted idempotency tracking for retry safety (`0002_idempotency.py`).

---

## Local Verification Commands

```bash
cd bhow-v0.2
python -m pip install -e '.[dev]'
alembic upgrade head
pytest -q
python tools/backup_restore.py --rehearse
```

## Production Launch Blockers (Next Milestones)

As defined in [19_LAUNCH_GATES.md](bhow-v0.2/docs/19_LAUNCH_GATES.md):
1. **Mobile PKCE & Keyring:** Full OIDC authorization code flow with PKCE, token refresh, and Android Keystore on client.
2. **Managed PostgreSQL Staging:** Dual-target rehearsal against live hosted cloud PostgreSQL instances.
3. **Veterinary Content Sign-off:** Clinical review of food safety hazard catalog by licensed professionals.
