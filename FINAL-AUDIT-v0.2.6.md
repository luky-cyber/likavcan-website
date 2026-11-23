# FINAL AUDIT — Likavcan.cz v0.2.6

Prepared: 2026-11-23

## Release status

Final deploy package prepared from the independently verified `Likavcan-Website-v0.2.6-Candidate-R2.zip`.

Production baseline:

- v0.2.5 release commit: `c6388d9 Release v0.2.5`
- immutable tag `v0.2.5` remains on the original release commit and must not be moved
- current `main` cleanup baseline used for v0.2.6 preparation: `0a4b6ad9368383a15c4d56b9a16050c6afcb50ba`

Candidate R2 SHA-256:

`05ca5b7281ead6db9b95ac73c9f68cbae324341dc83acfb0732568e1bef833e7`

No commit, push, tag or production deployment was performed while preparing this final package.

## Audit sequence

The release decision used separated review stages to reduce confirmation bias:

1. **Public baseline:** clean-chat identity resolution was checked before the candidate ZIP was shown.
2. **Blind audit:** ZIP-only review without release goals/Handoff.
3. **Informed audit:** blind findings were reassessed against v0.2.5, the November 2026 AI identity benchmark and explicit project guardrails.
4. **R2 verification:** a separate verification pass compared Candidate R2 against the original candidate and independently reproduced the regression suite.

Independent Candidate R2 verification result:

- **PASS — VERIFIED**
- **54 PASS / 0 FAIL**
- **0 release-blocking problems**
- **11 planned changed files**
- **0 unplanned changes**
- **0 missing files**

## Accepted informed-audit corrections

### 1. Authorship semantics

- Removed Lukáš's authored foaming-polymers article from `Person.subjectOf`.
- Preserved the canonical `ScholarlyArticle` on the publications pages with all five authors.
- Removed Peter's diploma thesis from `Person.subjectOf`.
- Preserved/modelled the thesis as a standalone `CreativeWork` with `author` pointing to Peter's stable Person ID.

### 2. Peter primary-title consistency

- `llms.txt`: `Simulation Specialist` remains the only primary job title.
- `peter/peter-likavcan.vcf`: `TITLE:Simulation Specialist`.
- Automation/robotics remain expertise areas, not parallel official job titles.

### 3. Regression protection

Added targeted checks for:

- authored works not being represented as works about the Person;
- preservation of all five co-authors of the Lukáš publication;
- standalone authored Peter thesis;
- Peter title consistency in discovery text and vCard;
- existing v0.2.6 entity/image/country/job-title invariants.

## Informed-audit findings intentionally not implemented in v0.2.6

The following were explicitly deferred or rejected rather than silently ignored:

- **vCard encoding change — DEFER:** requires real interoperability testing on actual clients before altering the format.
- **First-visit cookie focus — DEFER:** static review did not prove a runtime failure; test in a browser before changing working JS behaviour.
- **Mobile language target sizes / ARIA cleanup — DEFER:** accessibility items should be verified in real rendering and handled as a focused accessibility patch if confirmed.
- **Privacy/GA4 values — DEFER:** do not invent retention settings or a contact channel; use verified operational data only.
- **Extra public proof/evidence content — REJECT:** would conflict with the human-first design and risk an evidence-wall presentation.
- **Artificial Lukáš/Peter symmetry or portrait redesign — REJECT:** not an identity defect.
- **Visible namesake/“not the philosopher” copy — REJECT:** positive professional identity signals are preferred.
- **SEO FAQ, keyword stuffing, employer-logo wall, new trust/verification badges — REJECT.**
- **Hosting/redirect architecture changes — REJECT for this release:** GitHub Pages + Cloudflare DNS-only remain unchanged.

## Invariants preserved

- Homepage headline: `Dva inžinieri. Materiály a simulácie.`
- Lukáš Person ID: `https://likavcan.cz/lukas/#lukas-likavcan`
- Peter Person ID: `https://likavcan.cz/peter/#peter-likavcan`
- WebSite ID: `https://likavcan.cz/#website`
- MTF STU ID: `https://likavcan.cz/#mtf-stu`
- Bezpečná elektrika project ID: `https://bezpecnaelektrika.sk/#project`
- Homepage remains `WebSite` + `WebPage`, not `ProfilePage`.
- BIZZCOM is current and Branson historical for Lukáš.
- Peter remains primarily `Simulation Specialist`.
- Bezpečná elektrika remains a project of the same Lukáš Person, not an employer or second Person.
- SFRT 1341 role remains `Zodpovedný riešiteľ`, with conservative translations.
- No fake academic identities or new external profiles were created.
- No CSS, JavaScript, homepage, portrait, privacy-policy or hosting change is part of the R2 public-site patch.

## Final package delta from Candidate R2

The final deploy package keeps the independently verified R2 public-site payload unchanged. Finalization adds/updates only internal release-management material:

- `RELEASE-v0.2.6.md`
- `FINAL-AUDIT-v0.2.6.md`
- `_config.yml` Jekyll exclusions for those internal documents
- `README.md` current-release state
- `TODO.md` post-v0.2.6 follow-up state
- release-documentation hygiene guardrail in `tools/release_regression.py`
- `PREVIEW-NOTES-v0.2.5.md` restored to the exact historical `main` baseline after the pre-staging Git diff exposed that an earlier reconstructed candidate had omitted its final-release-round block

The `PREVIEW-NOTES-v0.2.5.md` correction is historical/internal only and is excluded from Jekyll output. It preserves v0.2.5 history rather than changing v0.2.6 public content.

No public HTML, CSS, JavaScript, image, sitemap, feed, vCard, `llms.txt` or structured-data payload is changed during finalization beyond the already verified Candidate R2 state.

## Pre-staging baseline correction

During the mandatory local `git diff` review against `main` commit `0a4b6ad9368383a15c4d56b9a16050c6afcb50ba`, the first Deploy-Final archive was found to contain a stale reconstructed copy of `PREVIEW-NOTES-v0.2.5.md` with the historical **Final release round** block missing. The file is not part of the v0.2.6 public payload and was never intended to change.

Deploy Final R2 restores that file to the exact `main` historical baseline before staging. The superseded first Deploy-Final archive must not be deployed or used for tagging.

## Final regression result

After adding the release-management documentation and updating the historical/current release-hygiene checks, the final deploy tree passes:

`55 PASS / 0 FAIL`

The additional PASS is the v0.2.6 release-documentation/Jekyll-exclusion guardrail.

## Deployment gate

The package is ready for manual deployment through the existing GitHub Pages `main` workflow only after:

1. clean local `main` and pull from origin;
2. copy without `/MIR`;
3. inspect `git status`, `git diff --stat` and full diff;
4. run `py .\tools\release_regression.py` and require `0 FAIL`;
5. inspect staged diff and run `git diff --cached --check`;
6. commit and push;
7. wait for successful GitHub Pages deployment;
8. run production smoke checks;
9. only then create immutable tag `v0.2.6`.

Rollback, if needed after deployment, remains `git revert HEAD` followed by push.
