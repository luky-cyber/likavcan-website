# FINAL AUDIT — v0.2.2

Date: 2026-09-15
Baseline: audited `v0.2.1 RC10`
Release theme: Entity Authority & Identity Consistency

## Result

**Automated release regression: PASS 31 / FAIL 0.**

Additional build checks also passed:

- `sitemap.xml` valid XML
- `feed.xml` valid Atom/XML
- all `structured-data/*.jsonld` files parse as JSON
- canonical/hreflang reciprocity preserved
- no broken local href/src or fragment targets
- no duplicate HTML IDs
- stable Person IDs preserved for Lukáš and Peter
- shared Home/Privacy pages contain no ambiguous `rel="me"`
- `rel="me"` remains scoped to individual profile identity links
- SK/EN/DE full Person nodes contain `jobTitle`
- SK/EN/DE full Person nodes expose 1:1, 4:3 and 16:9 image variants
- Publications JSON-LD contains all 11 normalized journal records from the bibliography master
- current discovery/source files contain no legacy “Lukáš-first” framing
- JavaScript passes `node --check`
- QR/vCard identity regression checks pass

## Entity changes

- Lukáš and Peter remain equal Home entry points.
- Stable Person/ProfilePage `@id` values were not changed.
- Positive disambiguation is strengthened with MTF STU and current organization context.
- Full Person nodes now include explicit job titles.
- Lukáš ProfilePage links to the corresponding local projects and publications.
- Publications graph is materially expanded while keeping DOI as the canonical work ID where verified.
- No negative “not the philosopher” metadata was added.

## Final entity consistency corrections

- Peter `jobTitle` is identical across Home, SK/EN/DE profile pages, the structured-data mirror and `llms.txt`.
- All six published ProfilePage nodes use timezone-aware ISO 8601 `dateModified` values.
- Home JSON-LD contains only the visible Lukáš and Peter Person entities as `mainEntity`; non-visible Project/mentions metadata was removed.
- Lukáš `hasPart` points to the matching SK/EN/DE project and publication entities on each localized profile.
- Atom feed top-level chronology, entry IDs and Publications update date are internally consistent.
- Release tree contains no `.tmp`, `.pyc` or `__pycache__` artifacts.

## Privacy / analytics

- Consent Mode v2 now establishes a local default-denied state before any Google Analytics network script is loaded.
- GA4 still loads only after explicit analytics consent.
- Advertising storage/signals remain denied.
- Consent policy version updated to `2026-09-15-v0.2.2`.

## Intentionally unresolved manual facts

These must not be invented in source code:

1. Exact Google Analytics property retention period — verify in the live GA property before replacing the generic Privacy wording.
2. Direct privacy contact channel — publish only a real, intended contact.

## Manual production gates

- real-browser desktop/mobile spot check
- 200%/400% zoom spot check
- Windows/iOS/Android vCard import and QR scan
- deploy, then request reindexing of materially changed pages

## Approval

**APPROVED AS v0.2.2 RELEASE PACKAGE, subject to the manual production gates above.**
