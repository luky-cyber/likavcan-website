# Materials/R&D case study — evidence map for v0.2.0

Status: planning document only; not public content.

## Recommended case-study topic

**Fibre orientation in injection-moulded short-fibre reinforced thermoplastics**

Working SK title:

> Orientácia krátkych vlákien vo vstrekovaných termoplastoch: experiment, simulácia a overenie

Working EN title:

> Fibre Orientation in Injection-Moulded Short-Fibre Reinforced Thermoplastics: Experiment, Simulation and Verification

Working DE title:

> Faserorientierung in spritzgegossenen kurzfaserverstärkten Thermoplasten: Experiment, Simulation und Verifikation

Suggested future URL:

`/projects/fibre-orientation-injection-moulding/`

## Why this is the strongest first Materials case study

- Directly supports the primary Materials Engineering / R&D identity.
- Closely matches the 2017 doctoral dissertation topic.
- Has multiple independent public evidence sources across 2013–2017.
- Demonstrates the full engineering chain: manufacturing process -> material structure -> experiment -> numerical simulation -> comparison -> interpretation.
- Can be published without customer/NDA data.
- Allows original diagrams to be created without copying publisher figures.
- Creates a natural bridge between `/projects/`, `/publications/`, `/lukas/` and future Engineering Notes.

## Evidence hierarchy

Use sources in this order when claims differ:

1. STU / MTF STU official records and primary full-text papers.
2. Publisher / DOI landing pages and publisher full text.
3. Other journal-host full texts.
4. Professional academic profiles only as supporting discovery evidence.

Do not use a secondary database to override primary bibliographic or experimental data.

## Core evidence set

### E1 — Doctoral dissertation / academic scope

Claim safely supported:

- Lukáš Likavčan completed a doctoral dissertation in 2017 on the influence of injection-moulding process parameters on the properties of short-fibre reinforced thermoplastic mouldings.
- The doctoral programme was Mechanical Engineering Technologies and Materials at MTF STU.
- Supervisor: Maroš Martinkovič.
- The dissertation is recorded as 128 pages in the STU publication record.
- MTF STU separately confirms the successful dissertation defence in 2017.

Primary evidence:

- https://www.mtf.stuba.sk/sk/diani-na-mtf/aktuality/oznam-o-uspesnych-obhajobach-na-uvte-4.html?page_id=13318
- https://www.mtf.stuba.sk/buxus/docs/UVTE/publikacie/UVTE_Publikacie_2017.pdf

Publication wording rule:

Do not infer experimental details from the dissertation title alone. Detailed methods/results must be supported by a paper/full thesis or supplied source material.

### E2 — Simulation vs. experimental fibre orientation (2014)

Publication:

**Ways of Comparation of the Fibre Orientation in Injection Moulding Parts**

Safe claims:

- Fibre orientation in short-fibre reinforced thermoplastics is influenced by injection-moulding process parameters.
- The research compared fibre-orientation information from numerical simulation with experimental evaluation.
- Moldex3D was used for the injection-moulding simulation in this paper.
- Simulation output was represented using components of a second-order orientation tensor.
- Stereological metallography was used as the experimental method for estimating fibre orientation.
- The paper explicitly frames experimental comparison as a way to verify and potentially optimize a numerical simulation model.
- The published example analysed an injection-moulded PA6 gear reinforced with 30% glass fibres and used metallographic sections from a gear tooth.

Primary evidence:

- https://www.mtf.stuba.sk/buxus/docs/doc/casopis_Vedecke_prace/33SN/4-Likavcan.pdf
- DOI: https://doi.org/10.2478/rput-2014-0016

Important limitation:

Do not generalize the specific orientation value or gear geometry into a universal conclusion. If the numerical value is ever shown, label it explicitly as the published example/sample result.

### E3 — Earlier experimental verification approach (2013)

Publication:

**Possibilities of Evaluation of the Fibre Orientation in Injection Moulding Parts**

Safe claims:

- The work investigated ways to compare real-sample fibre orientation with simulation results.
- Stereological metallography was used for experimental estimation of short-glass-fibre orientation.
- The method was proposed as an experimental verification route for a numerical injection-moulding model.

Evidence:

- DOI: https://doi.org/10.2478/teen-2013-0018
- STU publication record / primary publication evidence as used in the bibliography master.

### E4 — Comparison using simulation software and materialography (2016)

Publication:

**Comparison of Fibre Orientation Using Simulation Software and Materialography**

Safe claims:

- Short-fibre reinforced thermoplastics exhibit locally varying anisotropy because fibre orientation depends on flow, processing conditions and material rheology.
- The paper compares numerical fibre-orientation predictions with materialographic observations.
- Published results report approximate agreement between the degree of orientation in real samples and the simulation software for the investigated samples.
- The paper demonstrates comparison at multiple sample locations/directions rather than treating a simulation contour as self-validating evidence.

Primary evidence:

- https://acta.fih.upt.ro/pdf/2016-1/ACTA-2016-1-11.pdf

Caution:

The abstract contains broader references to FE stiffness/strength modelling. Do not make this a main claim in the case study unless the exact workflow and authorship contribution can be verified from the full paper and is relevant to Lukáš's role.

### E5 — 2017 estimation paper

Publication:

**Estimation of Fibre Orientation in Injection Moulding Plastics Parts**

Safe claims:

- The paper focuses on estimating fibre orientation in injection-moulded parts and comparing experimental results with numerical simulation.
- Stereological metallography is used for experimental estimation.
- The paper connects preferred fibre orientation with anisotropic microstructure in short-glass-fibre reinforced thermoplastics.

Primary evidence:

