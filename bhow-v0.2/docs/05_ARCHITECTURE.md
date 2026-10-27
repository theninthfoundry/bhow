# 05 — System architecture / Python-first, not complexity-first

## Principles

- Modular monolith before microservices. One deployable FastAPI API, one relational database, a separately scheduled worker when needed, private object storage after consent workflows are ready.
- The domain (`bhow_core`) has no FastAPI, ORM, HTTP or Flet dependency; its rules are cheap to test.
- `bhow_api` provides OAuth/JWT boundary, database ownership checks, validation, endpoints and future provider adapters. `bhow_kb` is a separately versioned source-controlled reference set.
- No generative model may decide toxicity, clinical urgency or vaccine schedule. Photos and OCR only detect/extract; vetted rules decide guidance.
- The API lies about nothing: unavailable integrations return 503, unverified data is flagged unverified, missing locations remain missing.

## Logical component diagram

```text
                       ┌──────────────────────────────┐
                       │ Flet client (Python / Flutter)│
                       │ secure tokens, accessibility  │
                       └─────────────┬────────────────┘
                                     │ HTTPS / OIDC
                         ┌───────────▼───────────────┐
                         │ FastAPI /v1               │
                         │ routes + Pydantic schemas │
                         │ owner/caregiver authz     │
                         └──┬────────┬──────────┬────┘
                            │        │          │
                     ┌──────▼───┐ ┌──▼──────┐ ┌─▼────────────┐
                     │ Core     │ │ KB      │ │ Integration  │
                     │ Rules    │ │ Sources │ │ Ports        │
                     └──────────┘ └─────────┘ └─┬────────────┘
                                                │
                     ┌──────────────────────────┼─────────────┐
                     │                     future services    │
                ┌────▼────────┐    ┌─────────▼────────┐ ┌──────▼─────┐
                │PostgreSQL   │    │Private storage   │ │Weather /   │
                │records+ACLs │    │photos/docs       │ │OCR / ONNX  │
                └─────────────┘    └──────────────────┘ └────────────┘
```

`Client → backend routes → authorization → DB/domain → API response`. Auth is verified at server, **not trusted from dog IDs or user-entered names**. Trusted third-party JWT issuer must be configured for deployment; see `src/bhow_api/security.py`.

## Technology choices

| Layer | Choice / rationale |
|---|---|
| App | Flet (Python-first) for functional preview and Android-first experiment; verify camera, accessibility and native feel on target devices |
| Backend | FastAPI + Pydantic v2 typed schemas, versioned REST/OpenAPI |
| Persistence | SQLAlchemy 2.0 + Alembic; SQLite for single-developer quickstart, PostgreSQL for deployment |
| Geo (later) | PostGIS only when service geospatial lookups need it; not a day-one dependency |
| Auth | Third-party OIDC JWT validation via JWKS; native mobile login UI and secure storage to be integrated |
| ML (later) | PyTorch training, vetted ONNX models for inference; explicit model-card + commercial license |
| Photos (later) | S3-compatible private storage + signed short-lived URLs + EXIF stripping, antivirus, retention |
| Reminders (later) | Transactional outbox in Postgres, dedicated idempotent worker, FCM/APNs provider adapter |
| Operations | Docker, CI, versioned migrations, telemetry with PII redaction, backups and incident runbooks |

## Critical internal invariants

1. `dog_id` never authorizes itself. A caregiver membership check precedes every read/write.
2. Only verified identity/provider workflows may write `verified=true`. Caregiver entries remain unverified.
3. Health notes and KB entries include evidence provenance and approved status; release blocks unreviewed safety guidance.
4. A failed network call must not be silently replaced with invented data.
5. Raw photos, tokens, exact location and user symptoms must not appear in application logs/analytics.
6. Time storage is UTC; user-facing times use user locale; date-only due tasks are calendar dates, not midnight UTC timestamps.
7. All files and media are private by default; access is revocable and auditable when implemented.

## Scale roadmap (not overengineering)

**0–5k care profiles:** single API instance, managed Postgres, offsite backup, basic rate limits/alerts, no search cluster. **5k–100k:** background worker, pgBouncer or equivalent pool tuning, object storage/CDN with signed access, selective caching of nonprivate KB, async model service if CPU-bound inference saturates API. **100k+:** separate costly inference, read replicas only after evidence, partition high-volume events, customer support tools, vet partner portal. Numbers are directional triggers, not capacity claims. Measure latency, concurrency and infra spend under load before rearchitecting.

## Accepted tradeoffs

- Sync SQLAlchemy in FastAPI threadpool for initial correctness and testability. Review async conversion only if measured I/O is a bottleneck.
- Android-first may simplify launch in India, but Flet/native camera behavior must be tested on real Android models.
- Preview client is not final design; interface remains swappable because business logic lives on backend.
- Hosted IDP avoids unsafe custom password/OTP implementation; adds vendor and network dependency.
