# Final production corrections — v0.1.4

Applied before production release:

1. Removed optional `dateModified` from all six `ProfilePage` JSON-LD objects and standalone profile JSON-LD files.
2. Restored precise domain terms alongside linked Wikidata concepts: `Polymer processing` for Lukáš and `Digital factory` for Peter. Wikidata-linked `Polymer science` and `Digital twin` remain as additional, distinct concepts.
3. Simplified visible identity notes in SK/EN/DE by removing crawler-oriented wording about other people being separate entities. Machine-readable `disambiguatingDescription` remains unchanged.

No public URLs, canonical URLs, hreflang values, stable Person `@id`s, design, or verified external references were changed.
