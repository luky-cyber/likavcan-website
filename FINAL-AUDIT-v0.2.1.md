# Final audit — v0.2.1 release candidate

Date: 2026-09-14

## Scope

Accessibility, evidence and regression hardening of the existing v0.2.0 information architecture.

## Required checks

- [x] Automated release regression script passes with zero failures.
- [x] 27 public sitemap URLs remain valid.
- [x] No broken local paths or HTML fragment targets.
- [x] JSON-LD parses and stable Person/Project identifiers remain unchanged.
- [x] Person.sameAs does not contain Bezpečná elektrika.
- [x] Primary CTA default and hover contrast are at least 4.5:1.
- [x] EN/DE links to Bezpečná elektrika expose Slovak-language context.
- [x] Main portraits are eager/high-priority; lower related portraits may remain lazy.
- [x] Materials claims have direct source links near the relevant statements.
- [x] Mobile global header is compact and sticky; contextual profile/research navigation is fixed at the bottom with safe-area handling.
- [x] 27 public pages × 1440/390/320 px render regression: 81 combinations, 0 horizontal-overflow findings.
- [ ] 200% and 400% zoom remain usable.
- [ ] Windows/Outlook vCard and mobile QR tests remain successful.

Release date remains separate from this audit date.

## RC2 mobile follow-up

- Android/Acode: Lukáš vCard import PASS.
- Narrow header: flex-basis reset added to prevent oversized header whitespace.
- Visible # permalink controls removed; section IDs retained for deep links.

### Narrow-header render check

- 390 CSS px viewport: site header ~110 px; no horizontal overflow.
- 320 CSS px viewport: site header ~110 px; no horizontal overflow.
- 800/980 CSS px: site header ~65/73 px.
- Root cause of the Android/Acode oversized header was inherited `flex: 1 1 560px` after the nav group switched to column flow; RC2 resets it to content-sized flex behavior.

## RC3 information architecture follow-up

Android/Acode review exposed that the RC2 global navigation did not match the agreed hierarchy. RC3 restores Home / Lukáš / Peter as the only global destinations in SK/EN/DE. The three homepages now contain profile/identity presentation only; Projects and Publications remain discoverable from Lukáš's contextual profile navigation. The automated release regression suite now asserts this hierarchy to prevent recurrence.

## RC4 real-device mobile follow-up

Android/Acode review confirmed vCard import and exposed excessive vertical navigation chrome rather than broken content. The mobile global header is now a compact two-row grid and contextual profile navigation is a one-row horizontal scroller. This preserves all destinations while materially reducing the portion of a 320–390 px mobile viewport consumed before profile content. Heading permalink glyphs remain hidden while the underlying HTML `id` anchors remain available for deep links.

## RC5 homepage contact polish

- SK/EN/DE homepages expose compact LinkedIn + vCard links for Lukáš and Peter directly beside their profile entry points.
- QR codes remain on detailed profile pages only.
- `tools/release_regression.py` now guards this homepage-contact scope; current result: 16 PASS / 0 FAIL.


## RC6 visual-family and IA follow-up

- Homepage profile presentation is visually 1:1 for Lukáš and Peter while keeping their detailed content on separate profile pages.
- Likavcan.cz now shares the restrained visual family of Bezpečná elektrika: `#0b1016` background, `#121c27` surface, `#9fb1be` muted text, `#63d8d0` accent, teal-tinted borders, 24 px cards and 14 px CTAs.
- Homepage OG metadata now points to a neutral dual-profile 1200×630 image.
- Visible language switching is route-preserving with relative local targets; regression check confirms the target exists for every visible SK/EN/DE language link.
- Mobile header is sticky (~64 px at 320/390 CSS px). Contextual bottom dock is fixed (~64 px) on Lukáš/Peter profiles, Projects, Publications and both case studies.
- Lukáš bottom dock uses explicit four-item Professional/Academic contexts rather than an eight-link crowded strip.
- Cookie controls and page bottom padding account for the fixed dock.
- Current automated release regression after RC6 changes: 18 PASS / 0 FAIL.


## RC7 master-audit hardening follow-up

