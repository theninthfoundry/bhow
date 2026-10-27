# 23 — Precise developer-agent prompts (one milestone at a time)

> Use with a coding agent in this repository. Start with `README.md`, `docs/01_PRD.md`, `docs/05_ARCHITECTURE.md`, `docs/09_VETERINARY_SAFETY.md`, and `docs/10_SECURITY_PRIVACY.md`. **Do not hallucinate that missing integrations are done.**

## Prompt A — Core audit

"Inspect every Python module, Alembic revision, FastAPI route and test. Identify security/quality flaws with file and line references, then fix issues in small commits. Maintain object-level authorization; no endpoint may mark caregiver reports vet-verified. Run pytest, ruff, mypy and migration upgrade/downgrade against SQLite and Postgres. Add failing tests for each bug before fixing. Keep API schemas and docs in sync. Summarize verified results and unmet blockers; never say 100% secure."

## Prompt B — Complete beautiful Passport + Today UI (Python/Flet)

"Implement the design tokens and components in docs/03_UI_UX.md as reusable Python Flet code, using no stock or AI images. Build Today, Passport, profile switcher and add-event/task flows connected to actual FastAPI endpoints. Display source/verification labels and unavailable states accurately. Support phone size, screen-reader order, text scaling, reduced motion and meaningful empty/loading/error/offline states. No fake medical data. Add physical-device test checklist and UI integration tests. Do not overwrite backend domain logic."

## Prompt C — Production auth and sharing

"Implement a selected identity provider's OIDC authorization-code + PKCE flow with secure platform token storage, refresh/logout/revocation and backend RS256 verification. Add caregiver invitation and revocation with scoped membership, audit log, signed invitations and replay protection. Enforce authorization on all nested routes; write IDOR and expiry tests. Remove any dev-auth access from staging and prod. Publish an ADR and updated data-flow diagram."

## Prompt D — Vet-ready records and reminders

"Add private document storage and confirm-before-save OCR with verified file type, size, malware/quarantine, stripped EXIF, signed expiring URLs and complete erasure. Implement transactional outbox and idempotent push worker with delivery state. No automatic vaccine prescriptions. Make export include files' metadata and user-confirmed history with clear provenance, and run deletion propagation tests."

## Prompt E — Food scanner and clinical review

"Build a reviewed versioned veterinary KB workflow with source, region, reviewer credential, approval date and tests. Add label OCR whose output is editable and untrusted. Never return 'safe' from missing hazard; no dosage calculator; route suspected poisoning to professional assistance. Require vet-approved content before public release. Include confusion matrix from test corpus of Indian labels/food names and explicit unresolved limitations."

## Prompt F — Calibrated breed recognition

"Create a commercially licensed dog-disjoint dataset ledger including Indian breeds/mixes, train a lightweight vision backbone, export ONNX and implement a model adapter. Measure calibration, top-k, subgroup errors, OOD behavior and abstention. Return 'appearance resemblance' with explicit uncertainty, never ancestry. Store consent separately from optional model training. Include signed model card, latency and rollback controls; keep endpoint 503 until all gates pass."

## Prompt G — Welfare pilot

"Do not create an open public incident feed. Start from a signed partner operational agreement, define moderated case transitions, reports of abuse, coarse public location/private exact location, audited partner handoff, last-seen verification and non-response behavior. Implement server-side org permissions and case authorization tests, then a closed UI test with partner signoff."

## Prompt H — Launch audit

"Read docs/19_LAUNCH_GATES.md and check every box with evidence: test reports, licensing/professional signoff, accessibility recordings, security assessments, privacy policy, real vendor integration, backup restoration and user research outcomes. Mark outstanding items explicitly; do not claim deployability without deployed proof."
