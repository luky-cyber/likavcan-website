# Crawler policy — Likavcan.cz v0.2.0

## Current decision
- `OAI-SearchBot`: Allow
- `ChatGPT-User`: Allow
- `GPTBot`: Disallow
- `Googlebot`: Allow
- `Google-Extended`: Allow (intentional for now)

## Rationale
The OpenAI policy separates search/user retrieval from GPTBot training crawl. Google-Extended is a different trade-off: Google documents the token as controlling both use for future Gemini model training/model improvement and grounding from the Google Search index. Blocking it would therefore also opt the site out of those grounding uses, while not affecting inclusion/ranking in ordinary Google Search.

Revisit this policy if the project priority changes from discovery/grounding-first to a broader model-training opt-out.
