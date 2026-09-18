# RELEASE v0.2.4 — Integrated Sources & Identity Consistency

## Goal
Keep Likavcan.cz immediately understandable as a professional site of two engineers while retaining strong, precise entity and source relationships in the background. Sources support concrete facts; they are not a separate user-facing topic.

## User-facing changes
- Removed standalone “independent evidence / verification” sections from all SK/EN/DE profiles.
- Lukáš: Young Researcher project No. 1341 is integrated into Projects as a normal 2015 research project.
- Lukáš: PhD supervisor and Bc./Ing. thesis source links stay contextual inside Education.
- Lukáš: selected publication sources are compact links directly under the relevant publications.
- Peter: scholarship and admission records are no longer displayed as public achievements.
- Peter: the 2016 diploma thesis is integrated into the Ing. Education card and links to the STU catalogue; it directly supports the Process Simulate / Virtual Commissioning continuity.
- Homepage remains unchanged: “Dva inžinieri. Materiály a simulácie.” / language equivalents remain the five-second orientation layer.

## Final polish
- Removed the last verification-style Branson source labels; the links now identify the STU graduate-profile source only.
- Added Wikidata links for Lukáš's ultrasonic welding, injection moulding and CAE `knowsAbout` topics.
- Synchronized standalone structured-data mirrors with SK inline invariants while preserving localized/profile descriptions.
- Synchronized the DE Privacy information date with SK/EN; GA4 retention remains intentionally unresolved until the real property setting is known.
- Changed the site-wide Methodology voice from singular to plural in SK/EN/DE and aligned the related case-study link labels.
- Added `/apple-touch-icon.png` (180×180), derived from the existing favicon; no manifest, service worker or PWA layer was added.

## Final UX acceptance fixes
- Profile scrollspy now uses a single anchor offset source, so desktop section clicks and active labels stay aligned for Lukáš and Peter in SK/EN/DE.
- The last tracked section (`Contact`) becomes active at the document end on both desktop and mobile.
- Mobile dock route/scrollspy behavior is guarded independently from desktop profile navigation.
- Homepage portraits are direct, keyboard-focusable links to the corresponding profiles while the explicit Profile CTA remains.
- Lukáš Education now uses the same row-readable 2-column desktop / 1-column mobile pattern as the other four-card profile grids; chronological order is unchanged.
- Long pages now expose a compact fixed back-to-top control after scrolling; it is localized in SK/EN/DE, keyboard-focusable, respects reduced-motion preferences and sits above the fixed mobile dock.
- Cookie settings use the existing footer/privacy controls; the temporary floating Cookie-settings utility was removed so Back-to-top remains the only floating utility control.
- The E2/A credential viewer uses a native `<dialog>` and switches between fit-to-screen and native 100% inside the same modal (`100 %` ↔ `Prispôsobiť` and localized equivalents). The same toggle also works by clicking the document itself; it never navigates to the raw WebP, so close/Escape and page context stay available in both modes. For Android cold starts, the full-resolution image `src` is assigned only after `showModal()` and the next `requestAnimationFrame()`, with explicit contain sizing in fit mode.

## Structured data / discovery
- Stable Person IDs, canonical/hreflang, sameAs identity links, credentials and publication Book nodes are preserved.
- Engineer's degree (Ing.) remains the neutral structured-data name; no MEng mapping.
- Peter scholarship/admission documents were removed from public Person `subjectOf`; Peter's diploma thesis remains.
- Public Person `subjectOf` is limited to professionally relevant records represented by visible professional content; archival-only author lookups and the 2019 conference-consultant corroboration are retained only in the internal evidence registry.
- Vendor brand “KUKA robots” was removed from Peter `knowsAbout`; tools/brands are not modeled as fields of work.
- `feed.xml` and `llms.txt` describe professional facts rather than an evidence/verification strategy.
- Internal `docs/evidence-registry-v0.2.4.md` retains archival provenance URLs and is excluded from the public build.

## Preserved
- Homepage and equal Lukáš/Peter identity hierarchy.
- Existing Experience content.
- Global navigation and mobile/desktop scrollspy.
- Credential lightbox, vCards and accessibility behavior; privacy-first consent remains available through the existing footer and Privacy-page Cookie settings controls.
- Canonical/hreflang structure and stable entity IDs.

## Release gate
- Automated regression: **48 PASS / 0 FAIL** on the current source tree; the added guardrail covers native-dialog sizing and the Android cold-start load order.
- Manual acceptance of the content/navigation baseline is complete. After deploy: production desktop/mobile smoke, 200%/400% zoom/reflow, footer/privacy Cookie settings, Android credential viewer cold-start plus toolbar/document-click fit/native-size toggle and close behavior and representative external-source opening.
