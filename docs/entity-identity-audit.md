# Entity identity architecture audit

Updated: 2026-08-16

## Canonical entities

- Lukáš Likavčan: `https://likavcan.cz/lukas/#lukas-likavcan`
- Peter Likavčan: `https://likavcan.cz/peter/#peter-likavcan`
- Website: `https://likavcan.cz/#website`
- MTF STU: `https://likavcan.cz/#mtf-stu`

All language variants reference the same canonical Person ID. This avoids creating separate SK/EN/DE identities for the same person.

## Verified external references — Lukáš Likavčan

- MTF STU successful PhD defence, 2017: https://www.mtf.stuba.sk/sk/diani-na-mtf/aktuality/oznam-o-uspesnych-obhajobach-na-uvte-4.html?page_id=13318
- STU publication catalogue: https://kis.cvt.stuba.sk/arl-stu/en/result/?disp=+Likav%C4%8Dan%2C+Luk%C3%A1%C5%A1%2C&field=AUP&qt=zf&src=stu_us_cat&term=%22%5ELikav%C4%8Dan%2C+Luk%C3%A1%C5%A1%2C%5E%22
- STU article record: https://kis.stuba.sk/arl-stu/en/detail-stu_us_cat-0022597-Using-sodium-hydrogen-carbonate-for-foaming-polymers/
- ORCID: https://orcid.org/0000-0003-3949-6034
- Google Scholar: https://scholar.google.com/citations?user=rBvaSKQAAAAJ
- LinkedIn: https://www.linkedin.com/in/luk%C3%A1%C5%A1-likav%C4%8Dan-74695b84
- Wikidata: https://www.wikidata.org/wiki/Q139947576
- DOI, Estimation of Fibre Orientation: https://doi.org/10.4028/www.scientific.net/MSF.891.55
- DOI, Diesel Effect Problem Solving: https://doi.org/10.2478/rput-2014-0014

## Verified external references — Peter Likavčan

- STU permanent master thesis record, 2016: https://kis.stuba.sk/arl-stu/en/detail-stu_us_cat-stuzp55130-Navrh-simulacneho-modelu-robotickej-bunky-s-vyuzitim-signalneho-riadenia-v-prostredi-Process-Simulat/
- STU author catalogue showing academic works from 2014 and 2016: https://kis.stuba.sk/arl-stu/en/result/?disp=Likav%C4%8Dan+Peter&field=AUK&qt=zf&src=stu_us_cat&term=%22%5Estu_us_auth%5C%2Astu138973%5E%22
- MTF STU admission list, 2014, Automation and Informatization of Industrial Processes: https://www.mtf.stuba.sk/buxus/docs/doc/aktuality/2014/2014_07_18_Zoznam_prijatych_uch_ING.pdf
- LinkedIn: https://www.linkedin.com/in/peter-likav%C4%8Dan-4a668311a
- Wikidata: https://www.wikidata.org/wiki/Q139977167

The STU 2016 thesis record identifies Peter Likavčan as author, Dušan Šútora as thesis advisor, and explicitly indexes Virtual Commissioning, Process Simulate, KUKA, robotic cell and digital factory as subjects.

## Structured-data policy

`sameAs` is reserved for URLs representing the same person. Academic records, theses, defence notices and publication records are modelled through `subjectOf` / `CreativeWork` instead of `sameAs`.

Photographs are intentionally not included in this revision. When added later, create stable crawlable image URLs and reference them through `Person.image` / `ImageObject`.

## Additional external authority references (2026-08-16)

### Lukáš Likavčan
- STU graduate profile explicitly listing Ing. Lukáš Likavčan, PhD. as Application Engineer at Branson Ultrasonics: https://www.stuba.sk/sk/informacie-pre-uchadzacov/studijne-programy-a-studijne-odbory/vsetky-studijne-programy.html?d=186109-strojarske-technologie&i=profil&page_id=10703
- MTF STU Student Scientific Conference 2019 abstract listing Ing. Lukáš Likavčan, PhD. as consultant from Branson Ultrasonics and STTIr cooperation: https://www.mtf.stuba.sk/buxus/docs/doc/svk/2019/abstrakty/Vyrobne_technologie_2.pdf
- BIZZCOM official R&D page (employer context): https://bizzcom.sk/vyskum/
- Branson/Emerson official plastics joining technology context: https://www.branson.emerson.com/en

### Peter Likavčan
- Porsche Werkzeugbau official Simulation and Virtual Commissioning context: https://www.porsche-werkzeugbau.com/en/services/bodyinwhite/
- MATADOR Automation official Simulations / digital factory / offline programming context: https://www.matador-group.eu/en/our-companies/simulations/
- t-mech official Simulation and Offline Programming context: https://www.tmechgroup.com/our-services/

Company context pages are not treated as direct evidence that a person participated in a specific project. Direct university records remain Person.subjectOf; identity profiles remain Person.sameAs.
