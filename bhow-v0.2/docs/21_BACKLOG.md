# 21 — Engineer-ready implementation backlog

Tasks are in priority order. All work requires unit + API contract + security + accessibility acceptance where applicable.

| ID | Epic | Task | Done when | Depends |
|---|---|---|---|---|
| E-001 | Auth | Integrate real OIDC mobile flow | Sign in/out, token refresh, secure storage tested on Android | IDP choice |
| E-002 | Access | Role-based caregiver invites/revocation | Owner can invite/revoke; other caregiver gets scoped access; audit event | E-001 |
| E-003 | Documents | Private object store upload and AV pipeline | Checksum, content-type, size, EXIF and deletion validated | E-001 |
| E-004 | Care | Versioned correction events | Prior records linked, no hidden rewrite; source retained | E-002 |
| E-005 | Push | Outbox + worker + FCM | User-opt-in delivery, dedupe and retry tested | E-001 |
| E-006 | UX | Today screen | one next action + offline/unknown state + accessibility | Client shell |
| E-007 | UX | Passport records | timeline, upload, export, verification pill, shared scopes | E-003/004 |
| E-008 | KB | Clinical governance pipeline | reviewed items are signed, schema validated, can be disabled | Vet contract |
| E-009 | Food | OCR human-in-loop | misread words editable; no safe false-negative result | E-003/008 |
| E-010 | ML | Breed registry and ONNX inference | licensed dataset, card, calibrated abstention and out-of-domain test | ML training |
| E-011 | Weather | Real provider client with caching | source timestamp and failure state; no fake data | Weather license, vet |
| E-012 | Nearby | Verified directory | last-confirmed info, user contact action, correction process | Partner data |
| E-013 | Privacy | Full deletion orchestration | deletes records, images, tokens, analytics where applicable | E-001/003/005 |
| E-014 | Security | API limits and audit logs | quotas, sensitivity redaction and response workflow | Hosting |
| E-015 | UX | Gallery / accessibility | all component states and text scaling on target phones | Design |
| E-016 | Welfare | Organization-backed intake pilot | moderated report lifecycle with partner ack; location access control | Signed NGO agreement |
| E-017 | B2B | Vet provenance portal | clinician verified, signed attestation, revocation, audit | Pilot clinic |
| E-018 | Monetization | Plus subscription experiment | validated purchase intention and transparent payment lifecycle | Retention baseline |

Avoid parallelizing too many dependent tasks. Shipping three complete workflows is better than twelve partially working screens.
