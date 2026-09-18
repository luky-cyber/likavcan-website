# Likavcan.cz v0.2.1 — Accessibility & Evidence Hardening

Release date: TBD — release candidate; set only after successful production deployment.

## Scope

Small hardening release following v0.2.0. No new product surface or new professional claims.

## Included

- WCAG-oriented primary CTA contrast fix while preserving the existing blue link palette.
- High-zoom/reflow and mobile navigation hardening: compact sticky global header on mobile with a contextual fixed bottom dock on professional/research pages.
- Explicit Slovak-language context for Bezpečná elektrika links in EN/DE.
- Explicit eager/high-priority loading for above-the-fold profile portraits.
- Direct source links next to selected Materials case-study claims.
- Targeted Slovak human-facing copy cleanup without changing factual scope.
- Automated release regression checks for local paths, anchors, JSON-LD/entity guardrails, hreflang, CTA contrast, identity/vCard consistency, optional QR decoding and JS syntax.

## Deliberately not included

- Search, dark mode, CV, public email, new case studies or Engineering Notes.
- Large CSS/build refactor or single-source content generator.
- Privacy/legal details that have not been operationally verified.
- Changes to the declared commercial status of Bezpečná elektrika.

## Release gate

Run `python tools/release_regression.py`, complete browser spot checks at desktop/mobile and 200%/400% zoom, then verify vCard/QR on real devices before tagging final `v0.2.1`.

## RC2 mobile validation

- Fixed narrow/high-zoom header flex-basis regression that could create excessive vertical whitespace.
- Removed visible section permalink # controls; stable section IDs and deep links remain intact.
- Android/Acode vCard import confirmed for Lukáš.

## RC3 navigation hierarchy correction

- Restored the intended global information architecture: Home / Lukáš / Peter only (SK/EN/DE).
- Project and publication discovery is intentionally contextual to Lukáš's professional profile rather than exposed as peer-level global navigation.
- Simplified all three homepages to identity/profile content only: Lukáš-first profile entry plus Peter's related profile entry.
- Removed homepage shortcuts to Projects/Publications while retaining those destinations inside Lukáš's profile navigation.
- Extended the release regression suite with a navigation hierarchy/homepage-scope guardrail.

## RC4 mobile header compaction

Real-device Android/Acode QA showed that the corrected RC3 header was still visually too tall on narrow mobile viewports. RC4 keeps the agreed Home / Lukáš / Peter information architecture but compacts the global mobile header into two rows: logo + language controls, then primary navigation. Lukáš/Peter contextual profile navigation is kept as a single horizontally scrollable row on mobile instead of wrapping to two lines. Desktop behaviour is unchanged.

## RC5 homepage contact polish

- Added compact direct contact links for both profiles on the identity homepage: LinkedIn + downloadable vCard.
- QR codes remain only on the detailed profile contact sections to keep the homepage lightweight and mobile-friendly.
- Added a regression guardrail ensuring both homepage contact groups exist in SK/EN/DE and that QR assets do not leak onto the homepage.


## RC6 visual-family and navigation harmonisation

- Homepage redesigned as two visually equal 1:1 profile cards for Lukáš and Peter; Lukáš-specific competence tiles stay on his profile instead of the identity landing page.
- Shared visual DNA with Bezpečná elektrika: aligned dark background/surfaces, teal accent, muted text, border tone, 24 px card radius, 14 px CTA geometry, subtle card gradients and section tones.
- Neutral dual-profile homepage Open Graph card added at 1200×630.
- Visible SK/EN/DE language controls now use route-preserving relative targets, so local Acode/Live Server preview keeps the equivalent page instead of falling back to Home.
- Mobile global navigation is sticky at the top. Profile/research context pages use a fixed four-item bottom dock with safe-area spacing.
- Lukáš mobile profile dock is explicitly split into Professional and Academic contexts without crowding: the fourth item switches between Akadémia/Academia/Akademisch and Prax/Practice/Praxis.
- Mobile cookie-settings floating button is hidden when the fixed dock is present; cookie settings remain available in the footer and the consent banner is offset above the dock.
- Footer styling and the “Merať. Dokumentovať. Vysvetľovať.” engineering signature are harmonised with the related project site.
- Full render regression: 27 public pages × 1440/390/320 px = 81 combinations, 0 horizontal-overflow findings; mobile header and dock both measure ~64 px in the test viewport.

## RC7 master hardening — 2026-09-14

- Fixed the Peter SK/EN/DE mobile bottom dock so Profile/Career/Expertise/Contact stay inside Peter's profile instead of crossing into Lukáš's identity.
- Added semantic regression coverage for Peter dock identity, localized mobile-navigation accessible names and the custom 404 route.
- Hardened the custom 404 with root-safe language targets, Home/Lukáš/Peter recovery actions and route-aware SK/EN/DE copy.
- Synchronized the verified E2A status: examination completed, certificate issued, commercial inspection services still not launched.
- Updated the Bezpečná elektrika case-study framing to planned inspection services + expert content while preserving Materials Engineering / R&D as Lukáš's primary professional identity.
- Localized the remaining Slovak case-study eyebrow labels.
- Added `aria-current="location"` synchronization for the active contextual mobile-dock target.
- Localized mobile-dock accessible names in Slovak and German.
- Hardened consent storage to a versioned JSON record (`choice`, `decidedAt`, `policyVersion`) with a 12-month maximum age and re-prompt after policy changes.
- Minimized GA4 `page_location` and `page_referrer` by removing query strings and fragments before analytics configuration.
- Made the two first-layer consent choices visually equivalent and clarified that the × action means “essential only + close”.
- Expanded SK/EN/DE privacy information with controller identification, GitHub Pages technical operation, analytics legal basis, recipients/transfers, retention criterion and data-subject rights without inventing an unverified public email or national supervisory authority.
- Removed Python bytecode from the release tree and added `__pycache__/` + `*.pyc` to `.gitignore`.
- Updated sitemap/feed editorial dates only for pages with substantive factual/privacy changes.
- Extended automated release regression from 18 to 23 guardrails; RC7 result: 23 PASS / 0 FAIL.

