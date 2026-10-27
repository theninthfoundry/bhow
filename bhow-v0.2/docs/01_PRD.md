# 01 — Product requirements document (PRD) / BHOW

**Revision:** 0.2. **Status:** proposed product intent; scope frozen for MVP, pending user research. **Primary market hypothesis:** first-time pet parents and everyday dog caregivers in Hyderabad; purposefully allow indie, foster and community-dog contexts, even with incomplete details.

## Problem, not features

Today, knowledge about an individual dog is fractured across paper vaccine slips, photographs, messages from clinics, pet-food packaging, reminder apps and memory. People struggle to know what records are reliable, what care action is due, what changed recently, and where they can seek verified help. AI breed labels are fun, but do not solve continuity of care. Bhow's central job: **preserve a dog's care context and turn it into one credible next action**. User insight and willingness to pay remain hypotheses until interviews and pilots.

## Positioning

- Category: dog care operating system / canine care record companion.
- Brand promise: **“Every dog has a story. Every day deserves better care.”**
- Competitive wedge: lifetime living record + provenance (caregiver vs vet) + easy appointment preparation, paired with a premium daily experience. India-aware design is a research priority, not an excuse for unvalidated health claims.
- Product architecture: consumer care OS first; B2B clinic handoff and moderated animal welfare later.

## Jobs to be done

| User / situation | Job | What success looks like |
|---|---|---|
| First-time pet parent | Know what to record and ask at next vet visit | Profile + care reminder + doctor-ready summary |
| Working dog parent | Share care between family members | Permissioned, accurate handoff (Phase 2) |
| Indie caregiver | Track a dog when exact age/breed is unknown | Complete useful record with incomplete fields |
| Owner facing uncertain food label | Identify a possible hazard and find a safe next action | Correct escalation without false reassurance |
| Foster/rescuer | Preserve health and care history when a dog changes homes | Verified and unverified events remain distinguishable |
| Veterinarian (later) | Receive a concise, trustworthy history | Opt-in, provenance-aware export, no unverified diagnosis |

## North-star and counter-metrics

**North-star hypothesis:** active dogs with at least one *meaningful, voluntarily recorded or completed care action* over a rolling 28-day period. Anti-goal: inflated DAU through irrelevant push notifications. Safety guardrail: zero known urgent-risk responses that incorrectly reassure users; failures trigger a stop-ship and review. Secondary outcomes: verified record completeness, reminder follow-through, time to retrieve vet summary, repeat usage, cost per active dog.

## Functional requirements: release 0.1

- **FR-01 Identity:** a trusted auth subject; dog records are visible only to authorized caregivers. Initial subject is an external OIDC token on hosted environments; no email/phone collection required in our DB.
- **FR-02 Profiles:** dog name mandatory; date of birth *or* estimated months optional; weight optional; breed may be reported, never silently inferred; context owned/foster/community; multi-dog support.
- **FR-03 Care record:** append-only dated caregiver observations; source + verified flag not controlled by ordinary users; chronological retrieval and JSON export.
- **FR-04 Care tasks:** caregiver-defined reminder dates and completion; no automatically prescribed vaccine intervals.
- **FR-05 Food:** accept ingredient text; flag a short, cited sample set of hazards; return `unknown` if unmatched, never `safe`; real camera OCR and release approval require further work.
- **FR-06 Outdoor:** offline educational advice explicitly labeled not live; live weather only after provider + clinical rule review.
- **FR-07 Data rights:** initial JSON export and account-record deletion; shared profiles require controlled revocation flow before rollout.
- **FR-08 Accessibility/quality:** readable contrast, labels independent of color, accessible motion alternatives, localization-ready copy, full validation.

## Release 0.2 / pilot features (not done)

- Real OIDC mobile sign-in UX, secure credential storage, consent preferences and per-dog family invites.
- Document upload to private object storage, AV scanning and confirm-before-save OCR.
- Scheduled notification worker with idempotency, push provider and delivery receipts.
- A verified partner directory with source timestamps, 24-hour emergency availability *only when proven*.
- Licensed weather/AQI provider and vet-reviewed personalized guidance; graceful missing-data state.
- Commercially licensed visual breed model with calibrated abstention and Indian breed coverage.
- UX implementation of Passport, Today, Discover and controlled share cards.

## Explicit exclusions

No photo diagnosis, medically prescriptive meal generator, feeding toxic-dose calculator, biometric dog identity proof, public precise rescue map, social feed, giant marketplace, guaranteed rescue dispatch, or monetizing identifiable health history. None of these can become implicit requirements during MVP.

## Typical user story + acceptance criteria

**“When I add my dog, I can record a next appointment and read it back safely.”**

GIVEN an authenticated caregiver, WHEN they create a dog and task, THEN both persist, use server-generated IDs and appear in list/export. GIVEN another caregiver, WHEN they request that dog by ID, THEN they get 404, not a leaked record. GIVEN an unrecognized ingredient, WHEN they check it, THEN result is `unknown` and explicitly not safe. GIVEN no real weather provider, WHEN they request live weather, THEN they see unavailable, not a made-up forecast.

## Quantitative release gates (initial targets, not forecasts)

- Profile completion can be finished in <= 3 min in moderated testing with at least 10 participants.
- >= 90% of moderated users can find their next care task without guidance.
- All authorization tests (including IDOR) pass before every release; no knowingly unresolved critical findings.
- Every safety-related factual content item has source, reviewer, applicable region, and review date **before clinical release**.
- Model release requires pre-registered representative test set, calibration and abstention threshold; outcome targets defined with veterinary/ML advisors.

## Open questions for evidence gathering

Are reminders or record retrieval the painful problem? Who maintains records after a vet visit? Is food scanning repeated enough to matter? Do caregivers trust a QR passport? Which clinics would accept an electronic summary? Would users pay for family collaboration or storage? What local animal welfare organization will accept cases? Until answered, pricing, retention, and commercial scalability are experiments, not facts.

<!-- Product scope alignment verified -->
