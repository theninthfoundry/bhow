# 19 — Public-launch checklist / no premature “production ready” claims

**Current readiness:** functional development API with tests, not approved to launch as a full consumer/veterinary application. “Passing tests” is not a legal, clinical, security or market certification.

## Technical readiness (blocking)

- [x] Versioned FastAPI `/v1` with Pydantic validation and OpenAPI.
- [x] Dog-level ownership checks and IDOR regression tests.
- [x] Database migration and starter CI definition.
- [x] API can reject missing auth and production misconfiguration.
- [ ] OIDC sign-in, native secure token storage, refresh, logout, account deletion at IDP.
- [ ] Rate limiting, abuse prevention and budget controls on public/AI endpoints.
- [ ] Centralized monitoring, incident response, encrypted backups and restore rehearsal.
- [ ] Dependency lock committed, SBOM, vulnerability and secret scanning, penetration test.
- [ ] Full hosted Postgres migration tests, zero-downtime release rollback, observability.
- [ ] Real device UX, all primary production screens, accessibility, locale and offline-state tests.

## Clinical/knowledge readiness (blocking for health features)

- [ ] Named licensed veterinary advisor under contract, with review record.
- [ ] Ingredient dictionary reviewed for scope, current sources, local applicability and emergency guidance; review expiration dates.
- [ ] No false-negative “safe” state; OCR confirmation; tests for common dangerous ingredients, synonyms and negations.
- [ ] Professionally reviewed red flags and emergency content localized to launch geography.
- [ ] Veterinary verification only via authenticated vet credentialed role and signed record action.
- [ ] Breed model held-out evaluation, labeled licensing, release card; no implied genetic proof.
- [ ] Weather risk advice clinically reviewed and source/freshness visible; actual provider commercial usage rights.

## Privacy/legal readiness (blocking)

- [ ] DPDP applicability review, clear privacy notice and consent/privacy-choice flows; grievance channel.
- [ ] Data retention, deletion, export of future assets, audit and vendor data processing agreements.
- [ ] Photo and location opt-ins separate from model-training opt-in; metadata stripping.
- [ ] No precise public rescue location; vetted moderation/partner agreement.
- [ ] Terms, disclaimers, trademark search for Bhow, India app-store and payment requirements.

## Business readiness (validation gates)

- [ ] At least 20 owner interviews and 3–5 vet interviews, documented synthesis.
- [ ] Closed beta with 20–50 dogs and actual follow-through measurements.
- [ ] Support pathway, clear refund/billing rules if paid, provider listing verification.
- [ ] Decision log for whether retention is good enough to expand features.

**Release rule:** No “health approved,” “24/7 emergency guaranteed,” “AI knows breed,” “toxin cleared,” or “GDPR/DPDP certified” marketing without evidence and legal review.
