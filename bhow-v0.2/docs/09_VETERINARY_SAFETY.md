# 09 — Veterinary content governance and clinical safety case

**This is not veterinary advice or a clinical product approval.** The code deliberately does not provide remote diagnosis, a medication regimen or an “all clear” status.

## Three immutable rules

1. **A photo cannot diagnose or prove breed ancestry.** Breed resemblance ≠ genetic identity; health associations are general education and require the individual dog's context.
2. **No database match ≠ food safe.** The sample KB is illustrative, limited and marked `pending_veterinary_approval`. Hazard flagging and escalation are conservative; release needs regional professional signoff.
3. **No generic vaccine schedule is automatically prescribed.** Users enter known provider dates; vaccine guidance depends on veterinarian, animal, local risks and product specifics.

## Emergency content design

Provide plainly visible pathways to veterinary emergency assistance for difficulty breathing, collapse, severe bleeding, seizures, suspected poisoning, signs of heatstroke or bloated abdomen with unproductive retching. Do not delay help by forcing questionnaires, image uploads or login. Do not give toxic-dose reassurance. Emergency contact info must be verified and clearly labeled by source and last check.

## Vet-reviewed knowledge item schema (future)

```yaml
id: food.xylitol
version: 2
jurisdiction: IN-Telangana
species: dog
assertion: potential_hazard
source_url: https://www.aspca.org/pet-care/aspca-poison-control/people-foods-avoid-feeding-your-pets
source_checked_at: 2026-10-27
reviewer_name: null           # MUST be completed before release
reviewer_credentials: null
reviewer_approval_at: null
expires_at: null
approved_for_public_guidance: false
triage_policy_id: unknown_ingestion_escalate
```

Clinical reviewer signs exact text, situation, urgency, region and version. Changes produce new versions and test-case revisions. Store old versions for audit. Escalation failures are incidents, not merely UX bugs.

## Care-history provenance

`Caregiver observed` — never transformed into confirmed clinical finding. `Professional verified` — only after credential checks, professional action, and audit metadata. `ML suggestion` — visibly uncertain and never entered as medical diagnosis. `Unknown` — respected rather than filled with guessed values.

## Source starting points (not wholesale clinical authorization)

- [WSAVA 2024 vaccination guidelines](https://wsava.org/Global-Guidelines/Vaccination-Guidelines/) — region and patient variability matter.
- [ASPCA potential food hazards](https://www.aspca.org/pet-care/aspca-poison-control/people-foods-avoid-feeding-your-pets) — ingredient flags, not an exhaustive safe list.
- [WSAVA global nutrition guidance](https://wsava.org/global-guidelines/global-nutrition-guidelines/) — ask a veterinary nutrition professional to adapt to regional diets.

No dataset, source URL or AI system replaces veterinary review. Contract a Telangana/India-licensed professional for clinical review, escalation protocol, medical claims and periodic updates. Obtain written review records, not a verbal endorsement.
