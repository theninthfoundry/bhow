# 02 — Feature architecture and ruthless prioritization

## The product should feel like one dog, one story, one next action

Avoid a dashboard with 15 unrelated modules. Everything shares `Dog -> Care events -> Care tasks -> Evidence provenance -> Controlled sharing`.

| Capability | User value | Release | Status | Evidence needed |
|---|---|---|---|---|
| Living dog identity | Essential personalization | M0 | API functional | Observe onboarding |
| Care timeline | Records survive time and changes | M0 | API functional | Vet workflow research |
| User-created reminders | Never lose next visit date | M0 | API functional; no push | Push preference testing |
| Food ingredient text warnings | Avoid false certainty | M0 preview | Limited preview | Vet review, coverage |
| Offline heat awareness | Practical education | M0 | Working educational endpoint | Regional clinical review |
| App UI / dog profile | Premium emotional connection | M0 preview | Python UI sample | 10 usability tests |
| Health passport export | Handoff to clinician | M1 | JSON export functional | PDF/QR, consent design |
| Vet-verified records | Trust/provenance | M2 | Schema field only | Vet identity + signature |
| Photo food OCR | Faster label entry | M2 | Planned | OCR false-negative tests |
| Breed resemblance model | Shareable acquisition | M2 | Adapter unavailable | Commercial model + labels |
| Live walk weather | Daily decision aid | M2 | Adapter unavailable | Licensed feed + clinician |
| Push reminders | Timely next action | M1 | Planned | Opt-in + idempotency |
| Nearby clinics | Actual access to help | M2 | Adapter unavailable | Verified directory |
| Shared family care | Multi-person workflows | M3 | Schema foundation | Fine-grained roles |
| Rescue case management | Social impact with operators | M4 | Planned | NGO operational SLA |
| Lost dog human-reviewed sightings | Support retrieval | M4 | Planned | Abuse + fraud controls |
| Vet practice companion | B2B business model | M5 | Planned | Paid clinic pilot |

### `Help` must never imply a rescue promise

Initially, a safety-first information panel and local emergency resource pathway. Activate case-report submission ONLY after an organization consents to the exact workflow, capacity, escalation and moderation. Always show receipt vs accepted vs actioned vs resolved as separate states.

### Three differentiated signature experiences

1. **The Living Portrait:** dog's *real, consented photo*, one expressive editorial headline, and small evidence labels. Never guess breed from photo as fact.
2. **Field Notes:** change-over-time journal with source chips (`You noted`, `Vet verified`, `Unknown`) and only one highlighted next action.
3. **The Quiet Passport:** a shareable, expiring view of explicitly selected items; public QR contains no private payload. Not a fake official certificate.

### Design-to-business fit

Discovery creates the first session. Passport creates continuity. Responsible reminders produce repeated value. Vet-ready summary leads to partnership discovery. Community support creates optional mission expansion rather than polluting the primary user journey.
