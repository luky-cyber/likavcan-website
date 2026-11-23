# LIKAVCAN.CZ — TODO after v0.2.6

## Release / production follow-up
- [ ] Deploy v0.2.6 from the verified final package through the existing GitHub Pages `main` workflow.
- [ ] Verify the live homepage, `/lukas/`, `/peter/`, EN/DE variants, sitemap and feed after deployment.
- [ ] Verify that the stable Person IDs remain unchanged and that BIZZCOM/Porsche are current while Branson remains historical.
- [ ] Verify Peter remains `Simulation Specialist` in the live profile/discovery signals and that no authored work is represented as `Person.subjectOf`.
- [ ] Run the standard production desktop/mobile smoke test, credential-viewer check and a short cookie/keyboard sanity check.
- [ ] After successful production smoke, create/push immutable tag `v0.2.6` and publish the GitHub Release.
- [ ] Request recrawl only for materially changed canonical profile URLs; do not repeatedly resubmit unchanged URLs.

## Post-release observation
- [ ] Allow time for recrawl/reindexing before attributing any AI/search behaviour to v0.2.6.
- [ ] Re-run the same identity benchmark prompts after a reasonable indexing interval and compare against the November 2026 baseline.
- [ ] Watch for downstream model enrichment without automatically treating every hallucination as a website defect.
- [ ] Preserve the guardrails: one Lukáš Person, Bezpečná elektrika as his project, BIZZCOM current, Branson historical, Peter primarily Simulation Specialist, SFRT role `Zodpovedný riešiteľ`.

## Accessibility / runtime QA debt
- [ ] Test first-visit cookie focus order in a real browser before changing working JS behaviour.
- [ ] Measure mobile language-switcher target sizes and spacing in actual rendered layouts.
- [ ] Repeat 200%/400% zoom and reflow spot checks on production.
- [ ] Review generic ARIA grouping only as part of a focused accessibility pass, not as an identity-release hotfix.

## vCard / privacy / infrastructure debt
- [ ] Test the current vCard import on iOS, Android, Google Contacts and Outlook before changing encoding/version format.
- [ ] Verify the actual Google Analytics retention setting before replacing generic Privacy wording; do not invent the value.
- [ ] Publish a direct privacy contact channel only if the owner chooses and confirms it.
- [ ] Keep GitHub Pages + Cloudflare DNS-only unchanged unless a separate infrastructure review demonstrates a real need.

## External identity authority
- [ ] Periodically verify that LinkedIn, ORCID, Google Scholar, ResearchGate and Wikidata links still identify the intended person.
- [ ] Keep institutional evidence URLs out of `Person.sameAs`; use `sameAs` only for identity-equivalent profiles.
- [ ] Prefer current canonical `likavcan.cz` profiles over retired Google Sites.
- [ ] Add new external profiles only when they are real, maintained and useful; do not create accounts solely for SEO.

## Policy / future content
- [ ] Add visible content only for a real new project, publication, role change, relevant credential or substantial technical case study.
- [ ] Do not introduce Evidence / Authority / Verification sections, namesake-disambiguation copy, SEO FAQ, keyword stuffing, employer-logo walls, trust badges or artificial Lukáš/Peter symmetry.
- [ ] Keep human-facing presentation primary and machine/entity optimization mostly invisible.
