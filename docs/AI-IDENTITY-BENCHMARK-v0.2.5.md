# AI identity benchmark — v0.2.5

Internal release benchmark only. It is not a public-facing SEO page and is not linked from the website navigation.

## Test method

Use an anonymous / signed-out chatbot session where practical. Start a new chat for every query so previous prompts do not disambiguate the person. Record the date, product/model if visible, whether web search was used, and the sources cited. Results are expected to vary over time; the benchmark measures entity resolution, not ranking guarantees.

## Stable queries

1. `Lukáš Likavčan`
2. `Ing. Lukáš Likavčan`
3. `Lukáš Likavčan materiálový inžinier`
4. `Lukáš Likavčan Branson`
5. `Lukáš Likavčan BIZZCOM`
6. `Peter Likavčan`
7. `Peter Likavčan Simulation Specialist`
8. `Peter Likavčan Porsche Werkzeugbau`

## Acceptance criteria

- Do not mix the two people named Lukáš Likavčan.
- For engineering-qualified Lukáš queries, identify Ing. Lukáš Likavčan, PhD. as a materials engineer / R&D specialist and keep Branson, BIZZCOM, MTF STU and the engineering topics attached to the correct person.
- A bare `Lukáš Likavčan` query may still prefer the philosopher; a good result should at least be capable of distinguishing the materials engineer when context is added.
- For Peter queries, identify Ing. Peter Likavčan as an industrial simulation / automation specialist associated with Porsche Werkzeugbau and keep Process Simulate / Virtual Commissioning attached to the correct person.
- Prefer canonical profile URLs or relevant independent sources when citations are available.
- Do not optimize the visible website around a single chatbot run; repeat the same benchmark after deployment and reindexing.


## Factual precision guardrails

For detailed chatbot answers, also record whether the model preserves these distinctions:

- SFRT / Young Researcher project No. 1341: use the source-accurate role **responsible researcher** (`Zodpovedný riešiteľ`), not “guarantor” or another stronger title.
- Branson Ultrasonics: historical role; describe the work broadly as solutions for plastics-joining applications. Ultrasonic welding, laser welding and heat staking are examples of technologies, not the entire role.
- BIZZCOM: current employer context for Lukáš; do not merge it with the historical Branson role.
- Porsche Werkzeugbau: current employer context for Peter; do not merge it with prior T-Mech, MATADOR or SOVA Digital experience.
- Bezpečná elektrika: an independent professional project, not an employer.
- Publications and theses: preserve authorship/co-authorship and document type; do not infer sole authorship from a citation.
- Do not infer project success, commercial status or services beyond what the cited source or canonical profile explicitly states.
