# RELEASE v0.2.3-rc5 — Fit-to-Screen Credential Preview

Status: release candidate; not yet a final production release.

## Scope

- Preserves the v0.2.3-rc4 compact desktop header, right-aligned secondary profile navigation and shared desktop/mobile scrollspy.
- Preserves the responsive 4 / 2 / 1 reverse-chronological qualification grid without an inline certificate thumbnail.
- Changes the E2/A certificate CTA from a raw-image first step to a viewport-fitted overlay preview in SK/EN/DE.
- The first click shows the whole public redacted certificate within the available screen area; a deliberate second click on the document opens the original WebP at full resolution.
- The preview can be closed with the × control, by clicking outside the document, or with Escape on a keyboard.
- Keeps the direct image href as a no-JavaScript fallback.
- Keeps the watermark “VEREJNÁ KÓPIA · REDIGOVANÉ” baked into the public certificate image.
- Keeps stable Person IDs, E2/A structured data, canonical/hreflang, consent/privacy behavior and the v0.2.2 entity-authority foundation intact.

## Versioning

v0.2.2 remains the approved release baseline. v0.2.3-rc5 supersedes rc4 as the current v0.2.3 candidate after Android acceptance testing identified that a raw WebP link opens at natural image size instead of presenting a screen-fitted first view.
