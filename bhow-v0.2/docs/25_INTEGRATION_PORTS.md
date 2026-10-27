# 25 — Provider contracts, implementation protocol and integration guardrails

Typed future provider interfaces live in `src/bhow_api/adapters/ports.py`; they are **not live adapters**. An unavailable integration should return 503 with an honest fallback, not synthetic values.

## WeatherProvider

`current(lat, lon) -> WeatherSnapshot(temp, humidity, observed_at, source, license_id)`; validate geospatial ranges, keep explicit stale-data TTL, distinguish nearest-station observations from forecast. Store coordinates only with consent and coarsen if possible. Revalidate breed/age-related advice with veterinarian; no pretend “safe walking hours.”

## BreedInferenceProvider

`predict(image_bytes) -> BreedPrediction[]`. Must enforce upload MIME, size, frame bounds, EXIF removal, commercial model rights, image-consent policy, dog presence/quality check, calibrated output and abstention. App never stores prediction as reported/verified breed without caregiver confirmation.

## PlaceDirectory

`nearby(...) -> VerifiedPlace[]`; a listing's last verification timestamp and emergency-care flag are mandatory (latter may be `unknown`). Paid place ranking must be disclosed and never influence urgent clinical recommendations. Keep phone numbers current.

## PrivateAssetStore

`presign_upload(...)`; production must use randomized opaque keys, short TTL, object-size limits, private bucket, server-side content verification and malware scanning; do not trust the upload callback alone. Delete includes signed links/caches and respects lawful retention. Current service has no upload endpoint.

## NotificationProvider

`send(destination_token, message, idempotency_key)`; transactions create outbox rows, worker claims in batches with leases/retry backoff and collision-safe dedupe. Store delivery receipts, opt-in, unsubscription and token invalidation; no claim that “sent” equals “received.” Current service has no push worker.

## Implementation acceptance

Every adapter needs contract tests with fake provider, failure injection (timeout, malformed JSON, license/HTTP errors), monitoring metrics, spending limits, privacy review, provider switch plan, and a source timestamp surfaced in UI. `last_known` weather must be labeled stale; do not use previous values as if live.
