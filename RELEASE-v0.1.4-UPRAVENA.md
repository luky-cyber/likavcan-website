# Likavcan.cz v0.1.4 – upravená verzia

Táto verzia vychádza z pracovnej v0.1.4 a zachováva release číslo 0.1.4, pretože verejne bola predtým vydaná iba verzia 0.1.3.

## Úpravy digitálnej identity

- opravené `inLanguage` na `sk` v zdrojových JSON-LD profiloch Lukáša a Petra,
- odstránený prázdny/neplatný `structured-data/breadcrumb.jsonld`,
- `structured-data/organization.jsonld` premenovaný na presnejší `structured-data/site.jsonld`,
- doplnené vzájomné interné prelinkovanie profilov Lukáš ↔ Peter vo všetkých jazykových verziách,
- pridaný `_config.yml`, ktorý pri GitHub Pages/Jekyll deployi vylúči internú dokumentáciu a pomocné structured-data súbory z produkčného webu,
- zachovaná existujúca stabilná entity architektúra `ProfilePage → Person`, spoločná entita MTF STU, externé referencie a fotografie.

Dizajn, hlavný obsah a verejné URL zostali nezmenené.