- [x] Peter SK/EN/DE mobile dock stays inside Peter profile.
- [x] Mobile-dock accessible names are localized in SK/EN/DE.
- [x] Custom 404 uses root-safe `/`, `/en/`, `/de/` language targets and route-aware recovery copy.
- [x] E2A status is synchronized: examination completed, certificate issued, commercial services not launched.
- [x] Slovak Bezpečná elektrika case-study eyebrow drift is removed.
- [x] Active contextual mobile target receives `aria-current="location"`.
- [x] Consent record is versioned and timestamped with a 12-month maximum age.
- [x] GA4 page location/referrer are minimized by stripping query strings and fragments.
- [x] Privacy SK/EN/DE includes technical operation, legal basis, recipients/transfers, retention criterion and data-subject rights.
- [x] Python bytecode is removed from the release tree and ignored for future work.
- [x] Automated release regression after RC7: **23 PASS / 0 FAIL**.
- [ ] Verify the exact GA4 property retention setting and stronger direct privacy contact before treating the privacy notice as fully complete.
- [ ] 200% and 400% real-browser zoom acceptance.
- [ ] Android/mobile dock + consent + safe-area acceptance.
- [ ] Windows/Outlook vCard import and QR acceptance.
- [ ] Post-deploy HTTPS/404/security headers/cache/Search Console smoke test.

## RC8 human editorial follow-up — 2026-09-14

- [x] SK/EN/DE profile intros no longer expose internal identity/entity methodology as user-facing prose.
- [x] Projects and case studies use direct professional language instead of repeated “proof/evidence” framing.
- [x] Materials limitations remain explicit while duplicated caveats were removed.
- [x] Bezpečná elektrika safety boundaries and verified E2A/precommercial status remain intact.
- [x] Public Methodology is reduced to source, technical-content, AI-support and update principles; structured-data/crawler implementation remains outside visible prose.
- [x] Stable entity IDs, Home/Lukáš/Peter information architecture and publication counts remain unchanged.
- [x] `python tools/release_regression.py` => 23 PASS / 0 FAIL after the editorial pass.
- [ ] Existing manual release gates remain open: 200%/400% zoom, Android interaction/safe-area, Windows/Outlook vCard, and post-deploy production checks.


## RC9 human-cut follow-up — 2026-09-14

- [x] Homepage gives a direct five-second description without “verifiable output” language.
- [x] Lukáš/Peter remain equal homepage identities; global Home / Lukáš / Peter IA is unchanged.
- [x] Profile pages remove redundant manifest/reference/database presentation while preserving source links near substantive claims and machine-readable identity data.
- [x] Visible Wikidata buttons are removed; Wikidata remains available to structured-data/entity systems.
- [x] Materials case study uses six natural sections and no visible internal `LL-FIG-*` identifiers.
- [x] Methodology no longer discusses the AI writing/research workflow in visitor-facing copy.
- [x] `llms.txt` no longer describes Lukáš as primary and Peter as related, and no longer uses `proof-of-work` terminology.
- [x] No GA4/consent architecture change was made as part of the editorial simplification.
- [x] `python tools/release_regression.py` => **24 PASS / 0 FAIL** with the RC9 human-cut guardrail enabled.
- [ ] Existing manual release gates remain open: 200%/400% zoom, Android interaction/safe-area, Windows/Outlook vCard, and post-deploy production checks.


## RC10 real-device mobile follow-up — 2026-09-14

- [x] Mobile publications use one readable column instead of two narrow card columns.
- [x] Lukáš mobile dock is stable across profile, projects, publications and case studies.
- [x] Lukáš and Peter profile dock highlighting follows current scroll position rather than the last clicked item.
- [x] Dock active state is mirrored with `aria-current="location"`.
- [x] E2A profile wording reflects the completed examination and issued certificate.
- [x] Customer-training card is removed from Lukáš SK/EN/DE.
- [x] Bezpečná elektrika is linked directly from the Lukáš introduction.
- [x] Remaining decorative English badges on Slovak profiles are localized.
- [ ] Repeat Android real-device acceptance on the RC10 ZIP after packaging.
- [ ] Existing 200%/400% zoom, Windows/Outlook vCard and post-deploy production gates remain open.
