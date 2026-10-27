# 13 — Quality engineering and end-to-end test strategy

## Test pyramid

**Pure domain unit tests:** hazards never return `safe`; exact-token matches resist substring false positives; reminder dates have consistent calendar semantics; low-confidence breed classification abstains. Add Hypothesis fuzz tests for Unicode input, punctuation, long text, boundary dates and pathological score values.

**Database integration:** SQLite for fast CI plus nightly PostgreSQL migrations/constraints/transaction isolation tests. Test upgrading all historical versions, foreign keys and cascade deletion, concurrent task completion, unauthorized membership, account export scope.

**HTTP/API integration:** required auth, object authorization on every route, Pydantic edge cases, 404 to hide existence, malformed UUIDs, payload size, 503 integration semantics, JWKS expired/mismatched tokens, CORS and rate limits (once installed).

**Mobile E2E:** Android device matrix across screen size, camera permission denied/granted, data-loss prevention, font scaling, talkback, offline state, high contrast, every safety CTA visible without surprise animation. Flet package process must be tested on real hardware—not just desktop preview.

**Security:** OWASP API Top 10, IDOR enumeration, large payloads, upload decompression bombs, signed URL expiry, privilege escalation into vet verification, SSRF from user-submitted URLs, dependency CVEs, lost devices, revocation.

## Release quality bar

- All blocking tests green on PR and in target database.
- Domain changes require meaningful unit coverage; test failures should reproduce documented real bug scenarios.
- Ruff lint + strict MyPy pure-domain modules in CI; run Ruff formatter before each PR; import-layer boundaries tracked. Dependency lock + vulnerability scan as a release prerequisite.
- p95 latency target **hypothesis**: <300ms for simple cached/no-inference endpoints in staging; set real SLO after measurement. AI inference separate latency budget.
- Load test 100 concurrent authenticated tasks before public release; these are tests to run, not claims of achieved capacity.
- Migration rehearsal on anonymized production-like data + tested restore to backup snapshot.

## Failure injection list

1. Invalid/expired bearer. 2. Another user's UUID. 3. Long text containing unexpected Unicode. 4. Dog deleted during pending reminder. 5. Replayed task completion. 6. Weather provider times out. 7. Poison ingredient omitted from OCR. 8. Model predicts confidently for a non-dog image. 9. Vet verification revocation. 10. User requests erasure during photo processing. 11. Rescue partner never responds. 12. Network drops during offline journal save.

## CI pipeline delivered

See `.github/workflows/ci.yml` for lint, tests, migration upgrade/downgrade and bytecode compilation. **Not delivered:** SAST/secret scan/SBOM/DAST, actual Android matrix, dependency pinning/lock, Postgres CI service, perf test automation. These are listed as release blockers rather than presented as completed work.
