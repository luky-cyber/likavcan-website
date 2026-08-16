# Digital authority update – v0.1.4

This update strengthens external evidence and employer-context links for Lukáš Likavčan and Peter Likavčan.

## Lukáš Likavčan
- Added STU graduate-profile evidence explicitly linking Lukáš Likavčan, PhD. with Branson Ultrasonics.
- Added MTF STU Student Scientific Conference 2019 evidence linking him with Branson Ultrasonics and STTIr laser welding.
- Added official BIZZCOM R&D and Branson/Emerson technology-context links.
- Modelled BIZZCOM as a separate Organization entity; Person.worksFor points to its stable @id.

## Peter Likavčan
- Replaced older thesis/archive links with the current STU KIS permanent thesis and author-catalogue URLs.
- Added official Porsche Werkzeugbau Simulation and Virtual Commissioning, MATADOR Automation Simulations, and t-mech Simulation/Offline Programming context links.
- Modelled Porsche Werkzeugbau as a separate Organization entity; Person.worksFor points to its stable @id.

## Entity architecture rule
Direct university records about a person are included under Person.subjectOf. Employer technology/service pages are visible professional-context links and are not misrepresented as direct evidence that the person worked on a specific project. Identity profiles remain under Person.sameAs.
