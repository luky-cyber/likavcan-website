#!/usr/bin/env python3
"""Likavcan.cz release regression checks (stdlib-first, optional OpenCV QR decode)."""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from datetime import datetime
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://likavcan.cz"
EXPECTED = {
    "lukas": {
        "person_id": f"{SITE}/lukas/#lukas-likavcan",
        "linkedin": "https://www.linkedin.com/in/luk%C3%A1%C5%A1-likav%C4%8Dan-74695b84",
        "vcf": ROOT / "lukas/lukas-likavcan.vcf",
        "qr": ROOT / "assets/img/qr/lukas-vcard.png",
        "qr_value": f"{SITE}/lukas/lukas-likavcan.vcf",
    },
    "peter": {
        "person_id": f"{SITE}/peter/#peter-likavcan",
        "linkedin": "https://www.linkedin.com/in/peter-likav%C4%8Dan-4a668311a",
        "vcf": ROOT / "peter/peter-likavcan.vcf",
        "qr": ROOT / "assets/img/qr/peter-vcard.png",
        "qr_value": f"{SITE}/peter/peter-likavcan.vcf",
    },
}
BE_PROJECT_ID = "https://bezpecnaelektrika.sk/#project"

FAILS: list[str] = []
WARNS: list[str] = []
PASSES: list[str] = []


def fail(msg: str) -> None: FAILS.append(msg)
def warn(msg: str) -> None: WARNS.append(msg)
def ok(msg: str) -> None: PASSES.append(msg)


class DocParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.id_counts: dict[str, int] = {}
        self.aria_current: list[tuple[str, str]] = []
        self.refs: list[tuple[str, str, dict[str, str]]] = []
        self.jsonld: list[str] = []
        self._json_buf: list[str] | None = None
        self.canonical: str | None = None
        self.hreflang: dict[str, str] = {}

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"]); self.id_counts[d["id"]] = self.id_counts.get(d["id"], 0) + 1
        if tag == "a" and d.get("aria-current") == "page": self.aria_current.append((d.get("href", ""), d.get("class", "")))
        if tag in {"a", "img", "script", "link", "source"}:
            for key in ("href", "src", "srcset"):
                if key in d:
                    self.refs.append((tag, d[key], d))
        if tag == "link" and d.get("rel") == "canonical": self.canonical = d.get("href")
        if tag == "link" and d.get("rel") == "alternate" and d.get("hreflang"):
            self.hreflang[d["hreflang"]] = d.get("href", "")
        if tag == "script" and d.get("type") == "application/ld+json": self._json_buf = []

    def handle_endtag(self, tag):
        if tag == "script" and self._json_buf is not None:
            self.jsonld.append("".join(self._json_buf)); self._json_buf = None

    def handle_data(self, data):
        if self._json_buf is not None: self._json_buf.append(data)


def html_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.html") if "docs" not in p.parts and "tools" not in p.parts)


def public_index_files() -> list[Path]:
    out=[]
    for p in html_files():
        txt=p.read_text(encoding="utf-8")
        if '<meta name="robots" content="noindex' in txt or "noindex" in re.search(r'<meta[^>]+name=["\']robots["\'][^>]*>', txt, re.I).group(0).lower() if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*>', txt, re.I) else False:
            continue
        if p.name == "404.html": continue
        out.append(p)
    return out


def parse_docs():
    docs={}
    for p in html_files():
        parser=DocParser(); parser.feed(p.read_text(encoding="utf-8")); docs[p]=parser
    return docs


def local_path_for_url(url: str, current: Path) -> tuple[Path | None, str | None]:
    if not url or url.startswith(("mailto:", "tel:", "javascript:", "data:")): return None, None
    parts=urlsplit(url)
    if parts.scheme and parts.netloc and parts.netloc not in {"likavcan.cz", "www.likavcan.cz"}: return None, None
    path=unquote(parts.path)
    fragment=parts.fragment or None
    if not path:
        target=current
    elif path.startswith("/"):
        target=ROOT / path.lstrip("/")
    else:
        target=current.parent / path
    if path.endswith("/") or (path and not Path(path).suffix): target=target / "index.html"
    target=target.resolve()
    return target, fragment


def check_links(docs):
    broken=[]; bad_index=[]; bad_anchors=[]
    for p,doc in docs.items():
        for tag,url,attrs in doc.refs:
            if tag == "source" and " " in url: # srcset
                candidates=[c.strip().split()[0] for c in url.split(",")]
            else: candidates=[url]
            for u in candidates:
                if "index.html" in u and (u.startswith("/") or not urlsplit(u).scheme): bad_index.append((p,u))
                target,frag=local_path_for_url(u,p)
                if target is None: continue
                if not target.exists(): broken.append((p,u,target)) ; continue
                if frag and target.suffix.lower()==".html":
                    tdoc=docs.get(target)
                    if tdoc is None:
                        parser=DocParser(); parser.feed(target.read_text(encoding="utf-8")); tdoc=parser
                    if frag not in tdoc.ids: bad_anchors.append((p,u,frag))
    if broken: [fail(f"broken local ref: {p.relative_to(ROOT)} -> {u}") for p,u,_ in broken]
    else: ok("local href/src targets")
    if bad_index: [fail(f"internal index.html URL: {p.relative_to(ROOT)} -> {u}") for p,u in bad_index]
    else: ok("no internal index.html URLs")
    if bad_anchors: [fail(f"missing HTML anchor: {p.relative_to(ROOT)} -> #{frag}") for p,_,frag in bad_anchors]
    else: ok("HTML fragment targets")


