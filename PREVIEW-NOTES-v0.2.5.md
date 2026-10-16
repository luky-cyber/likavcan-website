# Likavcan.cz v0.2.5 preview

Local review build based on the deployed v0.2.4 RC15 baseline. This is **not** a GitHub release.

> Historical preview log: early-round bullets document the state at that review stage. Where they differ from the **Final release round**, the final-release state supersedes them (for example Lukáš homepage quick links now include ORCID).

## Implemented agreed changes

- Homepage SK/EN/DE: clickable names, concise role + employer anchors for both people.
- Homepage SK/EN/DE: visitor-first quick links `LinkedIn · vCard · Wikidata`, with Wikidata visually secondary.
- Stable Person IDs remain unchanged. Existing homepage JSON-LD graph was already using the canonical Person IDs, so it was not expanded unnecessarily.
- Lukáš SK/EN/DE: professional links reordered to `LinkedIn · vCard · Google Scholar · full ORCID · ResearchGate · Wikidata`.
- Peter SK/EN/DE: compact `LinkedIn · vCard · Wikidata` row; no artificial academic identities added.
- MTF STU Young Researcher project No. 1341 keeps its existing project card and now points to the supplied official 2015 MTF STU project overview PDF.
- Existing publication → Lukáš Person and Peter thesis → Peter Person structured-data links were audited and already correct, so they were left unchanged.
- Existing BIZZCOM, Porsche Werkzeugbau and MTF STU organization nodes were already consolidated, so no extra organization modelling was added.
- Profile `dateModified` updated because the profile pages were actually changed in this preview.

## Intentionally not added

No new SEO perex, evidence/verification sections, badges, meta keywords, blog content, extra Peter academic profiles, CV-only details, project proposals, Best Paper Award, or extra credential prominence.

## Review status

For local inspection in Acode / Visual Studio Code before any GitHub deployment.

## Review round 2 – natural language polish

- Removed the Lukáš “Technical support / Industrial Applications” card in SK/EN/DE.
- Rewrote visible profile copy in a simpler first-person voice across Lukáš and Peter.
- Simplified Peter’s simulation / online-offline programming descriptions and source labels.
- Simplified Lukáš’s materials, Branson, CAE, R&D and Bezpečná elektrika copy without expanding scope.
- Kept Wikidata last in link rows and visually neutral/non-accented. On the dark theme the link uses the neutral text colour rather than literal #000 so it remains readable.
- No new identity claims, employers, projects, credentials or homepage SEO paragraphs were added.


## Review round 3 – visual, entity and accessibility polish

- Lukáš hero intro now describes Branson work as solutions for different plastics-joining applications rather than simply “working on plastics welding”; EN/DE were updated semantically.
- Desktop-only profile hero scale was reduced for both Lukáš and Peter (portrait max 280 px; H1 max 4rem). Mobile sizing is unchanged.
- Wikidata is visually more subdued on both home cards and both profiles. Lukáš’s ORCID and ResearchGate links use the same subdued visual tier; the identity URLs and `rel=me` remain intact.
- Profile `<title>`, Open Graph/Twitter titles and descriptions now lead with the full professional identity and current employer context.
- Homepage Person stubs keep the same stable IDs and now carry concise `alternateName`, `worksFor`, `alumniOf` and `sameAs` context, plus minimal organization nodes. Homepage remains `WebSite` + `WebPage`.
- Bezpečná elektrika has a natural internal case-study route again from the Projects page while the external project website remains the primary CTA.
- The SK SFRT 1341 project card now uses the source-accurate role label `Zodpovedný riešiteľ` (EN/DE already conveyed the same meaning).
- Manual Cookie Settings opening now moves keyboard focus into the cookie dialog and restores focus to the trigger after closing. Automatic first-visit display still does not steal focus.
- Sitemap freshness dates were synchronized for the changed home/profile/project listing URLs; the Atom feed profile entries were refreshed without adding a preview release entry.
- Added an internal eight-query AI identity benchmark document for repeatable post-deploy checks.
- Social/OG artwork redesign, hosting/redirect infrastructure changes, CSS bundling, templating and second-home-portrait priority changes remain intentionally deferred.
- Before release: re-verify both current employments/roles and run the complete acceptance suite with 0 FAIL.


## Final release round

- Lukáš’s restored and updated ORCID is promoted back to the active identity tier. Homepage quick links are now `LinkedIn · vCard · ORCID · Wikidata`; the homepage ORCID label stays compact without the numeric identifier.
- On Lukáš’s profile, the full ORCID remains visible and active; ResearchGate and Wikidata remain visually secondary.
- The SFRT / Young Researcher project No. 1341 is now visible directly on Lukáš’s profile in SK/EN/DE, with the source-accurate role `Zodpovedný riešiteľ` / responsible researcher and the official MTF STU PDF next to the claim.
- Existing career, education, project and publication dates now expose machine-readable `<time datetime>` values without changing the visible copy.
- AI benchmark guardrails now check factual precision, including current vs historical employers, the SFRT role, project/employer separation and authorship wording.
- Profile `dateModified`, sitemap freshness and Atom feed entries were updated for the final v0.2.5 content.
