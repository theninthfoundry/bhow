# 06 — Relational data model, provenance, ownership

## Current schema (migration `0001_initial`)

```text
DOGS (id PK, name, date_of_birth?, estimated_age_months?,
      breed_reported?, weight_kg?, care_context,
      created_at, updated_at)
    │ one-to-many                 │ one-to-many
    ▼                             ▼
DOG_CAREGIVERS                  CARE_EVENTS
(id PK, dog_id FK,              (id PK, dog_id FK, kind, notes,
 subject, role)                 occurred_on, source, verified,
 UNIQUE(dog_id,subject)         created_by, recorded_at)
    │
    └ ownership gate
DOGS ──────────────────────► CARE_TASKS
                             (id PK, dog_id FK, title,
                              kind, due_on, status,
                              scheduled_by, created_at)
```

Why separate table for caregivers even before sharing ships? It supports multiple roles later without putting personally identifying owner emails into every dog row. External issuer subject is stored as `subject`, not a user-controlled display name. Data model tolerates unknown exact breed/age. No dog photograph or vet record is falsely certified by a model.

## Integrity, indexes and migrations

- 36-character UUID strings for portability of SQLite/PostgreSQL in this initial codebase; consider PostgreSQL native UUID in later migration.
- FK constraints plus ORM child cascade; verified with deletion integration test.
- Care events are append-only: edits require correction events and audit metadata after first production release. The present API provides no update event endpoint.
- Task dates are supplied by a caregiver or veterinary professional; not blindly inferred from a universal schedule.
- `verified` is server-owned and always false in consumer API. A future vet route may change it only through an authenticated professional verification workflow with audit trail.
- `ix_caregiver_subject` scopes a subject's profiles. `(dog_id, occurred_on)` supports timeline. `(dog_id, due_on)` supports care tasks.

## Next schema additions — explicit ADR before coding

| Table | Critical columns | Safety / lifecycle |
|---|---|---|
| `identity_accounts` | issuer, subject, consent version | Treat IDP subject as stable compound identity |
| `consent_grants` | subject, purpose, granted_at, revoked_at | Consent is purpose-specific and auditable |
| `assets` | dog_id, private_key, mime, bytes, checksum, exif_removed | No public URL; quarantine prior to publish |
| `veterinary_providers` | org_id, registration proof, verification status | Strict verification and expiry |
| `medical_documents` | dog_id, asset_id, source, reviewed_by, review_at | Uploaded ≠ verified |
| `verification_attestations` | record_id, vet_id, signature, timestamp | Reversible/expirable if incorrect |
| `care_event_corrections` | prior_id, new_id, reason, actor | Do not silently rewrite medical history |
| `device_tokens` | account, provider, encrypted token, consent | Push opt-in and revocation |
| `notification_outbox` | event_id, dedupe_key, attempt_count, lease_until | At-least-once with idempotent provider interface |
| `share_grants` | dog_id, scope, opaque_token_hash, expiry, revoked | Revocable purpose-limited QR sharing |
| `places` | provider source, last_confirmed, geometry, services | Listing ≠ verified opening hours |
| `rescue_cases` | approximate_public_area, exact_private_point, partner_ack | Never public precise sensitive location |
| `audit_entries` | actor, action, resource, digest, timestamp | Redacted immutable security events |

## Retention and portability

Deletion must cascade application DB and later include assets, caches, queued notifications, auth-provider account and legal exceptions. Current `DELETE /account/me` deletes MVP-only, single-caregiver records; it does **not** delete a third-party identity-provider account or data in integrations that do not yet exist. File retention and asynchronous purge proofs must be implemented before first media upload. Export is JSON MVP-only; later veterinary summary must be understandable on paper and preserve source labels.
