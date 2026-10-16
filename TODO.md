# LIKAVCAN.CZ — TODO after v0.2.5

## Release / production follow-up
- [ ] Deploy v0.2.5 from the verified final package and run a short production desktop/mobile smoke test.
- [ ] Verify the live homepage, `/lukas/`, `/peter/`, EN/DE variants, sitemap, ORCID/Wikidata links and Bezpečná elektrika case-study route.
- [ ] Verify manual Cookie Settings focus entry/return and first-visit consent behavior on production.
- [ ] Verify the E2/A credential viewer on desktop and Android cold start: first open fit-to-screen, native-size toggle, return to fit, close/Escape behavior.
- [ ] Complete 200%/400% zoom/reflow spot check.
- [ ] After successful production smoke, create/push tag `v0.2.5` and publish the GitHub Release.
- [ ] Request Google Search Console recrawl for materially changed canonical URLs; notify Bing/IndexNow only for genuinely changed URLs.

## Post-release observation
- [ ] Keep a 3–4 week content/metadata freeze unless a real defect is found.
- [ ] Re-run the eight-query AI identity benchmark after the freeze and compare entity resolution and factual precision.
- [ ] Watch specifically for SFRT 1341 being described as `zodpovedný riešiteľ` / responsible researcher, not `garant`; keep Branson/BIZZCOM chronology distinct.

## Privacy / infrastructure debt
- [ ] Verify the actual Google Analytics property retention setting before replacing generic Privacy wording; do not invent the value.
- [ ] Confirm a direct privacy contact channel only if the owner chooses to publish one.
- [ ] Review production security headers / redirects at the hosting layer before any infrastructure change.

## External identity authority
- [ ] Keep current facts synchronized on ORCID, Google Scholar, LinkedIn and Wikidata.
- [ ] ResearchGate remains a secondary/historical identity unless it is actively recovered and updated.
- [ ] Seek a natural authoritative BIZZCOM profile/reference for Lukáš and an appropriate employer/profile reference for Peter when available.
- [ ] Add public source links only when they materially support a current project, education item, publication or professional claim.

## Policy / future content
- [ ] `Google-Extended` remains intentionally allowed for discovery/grounding; revisit only if site policy changes.
- [ ] Keep institutional evidence URLs out of `Person.sameAs`; use `sameAs` only for identity-equivalent profiles.
- [ ] Add new visible profile content only for a real new project, publication, role change, relevant credential or substantial technical case study.
- [ ] Do not introduce Evidence / Authority / Verification sections, namesake-disambiguation copy, keyword stuffing or artificial Lukáš/Peter symmetry.