### RC7 remains a release candidate

Manual 200%/400% browser zoom, Android/mobile safe-area + consent interaction, Windows/Outlook vCard import and post-deploy HTTPS/404/headers/cache/Search Console checks remain release gates. The exact GA4 property retention setting and a stronger direct privacy contact should be operationally verified before the privacy notice is treated as fully complete.

## RC8 human editorial pass — 2026-09-14

- Reworked visible SK/EN/DE copy to read as a professional website written by people rather than as release/audit documentation.
- Removed the public “Professional identity” explanation from both profiles while preserving the underlying stable entity IDs, JSON-LD and external identity references.
- Simplified the Lukáš and Peter profile introductions without changing verified facts, employment, education or technical scope.
- Rewrote the Projects introduction and labels to describe the work directly instead of repeatedly framing it as “proof of work”.
- Consolidated repeated disclaimers in the Materials case study into one clearer limitations section while preserving source links, co-authorship boundaries and the distinction between simulation, experiment and engineering interpretation.
- Simplified the Bezpečná elektrika case study, retained the physical-safety boundaries and E2A/commercial status, and removed audit-style statements about what the page “demonstrates”.
- Reduced the public Methodology page to four human-facing principles: sources, technical content, AI as a supporting tool, and editorial updates. Entity/crawler implementation details remain in the code and project documentation rather than visible copy.
- Updated project/methodology metadata and editorial dates only on substantively edited routes.
- No changes to global Home / Lukáš / Peter IA, stable entity IDs, bibliography, privacy hardening, consent architecture or commercial status.
- Automated regression after the RC8 editorial pass: 23 PASS / 0 FAIL.

### RC8 remains a release candidate

Manual browser/device gates from RC7 remain open: 200%/400% zoom, Android mobile navigation + consent + safe-area interaction, Windows/Outlook vCard import, and post-deploy HTTPS/404/headers/cache/Search Console checks.


## RC9 human cut & simplification — 2026-09-14

- Reworked the SK/EN/DE homepage around a five-second message: two engineers, materials and simulation, while preserving the equal Lukáš/Peter identity hierarchy.
- Simplified both profile pages: removed duplicated back-home CTAs, audit-style manifest blocks, repeated reference/identity sections and visible Wikidata links; machine-readable identity data remains unchanged.
- Kept Lukáš in first-person voice and Peter in factual third-person voice; no unverified first-person authorship was introduced for Peter.
- Reduced Lukáš contextual navigation to six user-facing destinations and Peter to five.
- Consolidated technical tools/profiles into the content where users expect them instead of separate database/reference sections.
- Reduced the Materials case study from ten numbered chapters to six natural sections, removed visible `LL-FIG-*` editorial identifiers and retained direct source links, co-authorship boundaries and limitations.
- Removed the public AI-workflow section from Methodology; the public page now covers sources, technical interpretation and editorial updates.
- Rewrote `llms.txt` so Lukáš and Peter are peers rather than primary/related identities and removed `proof-of-work` / audit-style terminology.
- Slightly increased portrait prominence while retaining the existing visual family, static HTML/CSS/JS architecture, 27 localized public routes, stable entity IDs and structured data.
- GA4/consent remains unchanged in RC9; removing analytics is a separate product/privacy decision, not part of this editorial release candidate.
- Extended automated regression with an RC9 human-cut guardrail; current result: **24 PASS / 0 FAIL**.

### RC9 remains a release candidate

The existing manual gates remain open: 200%/400% zoom, Android mobile navigation + consent + safe-area interaction, Windows/Outlook vCard import, and post-deploy HTTPS/404/headers/cache/Search Console checks.


## RC10 mobile UX & qualification follow-up — 2026-09-14

- Replaced the changing Lukáš Professional/Academic bottom dock with one stable four-item dock: Profile / Projects / Publications / Contact (localized SK/EN/DE).
- Added scroll-position-aware active state on both Lukáš and Peter profile pages. Clicking no longer owns the active state; route + current section do. `aria-current="location"` follows the same state.
- Publication grids now use a dedicated responsive class and collapse to one readable column on narrow/mobile viewports.
- Updated the E2A wording from professional preparation to the achieved state: examination successfully completed and certificate issued; commercial inspection services remain not launched.
- Removed the customer-training card from Lukáš SK/EN/DE until it is intentionally reintroduced.
- Linked Bezpečná elektrika directly from the Lukáš intro to the live project website; EN/DE links retain Slovak-language context.
- Localized remaining decorative English category badges on the Slovak Lukáš/Peter profiles while keeping real product/discipline names where appropriate.
- Existing compact two-row mobile header remains unchanged after real-device review.
