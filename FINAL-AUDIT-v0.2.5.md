# FINAL AUDIT — Likavcan.cz v0.2.5

Prepared: 2026-10-16

## Release status

Final deploy package prepared from `Likavcan-Website-v0.2.5-Preview-R3.zip` after the final ORCID and factual-precision pass.

## Fresh role/employer check

- Lukáš Likavčan: current public LinkedIn result lists BIZZCOM s.r.o.; the public profile summary identifies him as a Materials Engineer and R&D Specialist.
- Peter Likavčan: current LinkedIn directory result lists Porsche Werkzeugbau GmbH; the current public professional profile context remains Simulation Specialist / industrial simulation and automation.

## Final changes after Preview R3

- Restored ORCID to the active identity tier after account recovery/update.
- Added compact `ORCID ↗` to Lukáš homepage quick links in SK/EN/DE.
- Kept full ORCID on `/lukas/`; ResearchGate and Wikidata remain visually secondary.
- Added the SFRT / Young Researcher project No. 1341 directly to Lukáš's profile in SK/EN/DE with the source-accurate role wording and official MTF STU PDF.
- Added machine-readable `<time datetime>` values to already-visible career, education, project and publication dates.
- Expanded the internal AI identity benchmark with factual-precision guardrails.
- Synchronized ProfilePage `dateModified`, sitemap `lastmod` values and Atom feed freshness for the actually changed pages.
- Added `RELEASE-v0.2.5.md`.
- Added the v0.2.5 release/audit/preview documents to Jekyll `exclude` so repository documentation is not emitted into the public site.
- Updated `README.md` and `TODO.md` to the v0.2.5 release/post-release state and marked early preview notes as historical where superseded.

## Invariants preserved

- Homepage headline: `Dva inžinieri. Materiály a simulácie.`
- Lukáš Person ID: `https://likavcan.cz/lukas/#lukas-likavcan`
- Peter Person ID: `https://likavcan.cz/peter/#peter-likavcan`
- Homepage remains `WebSite` + `WebPage`, not `ProfilePage`.
- No Evidence / Authority / Verification sections, no verified/proof badges and no visible disambiguation copy about namesakes.
- Credential E2/A viewer and privacy redaction remain intact.
- No CLARA / SILENCE / RAMINES / NATO DIANA proposal names were added as realised projects.

## Regression result

`52 PASS / 0 FAIL`

The release regression covers local links, canonical/hreflang reciprocity, JSON-LD parsing and stable entity IDs, accessibility semantics, identity links/vCards/QR codes, cookie consent/focus behavior, credential viewer behavior, mobile/desktop profile navigation, sitemap/feed chronology, source integration, ORCID/SFRT final guardrails and JavaScript syntax.

## Deployment

Package is ready for manual deployment through the existing GitHub Pages `main` workflow. After deployment, verify the live site before tagging `v0.2.5`.
