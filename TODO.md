# LIKAVCAN.CZ — TODO after v0.2.4

## Production gates
- [x] Content/navigation baseline manually accepted on desktop and mobile before deployment.
- [ ] Deploy v0.2.4 and run a short production desktop/mobile smoke, including footer/privacy Cookie settings and Back-to-top.
- [ ] Complete 200%/400% zoom/reflow spot check.
- [ ] Android production cold-start check: fully close/reopen the browser, then verify E2/A first opens fit-to-screen; `100 %` or a document click switches to native size inside the same viewer; `Prispôsobiť` or another document click returns to fit; `×` closes to the profile; desktop Escape.
- [ ] Request Search Console recrawl for Home, Lukáš, Peter and Publications.
- [ ] Re-test vCard import and QR scan on real Windows/iOS/Android devices only if contact handling changes in a future release.

## Privacy / infrastructure debt
- [ ] Verify the actual Google Analytics property retention setting before replacing generic Privacy wording; do not invent the value.
- [ ] Confirm a direct privacy contact channel only if the owner chooses to publish one.
- [ ] Review production security headers / redirects at the hosting layer before any infrastructure change.

## External identity authority
- [ ] Synchronize current facts on ResearchGate, ORCID, Google Scholar, LinkedIn and Wikidata.
- [ ] Seek an authoritative BIZZCOM profile/reference for Lukáš and an appropriate employer/profile reference for Peter.
- [ ] Add public source links only when they materially help explain a current project, education item, publication or professional claim.

## Policy
- [ ] `Google-Extended` remains intentionally allowed for discovery/grounding; revisit only if site policy changes.
- [ ] Keep institutional source URLs out of `Person.sameAs`; retain archival corroboration in the internal evidence registry.

## Content freeze
- [x] v0.2.4 content frozen for deployment; no further identity/evidence/SEO expansion.
- [ ] Add new visible profile content later only when there is a real new project, publication, role change, relevant credential or substantial technical case study.
