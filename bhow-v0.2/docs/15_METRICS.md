# 15 — Product analytics instrumentation without surveillance

## Event taxonomy (planned, not currently wired)

Naming format `entity_action_v1` with anonymous event ID and session ID, server dedupe and opt-out semantics. Do NOT attach health free-text, food ingredient strings, exact geolocation, full dog profile or image content to product analytics.

| Event | Success definition | Legitimate fields |
|---|---|---|
| `dog_created_v1` | DB commit complete | care context, optional-fields-completed count |
| `care_event_created_v1` | Stored timeline entry | kind, unverified vs verified (not content) |
| `care_task_completed_v1` | Transition to completed | task kind, days late (bucketed) |
| `food_check_completed_v1` | Result rendered | potential_hazard/unknown, KB version |
| `export_requested_v1` | Export delivered | count buckets, time to completion |
| `model_abstained_v1` | Model declined to label | model version, confidence bin (only with consent) |
| `weather_data_unavailable_v1` | User sees absence | provider/error class, not precise lat/lon |
| `clinic_contact_tapped_v1` | Initiated call/link | directory quality tier, not private phone |
| `welfare_case_accepted_v1` | Partner explicitly accepted | region bucket, partner class |

## Core funnel

Install/start → first profile → first care action → reminder created → reminder acted upon → exported/used with vet → retained after 28 days. Differentiate time to first value from merely completing onboarding. Keep partner/rescue cohort separate from household pets; their usage patterns differ.

## Safety and trust dashboard

- Potential hazard false-negative reports, content review overdue, missing-vet-signoff, model false-confidence, unauthorized access failures, stale place listings, incident count and remediation time.
- **North-star metric is subordinate to safety.** Growth is not permission to ship clinically unsafe outputs.
- Do not create emotional-pressure streaks that guilt owners when a pet is sick, or use data for discriminatory pricing.

## Experiment design

A/B test only nonclinical UX such as onboarding order or passport layout. Do not randomize urgent escalation, hazardous ingredient advice or consent rights. For small cohorts, prioritize moderated usability observations over statistically unsupported conversion claims.
