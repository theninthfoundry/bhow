# 12 — Build playbook / milestones, sequencing, staffing

No timeline guarantees; ranges are engineering planning envelopes assuming one capable full-stack developer, an available veterinarian and access to test participants. External credentials/licensing/review can dominate elapsed time. Each milestone has a runnable demonstration, tests, acceptance criteria and rollback path.

## Milestone 0 — engineering foundation (delivered in this kit)

Backend package; FastAPI and typed schemas; migration; object-ownership authorization; dog profiles; care timeline; care tasks; local demo UI; food educational preview; CI/test starter; core business, safety, UX docs. Definition of done: tests pass, migration upgrade/downgrade rehearsed, no default production bypass.

## Milestone 1 — polish trusted care records (next)

- Native OIDC sign-in (no home-built OTP) and secure local credential storage.
- Consent UX, roles and per-dog access invitation with explicit revoke.
- Passport document handling: S3-compatible private storage, malware and image validation, EXIF stripping, retention, upload audit.
- Real push: idempotent scheduled jobs, opt-in, deduplication, error retry/backoff, device tokens.
- Vet-visit print/export layout and real UI components for timeline/tasks; accessibility test pass.
- Monitoring and backup restore validation; dependency vulnerabilities CI.

**Done when:** 10 moderated users can add/find care events and reminders; cross-account access always denied; deletions and export include all data introduced in this milestone; a scheduled push is actually delivered and recorded.

## Milestone 2 — safe intelligence and useful daily context

- Food-label OCR with explicit confirmation; vet-approved, versioned knowledge entries; safety regression suite.
- Live weather/AQI provider with appropriate license, outage states and validated regional care copy.
- Breed recognition prototype → commercial rights clearance → dog-disjoint test set → calibrated ONNX deployment with abstain.
- Verified clinics directory (source/last checked, emergency capability not guessed).

**Done when:** independent evaluation is published internally, no clinical claims exceed evidence, disabled models remain disabled under deployment failure.

## Milestone 3 — launch-grade Flet experience

- Screen-level UI implementation: Today, Passport, Check, Explore, Help, profile switcher.
- Components gallery, interaction state docs, safe image cropping, actual font licenses, reduced motion, physical-device E2E and offline behavior.
- Telemetry event taxonomy with privacy constraints and cohort dashboards.
- Support workflows, account rights and incident drills.

**Done when:** performance, accessibility, translations and navigation success criteria are observed on representative Android hardware; app-store policy requirements reviewed.

## Milestone 4 — controlled welfare pilot

- Partner agreement with response hours, moderation, escalation, responsible contact and outcome definitions.
- Separate org role model, private location handling, anonymized public impact stats, abuse reporting.
- Closed pilot with one to two partners; measure response success and complaints before public launch.

## Milestone 5 — revenue experiments

- Test Plus with offer pages and interviews before billing integration.
- One clinic workflow paid-pilot negotiation, then permissioned provider portal if validated.
- Pricing/B2B experiments separate from emergency guidance. Analytics cannot turn medical advice into marketing targeting.

## Workstream ownership (initial)

| Workstream | Responsible | External dependency |
|---|---|---|
| API, DB, tests, deployments | Python/backend lead | Cloud/IDP contracts |
| UI/UX/accessibility | Product design + Flet developer | Device testing, licensed fonts |
| Veterinary content | Qualified veterinarian | Written scope, approval SLA |
| Breed/vision | ML engineer | Commercially cleared datasets |
| Welfare relationships | Local operations lead | Shelter/NGO commitments |
| Privacy/security | Founder + counsel/reviewer | Vendor contracts, audit |

## Week-one order

Day 1: run migrations and full tests; verify deployed production config rejects local bypass. Day 2: conduct 3 pet-parent interviews; map existing care record journey. Day 3: implement Today and Passport screens against real API. Day 4: add logout and IDP integration discovery; design share/revoke. Day 5: harden migration and export behaviors, review with veterinary advisor. Day 6–7: build first usability prototype, gather evidence and update roadmap. Treat as agenda, not promised delivery speed.