def walk_json(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values(): yield from walk_json(v)
    elif isinstance(obj, list):
        for v in obj: yield from walk_json(v)


def check_jsonld(docs):
    count=0; person_ids=set(); same_as=[]
    for p,doc in docs.items():
        for raw in doc.jsonld:
            try: data=json.loads(raw)
            except Exception as e: fail(f"JSON-LD parse: {p.relative_to(ROOT)}: {e}"); continue
            count += 1
            for o in walk_json(data):
                if o.get("@type") == "Person" and o.get("@id"): person_ids.add(o["@id"])
                if o.get("@type") == "Person":
                    vals=o.get("sameAs",[]); vals=[vals] if isinstance(vals,str) else vals
                    same_as.extend(vals)
    for key in ("lukas","peter"):
        if EXPECTED[key]["person_id"] not in person_ids: fail(f"missing stable Person ID: {EXPECTED[key]['person_id']}")
    if BE_PROJECT_ID in same_as: fail("Bezpečná elektrika incorrectly appears in Person.sameAs")
    if not any("https://bezpecnaelektrika.sk/#project" in p.read_text(encoding="utf-8") for p in html_files()): fail("Bezpečná elektrika Project ID missing")
    if not any("\"founder\"" in p.read_text(encoding="utf-8") and EXPECTED['lukas']['person_id'] in p.read_text(encoding="utf-8") for p in html_files()): fail("Project -> founder relation missing")
    if not FAILS: ok(f"JSON-LD parse and entity guardrails ({count} blocks)")


def check_hreflang(docs):
    url_to_doc={d.canonical:p for p,d in docs.items() if d.canonical}
    issues=[]
    for p,d in docs.items():
        if not d.canonical: continue
        for lang,url in d.hreflang.items():
            if lang == "x-default": continue
            tp=url_to_doc.get(url)
            if not tp: issues.append(f"{p.relative_to(ROOT)} hreflang {lang} target missing: {url}"); continue
            td=docs[tp]
            this_lang=re.search(r'<html[^>]+lang=["\']([^"\']+)', p.read_text(encoding="utf-8"), re.I)
            if this_lang and td.hreflang.get(this_lang.group(1).split('-')[0]) != d.canonical:
                issues.append(f"{p.relative_to(ROOT)} <-> {tp.relative_to(ROOT)} not reciprocal")
    if issues: [fail("hreflang: "+x) for x in issues]
    else: ok("canonical/hreflang reciprocity")


def hex_rgb(s):
    s=s.strip().lstrip('#');
    if len(s)==3: s=''.join(c*2 for c in s)
    return tuple(int(s[i:i+2],16)/255 for i in (0,2,4))

def luminance(s):
    def f(c): return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    r,g,b=map(f,hex_rgb(s)); return .2126*r+.7152*g+.0722*b

def contrast(a,b):
    x,y=luminance(a),luminance(b); return (max(x,y)+.05)/(min(x,y)+.05)


def check_contrast():
    css=(ROOT/'assets/css/variables.css').read_text(encoding='utf-8')
    vals=dict(re.findall(r'--([\w-]+):\s*(#[0-9a-fA-F]{6})\s*;',css))
    fg=vals.get('color-on-primary'); bg=vals.get('color-primary'); hover=vals.get('color-primary-hover')
    if not (fg and bg and hover): fail('CTA color variables missing'); return
    c1=contrast(fg,bg); c2=contrast(fg,hover)
    if c1 < 4.5 or c2 < 4.5: fail(f'CTA contrast below 4.5:1 ({c1:.2f}, {c2:.2f})')
    else: ok(f'primary CTA contrast {c1:.2f}:1 / hover {c2:.2f}:1')


def vcard_urls(vcf: Path) -> list[str]:
    raw=vcf.read_bytes().decode("ascii",errors="replace")
    return [m.group(1).strip("\r") for m in re.finditer(r"^URL(?:;[^:]*)?:(.+)$",raw,re.M)]


def check_identity_contacts():
    for who,ex in EXPECTED.items():
        pages=[ROOT/f'{who}/index.html',ROOT/f'en/{who}/index.html',ROOT/f'de/{who}/index.html']
        for p in pages:
            txt=p.read_text(encoding='utf-8')
            if ex['linkedin'] not in txt: fail(f'{who} LinkedIn mismatch in {p.relative_to(ROOT)}')
        got=vcard_urls(ex['vcf'])
        if ex['linkedin'] not in got: fail(f'{who} vCard LinkedIn mismatch: {got!r}')
    if not any(x.startswith('lukas LinkedIn') or x.startswith('peter LinkedIn') or 'vCard LinkedIn mismatch' in x for x in FAILS): ok('HTML/vCard LinkedIn consistency')

    try:
        import cv2  # type: ignore
        for who,ex in EXPECTED.items():
            img=cv2.imread(str(ex['qr']))
            data,_,_=cv2.QRCodeDetector().detectAndDecode(img)
            if data != ex['qr_value']: fail(f'{who} QR mismatch: {data!r}')
        if not any('QR mismatch' in x for x in FAILS): ok('QR targets')
    except Exception as e:
        warn(f'QR decode skipped (OpenCV unavailable or failed): {e}')


def check_language_markers():
    bad=[]
    for lang in ('en','de'):
        for p in (ROOT/lang).rglob('*.html'):
            txt=p.read_text(encoding='utf-8')
            for m in re.finditer(r'<a([^>]*href="https://bezpecnaelektrika\.sk/[^\"]*"[^>]*)>',txt):
                if 'hreflang="sk"' not in m.group(1): bad.append(str(p.relative_to(ROOT)))
    if bad: fail('BE links without hreflang=sk: '+', '.join(sorted(set(bad))))
    else: ok('EN/DE Bezpečná elektrika language markers')


def check_hero_loading():
    for rel in ('index.html','en/index.html','de/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        imgs=re.findall(r'<img[^>]+class="home-profile-card__portrait"[^>]*>',txt)
        if len(imgs) != 2 or any('loading="eager"' not in m or 'fetchpriority="high"' not in m for m in imgs): fail(f'home portrait priority: {rel}')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html','peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<img[^>]+class="profile-portrait"[^>]*>',txt)
        if not m or 'loading="eager"' not in m.group(0) or 'fetchpriority="high"' not in m.group(0): fail(f'hero portrait priority: {rel}')
    if not any(x.startswith(('hero portrait priority','home portrait priority')) for x in FAILS): ok('home/profile portraits eager/high priority')




def check_navigation_hierarchy():
    expected = {
        'sk': [('Domov','/'), ('Lukáš','/lukas/'), ('Peter','/peter/')],
        'en': [('Home','/en/'), ('Lukáš','/en/lukas/'), ('Peter','/en/peter/')],
        'de': [('Startseite','/de/'), ('Lukáš','/de/lukas/'), ('Peter','/de/peter/')],
    }
    issues=[]
    for pth in html_files():
        txt=pth.read_text(encoding='utf-8')
        m=re.search(r'<nav[^>]*class="site-nav"[^>]*>(.*?)</nav>', txt, re.S)
        if not m:
            # Redirect-only pages intentionally have no site navigation.
            continue
        langm=re.search(r'<html[^>]*\blang="([^"]+)"', txt, re.I)
        lang=(langm.group(1).split('-')[0].lower() if langm else 'sk')
        links=[(re.sub(r'<[^>]+>','',a).strip(), href) for href,a in re.findall(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', m.group(1), re.S)]
        if links != expected.get(lang, expected['sk']):
            issues.append(f"{pth.relative_to(ROOT)} -> {links!r}")
    # Homepages are identity landing pages only; project/publication detail discovery starts inside profiles.
    for rel,prefix in [('index.html','/'),('en/index.html','/en/'),('de/index.html','/de/')]:
        txt=(ROOT/rel).read_text(encoding='utf-8')
        main=re.search(r'<main[^>]*>(.*?)</main>', txt, re.S)
        if not main:
            issues.append(f'{rel}: main missing'); continue
        body=main.group(1)
        if '/projects/' in body or '/publications/' in body or '/en/projects/' in body or '/en/publications/' in body or '/de/projects/' in body or '/de/publications/' in body:
            issues.append(f'{rel}: project/publication link leaked onto identity homepage')
        sections=len(re.findall(r'<section\b', body))
        if sections != 1:
            issues.append(f'{rel}: expected 1 equal-profile section, got {sections}')
        if body.count('class="card home-profile-card"') != 2:
            issues.append(f'{rel}: expected 2 equal home profile cards')
    if issues:
        for x in issues: fail('navigation hierarchy: '+x)
    else:
        ok('Home/Lukáš/Peter navigation hierarchy')


def check_homepage_quick_contacts():
    expected = {
        'index.html': [
            EXPECTED['lukas']['linkedin'], 'lukas/lukas-likavcan.vcf',
            EXPECTED['peter']['linkedin'], 'peter/peter-likavcan.vcf',
        ],
        'en/index.html': [
            EXPECTED['lukas']['linkedin'], '../lukas/lukas-likavcan.vcf',
            EXPECTED['peter']['linkedin'], '../peter/peter-likavcan.vcf',
        ],
        'de/index.html': [
            EXPECTED['lukas']['linkedin'], '../lukas/lukas-likavcan.vcf',
            EXPECTED['peter']['linkedin'], '../peter/peter-likavcan.vcf',
        ],
    }
    issues=[]
    for rel, needles in expected.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        main=re.search(r'<main[^>]*>(.*?)</main>', txt, re.S)
        body=main.group(1) if main else ''
        if body.count('class="profile-quick-contact"') != 2:
            issues.append(f'{rel}: expected 2 compact contact groups')
        for needle in needles:
            if needle not in body:
                issues.append(f'{rel}: missing quick contact target {needle}')
        if 'assets/img/qr/' in body:
            issues.append(f'{rel}: QR leaked onto homepage')
    if issues:
        for x in issues: fail('homepage quick contacts: '+x)
    else:
        ok('homepage compact LinkedIn/vCard contacts')


def check_visible_language_routes():
    issues=[]
    for p in html_files():
        txt=p.read_text(encoding='utf-8')
        m=re.search(r'<nav[^>]*class="language-nav"[^>]*>(.*?)</nav>',txt,re.S)
        if not m: continue
        for href,lang in re.findall(r'<a[^>]*href="([^"]+)"[^>]*hreflang="(sk|en|de)"[^>]*>',m.group(1)):
            target,_=local_path_for_url(href,p)
            if target is None or not target.exists(): issues.append(f'{p.relative_to(ROOT)} {lang} -> {href}')
            if href.startswith('/') and p.name != '404.html':
                issues.append(f'{p.relative_to(ROOT)} {lang} remains root-relative ({href})')
    if issues:
        for x in issues: fail('visible language route: '+x)
    else: ok('visible language switch preserves local route')

def check_mobile_docks():
    issues=[]
    expected=[
      'lukas/index.html','en/lukas/index.html','de/lukas/index.html',
      'peter/index.html','en/peter/index.html','de/peter/index.html',
      'projects/index.html','en/projects/index.html','de/projects/index.html',
      'publications/index.html','en/publications/index.html','de/publications/index.html',
      'projects/bezpecna-elektrika/index.html','en/projects/bezpecna-elektrika/index.html','de/projects/bezpecna-elektrika/index.html',
      'projects/fibre-orientation-injection-moulding/index.html','en/projects/fibre-orientation-injection-moulding/index.html','de/projects/fibre-orientation-injection-moulding/index.html']
    for rel in expected:
      txt=(ROOT/rel).read_text(encoding='utf-8')
      if 'class="mobile-profile-dock' not in txt: issues.append(rel)
    css=(ROOT/'assets/css/responsive.css').read_text(encoding='utf-8')
    if 'position: fixed' not in css or '.mobile-profile-dock' not in css: issues.append('mobile dock CSS missing')
    if issues:
      for x in issues: fail('mobile dock: '+x)
    else: ok('sticky top + contextual mobile bottom navigation')

def check_peter_dock_identity():
    expected = {
        'peter/index.html': [('profile','#profile','Profil'),('career','#experience','Kariéra'),('expertise','#expertise','Oblasti'),('contact','#contact','Kontakt')],
        'en/peter/index.html': [('profile','#profile','Profile'),('career','#experience','Career'),('expertise','#expertise','Expertise'),('contact','#contact','Contact')],
        'de/peter/index.html': [('profile','#profile','Profil'),('career','#experience','Karriere'),('expertise','#expertise','Fachgebiete'),('contact','#contact','Kontakt')],
    }
    issues=[]
    for rel,want in expected.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<nav[^>]*class="mobile-profile-dock[^"]*"[^>]*data-dock-owner="peter"[^>]*>.*?<div[^>]*>(.*?)</div>.*?</nav>',txt,re.S)
        if not m:
            issues.append(f'{rel}: Peter dock missing'); continue
        got=[(key,href,re.sub(r'<[^>]+>','',label).strip()) for key,href,label in re.findall(r'<a[^>]*data-dock-key="([^"]+)"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',m.group(1),re.S)]
        if got != want: issues.append(f'{rel}: {got!r}')
    if issues:
        for x in issues: fail('Peter dock identity: '+x)
    else: ok('Peter mobile dock stays within Peter profile')

def check_mobile_nav_accessible_labels():
    expected = {'sk':'Mobilná navigácia profilu','en':'Mobile profile navigation','de':'Mobile Profilnavigation'}
    issues=[]
    for p in html_files():
        txt=p.read_text(encoding='utf-8')
        m=re.search(r'<nav[^>]*class="mobile-profile-dock[^"]*"[^>]*aria-label="([^"]+)"',txt)
        if not m: continue
        langm=re.search(r'<html[^>]*\blang="([^"]+)"',txt,re.I)
        lang=(langm.group(1).split('-')[0].lower() if langm else 'sk')
        want=expected.get(lang,expected['sk'])
        if m.group(1) != want: issues.append(f'{p.relative_to(ROOT)}: {m.group(1)!r} != {want!r}')
    if issues:
        for x in issues: fail('mobile nav accessible label: '+x)
    else: ok('localized mobile navigation accessible names')

def check_custom_404():
    p=ROOT/'404.html'; txt=p.read_text(encoding='utf-8')
    issues=[]
    for href,lang in [('/','sk'),('/en/','en'),('/de/','de')]:
        if not re.search(rf'<a[^>]*href="{re.escape(href)}"[^>]*hreflang="{lang}"',txt): issues.append(f'language {lang} != {href}')
    if 'aria-current="page"' in txt: issues.append('static aria-current=page must be route-derived')
    if 'data-page="404"' not in txt: issues.append('route-aware 404 hook missing')
    main=re.search(r'<main[^>]*>(.*?)</main>',txt,re.S)
    body=main.group(1) if main else ''
    for href in ('/','/lukas/','/peter/'):
        if f'href="{href}"' not in body: issues.append(f'recovery CTA missing {href}')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    if 'data.page === "404"' in js: issues.append('invalid 404 hook check')
    if 'document.body.dataset.page === "404"' not in js: issues.append('404 route localization missing in JS')
    if issues:
        for x in issues: fail('custom 404: '+x)
    else: ok('custom 404 root-safe and route-aware')


def check_e2a_status():
    files=[ROOT/'lukas/index.html',ROOT/'en/lukas/index.html',ROOT/'de/lukas/index.html',ROOT/'projects/bezpecna-elektrika/index.html',ROOT/'en/projects/bezpecna-elektrika/index.html',ROOT/'de/projects/bezpecna-elektrika/index.html']
    stale=('čakám na vydanie osvedčenia','certificate is still pending','steht die Ausstellung des Nachweises noch aus')
    required=('osvedčenie bolo vydané','certificate has been issued','Bescheinigung wurde ausgestellt')
    blob='\n'.join(p.read_text(encoding='utf-8') for p in files)
    issues=[x for x in stale if x in blob]
    for x in required:
        if x not in blob: issues.append('missing confirmed status: '+x)
    if issues:
        for x in issues: fail('E2A status: '+x)
    else: ok('E2A certificate issued / commercial services not launched')


def check_consent_hardening():
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    required=['policyVersion = "2026-09-15-v0.2.2"','gtag("consent", "default"','analytics_storage:"denied"','ad_user_data:"denied"','decidedAt: new Date().toISOString()','consentMaxAgeMs','url.search = ""','url.hash = ""','Use essential only and close','Použiť len nevyhnutné a zavrieť']
    missing=[x for x in required if x not in js]
    privacy=(ROOT/'privacy/index.html').read_text(encoding='utf-8')
    for x in ('GitHub Pages','Právny základ','Práva dotknutej osoby','12 mesiacoch'):
        if x not in privacy: missing.append('privacy: '+x)
    if missing:
        for x in missing: fail('consent/privacy hardening missing: '+x)
    else: ok('versioned consent, URL minimisation and privacy disclosure hardening')



def check_rc9_human_cut():
    issues=[]
    llms=(ROOT/'llms.txt').read_text(encoding='utf-8')
    for stale in ('proof-of-work','## Primary person','## Related person'):
        if stale in llms: issues.append('llms.txt still contains '+stale)
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for stale in ('id="engineering-approach"','id="profiles"','id="references"'):
            if stale in txt: issues.append(f'{rel}: stale section {stale}')
    for rel in ('peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for stale in ('id="skills"','id="references"','id="external-profile"'):
            if stale in txt: issues.append(f'{rel}: stale section {stale}')
    for rel in ('projects/fibre-orientation-injection-moulding/index.html','en/projects/fibre-orientation-injection-moulding/index.html','de/projects/fibre-orientation-injection-moulding/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'LL-FIG-' in txt: issues.append(f'{rel}: visible internal figure label remains')
        ids=re.findall(r'<section[^>]+id="([^"]+)"',txt)
        want=['context','workflow','comparison','interpretation','limitations','evidence']
        if ids != want: issues.append(f'{rel}: case-study sections {ids!r} != {want!r}')
    for rel in ('methodology/index.html','en/methodology/index.html','de/methodology/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'id="ai"' in txt: issues.append(f'{rel}: public AI workflow section remains')
    if issues:
        for x in issues: fail('RC9 human cut: '+x)
    else: ok('RC9 human-cut simplification guardrails')

def check_rc10_mobile_ux():
    issues=[]
    # Stable Lukáš dock everywhere, no adaptive/switch-context legacy.
    for rel in (
      'lukas/index.html','en/lukas/index.html','de/lukas/index.html',
      'projects/index.html','en/projects/index.html','de/projects/index.html',
      'publications/index.html','en/publications/index.html','de/publications/index.html',
      'projects/bezpecna-elektrika/index.html','en/projects/bezpecna-elektrika/index.html','de/projects/bezpecna-elektrika/index.html',
      'projects/fibre-orientation-injection-moulding/index.html','en/projects/fibre-orientation-injection-moulding/index.html','de/projects/fibre-orientation-injection-moulding/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'data-dock-owner="lukas"' not in txt: issues.append(f'{rel}: stable Lukáš dock hook missing')
        m=re.search(r'<nav[^>]*class="mobile-profile-dock".*?</nav>',txt,re.S)
        keys=re.findall(r'data-dock-key="([^"]+)"',m.group(0)) if m else []
        if keys != ['profile','projects','publications','contact']: issues.append(f'{rel}: dock keys {keys!r}')
        if 'mobile-profile-dock--adaptive' in txt or 'data-switch-context' in txt: issues.append(f'{rel}: adaptive dock legacy remains')
    # Scrollspy hooks on both profiles.
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html','peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'data-dock-section=' not in txt: issues.append(f'{rel}: scrollspy sections missing')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    for token in ('dataset.dockSection','requestAnimationFrame(updateProfileNavFromScroll)','aria-current", "location"'):
        if token not in js: issues.append('main.js scrollspy missing '+token)
    # Publication grids have a mobile-specific class/rule.
    for rel in ('publications/index.html','en/publications/index.html','de/publications/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if txt.count('publication-grid') < 4: issues.append(f'{rel}: publication grid class incomplete')
    css=(ROOT/'assets/css/responsive.css').read_text(encoding='utf-8')
    if '@media (max-width: 900px)' not in css or '.publication-grid' not in css: issues.append('mobile publication CSS missing')
    # Qualification + editorial requests.
    sk=(ROOT/'lukas/index.html').read_text(encoding='utf-8')
    if 'Revízny technik VTZ elektrických' not in sk or 'Osvedčenie bolo vydané' not in sk: issues.append('SK E2/A achieved qualification wording missing')
    en=(ROOT/'en/lukas/index.html').read_text(encoding='utf-8')
    de=(ROOT/'de/lukas/index.html').read_text(encoding='utf-8')
    if 'Electrical inspection technician qualification' not in en or 'The certificate was issued.' not in en: issues.append('EN E2/A achieved qualification wording missing')
    if 'Qualifikation für elektrische Prüf- und Revisionstätigkeiten' not in de or 'Die Bescheinigung wurde ausgestellt.' not in de: issues.append('DE E2/A achieved qualification wording missing')
    for rel,stale in [('lukas/index.html','Odborné školenia zákazníkov'),('en/lukas/index.html','Customer Training'),('de/lukas/index.html','Kundenschulungen')]:
        if stale in (ROOT/rel).read_text(encoding='utf-8'): issues.append(f'{rel}: customer-training card remains')
    if '<a href="https://bezpecnaelektrika.sk/">Bezpečná elektrika</a>' not in sk: issues.append('SK intro project hyperlink missing')
    for stale in ('>Research<','>Simulation<','>Innovation<'):
        if stale in sk: issues.append('SK Lukáš decorative English badge remains: '+stale)
    psk=(ROOT/'peter/index.html').read_text(encoding='utf-8')
    for stale in ('>Simulation<','>Commissioning<','>Programming<','>Software<'):
        if re.search(stale.replace('>',r'>\s*',1).replace('<',r'\s*<',1),psk): issues.append('SK Peter decorative English badge remains: '+stale)
    if issues:
        for x in issues: fail('RC10 mobile UX: '+x)
    else: ok('RC10 mobile UX / scrollspy / qualification guardrails')

def check_accessibility_semantics(docs):
    dup=[]; false_current=[]
    for p,d in docs.items():
        for ident,count in d.id_counts.items():
            if count > 1: dup.append(f"{p.relative_to(ROOT)}#{ident} ({count}x)")
        for href,cls in d.aria_current:
            if href.startswith("#") or "nav-context-active" in cls:
                false_current.append(f"{p.relative_to(ROOT)} -> {href}")
    if dup: fail("duplicate HTML ids: "+", ".join(dup))
    else: ok("unique HTML ids")
    if false_current: fail("suspicious aria-current=page: "+", ".join(false_current))
    else: ok("aria-current page semantics")


def check_vcard_bytes():
    for who,ex in EXPECTED.items():
        b=ex["vcf"].read_bytes()
        if re.search(b"(?<!\r)\n", b): fail(f"{who} vCard contains bare LF")
        if not b.startswith(b"BEGIN:VCARD\r\nVERSION:3.0\r\n"): fail(f"{who} vCard 3.0/CRLF header mismatch")
    if not any("vCard contains bare LF" in x or "vCard 3.0/CRLF" in x for x in FAILS): ok("vCard 3.0 CRLF byte format")


def check_v022_entity_authority():
    issues=[]
    # Shared pages must not claim either external profile as rel=me.
    for rel in ('index.html','en/index.html','de/index.html','privacy/index.html','en/privacy/index.html','de/privacy/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'rel="me ' in txt or ' rel="me"' in txt:
            issues.append(f'{rel}: ambiguous rel=me on shared/non-identity page')
    # Full Person nodes need explicit job titles and three representative image ratios.
    for who in ('lukas','peter'):
        for rel in (f'{who}/index.html',f'en/{who}/index.html',f'de/{who}/index.html'):
            doc=DocParser(); doc.feed((ROOT/rel).read_text(encoding='utf-8'))
            found=False
            for raw in doc.jsonld:
                data=json.loads(raw)
                for o in walk_json(data):
                    if o.get('@type')=='Person' and o.get('@id')==EXPECTED[who]['person_id']:
                        found=True
                        if not o.get('jobTitle'): issues.append(f'{rel}: Person.jobTitle missing')
                        imgs=o.get('image',[])
                        if not isinstance(imgs,list) or len(imgs)<3: issues.append(f'{rel}: expected 3 Person image variants')
            if not found: issues.append(f'{rel}: canonical Person node missing')
    for who in ('lukas','peter'):
        for suffix in ('4x3','16x9'):
            if not (ROOT/f'assets/img/profiles/{who}-likavcan-{suffix}.jpg').exists(): issues.append(f'{who}: image variant {suffix} missing')
    # Lukáš publications graph should cover the normalized journal list, not only two articles.
    for rel in ('publications/index.html','en/publications/index.html','de/publications/index.html'):
        doc=DocParser(); doc.feed((ROOT/rel).read_text(encoding='utf-8'))
        count=0
        for raw in doc.jsonld:
            data=json.loads(raw)
            count += sum(1 for o in walk_json(data) if o.get('@type')=='ScholarlyArticle')
        if count < 11: issues.append(f'{rel}: only {count} ScholarlyArticle nodes')
    # Current discovery/source files must not retain the obsolete Lukáš-first framing.
    for rel in ('feed.xml','structured-data/site.jsonld','llms.txt','README.md'):
        txt=(ROOT/rel).read_text(encoding='utf-8').lower()
        if 'lukáš-first' in txt or 'lukáš first' in txt or 'lukas-first' in txt or 'lukas first' in txt:
            issues.append(f'{rel}: legacy Lukáš-first wording')
    if issues:
        for x in issues: fail('v0.2.2 entity authority: '+x)
    else: ok('v0.2.2 entity authority / identity consistency guardrails')


def _jsonld_objects(rel: str):
    doc=DocParser(); doc.feed((ROOT/rel).read_text(encoding='utf-8'))
    for raw in doc.jsonld:
        data=json.loads(raw)
        yield from walk_json(data)


def check_cross_page_person_consistency():
    issues=[]
    for who in ('lukas','peter'):
        rels=['index.html','en/index.html','de/index.html',f'{who}/index.html',f'en/{who}/index.html',f'de/{who}/index.html']
        titles=[]
        for rel in rels:
            nodes=[o for o in _jsonld_objects(rel) if o.get('@type')=='Person' and o.get('@id')==EXPECTED[who]['person_id']]
            if len(nodes)!=1:
                issues.append(f'{rel}: expected one canonical {who} Person node, got {len(nodes)}')
                continue
            jt=nodes[0].get('jobTitle')
            if isinstance(jt,str): jt=[jt]
            titles.append((rel,tuple(jt or [])))
        if titles:
            base=titles[0][1]
            for rel,jt in titles[1:]:
                if jt != base: issues.append(f'{who}: jobTitle drift in {rel}: {jt!r} != {base!r}')
    if issues:
        for x in issues: fail('Person consistency: '+x)
    else: ok('cross-page Person jobTitle consistency')


def check_profile_datetime():
    issues=[]
    rels=['lukas/index.html','peter/index.html','en/lukas/index.html','en/peter/index.html','de/lukas/index.html','de/peter/index.html']
    for rel in rels:
        nodes=[o for o in _jsonld_objects(rel) if o.get('@type')=='ProfilePage']
        if len(nodes)!=1:
            issues.append(f'{rel}: expected one ProfilePage, got {len(nodes)}'); continue
        value=nodes[0].get('dateModified')
        if not isinstance(value,str) or 'T' not in value:
            issues.append(f'{rel}: dateModified is not ISO DateTime: {value!r}'); continue
        try:
            dt=datetime.fromisoformat(value.replace('Z','+00:00'))
            if dt.tzinfo is None: issues.append(f'{rel}: dateModified has no timezone: {value}')
        except ValueError:
            issues.append(f'{rel}: invalid dateModified: {value!r}')
    if issues:
        for x in issues: fail('ProfilePage DateTime: '+x)
    else: ok('ProfilePage dateModified uses timezone-aware DateTime')


def check_home_graph_and_localized_haspart():
    issues=[]
    for rel in ('index.html','en/index.html','de/index.html'):
        objs=list(_jsonld_objects(rel))
        pages=[o for o in objs if o.get('@type')=='WebPage']
        if len(pages)!=1: issues.append(f'{rel}: expected one WebPage')
        elif pages[0].get('mentions'): issues.append(f'{rel}: Home WebPage has non-visible mentions')
        if any(o.get('@type')=='Project' for o in objs): issues.append(f'{rel}: Home graph contains non-visible Project node')
    expected={
        'lukas/index.html': ['https://likavcan.cz/projects/fibre-orientation-injection-moulding/#webpage','https://likavcan.cz/projects/bezpecna-elektrika/#webpage','https://likavcan.cz/publications/#collection'],
        'en/lukas/index.html': ['https://likavcan.cz/en/projects/fibre-orientation-injection-moulding/#webpage','https://likavcan.cz/en/projects/bezpecna-elektrika/#webpage','https://likavcan.cz/en/publications/#collection'],
        'de/lukas/index.html': ['https://likavcan.cz/de/projects/fibre-orientation-injection-moulding/#webpage','https://likavcan.cz/de/projects/bezpecna-elektrika/#webpage','https://likavcan.cz/de/publications/#collection'],
    }
    for rel,want in expected.items():
        nodes=[o for o in _jsonld_objects(rel) if o.get('@type')=='ProfilePage']
        got=[x.get('@id') for x in nodes[0].get('hasPart',[])] if len(nodes)==1 else []
        if got!=want: issues.append(f'{rel}: localized hasPart mismatch: {got!r}')
    if issues:
        for x in issues: fail('entity graph relevance: '+x)
    else: ok('Home graph visibility + localized ProfilePage hasPart')


def check_feed_consistency():
    issues=[]
    try:
        root=ET.parse(ROOT/'feed.xml').getroot()
        ns={'a':'http://www.w3.org/2005/Atom'}
        feed_updated=root.findtext('a:updated', namespaces=ns)
        entries=root.findall('a:entry',ns)
        ids=[e.findtext('a:id',namespaces=ns) for e in entries]
        if len(ids)!=len(set(ids)): issues.append('duplicate Atom entry IDs')
        def parse_dt(v): return datetime.fromisoformat(v.replace('Z','+00:00'))
        fu=parse_dt(feed_updated)
        eus=[parse_dt(e.findtext('a:updated',namespaces=ns)) for e in entries]
        if eus and fu < max(eus): issues.append('feed-level updated is older than an entry')
        pub=next((e for e in entries if e.findtext('a:id',namespaces=ns)=='https://likavcan.cz/publications/'),None)
        if pub is None: issues.append('publications Atom entry missing')
        else:
            pubdate=parse_dt(pub.findtext('a:updated',namespaces=ns)).date().isoformat()
            sm=ET.parse(ROOT/'sitemap.xml').getroot(); sns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
            lm=None
            for u in sm.findall('s:url',sns):
                if u.findtext('s:loc',namespaces=sns)=='https://likavcan.cz/publications/': lm=u.findtext('s:lastmod',namespaces=sns)
            if lm and pubdate!=lm: issues.append(f'publications feed date {pubdate} != sitemap lastmod {lm}')
    except Exception as exc:
        issues.append(str(exc))
    if issues:
        for x in issues: fail('feed consistency: '+x)
    else: ok('Atom feed chronology, unique IDs and publications date')



def check_v023_content_cta():
    issues=[]
    checks={
        'lukas/index.html': ['technickej príprave medzinárodných R&amp;D projektov', 'Navštíviť web ↗'],
        'en/lukas/index.html': ['technical preparation and engineering development of international R&amp;D projects', 'Visit website (Slovak) ↗'],
        'de/lukas/index.html': ['technischen Konzeption und ingenieurwissenschaftlichen Ausarbeitung internationaler F&amp;E-Projekte', 'Website besuchen (Slowakisch) ↗'],
        'projects/index.html': ['Pozrieť výskum', 'Navštíviť web ↗', 'button button--primary" href="/publications/">Publikácie'],
        'en/projects/index.html': ['View research', 'Visit website (Slovak) ↗', 'button button--primary" href="/en/publications/">Publications'],
        'de/projects/index.html': ['Forschung ansehen', 'Website besuchen (Slowakisch) ↗', 'button button--primary" href="/de/publications/">Publikationen'],
    }
    forbidden=('four international R&D project proposals','štyroch projekt','Horizon Europe','NATO DIANA','European Defence Fund')
    for rel,want in checks.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for token in want:
            if token not in txt: issues.append(f'{rel}: missing {token!r}')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for token in forbidden:
            if token in txt: issues.append(f'{rel}: unwanted proposal detail {token!r}')
    case_study_links={
      'projects/index.html': ('/projects/bezpecna-elektrika/','Prípadová štúdia'),
      'en/projects/index.html': ('/en/projects/bezpecna-elektrika/','Case study'),
      'de/projects/index.html': ('/de/projects/bezpecna-elektrika/','Fallstudie'),
    }
    for rel,(href,label) in case_study_links.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if f'href="{href}"' not in txt or f'>{label}</a>' not in txt:
            issues.append(f'{rel}: internal Bezpečná elektrika case-study CTA missing')
    if issues:
        for x in issues: fail('v0.2.3 content/CTA: '+x)
    else: ok('v0.2.3 R&D copy + clear primary CTA guardrails')



def check_v023_rc2_scrollspy():
    issues=[]
    for rel in ('peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<section[^>]*data-dock-section="([^"]+)"[^>]*id="education"|<section[^>]*id="education"[^>]*data-dock-section="([^"]+)"',txt)
        got=(m.group(1) or m.group(2)) if m else None
        if got!='career': issues.append(f'{rel}: education maps to {got!r}, expected career')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        pi=txt.find('id="projects"'); ui=txt.find('id="publications"'); ci=txt.find('id="contact"')
        if min(pi,ui,ci)<0 or not (pi < ui < ci): issues.append(f'{rel}: expected Projects -> Publications -> Contact section order')
    if issues:
        for x in issues: fail('v0.2.3-rc2 scrollspy: '+x)
    else: ok('v0.2.3-rc2 profile scrollspy sequence')


def check_v023_rc2_chronology():
    issues=[]
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<section[^>]*id="education".*?<div class="grid education-grid">(.*?)</div>\s*</div>\s*</section>',txt,re.S)
        if not m:
            issues.append(f'{rel}: education grid not found'); continue
        years=re.findall(r'<span class="badge">\s*(?:<time[^>]*>)?(2026|2017|2013|2011)(?:</time>)?\s*</span>',m.group(1))
        if years[:4] != ['2026','2017','2013','2011']:
            issues.append(f'{rel}: education order {years[:4]!r}')
    for rel in ('projects/index.html','en/projects/index.html','de/projects/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        bi=txt.find('id="bezpecna-elektrika"'); mi=txt.find('id="materials-research"')
        if min(bi,mi)<0 or not bi < mi: issues.append(f'{rel}: newest Bezpečná elektrika project is not first')
    if issues:
        for x in issues: fail('v0.2.3-rc2 chronology: '+x)
    else: ok('v0.2.3-rc2 reverse chronology on qualifications and projects')


def check_v023_rc5_credential_fit_preview():
    issues=[]
    image=ROOT/'assets/img/credentials/osvedcenie-e2a-lukas-likavcan-verejna-kopia.webp'
    preview=ROOT/'assets/img/credentials/osvedcenie-e2a-lukas-likavcan-verejna-kopia-preview.webp'
    if not image.exists() or image.stat().st_size < 10000:
        issues.append('missing/invalid public credential image')
    if preview.exists():
        issues.append('credential thumbnail must not return to education card')
    expected={
      'lukas/index.html':'Zobraziť verejnú kópiu osvedčenia',
      'en/lukas/index.html':'View public copy of certificate',
      'de/lukas/index.html':'Öffentliche Kopie der Bescheinigung anzeigen',
    }
    for rel,label in expected.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if label not in txt: issues.append(f'{rel}: credential label missing')
        if 'osvedcenie-e2a-lukas-likavcan-verejna-kopia.webp' not in txt: issues.append(f'{rel}: public credential href missing')
        if 'data-credential-viewer' not in txt or 'aria-haspopup="dialog"' not in txt:
            issues.append(f'{rel}: fit-preview viewer hook/semantics missing')
        if 'credential-card__preview' in txt:
            issues.append(f'{rel}: inline credential thumbnail returned')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    for token in ('data-credential-viewer', 'credential-lightbox', 'document.createElement("dialog")', 'dialog.showModal()', 'sizeButton', 'setCredentialSize'):
        if token not in js: issues.append('credential viewer JS missing '+token)
    for token in ('.credential-lightbox', '.credential-lightbox__image', '.credential-lightbox__viewport', 'body.is-credential-viewer-open'):
        if token not in css: issues.append('credential viewer CSS missing '+token)
    if issues:
        for x in issues: fail('credential viewer base: '+x)
    else: ok('credential viewer opens fit-to-screen and preserves dialog/keyboard behavior')


def check_v024_credential_in_viewer_size_toggle():
    issues=[]
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    required_js=(
        'fitStatus: "Prispôsobené displeju"',
        'nativeStatus: "100 % · natívna veľkosť"',
        'fitAction: "Prispôsobiť"',
        'fitStatus: "Fit to screen"',
        'fitAction: "Fit"',
        'fitStatus: "An Display angepasst"',
        'fitAction: "Anpassen"',
        'dialog.classList.toggle("is-native-size", nativeSize)',
        'sizeButton.setAttribute("aria-pressed"',
        'sizeButton.addEventListener("click", () => setCredentialSize(!nativeSize))',
        'image.addEventListener("click", () => setCredentialSize(!nativeSize))',
        'image.dataset.src = trigger.href',
        'requestAnimationFrame(() =>',
        'image.src = image.dataset.src',
    )
    for token in required_js:
        if token not in js: issues.append('missing in-viewer size-toggle JS: '+token)
    forbidden_js=(
        'imageLink.target = "_blank"',
        'imageLink.href = href',
        'window.open(',
        'location.href = trigger.href',
    )
    for token in forbidden_js:
        if token in js: issues.append('raw credential navigation returned: '+token)
    required_css=(
        '.credential-lightbox.is-native-size .credential-lightbox__viewport',
        '.credential-lightbox.is-native-size .credential-lightbox__image',
        'max-width: none;',
        'max-height: none;',
        'overflow: auto;',
        'cursor: zoom-in;',
        'cursor: zoom-out;',
    )
    for token in required_css:
        if token not in css: issues.append('missing native-size viewer CSS: '+token)
    if issues:
        for x in issues: fail('v0.2.4 credential in-viewer size toggle: '+x)
    else: ok('v0.2.4 credential toggles fit/native 100% by toolbar or image click without raw-image navigation')

def check_v024_credential_dialog_cold_start():
    issues=[]
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    required_js=(
        'document.createElement("dialog")',
        'dialog.setAttribute("aria-describedby", "credential-lightbox-hint")',
        'image.width = 1097',
        'image.height = 1536',
        'image.dataset.src = trigger.href',
        'setCredentialSize(false)',
        'dialog.showModal()',
        'requestAnimationFrame(() =>',
        'image.src = image.dataset.src',
        'closeButton.focus()',
        'dialog.addEventListener("close", cleanupClosedCredentialViewer)',
        'if (event.target === dialog) closeCredentialViewer()',
    )
    for token in required_js:
        if token not in js: issues.append('missing RC15-style dialog/cold-start JS: '+token)
    order_tokens=(
        'setCredentialSize(false)',
        'dialog.showModal()',
        'requestAnimationFrame(() =>',
        'image.src = image.dataset.src',
    )
    positions=[js.find(token, js.find('const openCredentialViewer')) for token in order_tokens]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        issues.append('credential cold-start order must be fit -> showModal -> requestAnimationFrame -> image src')
    open_block=js[js.find('const openCredentialViewer'):js.find('credentialViewerLinks.forEach', js.find('const openCredentialViewer'))]
    show_pos=open_block.find('dialog.showModal()')
    src_pos=open_block.find('image.src = image.dataset.src')
    if src_pos >= 0 and show_pos >= 0 and src_pos < show_pos:
        issues.append('full credential src assigned before dialog.showModal')
    required_css=(
        'width: min(96vw, 1500px);',
        'height: min(95dvh, 1100px);',
        '.credential-lightbox::backdrop',
        'background: rgba(0, 0, 0, 0.78);',
        'width: 100%;',
        'height: 100%;',
        'object-fit: contain;',
        'width: 1097px;',
        'height: 1536px;',
        '@media (max-width: 620px)',
        'width: 100vw;',
        'height: 100dvh;',
        'border-radius: 0;',
    )
    for token in required_css:
        if token not in css: issues.append('missing RC15-style dialog sizing CSS: '+token)
    if issues:
        for x in issues: fail('v0.2.4 credential dialog cold-start: '+x)
    else: ok('v0.2.4 credential uses native dialog with deferred Android cold-start load and explicit fit/native sizing')


def check_v023_rc2_credential_schema():
    issues=[]
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html','structured-data/lukas.jsonld'):
        if rel.endswith('.html'):
            objs=_jsonld_objects(rel)
        else:
            data=json.loads((ROOT/rel).read_text(encoding='utf-8'))
            objs=data.get('@graph',[])
        people=[o for o in objs if o.get('@type')=='Person' and o.get('@id')==EXPECTED['lukas']['person_id']]
        if len(people)!=1:
            issues.append(f'{rel}: canonical Person missing'); continue
        creds=people[0].get('hasCredential',[])
        e2a=[c for c in creds if isinstance(c,dict) and c.get('credentialCategory')=='E2/A']
        if len(e2a)!=1 or e2a[0].get('dateCreated')!='2026-08-20': issues.append(f'{rel}: E2/A credential schema missing or inconsistent')
    if issues:
        for x in issues: fail('credential schema: '+x)
    else: ok('E2/A credential reflected consistently in Person structured data')



def check_v023_rc3_desktop_profile_nav():
    issues=[]
    expected={
      'lukas/index.html':['profile','projects','publications','contact'],
      'en/lukas/index.html':['profile','projects','publications','contact'],
      'de/lukas/index.html':['profile','projects','publications','contact'],
      'peter/index.html':['profile','career','expertise','contact'],
      'en/peter/index.html':['profile','career','expertise','contact'],
      'de/peter/index.html':['profile','career','expertise','contact'],
    }
    for rel,keys_expected in expected.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<nav[^>]*class="profile-nav"[^>]*data-profile-nav[^>]*>.*?</nav>',txt,re.S)
        if not m:
            issues.append(f'{rel}: desktop profile nav hook missing'); continue
        keys=re.findall(r'data-dock-key="([^"]+)"',m.group(0))
        if keys!=keys_expected: issues.append(f'{rel}: desktop profile keys {keys!r}')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    for token in ('.profile-nav[data-profile-nav]', 'position: sticky', '.profile-nav a.is-active'):
        if token not in css: issues.append('desktop profile nav CSS missing '+token)
    for token in ('desktopProfileNav', 'profileNavSurfaces', 'setProfileNavActive', 'aria-current", "location"'):
        if token not in js: issues.append('shared desktop/mobile scrollspy missing '+token)
    if issues:
        for x in issues: fail('v0.2.3-rc3 desktop nav: '+x)
    else: ok('v0.2.3-rc3 sticky desktop profile nav shares mobile scrollspy')


def check_v023_rc4_compact_desktop_and_education():
    issues=[]
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    for token in ('.education-grid', 'grid-template-columns: repeat(2, minmax(0, 1fr))', '@media (max-width: 800px)', 'justify-content: flex-end', 'min-height: 56px', 'min-height: 40px'):
        if token not in css: issues.append('compact/grid CSS missing '+token)
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'class="grid education-grid"' not in txt: issues.append(f'{rel}: education-grid hook missing')
        if 'credential-card__preview' in txt or 'osvedcenie-e2a-lukas-likavcan-verejna-kopia-preview.webp' in txt:
            issues.append(f'{rel}: credential thumbnail remains')
        years=re.findall(r'<span class="badge">\s*(?:<time[^>]*>)?(2026|2017|2013|2011)(?:</time>)?\s*</span>', txt[txt.find('id="education"'):txt.find('id="expertise"')])
        if years[:4] != ['2026','2017','2013','2011']:
            issues.append(f'{rel}: education order {years[:4]!r}')
    data=json.loads((ROOT/'structured-data/lukas.jsonld').read_text(encoding='utf-8'))
    people=[o for o in data.get('@graph',[]) if o.get('@type')=='Person' and o.get('@id')==EXPECTED['lukas']['person_id']]
    creds=people[0].get('hasCredential',[]) if len(people)==1 else []
    if not any(isinstance(c,dict) and c.get('credentialCategory')=='E2/A' for c in creds):
        issues.append('structured-data/lukas.jsonld: E2/A credential missing')
    if issues:
        for x in issues: fail('v0.2.3-rc4 compact desktop/education: '+x)
    else: ok('v0.2.4 compact desktop nav + row-readable 2-column education grid / 1-column mobile')



def check_v024_integrated_sources():
    issues=[]
    profiles=('lukas/index.html','en/lukas/index.html','de/lukas/index.html',
              'peter/index.html','en/peter/index.html','de/peter/index.html')

    # Human-first rule: no standalone verification/evidence section on either profile.
    forbidden_visible=(
        'Nezávislé zdroje a overenie','Nezávislé akademické zdroje',
        'Independent sources and verification','Independent academic evidence',
        'Unabhängige Quellen und Nachweise','Unabhängige akademische Nachweise',
        'Prospechové štipendium','Merit scholarship','Leistungsstipendium',
        'Prijatie na Ing. program','Admission to engineering programme','Zulassung zum Ingenieurstudium'
    )
    for rel in profiles:
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'class="section evidence-section"' in txt:
            issues.append(f'{rel}: standalone profile evidence section remains')
        for phrase in forbidden_visible:
            if phrase in txt:
                issues.append(f'{rel}: public proof/achievement wording remains: {phrase}')

    # Degree normalization remains stable across embedded and mirror structured data.
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html',
                'peter/index.html','en/peter/index.html','de/peter/index.html',
                'structured-data/lukas.jsonld','structured-data/peter.jsonld'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'Master of Engineering (Ing.)' in txt or 'MEng' in txt:
            issues.append(f'{rel}: misleading MEng credential remains')
        if "Engineer's degree (Ing.)" not in txt:
            issues.append(f'{rel}: normalized Engineer degree credential missing')

    # Lukáš: project 1341 is normal Projects content; academic sources are contextual.
    for rel in ('projects/index.html','en/projects/index.html','de/projects/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'id="young-researcher-1341"' not in txt or 'Prehlad_projektov_riesenych_v_r._2015.pdf' not in txt:
            issues.append(f'{rel}: project 1341 not integrated into Projects')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for token in ('page_id=13318','page_id=10880','page_id=8406'):
            if token not in txt: issues.append(f'{rel}: contextual Education source missing {token}')

    # Peter: only the professionally relevant thesis is public; scholarship/admission are archival only.
    for rel in ('peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'stu.stuzp55130' not in txt or 'Process Simulate' not in txt or 'Virtual Commissioning' not in txt:
            issues.append(f'{rel}: Peter thesis not integrated in Education')
        if '2012_prosp_stip_web_2bc_zoznam.pdf' in txt or '2014_07_18_Zoznam_prijatych_uch_ING.pdf' in txt:
            issues.append(f'{rel}: archival scholarship/admission URL leaked into public profile')

    # Publications keep stable Book nodes and quiet contextual source links.
    for rel in ('publications/index.html','en/publications/index.html','de/publications/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if txt.count('class="publication-source"') < 2 or 'publication-evidence' in txt:
            issues.append(f'{rel}: publication sources not converted to contextual model')
        objs=_jsonld_objects(rel)
        books=[o for o in objs if o.get('@type')=='Book']
        isbns={o.get('isbn') for o in books}
        if {'978-80-8096-296-8','978-80-8096-281-4'} - isbns:
            issues.append(f'{rel}: stable Book nodes missing')
        for book in books:
            if book.get('isbn') in {'978-80-8096-296-8','978-80-8096-281-4'}:
                authors=book.get('author',[])
                if not any(isinstance(a,dict) and a.get('@id')==EXPECTED['lukas']['person_id'] for a in authors):
                    issues.append(f'{rel}: Book -> canonical Lukáš author relation missing')

    # Institutional sources must never become sameAs; Peter subjectOf must not expose scholarship/admission.
    for rel in profiles:
        for o in _jsonld_objects(rel):
            if o.get('@type')=='Person':
                vals=o.get('sameAs',[]); vals=[vals] if isinstance(vals,str) else vals
                if any('mtf.stuba.sk' in x or 'dk.fchpt.stuba.sk' in x for x in vals if isinstance(x,str)):
                    issues.append(f'{rel}: institutional source leaked into Person.sameAs')
                if o.get('@id')==EXPECTED['peter']['person_id']:
                    raw=json.dumps(o.get('subjectOf',[]),ensure_ascii=False)
                    if 'prosp_stip' in raw or 'Zoznam_prijatych_uch_ING' in raw:
                        issues.append(f'{rel}: Peter archival scholarship/admission remains in subjectOf')
                    ka=o.get('knowsAbout',[])
                    if 'KUKA robots' in ka: issues.append(f'{rel}: vendor brand remains in Peter knowsAbout')

    # Discovery copy should describe professional facts, not verification strategy.
    feed=(ROOT/'feed.xml').read_text(encoding='utf-8')
    for token in ('#release-v0.2.4','https://likavcan.cz/lukas/','https://likavcan.cz/peter/'):
        if token not in feed: issues.append('feed missing '+token)
    if 'Identity &amp; Evidence Layer' in feed or 'independent institutional evidence' in feed or 'academic evidence' in feed:
        issues.append('feed still foregrounds evidence/verification rhetoric')
    llms=(ROOT/'llms.txt').read_text(encoding='utf-8')
    if 'Institutional evidence:' in llms:
        issues.append('llms.txt still foregrounds evidence strategy')
    if llms.count('- LinkedIn: ') != 2: issues.append('llms.txt must expose LinkedIn identity for both people')

    sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8')
    profile_urls=('/lukas/','/peter/','/en/lukas/','/en/peter/','/de/lukas/','/de/peter/')
    changed_project_indexes=('/projects/','/en/projects/','/de/projects/')
    changed_publications=('/publications/','/en/publications/','/de/publications/')
    for url in profile_urls:
        if f'<loc>https://likavcan.cz{url}</loc>\n    <lastmod>2026-10-16</lastmod>' not in sitemap:
            issues.append(f'sitemap profile lastmod not updated for {url}')
    for url in changed_project_indexes:
        if f'<loc>https://likavcan.cz{url}</loc>\n    <lastmod>2026-10-16</lastmod>' not in sitemap:
            issues.append(f'sitemap changed project-index lastmod drift for {url}')
    for url in changed_publications:
        if f'<loc>https://likavcan.cz{url}</loc>\n    <lastmod>2026-10-16</lastmod>' not in sitemap:
            issues.append(f'sitemap changed publications lastmod drift for {url}')

    registry=(ROOT/'docs/evidence-registry-v0.2.4.md')
    if not registry.exists() or '2012_prosp_stip_web_2bc_zoznam.pdf' not in registry.read_text(encoding='utf-8'):
        issues.append('internal evidence registry missing archival provenance')

    if issues:
        for x in issues: fail('v0.2.4 integrated sources: '+x)
    else: ok('v0.2.4 human-first integrated sources / identity consistency guardrails')



def check_v024_final_polish():
    issues=[]

    # Human-facing source labels: no verification/evidence rhetoric in the Branson source link.
    expected_labels={
      'lukas/index.html':'STU – profil absolventa ↗',
      'en/lukas/index.html':'STU – graduate profile ↗',
      'de/lukas/index.html':'STU – Absolventenprofil ↗',
    }
    forbidden=('Overenie väzby STU + odborný kontext Branson',
               'STU employment evidence + Branson technology context',
               'STU-Nachweis + Branson-Technologiekontext')
    for rel,label in expected_labels.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if label not in txt: issues.append(f'{rel}: factual STU graduate-profile label missing')
        for phrase in forbidden:
            if phrase in txt: issues.append(f'{rel}: verification-style Branson label remains')

    # Three current Lukáš fields are linked to precise Wikidata topics in all localized inline graphs and standalone data.
    topics={
      'Ultrasonic welding':'https://www.wikidata.org/wiki/Q580160',
      'Injection moulding':'https://www.wikidata.org/wiki/Q260606',
      'Computer-aided engineering (CAE)':'https://www.wikidata.org/wiki/Q1050567',
    }
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        people=[o for o in _jsonld_objects(rel) if o.get('@type')=='Person' and o.get('@id')==EXPECTED['lukas']['person_id']]
        if len(people)!=1:
            issues.append(f'{rel}: canonical Lukáš Person count {len(people)}')
            continue
        vals=people[0].get('knowsAbout',[])
        found={x.get('name'):x.get('sameAs') for x in vals if isinstance(x,dict)}
        for name,url in topics.items():
            if found.get(name)!=url: issues.append(f'{rel}: knowsAbout Wikidata mapping missing for {name}')

    # Standalone JSON-LD mirrors selected canonical invariants from the SK inline graph, but descriptions may remain language-neutral.
    def keyed(objs):
        return {o.get('@id'):o for o in objs if isinstance(o,dict) and o.get('@id')}
    def top_level_graph(rel):
        doc=DocParser(); doc.feed((ROOT/rel).read_text(encoding='utf-8'))
        out=[]
        for raw in doc.jsonld:
            data=json.loads(raw)
            out.extend(data.get('@graph',[data]))
        return out
    person_fields=('sameAs','jobTitle','alumniOf','knowsAbout','hasCredential','subjectOf')
    page_fields=('dateModified','primaryImageOfPage','mainEntity','hasPart')
    for person in ('lukas','peter'):
        inline=keyed(top_level_graph(f'{person}/index.html'))
        standalone=json.loads((ROOT/f'structured-data/{person}.jsonld').read_text(encoding='utf-8'))
        mirror=keyed(standalone.get('@graph',[]))
        pid=EXPECTED[person]['person_id']
        pgid=f'https://likavcan.cz/{person}/#profile-page'
        for oid,fields in ((pid,person_fields),(pgid,page_fields)):
            if oid not in inline or oid not in mirror:
                issues.append(f'{person}: canonical JSON-LD object missing {oid}')
                continue
            for field in fields:
                if inline[oid].get(field)!=mirror[oid].get(field):
                    issues.append(f'{person}: standalone/inline invariant drift in {field}')

    # Privacy date synchronization: no invented GA4 retention value is introduced.
    de_priv=(ROOT/'de/privacy/index.html').read_text(encoding='utf-8')
    if '<strong>Stand der Informationen:</strong> 15.09.2026.' not in de_priv:
        issues.append('DE Privacy information date not synchronized to 15.09.2026')
    if '<strong>Stand der Informationen:</strong> 14.09.2026.' in de_priv:
        issues.append('stale DE Privacy date 14.09.2026 remains')
    for rel in ('privacy/index.html','en/privacy/index.html','de/privacy/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'Podľa aktuálneho nastavenia Google Analytics property' not in txt and rel=='privacy/index.html':
            issues.append('SK generic GA4 retention wording unexpectedly changed')
        if 'According to the current Google Analytics property setting' not in txt and rel=='en/privacy/index.html':
            issues.append('EN generic GA4 retention wording unexpectedly changed')
        if 'Gemäß der aktuellen Einstellung der Google-Analytics-Property' not in txt and rel=='de/privacy/index.html':
            issues.append('DE generic GA4 retention wording unexpectedly changed')

    # Methodology is site-wide (my/we/wir), with no stale singular metadata or case-study link labels.
    methodology={
      'methodology/index.html':('Ako pracujeme so zdrojmi','Oddeľujeme meranie','Dátum aktualizácie meníme'),
      'en/methodology/index.html':('How we work with sources','We separate measurement','We change an update date'),
      'de/methodology/index.html':('Wie wir mit Quellen','Wir trennen Messung','Ein Aktualisierungsdatum ändern wir'),
    }
    stale=('Ako pracujem so zdrojmi','uprednostňujem','Oddeľujem meranie','Dátum aktualizácie mením pri',
           'How I work with sources','I prefer original','I separate measurement','I change an update date',
           'Wie ich mit Quellen','bevorzuge ich','Ich trenne Messung','ändere ich')
    for rel,required in methodology.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for phrase in required:
            if phrase not in txt: issues.append(f'{rel}: shared methodology voice missing {phrase}')
        for phrase in stale:
            if phrase in txt: issues.append(f'{rel}: stale singular methodology voice remains: {phrase}')
    for rel,phrase in (
      ('projects/fibre-orientation-injection-moulding/index.html','Ako pracujeme so zdrojmi'),
      ('en/projects/fibre-orientation-injection-moulding/index.html','How we work with sources'),
      ('de/projects/fibre-orientation-injection-moulding/index.html','Wie wir mit Quellen arbeiten')):
        if phrase not in (ROOT/rel).read_text(encoding='utf-8'):
            issues.append(f'{rel}: methodology link label not synchronized')

    # Apple touch icon: one 180x180 PNG, root-relative link on every HTML page, no PWA layer.
    icon=ROOT/'apple-touch-icon.png'
    if not icon.exists():
        issues.append('apple-touch-icon.png missing')
    else:
        data=icon.read_bytes()
        if len(data)<24 or data[:8]!=b'\x89PNG\r\n\x1a\n':
            issues.append('apple-touch-icon.png is not a valid PNG header')
        else:
            w=int.from_bytes(data[16:20],'big'); h=int.from_bytes(data[20:24],'big')
            if (w,h)!=(180,180): issues.append(f'apple-touch-icon dimensions {(w,h)!r}, expected 180x180')
    for p in ROOT.rglob('*.html'):
        txt=p.read_text(encoding='utf-8')
        if txt.count('href="/apple-touch-icon.png" rel="apple-touch-icon" sizes="180x180"')!=1:
            issues.append(f'{p.relative_to(ROOT)}: apple touch icon link missing/duplicated')
    for name in ('manifest.json','site.webmanifest','manifest.webmanifest','service-worker.js','sw.js'):
        if (ROOT/name).exists(): issues.append(f'unrequested PWA artifact present: {name}')

    if issues:
        for x in issues: fail('v0.2.4 final polish: '+x)
    else: ok('v0.2.4 final polish / JSON-LD sync / methodology voice / Apple touch icon')


def check_v024_contact_scrollspy_bottom():
    issues=[]
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    for token in (
        'const maxScroll = Math.max(0, root.scrollHeight - window.innerHeight);',
        'const atDocumentEnd = maxScroll > 0 && window.scrollY >= maxScroll - 8;',
        'const lastSection = trackedSections[trackedSections.length - 1];',
        'activeKey = lastSection?.dataset.dockSection || activeKey;',
    ):
        if token not in js:
            issues.append('bottom-of-page scrollspy fallback missing '+token)

    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html',
                'peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        sections=re.findall(r'<section[^>]*data-dock-section="([^"]+)"[^>]*',txt)
        if not sections or sections[-1] != 'contact':
            issues.append(f'{rel}: Contact is not the final tracked scrollspy section')
        if 'data-dock-key="contact"' not in txt:
            issues.append(f'{rel}: Contact navigation key missing')

    if issues:
        for x in issues: fail('v0.2.4 contact scrollspy: '+x)
    else: ok('v0.2.4 Contact activates at document end on desktop/mobile scrollspy')

def check_v024_profile_nav_anchor_alignment():
    issues=[]
    base=(ROOT/'assets/css/base.css').read_text(encoding='utf-8')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')

    # Fragment scrolling must use exactly one sticky-header offset source.
    # Combining scroll-padding on <html> with the same scroll-margin on the
    # target section places the target below the scrollspy trigger and leaves
    # the previous navigation item active after a click.
    if 'scroll-padding-top: var(--scroll-offset, 96px);' not in base:
        issues.append('root scroll-padding offset missing')
    if re.search(r'scroll-margin-top\s*:\s*var\(--scroll-offset', base):
        issues.append('duplicate section scroll-margin uses --scroll-offset')
    if '`${headerHeight + profileNavHeight + 16}px`' not in js:
        issues.append('scroll offset no longer matches sticky header + profile nav model')
    if 'headerBottom + desktopHeight + 24' not in js:
        issues.append('scrollspy trigger no longer keeps the intended 8px activation tolerance')

    # Every desktop profile-nav fragment must resolve to a tracked section
    # with the same dock key in every locale and on both profiles.
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html',
                'peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        nav_match=re.search(r'<nav[^>]*class="profile-nav"[^>]*data-profile-nav[^>]*>(.*?)</nav>', txt, re.S)
        if not nav_match:
            issues.append(f'{rel}: desktop profile nav missing')
            continue
        links=re.findall(r'<a[^>]*data-dock-key="([^"]+)"[^>]*href="#([^"]+)"[^>]*>', nav_match.group(1))
        if not links:
            issues.append(f'{rel}: no desktop profile-nav fragment links found')
            continue
        for key,target in links:
            section=re.search(rf'<section[^>]*(?=[^>]*\bid="{re.escape(target)}")(?=[^>]*\bdata-dock-section="([^"]+)")[^>]*>', txt)
            if not section:
                issues.append(f'{rel}: #{target} is not a tracked section for {key}')
            elif section.group(1) != key:
                issues.append(f'{rel}: #{target} maps to {section.group(1)}, expected {key}')

    if issues:
        for x in issues: fail('v0.2.4 profile-nav anchor alignment: '+x)
    else: ok('v0.2.4 profile-nav clicks align with scrollspy on Lukáš/Peter in SK/EN/DE')



def check_v024_mobile_nav_alignment():
    issues=[]
    base=(ROOT/'assets/css/base.css').read_text(encoding='utf-8')
    responsive=(ROOT/'assets/css/responsive.css').read_text(encoding='utf-8')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')

    # On mobile the desktop profile strip is hidden, so anchor positioning must
    # use only the sticky site header. The fixed bottom dock must not be folded
    # into the top anchor offset.
    for token in (
        '.profile-nav {\n    display: none;',
        '.mobile-profile-dock {\n    position: fixed;',
    ):
        if token not in responsive:
            issues.append('mobile navigation CSS invariant missing: '+token.split('{')[0].strip())
    if 'profileNav && window.getComputedStyle(profileNav).display !== "none"' not in js:
        issues.append('hidden desktop profile nav is not excluded from mobile scroll offset')
    if 'desktopProfileNav && window.getComputedStyle(desktopProfileNav).display !== "none"' not in js:
        issues.append('hidden desktop profile nav is not excluded from mobile scrollspy trigger')
    if 'scroll-padding-top: var(--scroll-offset, 96px);' not in base:
        issues.append('mobile fragment scroll-padding source missing')
    if re.search(r'scroll-margin-top\s*:\s*var\(--scroll-offset', base):
        issues.append('duplicate mobile section scroll-margin uses --scroll-offset')

    # Peter's mobile dock is same-page section navigation. Every fragment must
    # map to the same data-dock key, just like the desktop strip.
    peter_expected=[('profile','profile'),('career','experience'),('expertise','expertise'),('contact','contact')]
    for rel in ('peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        nav=re.search(r'<nav[^>]*class="mobile-profile-dock"[^>]*>(.*?)</nav>',txt,re.S)
        if not nav:
            issues.append(f'{rel}: mobile dock missing'); continue
        links=re.findall(r'<a[^>]*data-dock-key="([^"]+)"[^>]*href="#([^"]+)"[^>]*>',nav.group(1))
        if links != peter_expected:
            issues.append(f'{rel}: mobile fragment map {links!r}, expected {peter_expected!r}')
        for key,target in links:
            sec=re.search(rf'<section[^>]*(?=[^>]*\bid="{re.escape(target)}")(?=[^>]*\bdata-dock-section="([^"]+)")[^>]*>',txt)
            if not sec or sec.group(1)!=key:
                issues.append(f'{rel}: mobile #{target} does not map to {key}')

    # Lukáš deliberately uses the fixed mobile dock as stable cross-page
    # navigation for Projects/Publications; Profile and Contact return to the
    # profile. Verify the destination page declares the matching default key.
    lukas_expected=[('profile','./'),('projects','../projects/'),('publications','../publications/'),('contact','./#contact')]
    for lang_prefix in ('','en/','de/'):
        rel=f'{lang_prefix}lukas/index.html'
        txt=(ROOT/rel).read_text(encoding='utf-8')
        nav=re.search(r'<nav[^>]*class="mobile-profile-dock"[^>]*>(.*?)</nav>',txt,re.S)
        if not nav:
            issues.append(f'{rel}: mobile dock missing'); continue
        links=re.findall(r'<a[^>]*data-dock-key="([^"]+)"[^>]*href="([^"]+)"[^>]*>',nav.group(1))
        if links != lukas_expected:
            issues.append(f'{rel}: stable mobile routes {links!r}, expected {lukas_expected!r}')
        contact=re.search(r'<section[^>]*(?=[^>]*\bid="contact")(?=[^>]*\bdata-dock-section="([^"]+)")[^>]*>',txt)
        if not contact or contact.group(1)!='contact':
            issues.append(f'{rel}: mobile Contact target is not tracked as contact')
        for page,key in (('projects/index.html','projects'),('publications/index.html','publications')):
            dest=(ROOT/f'{lang_prefix}{page}').read_text(encoding='utf-8')
            m=re.search(r'<nav[^>]*class="mobile-profile-dock"[^>]*data-dock-default="([^"]+)"',dest)
            if not m:
                # attribute order differs on Publications, accept the inverse order too.
                m=re.search(r'<nav[^>]*data-dock-default="([^"]+)"[^>]*class="mobile-profile-dock"',dest)
            if not m or m.group(1)!=key:
                issues.append(f'{lang_prefix}{page}: mobile destination default is not {key}')

    if issues:
        for x in issues: fail('v0.2.4 mobile nav alignment: '+x)
    else: ok('v0.2.4 mobile dock navigation aligns with scrollspy/routes on Lukáš/Peter in SK/EN/DE')

def check_v024_home_portrait_links():
    issues=[]
    pages={
        'SK': ROOT/'index.html',
        'EN': ROOT/'en/index.html',
        'DE': ROOT/'de/index.html',
    }
    expected={
        'SK': [('lukas/', 'Otvoriť profil Lukáša Likavčana'), ('peter/', 'Otvoriť profil Petra Likavčana')],
        'EN': [('lukas/', 'Open Lukáš Likavčan profile'), ('peter/', 'Open Peter Likavčan profile')],
        'DE': [('lukas/', 'Profil von Lukáš Likavčan öffnen'), ('peter/', 'Profil von Peter Likavčan öffnen')],
    }
    for lang,path in pages.items():
        html=path.read_text(encoding='utf-8')
        for href,label in expected[lang]:
            pattern=rf'<a[^>]*class="home-profile-card__portrait-link"[^>]*href="{re.escape(href)}"[^>]*aria-label="{re.escape(label)}"|<a[^>]*aria-label="{re.escape(label)}"[^>]*href="{re.escape(href)}"[^>]*class="home-profile-card__portrait-link"'
            if not re.search(pattern, html):
                issues.append(f'{lang}: missing accessible portrait link to {href}')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    if '.home-profile-card__portrait-link:focus-visible' not in css:
        issues.append('portrait links missing visible keyboard focus style')
    if issues:
        for x in issues: fail('v0.2.4 homepage portrait links: '+x)
    else: ok('v0.2.4 homepage portraits link directly to Lukáš/Peter profiles in SK/EN/DE with keyboard focus')

def check_v024_back_to_top():
    issues=[]
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    components=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    responsive=(ROOT/'assets/css/responsive.css').read_text(encoding='utf-8')
    for token in (
        'const backToTopCopy = {sk:"Späť hore", en:"Back to top", de:"Nach oben"};',
        'backToTop.className = "back-to-top";',
        'window.scrollTo({top:0, behavior});',
        'prefersReducedMotion.matches ? "auto" : "smooth"',
        'scrollRange > 640',
        'document.querySelector(".cookie-banner.is-visible")',
    ):
        if token not in js:
            issues.append('back-to-top JS invariant missing: '+token)
    for token in (
        '.back-to-top {',
        '.back-to-top.is-visible {',
        '.back-to-top:focus-visible {',
    ):
        if token not in components:
            issues.append('back-to-top component style missing: '+token)
    if 'body.has-mobile-dock .back-to-top {' not in responsive or 'var(--mobile-dock-height)' not in responsive:
        issues.append('back-to-top is not offset above the fixed mobile dock')
    if issues:
        for x in issues: fail('v0.2.4 back-to-top: '+x)
    else: ok('v0.2.4 long-page back-to-top control is localized, accessible and mobile-dock aware')


def check_v024_deploy_readiness():
    issues=[]
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    components=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    responsive=(ROOT/'assets/css/responsive.css').read_text(encoding='utf-8')
    if 'createSettingsButton' in js or 'cookie-settings-button' in js:
        issues.append('floating Cookie settings control returned in JS')
    if '.cookie-settings-button' in components or '.cookie-settings-button' in responsive:
        issues.append('floating Cookie settings control returned in CSS')
    for p in public_index_files():
        txt=p.read_text(encoding='utf-8')
        if 'data-open-cookie-settings' not in txt:
            issues.append(f'{p.relative_to(ROOT)}: footer Cookie settings control missing')

    hidden_only=(
      'https://www.mtf.stuba.sk/buxus/docs/doc/svk/2019/abstrakty/Vyrobne_technologie_2.pdf',
      'https://kis.cvt.stuba.sk/arl-stu/en/result/?disp=+Likav%C4%8Dan%2C+Luk%C3%A1%C5%A1%2C&field=AUP&qt=zf&src=stu_us_cat&term=%22%5ELikav%C4%8Dan%2C+Luk%C3%A1%C5%A1%2C%5E%22',
      'https://kis.stuba.sk/arl-stu/en/result/?disp=Likav%C4%8Dan+Peter&field=AUK&qt=zf&src=stu_us_cat&term=%22%5Estu_us_auth%5C%2Astu138973%5E%22',
    )
    public_profiles=('lukas/index.html','en/lukas/index.html','de/lukas/index.html','peter/index.html','en/peter/index.html','de/peter/index.html','structured-data/lukas.jsonld','structured-data/peter.jsonld')
    for rel in public_profiles:
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for url in hidden_only:
            if url in txt:
                issues.append(f'{rel}: archival-only corroboration remains in public/mirrored Person graph')
    registry=(ROOT/'docs/evidence-registry-v0.2.4.md').read_text(encoding='utf-8')
    for url in hidden_only:
        if url not in registry:
            issues.append('internal evidence registry lost archival provenance '+url)

    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html','peter/index.html','en/peter/index.html','de/peter/index.html'):
        objs=_jsonld_objects(rel)
        pages=[o for o in objs if o.get('@type')=='ProfilePage']
        if len(pages)!=1 or pages[0].get('dateModified')!='2026-10-16T17:08:00+02:00':
            issues.append(f'{rel}: final ProfilePage dateModified drift')

    if issues:
        for x in issues: fail('v0.2.4 deploy readiness: '+x)
    else: ok('v0.2.5 preview footer/privacy controls + schema purity + updated profile metadata')

def check_v025_preview_identity_reinforcement():
    issues=[]
    homes={
      'index.html': ('Materiálový inžinier · R&amp;D špecialista · BIZZCOM','Simulation Specialist · Porsche Werkzeugbau'),
      'en/index.html': ('Materials Engineer · R&amp;D Specialist · BIZZCOM','Simulation Specialist · Porsche Werkzeugbau'),
      'de/index.html': ('Werkstoffingenieur · F&amp;E-Spezialist · BIZZCOM','Simulationsspezialist · Porsche Werkzeugbau'),
    }
    for rel,(lukas_role,peter_role) in homes.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if lukas_role not in txt or peter_role not in txt:
            issues.append(f'{rel}: role/employer anchors missing')
        if 'home-profile-card__name-link' not in txt or txt.count('home-profile-card__name-link') != 2:
            issues.append(f'{rel}: canonical name links missing')
        if txt.count('Wikidata ↗') != 2:
            issues.append(f'{rel}: expected two subtle Wikidata links')
        for qid in ('Q139947576','Q139977167'):
            if qid not in txt: issues.append(f'{rel}: missing {qid}')
        # Human-first order: LinkedIn, vCard, Wikidata inside each compact row.
        for who in ('Lukáš Likavčan','Peter Likavčan'):
            m=re.search(rf'<div aria-label="{re.escape(who)}" class="profile-quick-contact">(.*?)</div>',txt,re.S)
            if not m or not (m.group(1).find('LinkedIn') < m.group(1).find('vCard') < m.group(1).find('Wikidata')):
                issues.append(f'{rel}: {who} quick-link order drift')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        order=['LinkedIn ↗','vCard','Google Scholar ↗','ORCID 0000-0003-3949-6034 ↗','ResearchGate ↗','Wikidata ↗']
        pos=[txt.find(x) for x in order]
        if any(x<0 for x in pos) or pos != sorted(pos): issues.append(f'{rel}: visitor-first professional link order drift')
    for rel in ('peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'profile-links-bridge' not in txt or 'Q139977167' not in txt: issues.append(f'{rel}: Peter compact identity row missing')
        if 'orcid.org' in txt.lower() or 'researchgate.net' in txt.lower() or 'scholar.google.com' in txt.lower():
            issues.append(f'{rel}: artificial academic identity added to Peter')
    source='https://www.mtf.stuba.sk/buxus/docs/doc/informacie_o/Prehlad_projektov_riesenych_v_r._2015.pdf'
    for rel in ('projects/index.html','en/projects/index.html','de/projects/index.html','lukas/index.html','en/lukas/index.html','de/lukas/index.html','structured-data/lukas.jsonld'):
        if source not in (ROOT/rel).read_text(encoding='utf-8'):
            issues.append(f'{rel}: authoritative MTF 2015 project source missing')
    if issues:
        for x in issues: fail('v0.2.5 preview identity reinforcement: '+x)
    else: ok('v0.2.5 preview homepage/profile identity reinforcement + MTF project source')


def check_v025_preview_r3_polish():
    issues=[]
    # Profile metadata should lead with the full professional identity and current employer context.
    expected_titles={
      'lukas/index.html':'Ing. Lukáš Likavčan, PhD. | Materiálový inžinier | BIZZCOM',
      'en/lukas/index.html':'Ing. Lukáš Likavčan, PhD. | Materials Engineer | BIZZCOM',
      'de/lukas/index.html':'Ing. Lukáš Likavčan, PhD. | Werkstoffingenieur | BIZZCOM',
      'peter/index.html':'Ing. Peter Likavčan | Simulation Specialist | Porsche Werkzeugbau',
      'en/peter/index.html':'Ing. Peter Likavčan | Simulation Specialist | Porsche Werkzeugbau',
      'de/peter/index.html':'Ing. Peter Likavčan | Simulation Specialist | Porsche Werkzeugbau',
    }
    for rel,want in expected_titles.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if f'<title>{want}</title>' not in txt: issues.append(f'{rel}: profile title drift')
        if '2026-10-16T17:08:00+02:00' not in txt: issues.append(f'{rel}: dateModified not refreshed')
    sk=(ROOT/'lukas/index.html').read_text(encoding='utf-8')
    if 'riešeniach pre rôzne aplikácie spájania plastov' not in sk: issues.append('SK Lukáš Branson intro polish missing')
    projects_sk=(ROOT/'projects/index.html').read_text(encoding='utf-8')
    if 'Zodpovedný riešiteľ: Ing. Lukáš Likavčan.' not in projects_sk: issues.append('SK SFRT 1341 responsible-researcher wording missing')
    for rel in ('index.html','en/index.html','de/index.html','lukas/index.html','en/lukas/index.html','de/lukas/index.html','peter/index.html','en/peter/index.html','de/peter/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if 'Wikidata ↗' in txt and 'profile-quick-contact__muted-identity' not in txt:
            issues.append(f'{rel}: muted Wikidata identity styling missing')
    for rel in ('lukas/index.html','en/lukas/index.html','de/lukas/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        # ORCID is current again and should be active; ResearchGate remains visually secondary.
        m=re.search(r'<a(?![^>]*profile-quick-contact__muted-identity)[^>]*href="https://orcid.org/0000-0003-3949-6034"[^>]*>ORCID 0000-0003-3949-6034 ↗</a>',txt)
        if not m: issues.append(f'{rel}: ORCID is not in the active identity tier')
        m=re.search(r'<a[^>]*class="[^"]*profile-quick-contact__muted-identity[^"]*"[^>]*href="https://www.researchgate.net/profile/Lukas-Likavcan-2"[^>]*>ResearchGate ↗</a>',txt)
        if not m: issues.append(f'{rel}: ResearchGate is not visually muted')
    css=(ROOT/'assets/css/components.css').read_text(encoding='utf-8')
    if '@media (min-width: 769px)' not in css or 'minmax(220px, 280px)' not in css or 'clamp(3rem, 5vw, 4rem)' not in css:
        issues.append('desktop-only compact profile hero CSS missing')
    js=(ROOT/'assets/js/main.js').read_text(encoding='utf-8')
    for token in ('cookieReturnFocus','showBanner(true,b)','returnFocus.focus()'):
        if token not in js: issues.append('cookie focus management missing '+token)
    for rel in ('index.html','en/index.html','de/index.html'):
        nodes=list(_jsonld_objects(rel))
        for who,org in (('lukas','https://likavcan.cz/#bizzcom'),('peter','https://likavcan.cz/#porsche-werkzeugbau')):
            person=next((o for o in nodes if o.get('@type')=='Person' and o.get('@id')==EXPECTED[who]['person_id']),None)
            if not person: issues.append(f'{rel}: {who} homepage Person stub missing'); continue
            if person.get('worksFor',{}).get('@id')!=org: issues.append(f'{rel}: {who} worksFor homepage stub missing')
            if person.get('alumniOf',{}).get('@id')!='https://likavcan.cz/#mtf-stu': issues.append(f'{rel}: {who} alumniOf homepage stub missing')
            if not person.get('sameAs'): issues.append(f'{rel}: {who} sameAs homepage stub missing')
    if issues:
        for x in issues: fail('v0.2.5 Preview R3 polish: '+x)
    else: ok('v0.2.5 Preview R3 visual/entity/accessibility polish')



def check_v025_final_identity_precision():
    issues=[]
    # Restored ORCID is visible on Lukáš homepage in a compact active label; Peter remains unchanged.
    for rel in ('index.html','en/index.html','de/index.html'):
        txt=(ROOT/rel).read_text(encoding='utf-8')
        m=re.search(r'<div aria-label="Lukáš Likavčan" class="profile-quick-contact">(.*?)</div>',txt,re.S)
        if not m: issues.append(f'{rel}: Lukáš quick links missing'); continue
        row=m.group(1)
        order=['LinkedIn','vCard','ORCID ↗','Wikidata ↗']
        pos=[row.find(x) for x in order]
        if any(x<0 for x in pos) or pos != sorted(pos): issues.append(f'{rel}: Lukáš homepage quick-link order drift')
        if 'ORCID 0000-0003-3949-6034' in row: issues.append(f'{rel}: homepage ORCID should use compact label')
        if 'profile-quick-contact__muted-identity" href="https://orcid.org/' in row: issues.append(f'{rel}: homepage ORCID incorrectly muted')

    source='https://www.mtf.stuba.sk/buxus/docs/doc/informacie_o/Prehlad_projektov_riesenych_v_r._2015.pdf'
    profile_expect={
      'lukas/index.html':('Mladý výskumník / SFRT – projekt č. 1341','Zodpovedný riešiteľ:'),
      'en/lukas/index.html':('Young Researcher / SFRT – project No. 1341','Responsible researcher:'),
      'de/lukas/index.html':('Mladý výskumník / SFRT – Projekt Nr. 1341','Projektverantwortlicher:'),
    }
    for rel,(title,role) in profile_expect.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        if title not in txt or role not in txt or source not in txt:
            issues.append(f'{rel}: visible SFRT 1341 fact/source block missing')
        if '<time datetime="2015">2015</time>' not in txt:
            issues.append(f'{rel}: SFRT year lacks machine-readable time')

    # Current/historical chronology must expose machine-readable dates on person profiles.
    chronology={
      'lukas/index.html':('datetime="2026-05"','datetime="2017-09"','datetime="2026-04"'),
      'en/lukas/index.html':('datetime="2026-05"','datetime="2017-09"','datetime="2026-04"'),
      'de/lukas/index.html':('datetime="2026-05"','datetime="2017-09"','datetime="2026-04"'),
      'peter/index.html':('datetime="2020-06"','datetime="2018-11"','datetime="2016-07"'),
      'en/peter/index.html':('datetime="2020-06"','datetime="2018-11"','datetime="2016-07"'),
      'de/peter/index.html':('datetime="2020-06"','datetime="2018-11"','datetime="2016-07"'),
    }
    for rel,tokens in chronology.items():
        txt=(ROOT/rel).read_text(encoding='utf-8')
        for token in tokens:
            if token not in txt: issues.append(f'{rel}: chronology token missing {token}')

    benchmark=(ROOT/'docs/AI-IDENTITY-BENCHMARK-v0.2.5.md').read_text(encoding='utf-8')
    for token in ('Factual precision guardrails','responsible researcher','Bezpečná elektrika: an independent professional project'):
        if token not in benchmark: issues.append('AI benchmark precision guardrail missing '+token)

    if issues:
        for x in issues: fail('v0.2.5 final identity precision: '+x)
    else: ok('v0.2.5 final ORCID/SFRT chronology and factual-precision guardrails')

def check_release_hygiene():
    bad=[]
    for p in ROOT.rglob('*'):
        if p.is_dir() and p.name=='__pycache__': bad.append(str(p.relative_to(ROOT)))
        elif p.is_file() and (p.suffix in ('.pyc','.tmp')): bad.append(str(p.relative_to(ROOT)))
    if bad: fail('release hygiene artifacts: '+', '.join(bad))
    else: ok('release tree has no .tmp/.pyc/__pycache__ artifacts')


def check_js():
    try:
        cp=subprocess.run(['node','--check',str(ROOT/'assets/js/main.js')],capture_output=True,text=True)
        if cp.returncode: fail('main.js syntax: '+cp.stderr.strip())
        else: ok('main.js syntax')
    except FileNotFoundError: warn('node not installed; JS syntax check skipped')


def main() -> int:
    docs=parse_docs()
    check_links(docs)
    check_accessibility_semantics(docs)
    check_jsonld(docs)
    check_hreflang(docs)
    check_visible_language_routes()
    check_contrast()
    check_identity_contacts()
    check_vcard_bytes()
    check_language_markers()
    check_navigation_hierarchy()
    check_homepage_quick_contacts()
    check_mobile_docks()
    check_peter_dock_identity()
    check_mobile_nav_accessible_labels()
    check_custom_404()
    check_e2a_status()
    check_consent_hardening()
    check_rc9_human_cut()
    check_rc10_mobile_ux()
    check_v022_entity_authority()
    check_cross_page_person_consistency()
    check_profile_datetime()
    check_home_graph_and_localized_haspart()
    check_feed_consistency()
    check_v023_content_cta()
    check_v023_rc2_scrollspy()
    check_v023_rc2_chronology()
    check_v023_rc5_credential_fit_preview()
    check_v024_credential_in_viewer_size_toggle()
    check_v024_credential_dialog_cold_start()
    check_v023_rc2_credential_schema()
    check_v023_rc3_desktop_profile_nav()
    check_v023_rc4_compact_desktop_and_education()
    check_v024_integrated_sources()
    check_v024_final_polish()
    check_v024_contact_scrollspy_bottom()
    check_v024_profile_nav_anchor_alignment()
    check_v024_mobile_nav_alignment()
    check_v024_home_portrait_links()
    check_v024_back_to_top()
    check_v024_deploy_readiness()
    check_v025_preview_identity_reinforcement()
    check_v025_preview_r3_polish()
    check_v025_final_identity_precision()
    check_release_hygiene()
    check_hero_loading()
    check_js()
    print(f'PASS {len(PASSES)}')
    for x in PASSES: print('  ✓',x)
    if WARNS:
        print(f'WARN {len(WARNS)}')
        for x in WARNS: print('  !',x)
    print(f'FAIL {len(FAILS)}')
    for x in FAILS: print('  ✗',x)
    return 1 if FAILS else 0

if __name__ == '__main__':
    raise SystemExit(main())
