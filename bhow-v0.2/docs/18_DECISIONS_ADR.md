# 18 — Architecture Decision Records (ADRs)

## ADR-001: Combined Bhow x PAWPRINT, care OS first (Accepted)

**Context:** Bhow offers coherent dog-specific long-term profile; PAWPRINT offers mission breadth. **Decision:** Bhow working brand, one consumer care OS with optional welfare network later. **Tradeoff:** cannot advertise every welfare workflow at launch. **Revisit:** after owner pilot and partner agreement.

## ADR-002: Python-first via Flet (Provisional)

**Decision:** Flet client for Android-first preview; FastAPI for API, pure-Python domain, SQLAlchemy/Postgres. **Rationale:** maximize Python with one codebase, keep maintainable boundaries. **Risk:** Flet maturity/platform feature parity, specialist UI animation limits. **Exit condition:** device tests show unfixable UX issues; frontend may change while domain/API remain intact.

## ADR-003: Auth via external OIDC, not homemade OTP (Accepted)

**Decision:** validate JWT against issuer JWKS/audience/expiry; local dev header only explicit local environment. **Consequence:** must integrate native auth, logout and refresh; cannot declare user auth complete solely because bearer verification works.

## ADR-004: No autonomous veterinary outputs (Accepted)

**Decision:** model recognizes/extracts only; professionally approved KB + deterministic rules provide safety education; urgent care uses conservative human escalation. **Consequence:** several demo-style flashy features remain unavailable until review.

## ADR-005: SQLite local and Postgres hosted (Accepted)

**Decision:** SQLAlchemy sync session for early correctness, Alembic migrations from day one. PostGIS added when geospatial workflows are real. **Risk:** DB-specific migrations require PostgreSQL CI checks.

## ADR-006: Owner-only operations in 0.1, roles later (Accepted)

**Decision:** membership table exists, but invites and shared ownership are not exposed. **Why:** avoid shipping half-secure sharing. **Trigger:** user interviews show multi-caregiver demand.

## ADR-007: No unreviewed ‘safe’ food verdict (Accepted)

**Decision:** outputs only potential hazard/unknown. Starter KB marked not-vet-reviewed. **Consequence:** must run safety signoff to release a fully public scanner.

## ADR-008: Separate release and ML model cadences (Proposed)

**Decision:** version model artifacts and KB independently of UI; rollback individually. **Trigger:** first deployed ML service. **Requirement:** audit of training/license/professional approval.
