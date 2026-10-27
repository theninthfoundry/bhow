# 22 — Licensing, source provenance, and brand assets

## No generated or borrowed stock artwork

The starter contains **no dog photographs, no AI-generated images, and no embedded font binaries**. The Python UI uses native text/shapes/colors. Future photography must be user-owned with consent for private display, or commissioned with written rights. If public promotional photography is needed, license it deliberately; do not silently scrape social media images or copy competitor illustrations.

## Fonts

Suggested display/UI/code families: Bricolage Grotesque, Instrument Sans, JetBrains Mono. Verify the exact font file version and license before bundling into the app. **Do not distribute third-party font binaries without their licensing requirements**, and do not assume all fonts on the Internet have the same license.

## Data/model licensing

Dog breed benchmark datasets may contain noncommercial/research-only or unclear licenses; never assume ImageNet-style data rights for commercial use. Maintain per-asset provenance ledger (`dataset`, `contributor`, `consent`, `license`, `allowed use`, `restriction`, `expiry/deletion`, `hash`). A model's weights license is separate from its training-data rights. Keep nonconsenting user profile photos entirely out of model training.

## Third-party services

Check mapping terms, place-directory caching conditions, weather redistribution rights, push notification vendor privacy, SMS DLT needs in India, OIDC contractual terms, storage/data residency, and veterinary knowledge copyrights. Linking to public guidance is not permission to reprint a complete guideline.

## Source reference ledger (starting points, not vet approval)

- WSAVA vaccination: https://wsava.org/Global-Guidelines/Vaccination-Guidelines/
- WSAVA nutrition: https://wsava.org/global-guidelines/global-nutrition-guidelines/
- ASPCA food list: https://www.aspca.org/pet-care/aspca-poison-control/people-foods-avoid-feeding-your-pets
- India DPDP Rules: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025%3B
- Flet mobile camera: https://flet.dev/docs/controls/camera/
- Flet location: https://flet.dev/docs/services/geolocator/
- SQLAlchemy session pattern: https://docs.sqlalchemy.org/en/20/orm/session_basics.html

The user-supplied material contained older alternative React/Supabase plans and the newer Flet/Python-first choice. This kit chooses Flet/FastAPI to honor maximum Python; UI alternatives remain documented in ADR-002 rather than silently merging conflicting stacks.
