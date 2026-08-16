# Final publish audit — Likavcan.cz v0.1.4

Audit date: 2026-08-16

## Applied correction

The following internal release-note files were added to `_config.yml` exclusions so GitHub Pages/Jekyll does not emit them into the public site:

- `FINAL-HOMEPAGE-IDENTITY-POLISH-v0.1.4.md`
- `IDENTITY-NOTE-PATCH-v0.1.4.md`
- `FINAL-PRODUCTION-CORRECTIONS-v0.1.4.md`

This audit report is also excluded from the production build.

## Final checks

- Canonical URLs: PASS — one canonical per public page; all 12 point to the intended `https://likavcan.cz/` URL.
- hreflang: PASS — `sk`, `en`, `de`, and `x-default` are present and mutually consistent on all 12 public pages.
- Person IDs: PASS — Lukáš uses `https://likavcan.cz/lukas/#lukas-likavcan` across SK/EN/DE; Peter uses `https://likavcan.cz/peter/#peter-likavcan` across SK/EN/DE.
- ProfilePage IDs: PASS — each localized profile page has its own localized `#profile-page` identifier while `mainEntity` points to the stable Person ID.
- `dateModified`: PASS — not present on ProfilePage nodes.
- Profile photos: PASS — JPG and WebP variants for both people exist and are 1000 × 1000 px.
- Structured image data: PASS — profile pages retain `Person.image` / `ImageObject` associations.
- Open Graph / Twitter images: PASS — profile pages use production `likavcan.cz` portrait URLs.
- JSON-LD syntax: PASS — all inline JSON-LD blocks on the 12 public pages parse successfully; standalone helper JSON-LD files also parse successfully.
- Sitemap: PASS — valid XML with exactly 12 public indexable URLs.
- Robots: PASS — public crawling is allowed and the production sitemap is declared. The Atom feed is also exposed for discovery.
- GA4 consent: PASS — Measurement ID `G-0F00N4385D`; analytics is loaded only after stored consent value `all`; `essential` does not load GA4; Google signals and ad personalization signals are disabled in the current configuration.
- GitHub Pages/Jekyll `_config.yml`: PASS — documentation, helper structured data, future placeholder sections, and release/audit notes are excluded.
- `CNAME`: PASS — `likavcan.cz`.
- Web manifest: PASS — valid JSON.
- Atom feed: PASS — valid XML.
- Favicon: PASS — non-empty file.
- Future Bezpečná elektrika pages: PASS — remain `noindex`.
- Local references: PASS — no missing local CSS, JS, image, or internal-page targets were found across the 12 public pages.

## Release conclusion

This package is technically consistent for publication as Likavcan.cz v0.1.4. No further entity-schema changes are recommended for this release before deployment. Stable Person IDs and the current public URL structure should remain unchanged after publication to allow search engines and other crawlers to consolidate the identity signals.
