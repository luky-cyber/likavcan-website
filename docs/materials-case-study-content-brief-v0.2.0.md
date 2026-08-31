# v0.2.0 Materials case study — content brief

Status: internal draft only. Do not publish until role attribution and visual assets are confirmed.

Evidence basis: `docs/materials-case-study-evidence-map-v0.2.0.md`

## Purpose

Balance the current portfolio so that Lukáš's primary Materials Engineering / R&D identity has a proof-of-work page at least as concrete as the Bezpečná elektrika case study.

The page should not imitate a marketing client case study. It should present a publicly evidenced research problem and show the engineering logic behind the work.

## Recommended page identity

### SK

**Orientácia krátkych vlákien vo vstrekovaných termoplastoch**

Experiment, simulácia a overenie v rámci doktorandského výskumu a súvisiacich odborných publikácií.

### EN

**Fibre Orientation in Injection-Moulded Short-Fibre Reinforced Thermoplastics**

Experiment, simulation and verification across doctoral research and related publications.

### DE

**Faserorientierung in spritzgegossenen kurzfaserverstärkten Thermoplasten**

Experiment, Simulation und Verifikation im Rahmen der Promotionsforschung und zugehöriger Publikationen.

Suggested slug:

`/projects/fibre-orientation-injection-moulding/`

## Hero / positioning

Badge:

`Materials Research · Injection Moulding · Composite Materials`

Core message:

> Vstrekovanie termoplastu spevneného krátkymi vláknami nevytvára iba tvar dielu. Tok materiálu a procesné podmienky ovplyvňujú orientáciu výstuže a tým aj lokálnu anizotropiu materiálu. Verejne publikovaný výskum sa preto sústredil na porovnanie numericky predikovanej orientácie vlákien so skutočnou štruktúrou výstreku.

This is safe because it is directly supported by the primary papers.

## Suggested page flow

### 01 — Context

Headline:

**Proces vytvára aj materiálovú štruktúru**

Content direction:

- Short-fibre reinforced thermoplastics are locally anisotropic.
- Fibre orientation is not prescribed independently of the process; it is influenced by mould filling, process conditions and material behaviour.
- This creates a connection between manufacturing process, material structure and engineering properties.

Do not claim a specific property change unless the cited source demonstrates it.

### 02 — Engineering question

Headline:

**Ako overiť, že simulovaná orientácia zodpovedá reálnemu výstreku?**

Core idea:

A contour plot from injection-moulding simulation is a model output. The engineering problem is how to compare that prediction with the real microstructure.

Reusable pull quote:

> Výsledok solvera ešte nie je engineering conclusion.

Preferred English final form:

> A solver result is not automatically an engineering conclusion.

This should be positioned as an editorial/engineering principle derived from the workflow, not as a quotation from a publication.

### 03 — Research workflow

Original diagram candidate:

**LL-FIG-01 — From process to verification**

`Injection moulding parameters -> simulated fibre orientation -> selected sample locations -> metallographic sections -> stereological/materialographic evaluation -> comparison -> interpretation`

Copy direction:

- Numerical model predicts orientation.
- Experimental sample provides physical evidence.
- Both need a common comparison quantity/representation.
- Agreement or disagreement is interpreted in context.

### 04 — Numerical representation

Headline:

**Orientáciu treba opísať, nie iba zobraziť**

Safe details from the 2014 primary paper:

- Moldex3D was used in the published study.
- X/Y/Z orientation components were used in relation to a second-order orientation tensor.
- The tensor representation provides a compact description of fibre-orientation distribution.

Do not turn this into a general software endorsement.

Original diagram candidate:

**LL-FIG-02 — Orientation tensor as a comparison bridge**

Use a conceptual schematic rather than reproducing the publisher's tensor figures.

### 05 — Experimental evaluation

Headline:

**Materialografia ako fyzická kontrola modelu**

Safe details:

- Samples were metallographically prepared.
- Light microscopy / materialographic sections were used in the published examples.
- Stereological methods were used to estimate degree/orientation characteristics of fibres.
- In the 2014 example, an injection-moulded PA6 gear with glass-fibre reinforcement was analysed.

Important:

The PA6 gear is a published example, not the whole dissertation.

### 06 — Comparison

Headline:

**Model a vzorka musia hovoriť porovnateľným jazykom**

Safe claim:

The published workflow compares the experimentally estimated degree of orientation with orientation information derived from simulation. The 2016 paper reports approximate agreement for the investigated samples.

Avoid:

- "the model was validated" without scope.
- "simulation accurately predicts fibre orientation" as a universal claim.

Preferred wording:

> V publikovaných vzorkách bolo možné numerické výsledky porovnať s materialografickým vyhodnotením a posúdiť mieru zhody medzi modelom a reálnou štruktúrou.

