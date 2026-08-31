# Likavcan.cz v0.2.0 — Lukáš First & Materials Proof of Work

Release date: TBD — publish-ready package; set only after successful production deployment

## Highlights
- Reworked the SK/EN/DE homepages into a minimalist professional identity/contact directory: Lukáš first, Peter second, each with portrait, concise professional description, profile link, LinkedIn, vCard and QR.
- Removed projects/publications/methodology-style content blocks from the homepage so detailed proof-of-work lives in the corresponding professional branches instead of duplicating the profile pages.
- Added explicit context-aware primary navigation: Home + Lukáš + Peter on the homepage/utility layer; Home + Lukáš + Projects + Publications in the Lukáš branch; Home + Peter in the Peter branch.
- Added `/projects/` in SK/EN/DE as a real public collection instead of an empty placeholder.
- Added a full Bezpečná elektrika service-first proof-of-work case study in SK/EN/DE, aligned with the current inspection-services positioning.
- Added a Materials/R&D case study on fibre orientation in injection-moulded thermoplastics in SK/EN/DE.
- Prioritized the current Bezpečná elektrika project above the older Materials research case on `/projects/`, with primary CTAs leading directly to the inspection-services page.
- Reduced oversized Full HD H1 presentation and widened case-study heroes so useful context appears earlier above the fold.
- Added original LL-FIG explanatory diagrams and publication ↔ case-study evidence links.
- Preserved the primary materials/R&D identity; electrical safety remains a separate complementary project branch.
- Added synchronized qualification/commercial-status wording based on the current Bezpečná elektrika project state; the E2A exam is completed, the certificate has been issued and commercial inspection services are not yet launched.
- Added QR-enabled vCard contact panels for Lukáš and Peter without publishing new private contact data; vCard 3.0 uses plain UTF-8, CRLF and no BOM; runtime testing now confirms correct display in the tested Windows contact/Outlook clients.
- Switched profile QR/vCard links to relative paths for reliable local/Acode preview while preserving the same production URLs.
- Added human-facing Professional identity wording and `ProfilePage.dateModified` to all SK/EN/DE person profiles.
- Standardized compact metadata blocks across both public case studies (type/context/evidence/status/last substantive update).
- Applied targeted German-language polish to UI labels and case-study terminology without translating original publication titles.
- Methodology remains available as a footer trust/source utility; language switching is semantically separate from the context-aware primary navigation.
- Added page TOC and copyable section permalinks on long content pages; the technical `#` controls are hidden by default and removed from touch/mobile presentation.
- Normalized publication metadata across SK/EN/DE, separating conference records from journal records and correcting DOI-to-work associations.
- Added visible DOI links for verified journal records while keeping structured-data expansion conservative.
- Added sitewide social-sharing metadata and dedicated 1200×630 OG cards for major page types.
- Added Privacy & Analytics pages in SK/EN/DE.
- Improved GA4 consent withdrawal: denied consent, GA disable flag, first-party GA cookie cleanup and reload after revocation.
- Preserved OAI-SearchBot/ChatGPT-User access while keeping GPTBot disallowed.
- Removed empty `certificates/`, orphan `site.webmanifest` and unused Bezpečná elektrika PNG asset.
- Removed internal links ending in `index.html`.
- Fixed missing `--shadow-lg`, duplicate CSS blocks and aligned 404 styling with the design system.

## Stable entities preserved
- Lukáš: https://likavcan.cz/lukas/#lukas-likavcan
- Peter: https://likavcan.cz/peter/#peter-likavcan
- Bezpečná elektrika project: https://bezpecnaelektrika.sk/#project
