# 03 — UI/UX framework / BHOW Studio Design Language

**Design thesis:** *An editorial field guide that lives in your pocket.* Bold minimalism with moments of tenderness and utility: high-contrast type, off-white paper, black rule lines, a little haldi yellow, real memories of real dogs. Never a generic pet marketplace, hospital admin panel, or purple AI chatbot.

## Visual identity

| Token | Value | Use |
|---|---|---|
| `paper` | `#F4F0E7` | Root canvas |
| `ink` | `#161713` | Type/navigation |
| `muted` | `#686A61` | Supporting metadata |
| `haldi` | `#F1BD37` | One highlighted decision per screen |
| `surface` | `#FFFFFF` | Content elevation sparingly |
| `rule` | `#D6D3C9` | 1px editorial dividers |
| `danger` | `#A9231B` | Emergency/action content with text+icon |

**Type:** Bricolage Grotesque for display, Instrument Sans for UI, JetBrains Mono for small data/meta labels — bundle under their actual open-source licenses after verification. Keep 2 fonts on typical screens. Type ramp: display 40/44, hero 32/38, section 24/30, body 16/24, fine 12/18. Dynamic font scaling required. Use at most 2 radii (4px and 12px); 8pt grid with purposeful 4px micro-spacing.

**Motion:** 160–280ms UI feedback; no animation that blocks care, food hazard, emergency action, or navigation. Real photographs may gently reveal as content scrolls. `Reduce motion` swaps animation for instant transitions. No heavy WebGL in the core care flow; reserve motion craft for onboarding/Yearbook when performance permits.

**Photography:** Only a user's own consented dog photo or original commissioned photography with written rights. No AI-generated images. No stock dog hero shots. No identifiable pet/owner location embedded in public media; strip EXIF metadata. Cropping guidance should preserve ears, nose, body context while not implying breed certainty.

## Screen map and navigation

Bottom navigation (max 4 persistent items): `Today` · `Passport` · `Check` · `Explore`; `Help now` remains a persistent, discoverable nonpaywalled action reachable in <=2 taps (not a quiet subtab). Profile switcher in header supports multiple dogs. The large `+` on Today adds a care note or task. Avoid eight primary nav tabs. Community features become a separate opt-in experience when ready.

- **Onboarding:** no carousel of boastful AI benefits; intro -> role -> dog name -> optional age/weight/photo -> next useful action. No forced camera or location permission.
- **Today:** dog portrait/initials; big next action, upcoming task, safety note with source and data freshness. If conditions unknown show `Not checked`, not a green status.
- **Passport:** chronological events with provenance, planned appointments, document placeholders, controlled sharing and export.
- **Check:** switch `Food ingredient`, `Breed discovery (when available)`, `Outdoor conditions (when available)`; never blend three different certainty scales.
- **Explore:** enrichment, behavior education, region-aware content and later vetted resources.
- **Help:** clear crisis workflow and closest verified contact only if data actually available; offline fallback to call a known provider supplied by the user.

## Component inventory (one Python source of design tokens)

`BhowTopBar`, `DogIdentityHeader`, `NextActionBanner`, `JournalRow`, `SourcePill`, `DateChip`, `TimeRail`, `FlaggedIngredientRow`, `KnowledgeFootnote`, `EmptyState`, `DogSwitcher`, `PermissionExplainer`, `BottomSheet`, `ActionButton`, `QuietButton`, `InlineRetry`, `LoadingSkeleton`, `Confirmation`, `ExportPanel`, `EmergencyCallRow`, `MapSourceLegend`.

**SourcePill** variants: `Caregiver entry` (not verified), `Verified by [professional + date]` (after actual verification), `Model suggestion` (nonclinical), `Unknown source`. Never use green checkmark for unsourced facts.

## Signature moments

**First dog:** large type `Who are we caring for?`; input begins with a name; a thin hand-drawn underline animates on valid submission. On next screen, `Kaju's story starts here.` No loud confetti, XP rewards, or forced social sharing.

**Food-check result:** plain-language risk headline above every flourish. Hazard = strong outline + high-priority copy, sources and human next step; unknown = quiet but conspicuous caution. No gold star, no “100% safe,” no fake numeric certainty.

**Passport:** beautifully composed typographic record page with an export sheet for veterinarians. Visual art should support chronology and provenance instead of inventing medical meaning.

## Interaction states, accessibility and trust

Every button: idle, pressed, loading, success, recoverable error, offline. All icons need text labels where the action matters. Contrast target WCAG AA; 44x44pt touch target; font scaling; input labels; screen reader order; no reliance on color alone; high-contrast mode; keyboard support on desktop/web. Consent prompt explains why, offers `Not now`, and has corresponding delete/revoke flow. No dark patterns around paid upgrades. Medical advice never appears inside novelty/celebration UI.

## Implementation mapping

Tokens live in `client/tokens.py` as source for Flet preview; production component gallery lives in `client/gallery.py` when built. Flet is a Python UI wrapper over Flutter, not a guarantee of parity with hand-crafted native motion. If user research requires much more sophisticated interaction fidelity, preserve FastAPI/domain backend and reconsider the frontend without rewriting the domain.
