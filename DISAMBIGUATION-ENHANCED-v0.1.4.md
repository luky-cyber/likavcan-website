# v0.1.4 – disambiguation enhanced

This patch preserves the v0.1.4 release number and strengthens entity disambiguation without changing public URLs or visual design.

## Changes
- Added `disambiguatingDescription` to Lukáš Likavčan and Peter Likavčan in SK/EN/DE inline JSON-LD.
- Added `mainEntityOfPage` from each `Person` entity back to the language-specific `ProfilePage`.
- Added visible positive identity statements on both profiles in SK/EN/DE.
- Added `CollectionPage.hasPart` and `mainEntity` references to already verified `ScholarlyArticle` entities on the publication pages.
- Kept `sameAs` limited to actual identity/profile URLs; publication URLs remain separate scholarly entities.
- No `speakable` markup and no negative naming of unrelated people was added.
