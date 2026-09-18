# JSON-LD entity contract — v0.2.2

Stable identifiers must not change between releases:

- WebSite: `https://likavcan.cz/#website`
- Lukáš Person: `https://likavcan.cz/lukas/#lukas-likavcan`
- Lukáš ProfilePage: `https://likavcan.cz/lukas/#profile-page`
- Peter Person: `https://likavcan.cz/peter/#peter-likavcan`
- Peter ProfilePage: `https://likavcan.cz/peter/#profile-page`
- MTF STU: `https://likavcan.cz/#mtf-stu`
- BIZZCOM: `https://likavcan.cz/#bizzcom`
- Porsche Werkzeugbau: `https://likavcan.cz/#porsche-werkzeugbau`

Rules:

1. Shared pages may mention both people but must not use `rel="me"` for either identity.
2. Individual profile pages may use `rel="me"` for verified external identity profiles.
3. `sameAs` is reserved for profiles/entities representing the same person; independent evidence belongs in `subjectOf`.
4. Publications use DOI URLs as `@id` where a verified DOI exists.
5. SK/EN/DE pages preserve the same Person `@id` and factual entity relationships.
6. Disambiguation is positive: profession, education, organization and identifiers; do not repeat negative references to namesakes in metadata.
