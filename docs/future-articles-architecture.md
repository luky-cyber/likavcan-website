# Future expert-content architecture

Do not publish an empty `/articles/` section. Create it only when the first original expert article is ready.

## Recommended URL model

- `/articles/<slug>/`
- Canonical URL points to itself.
- SK/EN/DE variants use hreflang only when a real translation exists.
- Each article must name one primary author and link that author to the stable Person `@id`:
  - Lukáš: `https://likavcan.cz/lukas/#lukas-likavcan`
  - Peter: `https://likavcan.cz/peter/#peter-likavcan`

## Structured data

Use `Article` or `TechArticle` for original expert notes, and `ScholarlyArticle` only for genuine scholarly publications. `author` must point to the stable Person `@id`. DOI/publisher URLs identify the work and must not be placed in `Person.sameAs`.

## Feed

`/feed.xml` is already present. When new expert content is published, add the newest entries to the feed with accurate `<updated>` timestamps.

## Scopus / Web of Science

Add a Scopus Author Profile or Web of Science Researcher Profile to `Person.sameAs` only after the exact author identifier has been independently verified. Do not add individual article URLs to `Person.sameAs`.
