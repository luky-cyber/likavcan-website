# FINAL AUDIT — Likavcan.cz v0.2.0 RC3

## Release identity

**Likavcan.cz v0.2.0 — Lukáš First & Materials Proof of Work**

RC3 is the merged successor to the unpublished v0.2.0/v0.2.1 working candidates. No intermediate public release is required.

## Static release gate

- 27 public indexable URLs in `sitemap.xml` (9 page families × SK/EN/DE).
- Canonical URL and reciprocal `hreflang` (`sk`, `en`, `de`, `x-default`) present on all public pages.
- 27 valid JSON-LD blocks; stable Lukáš, Peter and Bezpečná elektrika entity IDs preserved.
- Bezpečná elektrika is not present in `Person.sameAs`; Project → founder → Lukáš relation is preserved.
- 0 broken local links/assets, duplicate HTML IDs or internal `index.html` links.
- No linked PWA manifest.
- Robots policy preserves OAI-SearchBot/ChatGPT-User discovery and disallows GPTBot.
- Bibliography normalized across SK/EN/DE: 11 journal articles, 5 conference papers, 2 books/teaching texts and 3 academic theses.
- 7 verified DOI links per language; DOI links are attached only to the corresponding journal records.
- Materials/R&D case study added in SK/EN/DE with evidence, limitations, original LL-FIG diagrams and publication cross-links.
- Bezpečná elektrika case study retains separate Project identity and receives the same evidence/limitations discipline.
- Dedicated 1200×630 OG card added for the Materials case study.
- Hash/sticky-header offset and `aria-current` semantics cleaned up.
- GA4 consent withdrawal code uses consent denied + GA disable flag + accessible first-party GA cookie cleanup + reload.
- vCards use vCard 3.0, CRLF line endings and ASCII-safe UTF-8 quoted-printable name fields for improved Windows/Outlook compatibility.
- QR assets regenerated at 492×492 and displayed at a larger scan-friendly size.
- `.gitattributes` marks `*.vcf` as binary so Git preserves vCard line endings.
- Profile QR/vCard links are relative for local/Acode compatibility; production targets remain unchanged.
- Primary navigation contains only Lukáš, Projects, Publications and Peter; Methodology is retained in the footer utility layer.
- All six localized `ProfilePage` nodes carry `dateModified: 2026-08-30`; visible profile-disambiguation text is phrased as Professional identity.
- Both case studies expose a consistent metadata block with type/context/evidence/status/last substantive update.
- German UI/case-study wording received targeted localization polish.

## Runtime checks already completed

- Homepage and Materials case-study visual review: PASS.
- Sticky hash navigation (`/lukas/#experience`, Materials `#evidence`): PASS.
- Publication and DOI links spot-check: PASS.
- GA4 after analytics consent: PASS (`collect` request observed).
- GA4 revoke All → Essential: PASS (`likavcan_cookie_consent=essential`, no subsequent `collect`, `ga-disable-G-0F00N4385D === true`).

## RC3 checks still required locally

- Re-open Lukáš and Peter `.vcf` in Windows Contacts / Classic Outlook and confirm Slovak diacritics after the RC3 encoding/path changes.
- Scan the larger Lukáš/Peter QR at 100% browser zoom and confirm the stable production `.vcf` URL.
- Final mobile spot-check at approximately 320–390 px.

## Release date

Keep the public release date `TBD` until the production deployment is successful. Editorial `lastmod`/feed dates represent substantive content changes, not build time.
