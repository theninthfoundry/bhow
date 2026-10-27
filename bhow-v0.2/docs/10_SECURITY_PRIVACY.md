# 10 — Security, privacy and data governance

## Data inventory / explicit purpose

| Data | Purpose | Sensitivity | Default |
|---|---|---|---|
| IDP issuer subject | Authorization | Personal pseudonymous identifier | Required for authenticated care |
| Dog name, age, weight, notes | Personalized records | May reveal owner/private context | Private |
| Dog photographs | Profile / optional ML | Can reveal home, faces, GPS metadata | Not collected in starter |
| Location | Weather, nearby help | Sensitive when precise + repeated | Opt-in / coarse by default |
| Veterinary documents | Record continuity | Sensitive personal context | Not collected in starter |
| Rescue reports | Partner response | Can endanger people/animals if public | Not implemented / must be private |
| Model training consent | Optional improvement | Different purpose from inference | Off by default |

## Security boundaries in delivered code

- JWT authentication: RS256, token expiry, issuer and audience validated via configured JWKS. No self-issued dev tokens for production.
- `X-Dev-User` is accepted **only** in explicit `BH_APP_ENV=local` and `BH_ALLOW_DEV_AUTH=true`, never staging/production.
- Every dog fetch/update/delete/care endpoint verifies `dog_caregivers.subject` access. Cross-user lookup responds 404. Tests cover IDOR.
- SQLAlchemy ORM parameterizes queries; Pydantic validation enforces bounds. API responses are typed and avoid sending raw ORM objects with unfiltered private fields.
- CORS in staging/prod forbids wildcard and localhost; production must terminate TLS securely and protect forwarded headers at the trusted ingress.
- Private media, upload scanning and signed URLs are planned, not present. Never claim full security/compliance certification for this starter.
- `.env` ignored; no secret committed. Host must use secret manager and secret rotation policy.

## Production controls still required (blocking)

A managed identity-provider integration with mobile flow, refresh/revocation and secure token store; independent security review; vulnerability/dependency scanning with SBOM; brute-force/rate limiting especially on costly scan endpoints; security event logs with PII redaction; WAF and restrictive upload policy; daily encrypted backups plus restore drill; leak response process; centralized audit trail; deletion propagation; data processing/vendor contracts; incident on-call; tested disaster recovery; data-subject requests and consent UX.

## India DPDP context

India's 2025 DPDP Rules were notified in November 2025, and obligations have phased commencement. Consult the latest official MeitY rules and applicable Gazette notifications at launch; do not treat the product spec as legal advice. Implement purpose limitation, clear notices, appropriate lawful basis/consent, data minimization, rights handling, retention, grievance workflow, vendor/subprocessor inventory and data transfers with qualified India counsel.

- Official documents: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025%3B
- Official government announcement: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014&lang=1&reg=3

## Media and location privacy (future)

Never place full GPS, personal phone numbers, veterinary histories or home locations in public QR tokens or on open rescue maps. Consent for photo use in feature ≠ consent for training or marketing. Strip EXIF, default photo visibility private, encrypt at rest in managed store, short-lived signed URLs, cache eviction and delete-on-revoke. Rescue partner should receive precise coordinates privately only if necessary and within a defined service agreement.

## Account deletion caveat

`DELETE /v1/account/me` deletes only the current MVP's solely-owned local records. It is **not** a production-complete data-erasure workflow: external IDP users, queued notifications, partner records, object storage and backups require dedicated orchestration and retention treatment. Do not expose it as a full compliance promise before that orchestration is built.

<!-- Data encryption at rest and transit guidelines -->