### 07 — Engineering interpretation

Headline:

**Dôležitá nie je iba zhoda, ale dôvod zhody alebo rozdielu**

Editorial interpretation, clearly marked as the site's engineering approach:

- assumptions matter;
- sample location matters;
- process conditions matter;
- experimental method has its own uncertainty;
- model verification is iterative rather than binary.

Do not attribute these exact sentences to a paper unless sourced.

### 08 — What this work demonstrates

Use evidence-backed competency labels, not skill percentages:

- Materials engineering
- Short-fibre reinforced thermoplastics
- Injection moulding
- Composite microstructure
- Numerical simulation
- Materialography / stereology
- Simulation-to-experiment comparison
- Technical documentation and interpretation

### 09 — Limitations

Recommended visible section:

**Hranice tejto case study**

Text direction:

- The page summarizes publicly available doctoral/co-authored research.
- It is not a reproduction of the full dissertation.
- Individual published examples do not establish universal behaviour for all thermoplastics, fibre fractions, geometries or process settings.
- Co-authored work is described collectively unless Lukáš's exact contribution is documented.
- No confidential industrial data are included.

This section is important and should remain visible, not hidden in Methodology.

### 10 — Evidence / related publications

Primary cards:

1. **Estimation of Fibre Orientation in Injection Moulding Plastics Parts**
   - Materials Science Forum 891, 55–59 (2017)
   - Maroš Martinkovič, Lukáš Likavčan
   - DOI 10.4028/www.scientific.net/MSF.891.55

2. **Comparison of Fibre Orientation Using Simulation Software and Materialography**
   - Acta Technica Corviniensis – Bulletin of Engineering 9(1), 71–77 (2016)
   - Lukáš Likavčan, Maroš Martinkovič

3. **Ways of Comparation of the Fibre Orientation in Injection Moulding Parts**
   - Research Papers MTF STU 22, Special Number, 109–114 (2014)
   - Lukáš Likavčan, Maroš Martinkovič, Jozef Bílik, Miroslav Košík
   - DOI 10.2478/rput-2014-0016

4. **Possibilities of Evaluation of the Fibre Orientation in Injection Moulding Parts**
   - Technological Engineering 10(2), 26–28 (2013)
   - Maroš Martinkovič, Lukáš Likavčan
   - DOI 10.2478/teen-2013-0018

Academic evidence card:

- 2017 doctoral dissertation and successful defence at MTF STU.

Do not overload the case study with all 21 bibliography records.

### 11 — Related work

Secondary links only:

- apparent viscosity / fibre fraction in polypropylene;
- CAX-assisted injection mould design;
- plastics-processing textbooks;
- full Publications page.

## Homepage change when this page exists

Replace the current Materials card CTA from only `/publications/` to the new case study.

Recommended hierarchy:

**Materials Research**

Fibre orientation in injection-moulded composites — simulation, materialography and experimental comparison.

Buttons:

- `Case study`
- `Publications`

Keep Bezpečná elektrika as the second Selected Work card.

## Projects index change when this page exists

The Materials project should appear before Bezpečná elektrika because it supports the primary professional identity.

Suggested order:

1. Materials Research — fibre orientation / injection moulding
2. Bezpečná elektrika — independent engineering project

Do not call the academic research a commercial client project.

## Lukáš profile change when this page exists

In the Materials / research section, add a single clear CTA:

`View research case study`

Do not duplicate the full case-study narrative on the profile page.

## Machine-readable strategy

- Preserve stable Person ID.
- Do not create a new Person identity.
- Do not add the case-study URL to `sameAs`.
- Connect through `about` / `mainEntity` / `subjectOf` semantics as appropriate after the final page model is decided.
- Publication DOI entities remain separate works.

## Information needed from Lukáš before public drafting is finalized

### A. Personal contribution

For the core fibre-orientation work, confirm which of these accurately describe your own role:

- injection-moulding simulation setup;
- interpretation of Moldex3D results;
- sample preparation;
- optical microscopy / image acquisition;
- stereological/materialographic evaluation;
- data comparison;
- experiment planning;
- paper writing;
- figure preparation;
- dissertation integration.

Only confirmed items should be written in first person.

### B. Visual material

Ideal source files, if available and publishable:

- original Moldex3D simulation screenshot/export;
- original microscopy image;
- photo of metallographic sample;
- dissertation figure created by Lukáš;
- original process/workflow sketch.

Do not use publisher page screenshots as portfolio visuals by default.

### C. Results

If there are dissertation results that are not in the public papers and are suitable for publication, provide the relevant excerpt/table/figure or the dissertation PDF before including them.

## Release scope recommendation

This case study alone is sufficient to justify **v0.2.0 — Materials Proof of Work**.

Do not bundle it with search, dark mode, a new blog, CV, certificates or service features.
