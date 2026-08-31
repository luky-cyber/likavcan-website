# Privacy completion checklist — Likavcan.cz v0.2.0

This is an internal release/compliance checklist, not legal advice and not public web content.

## Verified in the current implementation
- Optional Google Analytics 4 Measurement ID: `G-0F00N4385D`.
- GA4 is loaded only after the visitor chooses analytics consent.
- Advertising storage/signals and ad personalization are denied/disabled in the site code.
- Consent preference key: `likavcan_cookie_consent` with values `essential` or `all`.
- Revocation path sets analytics storage to denied, enables the GA disable flag, removes accessible first-party `_ga*` cookies and reloads the page.
- There is no contact form or user account system in the current static site.
- Public professional inquiry channel is LinkedIn; no new public email is declared.

## Must be verified from real operational/legal settings before adding to the public notice
- Exact controller contact details to publish.
- Exact GA4 data-retention setting for this property.
- Applicable legal wording/basis for each processing purpose.
- International-transfer wording and safeguards applicable to the actual Google setup.
- Data-subject rights wording and competent supervisory authority.
- Whether any Cloudflare/GitHub processing details need explicit disclosure beyond normal hosting delivery.

Do not fill unknown fields with defaults or guessed values.
