# Bhow next build decision — after v0.2

**Build only one trust-critical milestone next:** authenticated, private, portable dog passports with *real* identity and read-only history on a device. Leave breed-photo inference and medical symptom assessment blocked until validation.

## v0.3 scope — real care identity

1. Choose hosted OIDC provider with Android authorization-code + PKCE, mobile app deep-link redirect and configurable issuer/audience.
2. Integrate PKCE login in Flet; store refresh/access tokens through an audited OS secure storage extension, rotate/revoke/logout. Never embed a fixed bearer token or dev auth in release builds.
3. Persist scoped dog care history in PostgreSQL staging, enable WAL/backups and restore tests, server-side access controls per dog (already present for CRUD).
4. Implement owner-controlled sharing as expiring capabilities with revocation and detailed audit events; do not expose medical records through a permanently public QR.
5. Design export: owner requests a deterministic PDF/structured JSON record of caregiver observations and actual professional records, with provenance and consent.
6. Replace UI blocking HTTP calls with async transport, tests for poor connectivity and retries that do not duplicate posted events or tasks.
7. Add on-device accessibility and usability tests, documented release provenance, and deploy a closed Android pilot with volunteers.

**Exit criterion:** 10 consenting testers each create a dog, add and retrieve records across sessions, export their own passport, and no tested cross-account request exposes another dog's record. Production auth and DB migrations must run on deployed staging, not only in mocks.

## v0.4 (after vet/field validation)

- Licensed food label OCR with human confirmation; vet-reviewed source/approval workflow.
- Weather provider with timestamp and explicit offline states, not a false heat score.
- Breed model using commercially licensed representative Indian dog data and abstention evaluation.
- Opt-in real location and a provider-verified veterinary clinic directory.

## Non-negotiable production gates

See `docs/19_LAUNCH_GATES.md`, `docs/20_THREAT_MODEL.md`, and `docs/29_CLIENT_MILESTONE.md`. No unsupported diagnosis, no false food safety assurance, and no automatically public stray-dog coordinates.

<!-- Phase 3 Milestones: Production deployment and telemetry integration -->
