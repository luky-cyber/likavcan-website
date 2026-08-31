# FINAL AUDIT — Likavcan.cz v0.2.0

## Release identity

**Likavcan.cz v0.2.0 — Lukáš First & Materials Proof of Work**

This is the publish-ready package for the single v0.2.0 release. No intermediate v0.2.1 release is required. The release date remains TBD until production deployment succeeds.


## Final information-architecture and homepage changes

- Replaced the former long homepage with a minimalist two-person professional identity/contact directory: Lukáš first, Peter second.
- Each homepage identity block contains portrait, name, concise professional positioning, localized profile link, LinkedIn, downloadable vCard and QR.
- Removed homepage project/publication/engineering-approach blocks; those remain available through the Lukáš branch where they have proper context.
- Added explicit localized Home/Startseite navigation instead of relying only on the Likavcan.cz logo convention.
- Context-aware navigation is now: homepage/utility `Home · Lukáš · Peter`; Lukáš/projects/publications `Home · Lukáš · Projects · Publications`; Peter `Home · Peter`.
- Homepage structured data remains Lukáš-first (`mainEntity` = stable Lukáš Person) and mentions the stable Peter Person; the now-invisible Bezpečná elektrika homepage mention was removed from JSON-LD.
- Homepage `dateModified` and sitemap `lastmod` were updated to 2026-08-31 because this is a substantive editorial/information-architecture change.
- Static validation after the change: 27 public sitemap URLs, 0 broken local links/assets, 0 duplicate IDs, valid JSON-LD, navigation policy PASS.
- Layout smoke test using the actual CSS at 1920, 768, 390 and 320 px across six representative page types: 24 combinations, 0 horizontal overflow.

## Runtime-driven hardening incorporated before release

- Reduced the global H1 scale from `clamp(2.5rem, 7vw, 4.75rem)` to `clamp(2.25rem, 5vw, 4rem)` and reduced large-section vertical padding so Full HD pages reveal more useful content above the fold.
- Widened case-study hero content to 980 px, allowing long titles and the five-item metadata block to use desktop space more efficiently.
- Section permalink `#` controls are hidden by default, appear only on desktop hover/keyboard focus, and are not shown on touch/mobile layouts. Stable section IDs and hash URLs remain unchanged.
- Reordered Projects so the current Bezpečná elektrika project appears before the older 2013–2017 Materials research case study.
- Repositioned Bezpečná elektrika in SK/EN/DE as a **service-first project preparing electrical inspection services**. Technical/educational content is explicitly secondary/supporting.
- Primary Bezpečná elektrika CTAs now point to `https://bezpecnaelektrika.sk/revizie/` with service-specific labels instead of a generic project visit label.
- Rewrote the Bezpečná elektrika case study around services → inspection approach → supporting engineering workflow → technical content → evidence/limitations → qualification/commercial status.
- Synchronized the current qualification boundary supplied for Bezpečná elektrika: E2A examination completed, certificate issued, commercial inspection services not yet launched.
- Updated homepage/project/profile machine-readable project descriptions and `llms.txt` to the same service-first/current-status model.
- Replaced the RC3 quoted-printable vCard experiment with vCard 3.0 using plain UTF-8 text, CRLF, no BOM and lower-case `CHARSET=utf-8`. This removes the raw quoted-printable failure observed in New Outlook; subsequent local testing confirmed correct display in the tested Windows Contacts, Classic Outlook and New Outlook clients.

## Static release gate

- 27 public indexable URLs in `sitemap.xml` (9 page families × SK/EN/DE).
- Canonical URL and reciprocal `hreflang` (`sk`, `en`, `de`, `x-default`) validated for all sitemap pages.
- JSON-LD parses cleanly; stable Lukáš, Peter and Bezpečná elektrika entity IDs are preserved.
- Bezpečná elektrika is not present in `Person.sameAs`; Project → founder → Lukáš relation is preserved.
- 0 broken local links/assets, duplicate HTML IDs, missing same/cross-page local anchors or internal `index.html` links in the static audit.
- All newly referenced Bezpečná elektrika paths (`/revizie/`, `/poradna/`, `/meranie/`, `/glosar/`, `/metodika/`) exist in the supplied Bezpečná elektrika v0.6.3 RC3 package.
- No linked PWA manifest.
- Robots policy preserves OAI-SearchBot/ChatGPT-User discovery and disallows GPTBot.
- Bibliography remains normalized across SK/EN/DE: 11 journal articles, 5 conference papers, 2 books/teaching texts and 3 academic theses.
- 7 verified DOI links per language remain attached only to the corresponding journal records.
- Stable Materials/R&D case study evidence, limitations, LL-FIG diagrams and publication cross-links are unchanged.
- GA4 consent withdrawal code remains unchanged after its successful runtime test.
- `.gitattributes` continues to mark `*.vcf` as binary so Git preserves CRLF line endings.

## Runtime results already observed by the user

- Acode/Android site review: completed.
- QR rendering/path in Acode: fixed; Google Lens can read the QR.
- Windows Contacts: current plain-UTF-8 vCard displays correctly.
- Classic/New Outlook: current plain-UTF-8 vCard display was confirmed correct in the latest local review.
- Google Lens: QR is readable at normal presentation size.
- Homepage/Materials visual review and sticky hash navigation: PASS on earlier candidates.
- Publication/DOI spot-check: PASS.
- GA4 consent and All → Essential revoke flow: PASS.

## Final user/runtime approval

- Acode/Android review completed; QR is visible and Google Lens reads it.
- Full-HD visual review approved after H1/hero sizing and navigation changes.
- Windows Contacts, Classic Outlook and New Outlook display the final plain-UTF-8 vCard correctly in the latest user test.
- The minimalist homepage and context-aware navigation were approved for release.
- Section permalink `#` controls remain hidden by default and are removed from touch/mobile presentation by CSS.

## Release date

Keep the public release date `TBD` until production deployment is successful. Editorial `lastmod`/feed dates represent substantive content changes, not build time.
