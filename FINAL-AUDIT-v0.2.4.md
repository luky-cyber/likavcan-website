# FINAL AUDIT v0.2.4 — Integrated Sources & Identity Consistency

## Editorial acceptance
- Homepage remains a five-second orientation layer: two engineers; Lukáš = materials/R&D, Peter = simulation/automation/robotics.
- No standalone “evidence”, “verification” or academic-proof section remains on either profile in SK/EN/DE.
- Sources are contextual and secondary to the professional narrative.
- Scholarships and admission lists are not visible profile achievements.
- Existing Experience sections remain intact.
- The last verification-style Branson link labels were reduced to factual STU graduate-profile source labels.
- Site-wide Methodology now consistently uses a shared SK/EN/DE voice (my/we/wir) without introducing an About-us layer.

## Lukáš
- Project No. 1341 is a normal 2015 research project on the Projects page, with one quiet MTF STU source link.
- PhD supervisor/source and Bc./Ing. thesis source links remain contextual inside Education.
- Publication source links are compact and attached to the relevant titles.
- Ultrasonic welding, injection moulding and CAE now have precise Wikidata topic links in `knowsAbout`; no extra visible SEO text was added.

## Peter
- 2016 diploma thesis is integrated in Education and links to the STU catalogue.
- Scholarship and admission records are retained only in the internal evidence registry.
- Main identity remains Simulation Specialist / Automation & Robotics Engineer.

## Final UX acceptance fixes
- Desktop profile-nav anchor clicks and scrollspy state are aligned for Lukáš and Peter in SK/EN/DE; the previous one-section-behind state is removed.
- Contact activates when the document reaches its real scroll end, including tall desktop viewports and mobile.
- Mobile dock behavior is regression-checked independently for both profiles and all languages.
- Homepage portraits are keyboard-focusable direct profile links; existing Profile, LinkedIn and vCard actions remain separate.
- Lukáš Education uses a 2×2 desktop grid and 1-column mobile grid, matching the row-readable pattern already used by other four-card profile groups.
- Long pages use a compact shared back-to-top control, visually consistent with the sister project pattern while using Likavcan.cz tokens; it is localized, keyboard-accessible, reduced-motion aware and offset above the mobile dock.
- Cookie settings use the existing footer and Privacy-page controls. The temporary floating Cookie-settings control was removed so Back-to-top remains the only floating utility.
- The E2/A credential stays inside one native `<dialog>` in both display modes: it opens fitted to the viewport; `100 %` or a click on the document switches to native size; `Prispôsobiť` or another document click returns to fit mode; and `×`/Escape remain available without creating a raw-image browser-history step. The first full-resolution load is deferred until `showModal()` + `requestAnimationFrame()` and fit mode explicitly uses 100% width/height with `object-fit: contain` to avoid the observed Android cold-start top-left crop.

## Entity / discovery / technical polish
- Stable Person `@id`, canonical/hreflang and `sameAs` boundaries preserved.
- Engineer's degree (Ing.) retained; no MEng mapping.
- Book nodes for selected Lukáš publications preserved.
- Public Person `subjectOf` is limited to professionally relevant records tied to visible professional content. Archival-only author lookups and the 2019 conference-consultant corroboration were removed from the public/mirror Person graph and retained in the excluded evidence registry.
- Standalone `structured-data/lukas.jsonld` and `peter.jsonld` now synchronize the selected canonical invariants with SK inline JSON-LD, including `dateModified` and `primaryImageOfPage`.
- DE Privacy information date synchronized to 15.09.2026. GA4 retention remains a TODO until the actual property setting is known.
- `apple-touch-icon.png` is a 180×180 derivative of the existing favicon and is linked root-relatively from all HTML pages. No PWA layer was added.
- Feed and llms wording remains factual rather than verification-oriented.

## Automated checks
`tools/release_regression.py` on the final working tree: **48 PASS / 0 FAIL**. The suite covers the integrated-source/content guardrails plus final polish, JSON-LD synchronization, Methodology voice, Apple touch icon, document-end Contact activation, desktop anchor/scrollspy alignment, mobile dock alignment, homepage portrait links, the row-readable Education grid, the localized mobile-dock-aware back-to-top control, footer/privacy consent controls, the in-viewer toolbar/document-click fit/native credential toggle, native-dialog Android cold-start load-order guardrail and final schema-purity/profile-metadata checks. The deployment ZIP is unpacked into a clean round-trip directory and must return the same **48 PASS / 0 FAIL** before delivery.

## Deployment acceptance
- The content/navigation baseline has been manually accepted on desktop and mobile.
- After GitHub Pages deploy, run a short production desktop/mobile smoke including footer/privacy Cookie settings and the Back-to-top control.
- Complete 200% and 400% zoom/reflow as the remaining accessibility spot check.
- Re-check the Android credential viewer from a cold browser start: first opening shows the full document fit-to-screen; `100 %` or a document click switches to native size without leaving the modal; `Prispôsobiť` or another document click returns to fit; `×` closes back to the profile. Also check one representative MTF STU/STU external link on production.

## Content freeze
After these checks, v0.2.4 is content-frozen. New visible identity material should be added only for a real new project, publication, role change, relevant credential or substantial technical case study.