- https://www.scientific.net/MSF.891.55
- DOI: https://doi.org/10.4028/www.scientific.net/MSF.891.55

## Additional supporting evidence

### Conference work

Relevant public conference records include:

- *Ways of Comparation of the Fibre Orientation in Injection Moulding Parts*, IDS 2014, pp. 117–123.
- *Possibilities of Simulation of Injection Moulding Parts*, 2014, pp. 91–92.
- *Estimation of Fibre Orientation in Injection Moulding Plastics Parts*, Metallography '16.

These support continuity of the research topic but should not be treated as separate results when they overlap with later journal papers.

### Related materials/process publications

Potential secondary links from the case study:

- *Determination of Apparent Viscosity as Function of Shear Rate and Fibres Fraction in Polypropylene* — supports the rheology/material-processing branch.
- *Design and Production of the Injection Mould with a CAX Assistance* — supports tooling/CAX context.
- 2021 and 2023 plastics-processing university publications — support later continuity in plastics-processing technical authorship.

These should appear under **Related work**, not be mixed into the core fibre-orientation narrative unless a direct technical connection is explicitly documented.

## Safe case-study narrative

The case study can safely tell this story:

1. **Engineering context** — In short-fibre reinforced thermoplastics, injection moulding does not merely create geometry; material flow and processing conditions also influence fibre orientation and therefore local anisotropy.
2. **Problem** — A simulation can predict fibre orientation, but the prediction should not be accepted as an engineering conclusion without comparison to the real moulded structure.
3. **Numerical representation** — Public research used injection-moulding simulation and orientation-tensor information to describe predicted fibre orientation.
4. **Experimental verification** — Metallographic preparation and stereological/materialographic evaluation provided an experimental estimate of fibre orientation in selected sample locations.
5. **Comparison** — Experimental and numerical results were compared as part of model verification.
6. **Engineering lesson** — The useful output is not the contour plot alone; it is the relationship between process assumptions, simulated structure, measured structure and the interpretation of their agreement or disagreement.

This narrative directly supports the site's existing principle:

> Measure. Document. Explain.

and a future Materials-specific formulation:

> A solver result is not automatically an engineering conclusion.

## Claims that must NOT be published without additional evidence

- Any percentage improvement, cost saving, scrap reduction or cycle-time improvement.
- Any claim that the model was universally validated for all geometries/materials/process settings.
- Any industrial/customer application not explicitly public.
- Any statement that Lukáš alone designed or performed every experimental/simulation step in co-authored work unless role evidence exists.
- Any specific commercial software expertise inferred solely from one paper, beyond saying that the published research used that software.
- Any claim that a particular fibre orientation directly produced a particular mechanical-property improvement unless the cited study demonstrates that causal result.
- Any unpublished dissertation result not available in a public source or supplied by Lukáš.

## Recommended role wording

Until author-contribution details are available, use conservative wording such as:

> Doctoral research and co-authored publications focused on the relationship between injection-moulding process conditions, fibre orientation, materialography and numerical simulation in short-fibre reinforced thermoplastics.

Avoid:

> I developed / I proved / I validated ...

unless the user's own contribution is separately documented.

## Recommended v0.2.0 page structure

1. Hero / summary
2. Context — short-fibre reinforced thermoplastics
3. Engineering question — how to compare simulated and real fibre orientation
4. Research workflow
5. Numerical representation
6. Experimental evaluation
7. Comparison and interpretation
8. What the research demonstrates
9. Limitations
10. Related publications / DOI
11. Academic evidence — dissertation and successful defence
12. Related work

## Original visual system — recommended

Do not copy publisher figures into Likavcan.cz by default.

Create original explanatory diagrams based on verified concepts:

- **LL-FIG-01 — Process -> flow -> fibre orientation -> anisotropic response**
- **LL-FIG-02 — Simulation -> orientation tensor -> experimental section -> comparison**
- **LL-FIG-03 — Model verification loop: assumptions -> simulation -> experiment -> comparison -> model revision / engineering interpretation**

Possible later evidence artifact:

- A user-supplied original microscopy image, simulation screenshot or dissertation figure, only after confirming publication/reuse rights and removing sensitive metadata.

## Structured-data recommendation

For the future case-study page:

- `WebPage` is sufficient as the primary page type.
- `mainEntity` can refer to a project/research-work entity only if a stable entity definition is useful and factual.
- Do not create a new `Project` merely to gain Schema.org coverage if the research is better represented as a case-study page about doctoral/co-authored research.
- Connect the page to the stable Person ID and to verified publication entities/DOIs.

## Evidence readiness

| Area | Readiness | Notes |
| --- | --- | --- |
| Dissertation title / year / supervisor | READY | Official STU evidence |
| Successful PhD defence | READY | Official MTF STU evidence |
| Research theme | READY | Dissertation + multiple papers |
| Injection-moulding / fibre-orientation context | READY | Multiple primary papers |
| Simulation-method evidence | READY | Published papers |
| Experimental metallography evidence | READY | Published papers |
| Simulation-vs-experiment comparison | READY | Published papers |
| Exact personal contribution per co-authored paper | NEEDS USER INPUT | Avoid over-attribution |
| Original images / screenshots | NEEDS USER INPUT | Prefer user's own source files |
| Industrial outcome / KPI | NOT AVAILABLE | Do not invent |
| Full dissertation results | PARTIAL | Need thesis/full supplied source for deeper claims |

## Decision

This topic is **READY for a truthful first-draft case study at conceptual/evidence level**, but the best portfolio version should wait for two user inputs:

1. confirmation of Lukáš's concrete contribution to the research workflow; and
2. one or more original visual artifacts that can legally and safely be published.

Until then, prepare only the evidence-backed text architecture and original explanatory diagrams.
