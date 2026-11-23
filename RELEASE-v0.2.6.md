# Likavcan.cz v0.2.6

Release date prepared: 2026-11-23

## Scope

Conservative **Entity clarity & identity consistency** release built on the verified v0.2.5 production baseline. The visible design, homepage structure and human-facing profile copy remain essentially unchanged; the release focuses on tighter structured-data semantics, narrower professional classification and regression protection against identity drift.

## Main changes

- Preserved the stable canonical Person IDs for Lukáš and Peter across SK/EN/DE.
- Preserved the homepage as `WebSite` + `WebPage` with two existing Person entities.
- Kept Lukáš primarily identified as a Materials Engineer / Research and Development Specialist and Peter primarily as a `Simulation Specialist`.
- Narrowed secondary occupation/knowledge signals where they could be misread as parallel professional identities.
- Kept Bezpečná elektrika modelled as a project of the existing Lukáš Person, not as a second person or employer.
- Added minimal Slovakia country context to relevant typed organization/university nodes without publishing personal address data.
- Corrected authorship semantics: authored works are no longer incorrectly placed in `Person.subjectOf`.
- Preserved the canonical scholarly publication entity and all five co-authors of *Using Sodium Hydrogen Carbonate for Foaming Polymers*.
- Modelled Peter's diploma thesis as a standalone `CreativeWork` with `author` pointing to his stable Person ID.
- Aligned Peter's discovery/vCard title with the canonical primary role `Simulation Specialist`.
- Added targeted regression guardrails for stable entity IDs, portraits, country context, professional-title consistency, `author`/`subjectOf` semantics, employer chronology, project identity and SFRT attribution.

## Audit path

The release was reviewed in four distinct stages:

1. public identity baseline before the ZIP was shown;
2. blind ZIP-only audit;
3. informed audit using the v0.2.5 baseline, November 2026 identity benchmark and project guardrails;
4. independent verification of Candidate R2.

Candidate R2 was independently reproduced at **54 PASS / 0 FAIL** with **0 release-blocking findings**. The final deploy package adds only internal release documentation/configuration hygiene on top of that verified public-site payload.

Final deploy-package regression after release-documentation finalization: **55 PASS / 0 FAIL**.

## Intentionally unchanged

- Homepage headline: **“Dva inžinieri. Materiály a simulácie.”**
- Existing visual design, CSS and JavaScript behaviour.
- Canonical portraits and profile navigation.
- Current/historical career chronology: BIZZCOM current and Branson historical for Lukáš; Porsche Werkzeugbau current for Peter.
- SFRT 1341 visible role wording (`Zodpovedný riešiteľ`).
- Credential viewer and privacy redaction.
- Hosting: GitHub Pages with Cloudflare DNS-only.

No visible namesake warning, SEO FAQ, Evidence/Authority/Verification layer, trust badge, employer-logo wall, artificial profile symmetry, new framework or infrastructure migration was added.

## Deferred outside v0.2.6

The following remain separate runtime/operational work and are not release blockers for this identity-focused release:

- real-browser accessibility QA for first-visit cookie focus, mobile language target sizes and 200–400% zoom/reflow;
- vCard interoperability testing across actual clients before changing encoding format;
- GA4 retention/contact/privacy completion after verifying real operational settings;
- performance/LCP measurements on the deployed site;
- periodic ownership/availability checks of external `sameAs` profiles.

## Stable entity IDs

- Lukáš: `https://likavcan.cz/lukas/#lukas-likavcan`
- Peter: `https://likavcan.cz/peter/#peter-likavcan`
- WebSite: `https://likavcan.cz/#website`
- MTF STU: `https://likavcan.cz/#mtf-stu`
- Bezpečná elektrika: `https://bezpecnaelektrika.sk/#project`

## Release rule

Deploy through the existing `main` GitHub Pages workflow, run production smoke checks, and create immutable tag `v0.2.6` **only after successful production verification**. The existing `v0.2.5` tag must remain untouched.
