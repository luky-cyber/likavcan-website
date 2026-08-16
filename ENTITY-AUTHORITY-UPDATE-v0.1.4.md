# Entity authority update – v0.1.4

Implemented 2026-08-16:

- Selected `knowsAbout` topics are now Schema.org `Thing` objects linked to verified Wikidata concepts.
- No Scopus/Web of Science author profile was added because no unambiguous public identifier for the materials-engineering Lukáš Likavčan was verified.
- `robots.txt` explicitly allows Google Search and OpenAI discovery/user agents; the wildcard remains open.
- Added `/feed.xml` (Atom) for profile/publication update discovery, plus feed autodiscovery links in HTML.
- Added a non-public documentation blueprint for future original expert articles; no empty/thin `/articles/` page was published.
