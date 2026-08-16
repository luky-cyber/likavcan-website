# Entity identity update – 2026-08-16

This repository has been updated to strengthen the machine-readable and human-visible digital identities of two distinct people:

- Lukáš Likavčan — materials engineer / R&D specialist
- Peter Likavčan — simulation specialist / industrial automation

## Implemented

- Stable canonical Person IDs shared across SK/EN/DE pages.
- ProfilePage -> Person JSON-LD expressed as an @graph.
- Clean Person.name values; academic titles moved to honorific/alternateName fields.
- Shared MTF STU CollegeOrUniversity entity.
- Explicit homepage disambiguation of both people.
- Stronger identity paragraphs on both profile pages.
- Visible independent-source sections on both profiles.
- Peter: STU permanent record of 2016 master's thesis, STU author catalogue (2014 + 2016 works), and MTF STU 2014 admission list.
- Lukáš: MTF STU PhD defence record, STU publication catalogue, STU article record, ORCID, Scholar, LinkedIn and Wikidata.
- Publication collection linked to Lukáš's stable Person ID.
- ScholarlyArticle JSON-LD and DOI links for two publications with independently verified DOIs.
- dateModified on profile pages.

## Deliberately not implemented yet

- Person.image / ImageObject. Photos were intentionally deferred.
- Additional third-party profile creation. Existing trustworthy sources are preferred over artificial microsites.

## Photo follow-up

When portraits are added, use crawlable 1:1, 4:3 and 16:9 variants and add one stable ImageObject per person, then reference it from that person's Person.image property.

## Source policy

`sameAs` is restricted to URLs that represent the same person. Pages that merely document a thesis, defence or publication are represented through `subjectOf` / CreativeWork rather than `sameAs`.
