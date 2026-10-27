# 29 — Phase 2 / Functional Flet care journal

**Delivered scope:** functional implementation source with live FastAPI endpoints; **not** a verified Flet installation or Android release. Flet package could not be fetched in the build environment. Device validation is an explicit gate.

## Experience map

```text
Welcome / no dogs
  -> Create a profile (name + owned/foster/community)
  -> Today [first pending reminder / counts / quick observation]
     |-> New reminder [name, type, local due date via picker]
     |-> Mark reminder complete
  -> Passport [caregiver notes and pending/completed reminders]
     |-> Add observation [visit, symptom, weight, etc.]
  -> Check [ingredient text, consumed toggle, hazard-or-unknown]
  -> Explore [offline outdoor precautions / future features clearly labeled]
  -> Help Now [always accessible, urgent-care signpost; no fake clinic]
  -> Dog switcher [+ add additional dog]
```

## Backend data flow (complete)

- `GET /v1/dogs` -> select active dog (all membership-scoped).
- `GET /v1/dogs/{uuid}/overview?tz=Asia/Kolkata` -> recent caregiver events and up to five pending tasks, count of all pending/overdue tasks. There is no inferred health/wellbeing score; caregiver-entered dates are not personalized medical recommendations.
- `POST /v1/dogs/{uuid}/tasks` -> create manually selected due date; `POST /.../complete` -> mark complete; immediate re-render from backend.
- `POST /v1/dogs/{uuid}/events` -> append observation; backend assigns `source=caregiver`, `verified=false`, `created_by` from authorized subject.
- `POST /v1/food/check` -> hazard flags or unknown; unknown never displayed as safe.
- `GET /v1/outdoor/advice` -> offline tips with `based_on_live_weather=false`.
- Breed, nearby clinics and live weather still return explicit unavailable responses.

## Components implemented

- Bold editorial welcome with minimal required information; no mandatory dog photo/location.
- Four-destination bottom navigation; dog switcher; Help Now; constrained 720px content width.
- Warm paper / ink / turmeric tokens; high-contrast information hierarchy.
- Bottom-sheet forms for new dogs, reminders and observations; date picker; empty and error states.
- Honest `Caregiver entry · not vet verified` provenance labels.

## Manual acceptance checklist (pending physical-device execution)

- [ ] Flet 0.80.x launches on Windows, Android emulator and physical Android.
- [ ] Zero-dog welcome -> create -> Today -> new reminder -> completion -> Passport.
- [ ] Phone keyboard does not obscure inputs; date picker reliably returns to task sheet.
- [ ] Navigation operates with back button, magnified text and TalkBack.
- [ ] Changing to dog B never briefly reveals dog A's passport, even with slow network.
- [ ] Connectivity loss -> retry; timeout; unauthorized session; reauthentication UX.
- [ ] Wide screens and 320px narrow screens; dark theme, reduced-motion options.
- [ ] Confirm colors, touch targets, contrast and text scaling with Flet rendered UI.
- [ ] No network requests include bearer tokens over plain HTTP.

## Technical debt / next milestone

1. Replace temporary `BH_ACCESS_TOKEN` support with a real mobile OIDC PKCE provider login, refresh rotation, and platform secure keystore; hide the local demo identity outside localhost.
2. Switch synchronous requests off the main UI thread; adopt explicit loading/error/success transitions and cancellation.
3. Device-tested typography/fonts, accessible semantic roles, system back handling, offline cache for read-only care passport and controlled background refresh.
4. Rich care export and consented photo/document upload with private S3, EXIF stripping, scanning, deletion.
5. Pagination/cursors for events/tasks and rate limiting for expensive endpoints before public launch.
6. Clinically review content and implement the vet approval workflow before any individualized health recommendation.
7. Rehearse load and reliability tests with PostgreSQL and a real deployment.

## Proof collected

- Backend and view-model tests: `pytest -q`.
- UI syntax: `python -m compileall -q client`.
- OpenAPI generated from live `FastAPI.app.openapi()`.
- Backend initial Alembic schema supports new overview without modification.
- Flet UI rendering was **not** verified because dependency downloads were unavailable.

## Why we picked this slice

Caregivers must first trust that the app remembers real facts. Breed recognition, maps, real-time weather and nutrition ML are differentiation candidates that should be released only after licensing, consent, integration and clinical review. This slice proves the central retention loop before adding risky intelligence or marketplace complexity.
