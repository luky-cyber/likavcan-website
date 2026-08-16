# Likavcan.cz v0.1.4 – production audit

Final pre-deployment audit performed on 2026-08-16.

## Verified
- canonical URLs on all indexable SK / EN / DE public pages
- reciprocal hreflang sets including x-default
- stable Person @id values for Lukáš and Peter across languages
- page-specific ProfilePage @id and url values for localized profile pages
- page-specific CollectionPage @id and url values for localized publications pages
- valid embedded JSON-LD syntax
- profile photos present in 1000 × 1000 JPEG and WebP variants
- Open Graph profile metadata and social portrait images on personal profile pages
- sitemap contains the 12 intended indexable public URLs
- robots.txt allows crawling and references the production sitemap
- GA4 remains consent-gated in assets/js/main.js
- GitHub Pages production exclusions are defined in _config.yml

## Corrected during audit
- replaced empty site.webmanifest with a valid manifest
- replaced empty favicon.ico with a valid multi-size favicon
- replaced empty 404.html with a functional noindex 404 page
- marked future Bezpečná elektrika placeholder pages noindex, nofollow
- excluded empty certificates/ and projects/ placeholders from GitHub Pages output
- made localized ProfilePage / CollectionPage identifiers page-specific while preserving stable Person entity IDs

## Deliberately unchanged
- the stable Person entity IDs remain:
  - https://likavcan.cz/lukas/#lukas-likavcan
  - https://likavcan.cz/peter/#peter-likavcan
- external identity links (ORCID, Google Scholar, LinkedIn, ResearchGate, Wikidata) were retained as supplied; this audit did not independently re-verify external account ownership.
- hidden future electrical-services content remains present but is not intended for indexing before launch.
