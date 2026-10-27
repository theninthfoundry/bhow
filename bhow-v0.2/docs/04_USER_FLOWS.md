# 04 — End-to-end user journeys / acceptance states

## A. First run / from interest to value

`Welcome → choose caretaker context (owned/foster/community) → dog name → optional age/weight/breed (unknown accepted) → first useful action (record visit, add task, check food) → Today.`

Avoid onboarding friction. Permissions for location, photos and push are contextual, never preemptively demanded. If skipped, show accurate empty-state behavior and allow access to profile and care records. A first-time pet parent should reach a meaningful record in under 3 minutes as a usability goal.

## B. Log vaccine/appointment

`Passport → Add record → kind + event date + description → shows “Added by you · unverified” → add next due date manually → Upcoming task → Complete after visit.`

**Critical:** a caregiver may attach a clinic document later, but an upload is not vet verification. Do not invent schedules automatically. When a vet verifies, a distinct provider-authenticated action signs the event; ordinary accounts cannot mark events verified.

## C. Food check

`Check → Ingredient text → Confirm actual text → classify using reviewed KB → potential hazard or unknown → human next step → source and review status.`

If a possible poisoning occurred, prominent professional contact guidance, no dosage “safe amount,” no 100%-safe state. If OCR is later added, highlight uncertain text for review. If offline or KB unavailable, abstain rather than guess.

## D. Breed insight (later)

`Photo permission → subject dog in frame → image quality check → licensed model → calibrated candidates / abstain → interpret as visual similarity → user can reject it → never overwrite manually reported breed.`

No external photo storage without consent. Distinguish confidence in *classifier label* from confidence in ancestry. Require consent for dataset reuse separate from inference.

## E. Share passport (later)

`Passport → Share → select exact records → choose recipient/expiry → generate opaque token → copy QR/link → viewer sees only selected fields + provenance → revoke at any moment → audit access.`

The current API only supports owner-authenticated JSON export. No public QR endpoint ships in 0.1; never put sensitive data directly into QR strings.

## F. Rescue assistance (later; operations-first)

`Help community dog → can I safely observe? → description + approximate location + optional photo → show “submitted” → moderated screening → partner acknowledgement → partner action → verified resolution / closed unconfirmed.`

No automatic broadcast of precise location, volunteer assignment, or promise that help is dispatched. A partner must accept responsibility for a case; prioritize safety of humans/dogs and protection from abuse.

## Error paths / essential fallbacks

| Scenario | Correct behavior |
|---|---|
| Weak/no network | Draft locally if encrypted offline capability exists; otherwise show no-save state, never imply saved |
| Food OCR uncertain | Require human confirmation, do not classify a hallucinated ingredient |
| Unknown ingredient | `Unknown` and professional next step, never `Safe` |
| Breed low confidence | Abstain and explain limitation |
| Weather feed down | Offline general precautions, no fake time window |
| Clinic hours stale | Show last verified timestamp and call to confirm |
| User has no photo | Typography/initials profile is complete and usable |
| Caregiver unauthorized | 404 and no unauthorized metadata |
| Consent revoked | Stop processing, purge eligible data per retention/deletion policy |
