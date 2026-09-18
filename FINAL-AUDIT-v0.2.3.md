# FINAL AUDIT — v0.2.3-rc5

## Automated acceptance

Run `python tools/release_regression.py` from the package root.

Expected result for this candidate: **38 PASS / 0 FAIL**.

## v0.2.3-rc5-specific checks

- Desktop profile navigation remains compact, sticky and synchronized with the mobile dock scrollspy.
- Lukáš progresses Profile → Projects → Publications → Contact.
- Peter progresses Profile → Career → Expertise → Contact, with Education grouped under Career.
- Qualification cards remain reverse chronological and use a responsive 4 / 2 / 1 grid.
- No certificate thumbnail is embedded in the qualification card.
- The localized certificate CTA retains a direct WebP href for graceful fallback but is enhanced by JavaScript with an accessible dialog-style preview.
- First interaction opens the entire redacted certificate fitted within the viewport rather than the raw natural-size image.
- A second deliberate click on the certificate opens the full-resolution WebP.
- The preview supports × close, outside-click close and Escape close; body scrolling is locked while open.
- The public certificate image retains the baked-in “VEREJNÁ KÓPIA · REDIGOVANÉ” watermark and personal-data redactions.
- E2/A remains present in Person structured data.
- v0.2.3 content/CTA, chronology, entity-authority, consent and language guardrails remain intact.

## Manual gates

- Android: tap “Zobraziť verejnú kópiu osvedčenia” and confirm the first view contains the entire document inside the screen rather than opening a cropped/natural-size raw image.
- Android: tap the displayed document and confirm the full-resolution image opens only on this second action.
- Android: verify the preview closes correctly with × and outside tap.
- Desktop: verify the same preview behavior and Escape-to-close.
- Desktop: scroll both profiles and confirm active-section highlighting follows the reader.
- Qualification grid: verify 4 cards on a wide desktop, 2 + 2 at narrower widths and one column on mobile.
- 200%/400% browser zoom acceptance.
- Normal production smoke test after deployment.

This document describes a release candidate, not a final production approval.
