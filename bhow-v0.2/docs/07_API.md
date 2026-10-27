# 07 — Versioned REST contract / live starter endpoints

**Base:** `/v1`. **HTTP:** JSON. **Identity:** production `Authorization: Bearer <OIDC RS256 JWT>`; local development only `X-Dev-User: founder` with explicitly opted-in settings. **OpenAPI:** `/openapi.json`, Swagger UI `/docs` only in local/test. All dog IDs are UUIDs; unauthorized dog objects respond 404.

| Method | Route | Status | Notes |
|---|---|---:|---|
| GET | `/healthz` | 200 | Process liveness; not full provider readiness |
| GET | `/v1/account/me` | 200 | Authenticated external subject |
| GET | `/v1/account/export` | 200 | JSON dog/events/tasks; MVP-only |
| DELETE | `/v1/account/me` | 204 | Delete solely owned MVP records; shared conflicts return 409 |
| POST | `/v1/dogs` | 201 | New dog + owner membership |
| GET | `/v1/dogs?limit=50` | 200 | Authenticated subject's dogs, max 100 |
| GET | `/v1/dogs/{dog_id}` | 200/404 | Membership check |
| GET | `/v1/dogs/{dog_id}/overview` | 200/404 | Own dog only; timezone-aware due dates via `tz=Asia/Kolkata`, manual tasks, recent caregiver events |
| PATCH | `/v1/dogs/{dog_id}` | 200/404 | Name, reported breed, weight |
| DELETE | `/v1/dogs/{dog_id}` | 204 | Guard shared profiles |
| POST | `/v1/dogs/{dog_id}/events` | 201 | Append caregiver entry, always unverified |
| GET | `/v1/dogs/{dog_id}/events` | 200 | Chronological limited list |
| POST | `/v1/dogs/{dog_id}/tasks` | 201 | Manually supplied due date |
| GET | `/v1/dogs/{dog_id}/tasks` | 200 | Due-date sorted |
| POST | `/v1/dogs/{dog_id}/tasks/{task_id}/complete` | 200 | Idempotently mark complete |
| POST | `/v1/food/check` | 200 | Potential hazard or unknown; never `safe` |
| GET | `/v1/outdoor/advice` | 200 | Offline precautions, explicitly not live |
| POST | `/v1/integrations/breed/estimate` | 503 | Model not deployed |
| GET | `/v1/integrations/places/nearby` | 503 | Verified directory unavailable |
| GET | `/v1/integrations/weather/live` | 503 | Weather feed unavailable |

## Example: create a dog and care task

```http
POST /v1/dogs
Content-Type: application/json
Authorization: Bearer <valid-token>

{"name":"Kaju","care_context":"foster","estimated_age_months":18}
```

The response includes `id`, `created_at`, and only fields supported by the model. Then:

```http
POST /v1/dogs/{dog_id}/tasks
Content-Type: application/json
Authorization: Bearer <valid-token>

{"kind":"appointment","title":"Discuss care plan with vet","due_on":"2026-12-02"}
```

## Planned API endpoints (design only, MUST NOT assume implemented)

`POST /v1/assets/presign` / `POST /v1/assets/complete` (content-type verification, quarantine), `POST /v1/breed/estimate` (licensed ONNX adapter, consent, bounded file), `GET /v1/weather/outdoor-window` (licensed weather, location accuracy and source timestamp), `POST /v1/share-grants` / `DELETE /v1/share-grants/{id}`, `POST /v1/notifications/devices`, `POST /v1/vet/attestations`, `POST /v1/community/reports`, `GET /v1/community/reports/{id}` (partner ACL). Use idempotency keys for POST calls creating external side effects.

## Consistent response/error conventions

- 400 malformed local identity; 401 missing/invalid bearer; 403 allowed identity but forbidden action (where no existence leak); 404 unavailable resource in member-specific namespace; 409 shared delete conflict; 422 request validation; 429 future rate limiting; 503 disabled integration or unconfigured IDP.
- Future standard error envelope: `{code, message, request_id, retryable, documentation_url}`; current FastAPI validation uses standard error schema.
- Server response uses UTC-aware datetimes for instants and ISO-8601 local *date* for due tasks.
- Do not log full request bodies for `/food/check`, `/dogs/*/events`, assets or location.
- Pagination v2: keyset cursor and stable sort rather than offset on high-volume timeline.

Generate client contracts from `openapi.json` with CI and schema-diff checks once teams split. Never hand-maintain a contradictory API list; this document is explanatory, code-generated schema is authoritative for implemented operations.

<!-- API response contracts synced with OpenAPI spec -->
