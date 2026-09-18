# RELEASE v0.2.2 — Entity Authority & Identity Consistency

Built directly from the audited v0.2.1 RC10 baseline.

## Implemented

- Added `jobTitle` to full Lukáš and Peter Person nodes across SK/EN/DE and structured-data mirrors.
- Preserved stable Person/ProfilePage `@id` values.
- Strengthened positive `disambiguatingDescription` with education and current organization context.
- Added 1:1, 4:3 and 16:9 Person image variants for both profiles in structured data.
- Added Lukáš ProfilePage links to the corresponding local project and publication entities.
- Expanded Publications JSON-LD from two entries to the normalized full journal-article set.
- Added MTF STU identity fingerprints to both Home profile cards.
- Removed ambiguous `rel="me"` from shared Home and Privacy pages; retained it on individual profile pages.
- Neutralized legacy “Lukáš-first” wording in current discovery/source-of-truth files.
- Expanded `llms.txt` with canonical Person URIs and verified identifiers.
- Added local Consent Mode v2 default-denied state before any external Google Analytics script loads.
- Updated changed sitemap entries to 2026-09-15.
- Refreshed documentation and outstanding production gates.

## Final consistency corrections

- Unified Peter’s canonical `jobTitle` across Home, SK/EN/DE profiles, structured-data mirror and `llms.txt`: `Simulation Specialist` + `Automation Engineer`.
- Changed all published ProfilePage `dateModified` values to timezone-aware ISO 8601 DateTime.
- Removed non-visible Home `mentions` and the Home-only Bezpečná elektrika Project node; Home now models only the two visible main Person entities.
- Localized Lukáš ProfilePage `hasPart` references for EN and DE routes.
- Corrected Atom feed chronology, unique release entry ID and the Publications update date.
- Removed the stray `tools/release_regression.py.tmp` artifact and added `*.tmp` to `.gitignore`.
- Extended release regression with cross-page Person consistency, ProfilePage DateTime, graph relevance/localized `hasPart`, feed consistency and release-tree hygiene checks.

## Intentionally not changed

- No redesign.
- No route changes.
- No negative “not the philosopher” metadata.
- No fabricated identifiers or unsupported project/publication claims for Peter.
- No crawler-policy change.
- No invented Google Analytics retention period or privacy contact data.
