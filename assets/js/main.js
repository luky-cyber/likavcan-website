document.addEventListener("DOMContentLoaded", () => {
  // v0.2.1 RC7 — custom 404 keeps language context for deep missing routes.
  if (document.body.dataset.page === "404") {
    const path = window.location.pathname.toLowerCase();
    const pageLang = path === "/en" || path.startsWith("/en/") ? "en" : path === "/de" || path.startsWith("/de/") ? "de" : "sk";
    const copy = {
      sk: {skip:"Preskočiť na hlavný obsah",home:"Domov",title:"Stránka sa nenašla",lead:"Požadovaná adresa neexistuje alebo bola presunutá.",tagline:"Merať. Dokumentovať. Vysvetľovať.",methodology:"Metodika a zdroje",privacy:"Ochrana súkromia",cookies:"Nastavenia cookies",mainNav:"Hlavná navigácia",language:"Jazyk"},
      en: {skip:"Skip to main content",home:"Home",title:"Page not found",lead:"The requested address does not exist or has been moved.",tagline:"Measure. Document. Explain.",methodology:"Methodology & sources",privacy:"Privacy",cookies:"Cookie settings",mainNav:"Main navigation",language:"Language"},
      de: {skip:"Zum Hauptinhalt springen",home:"Startseite",title:"Seite nicht gefunden",lead:"Die angeforderte Adresse existiert nicht oder wurde verschoben.",tagline:"Messen. Dokumentieren. Erklären.",methodology:"Methodik & Quellen",privacy:"Datenschutz",cookies:"Cookie-Einstellungen",mainNav:"Hauptnavigation",language:"Sprache"}
    };
    const t404 = copy[pageLang];
    document.documentElement.lang = pageLang;
    document.title = `404 | Likavcan.cz`;
    document.querySelectorAll("[data-404-text]").forEach((el) => { const key = el.dataset["404Text"]; if (t404[key]) el.textContent = t404[key]; });
    document.querySelectorAll("[data-404-label]").forEach((el) => { const key = el.dataset["404Label"]; if (t404[key]) el.setAttribute("aria-label", t404[key]); });
    const prefix = pageLang === "sk" ? "" : `/${pageLang}`;
    const nav = document.querySelector(".site-nav");
    const navLinks = nav ? nav.querySelectorAll("a") : [];
    if (navLinks.length === 3) { navLinks[0].href = `${prefix || ""}/`; navLinks[1].href = `${prefix}/lukas/`; navLinks[2].href = `${prefix}/peter/`; }
    const primaryButtons = document.querySelectorAll("main .button-group a");
    if (primaryButtons.length === 3) { primaryButtons[0].href = `${prefix || ""}/`; primaryButtons[1].href = `${prefix}/lukas/`; primaryButtons[2].href = `${prefix}/peter/`; }
    const methodology = document.querySelector('[data-404-role="methodology"]');
    const privacy = document.querySelector('[data-404-role="privacy"]');
    if (methodology) { methodology.href = `${prefix}/methodology/`; methodology.textContent = t404.methodology; }
    if (privacy) { privacy.href = `${prefix}/privacy/`; privacy.textContent = t404.privacy; }
    document.querySelectorAll(".language-nav a").forEach((link) => {
      if (link.getAttribute("hreflang") === pageLang) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
  }
  const updateScrollOffset = () => {
    const header = document.querySelector(".site-header");
    const profileNav = document.querySelector(".profile-nav[data-profile-nav]");
    const headerPosition = header ? window.getComputedStyle(header).position : "static";
    const headerHeight = header && (headerPosition === "sticky" || headerPosition === "fixed")
      ? Math.ceil(header.getBoundingClientRect().height) : 0;
    document.documentElement.style.setProperty("--site-header-height", `${headerHeight}px`);

    let profileNavHeight = 0;
    if (profileNav && window.getComputedStyle(profileNav).display !== "none") {
      const profilePosition = window.getComputedStyle(profileNav).position;
      if (profilePosition === "sticky" || profilePosition === "fixed") {
        profileNavHeight = Math.ceil(profileNav.getBoundingClientRect().height);
      }
    }
    document.documentElement.style.setProperty("--scroll-offset", `${headerHeight + profileNavHeight + 16}px`);
  };
  updateScrollOffset();
  window.addEventListener("resize", updateScrollOffset, {passive:true});

  // v0.2.3 RC3 — one section model drives both the desktop profile strip and mobile dock.
  const desktopProfileNav = document.querySelector(".profile-nav[data-profile-nav]");
  const mobileDock = document.querySelector(".mobile-profile-dock");
  const profileNavSurfaces = [desktopProfileNav, mobileDock].filter(Boolean);
  if (profileNavSurfaces.length) {
    if (mobileDock) document.body.classList.add("has-mobile-dock");

    const navLinks = profileNavSurfaces.flatMap((nav) => Array.from(nav.querySelectorAll("a[data-dock-key]")));
    const setProfileNavActive = (key) => {
      navLinks.forEach((link) => {
        const active = link.dataset.dockKey === key;
        link.classList.toggle("is-active", active);
        if (active) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
    };

    const defaultKey = (desktopProfileNav?.dataset.dockDefault || mobileDock?.dataset.dockDefault || "profile");
    const trackedSections = Array.from(document.querySelectorAll("section[data-dock-section]"));
    let profileNavFrame = 0;
    const updateProfileNavFromScroll = () => {
      profileNavFrame = 0;
      if (!trackedSections.length) {
        setProfileNavActive(defaultKey);
        return;
      }
      const header = document.querySelector(".site-header");
      const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
      const desktopHeight = desktopProfileNav && window.getComputedStyle(desktopProfileNav).display !== "none"
        ? desktopProfileNav.getBoundingClientRect().height : 0;
      const trigger = Math.max(headerBottom + desktopHeight + 24, Math.min(window.innerHeight * 0.32, 220));
      let activeKey = defaultKey;
      const root = document.documentElement;
      const maxScroll = Math.max(0, root.scrollHeight - window.innerHeight);
      const atDocumentEnd = maxScroll > 0 && window.scrollY >= maxScroll - 8;
      if (atDocumentEnd) {
        const lastSection = trackedSections[trackedSections.length - 1];
        activeKey = lastSection?.dataset.dockSection || activeKey;
      } else {
        for (const section of trackedSections) {
          if (section.getBoundingClientRect().top <= trigger) {
            activeKey = section.dataset.dockSection || activeKey;
          } else {
            break;
          }
        }
      }
      setProfileNavActive(activeKey);
    };
    const scheduleProfileNavUpdate = () => {
      if (profileNavFrame) return;
      profileNavFrame = window.requestAnimationFrame(updateProfileNavFromScroll);
    };
    window.addEventListener("scroll", scheduleProfileNavUpdate, {passive:true});
    window.addEventListener("resize", () => { updateScrollOffset(); scheduleProfileNavUpdate(); }, {passive:true});
    window.addEventListener("hashchange", scheduleProfileNavUpdate);
    updateProfileNavFromScroll();
  }
  // v0.2.4 — compact global back-to-top control for long pages.
  const backToTopCopy = {sk:"Späť hore", en:"Back to top", de:"Nach oben"};
  const backToTopLang = (document.documentElement.lang || "sk").toLowerCase();
  const backToTop = document.createElement("button");
  backToTop.className = "back-to-top";
  backToTop.type = "button";
  backToTop.textContent = "↑";
  backToTop.setAttribute("aria-label", backToTopCopy[backToTopLang] || backToTopCopy.sk);
  backToTop.setAttribute("title", backToTopCopy[backToTopLang] || backToTopCopy.sk);
  backToTop.tabIndex = -1;
  document.body.appendChild(backToTop);

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let backToTopFrame = 0;
  const updateBackToTopVisibility = () => {
    backToTopFrame = 0;
    const root = document.documentElement;
    const scrollRange = Math.max(0, root.scrollHeight - window.innerHeight);
    const longPage = scrollRange > 640;
    const scrolledEnough = window.scrollY > Math.min(640, window.innerHeight * 0.75);
    const cookieDialogOpen = Boolean(document.querySelector(".cookie-banner.is-visible"));
    const credentialViewerOpen = document.body.classList.contains("is-credential-viewer-open");
    const visible = longPage && scrolledEnough && !cookieDialogOpen && !credentialViewerOpen;
    backToTop.classList.toggle("is-visible", visible);
    backToTop.tabIndex = visible ? 0 : -1;
    backToTop.setAttribute("aria-hidden", visible ? "false" : "true");
  };
  const scheduleBackToTopUpdate = () => {
    if (backToTopFrame) return;
    backToTopFrame = window.requestAnimationFrame(updateBackToTopVisibility);
  };
  window.addEventListener("scroll", scheduleBackToTopUpdate, {passive:true});
  window.addEventListener("resize", scheduleBackToTopUpdate, {passive:true});
  backToTop.addEventListener("click", () => {
    const behavior = prefersReducedMotion.matches ? "auto" : "smooth";
    window.scrollTo({top:0, behavior});
    const focusTarget = document.querySelector(".site-logo");
    window.setTimeout(() => focusTarget?.focus({preventScroll:true}), behavior === "smooth" ? 450 : 0);
  });
  updateBackToTopVisibility();

  // v0.2.4 final — shared credential viewer model: native <dialog>, deferred cold-start load, fit <-> 100%.
  const credentialViewerLinks = Array.from(document.querySelectorAll("a[data-credential-viewer]"));
  if (credentialViewerLinks.length && typeof HTMLDialogElement !== "undefined") {
    const viewerCopy = {
      sk: {
        title: "Verejná redigovaná kópia osvedčenia",
        close: "Zavrieť zobrazenie osvedčenia",
        fitStatus: "Prispôsobené displeju",
        nativeStatus: "100 % · natívna veľkosť",
        nativeAction: "100 %",
        fitAction: "Prispôsobiť",
        nativeActionLabel: "Zobraziť osvedčenie v 100 % natívnej veľkosti",
        fitActionLabel: "Prispôsobiť osvedčenie displeju",
        hint: "Tlačidlo 100 % alebo kliknutie na dokument zobrazí dokument v natívnej veľkosti.",
        alt: "Verejná redigovaná kópia osvedčenia revízneho technika E2/A"
      },
      en: {
        title: "Public redacted copy of certificate",
        close: "Close certificate viewer",
        fitStatus: "Fit to screen",
        nativeStatus: "100% · native size",
        nativeAction: "100%",
        fitAction: "Fit",
        nativeActionLabel: "Show certificate at native 100% size",
        fitActionLabel: "Fit certificate to screen",
        hint: "The 100% button or clicking the document shows it at its native size.",
        alt: "Public redacted copy of the E2/A electrical inspection technician certificate"
      },
      de: {
        title: "Öffentliche redigierte Kopie der Bescheinigung",
        close: "Ansicht der Bescheinigung schließen",
        fitStatus: "An Display angepasst",
        nativeStatus: "100 % · Originalgröße",
        nativeAction: "100 %",
        fitAction: "Anpassen",
        nativeActionLabel: "Bescheinigung in nativer Größe von 100 % anzeigen",
        fitActionLabel: "Bescheinigung an das Display anpassen",
        hint: "Die Schaltfläche 100 % oder ein Klick auf das Dokument zeigt es in seiner Originalgröße.",
        alt: "Öffentliche redigierte Kopie der E2/A-Bescheinigung für elektrische Prüf- und Revisionstätigkeiten"
      }
    };
    const viewerLang = (document.documentElement.lang || "sk").toLowerCase();
    const viewerText = viewerCopy[viewerLang] || viewerCopy.sk;
    const dialog = document.createElement("dialog");
    dialog.className = "credential-lightbox";
    dialog.setAttribute("aria-labelledby", "credential-lightbox-title");
    dialog.setAttribute("aria-describedby", "credential-lightbox-hint");

    const panel = document.createElement("div");
    panel.className = "credential-lightbox__panel";

    const toolbar = document.createElement("div");
    toolbar.className = "credential-lightbox__toolbar";
    const heading = document.createElement("div");
    heading.className = "credential-lightbox__heading";
    const title = document.createElement("p");
    title.className = "credential-lightbox__title";
    title.id = "credential-lightbox-title";
    title.textContent = viewerText.title;
    const status = document.createElement("p");
    status.className = "credential-lightbox__status";
    status.setAttribute("aria-live", "polite");
    heading.append(title, status);

    const actions = document.createElement("div");
    actions.className = "credential-lightbox__actions";
    const sizeButton = document.createElement("button");
    sizeButton.className = "credential-lightbox__size";
    sizeButton.type = "button";
    const closeButton = document.createElement("button");
    closeButton.className = "credential-lightbox__close";
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", viewerText.close);
    closeButton.textContent = "×";
    actions.append(sizeButton, closeButton);
    toolbar.append(heading, actions);

    const viewport = document.createElement("div");
    viewport.className = "credential-lightbox__viewport";
    const image = document.createElement("img");
    image.className = "credential-lightbox__image";
    image.width = 1097;
    image.height = 1536;
    image.alt = viewerText.alt;
    image.decoding = "async";
    viewport.appendChild(image);

    const hint = document.createElement("p");
    hint.className = "credential-lightbox__hint";
    hint.id = "credential-lightbox-hint";
    hint.textContent = viewerText.hint;
    panel.append(toolbar, viewport, hint);
    dialog.appendChild(panel);
    document.body.appendChild(dialog);

    let viewerReturnFocus = null;
    let nativeSize = false;
    let openSequence = 0;
    const setCredentialSize = (useNativeSize) => {
      nativeSize = useNativeSize;
      dialog.classList.toggle("is-native-size", nativeSize);
      status.textContent = nativeSize ? viewerText.nativeStatus : viewerText.fitStatus;
      sizeButton.textContent = nativeSize ? viewerText.fitAction : viewerText.nativeAction;
      sizeButton.setAttribute("aria-label", nativeSize ? viewerText.fitActionLabel : viewerText.nativeActionLabel);
      sizeButton.setAttribute("aria-pressed", nativeSize ? "true" : "false");
      if (!nativeSize) {
        viewport.scrollTop = 0;
        viewport.scrollLeft = 0;
      }
    };
    const cleanupClosedCredentialViewer = () => {
      document.body.classList.remove("is-credential-viewer-open");
      setCredentialSize(false);
      const focusTarget = viewerReturnFocus;
      viewerReturnFocus = null;
      if (focusTarget && typeof focusTarget.focus === "function") focusTarget.focus({preventScroll:true});
    };
    const closeCredentialViewer = () => {
      if (dialog.open) dialog.close();
    };
    const openCredentialViewer = (trigger) => {
      if (typeof dialog.showModal !== "function") return false;
      viewerReturnFocus = trigger;
      title.textContent = trigger.dataset.credentialTitle || viewerText.title;
      image.dataset.src = trigger.href;
      setCredentialSize(false);
      document.body.classList.add("is-credential-viewer-open");
      const sequence = ++openSequence;
      dialog.showModal();
      closeButton.focus();
      requestAnimationFrame(() => {
        if (!dialog.open || sequence !== openSequence) return;
        if (image.src !== image.dataset.src) image.src = image.dataset.src;
      });
      return true;
    };

    credentialViewerLinks.forEach((link) => link.addEventListener("click", (event) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      if (typeof dialog.showModal !== "function") return;
      event.preventDefault();
      openCredentialViewer(link);
    }));
    sizeButton.addEventListener("click", () => setCredentialSize(!nativeSize));
    image.addEventListener("click", () => setCredentialSize(!nativeSize));
    closeButton.addEventListener("click", closeCredentialViewer);
    dialog.addEventListener("close", cleanupClosedCredentialViewer);
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog) closeCredentialViewer();
    });
  }
  const storageKey = "likavcan_cookie_consent";
  const policyVersion = "2026-09-15-v0.2.2";
  const consentMaxAgeMs = 365 * 24 * 60 * 60 * 1000;
  const measurementId = "G-0F00N4385D";
  const disableKey = `ga-disable-${measurementId}`;
  const lang = (document.documentElement.lang || "sk").toLowerCase();
  let analyticsLoaded = false;
  let memoryConsent = null;

  // Consent Mode v2 default state is established locally before any Google script is loaded.
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };
  window.gtag("consent", "default", {
    analytics_storage:"denied",
    ad_storage:"denied",
    ad_user_data:"denied",
    ad_personalization:"denied",
    wait_for_update:500
  });

  const readConsent = () => {
    let raw = null;
    try { raw = window.localStorage.getItem(storageKey); }
    catch { return memoryConsent; }
    if (!raw) return memoryConsent;
    try {
      const record = JSON.parse(raw);
      const decidedAt = Date.parse(record?.decidedAt || "");
      const fresh = Number.isFinite(decidedAt) && Date.now() - decidedAt <= consentMaxAgeMs;
      if ((record?.choice === "all" || record?.choice === "essential") && record?.policyVersion === policyVersion && fresh) {
        memoryConsent = record.choice;
        return record.choice;
      }
    } catch {
      // Legacy string consent is intentionally re-prompted after this policy hardening.
    }
    return memoryConsent;
  };

  const writeConsent = (value) => {
    const record = { choice: value, decidedAt: new Date().toISOString(), policyVersion };
    memoryConsent = value;
    try { window.localStorage.setItem(storageKey, JSON.stringify(record)); return true; }
    catch { return false; }
  };

  const translations = {
    sk: {title:"Cookies",text:"Táto stránka používa nevyhnutné technológie a voliteľnú analytiku Google Analytics. Analytika sa aktivuje iba po súhlase.",acceptAll:"Prijať analytiku",essentialOnly:"Len nevyhnutné",closeLabel:"Použiť len nevyhnutné a zavrieť",settings:"Nastavenia cookies",privacy:"Ochrana súkromia"},
    en: {title:"Cookies",text:"This website uses essential technologies and optional Google Analytics. Analytics is activated only after consent.",acceptAll:"Accept analytics",essentialOnly:"Essential only",closeLabel:"Use essential only and close",settings:"Cookie settings",privacy:"Privacy"},
    de: {title:"Cookies",text:"Diese Website verwendet notwendige Technologien und optional Google Analytics. Analytics wird erst nach Einwilligung aktiviert.",acceptAll:"Analytics akzeptieren",essentialOnly:"Nur notwendige",closeLabel:"Nur notwendige verwenden und schließen",settings:"Cookie-Einstellungen",privacy:"Datenschutz"}
  };
  const t = translations[lang] || translations.sk;
  const privacyUrl = lang === "en" ? "/en/privacy/" : lang === "de" ? "/de/privacy/" : "/privacy/";

  const clearAnalyticsCookies = () => {
    document.cookie.split(";").map(v => v.split("=")[0].trim()).filter(n => n === "_ga" || n.startsWith("_ga_")).forEach(name => {
      const expires = "expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax";
      document.cookie = `${name}=; ${expires}`;
      document.cookie = `${name}=; ${expires}; domain=${location.hostname}`;
      if (location.hostname.endsWith("likavcan.cz")) document.cookie = `${name}=; ${expires}; domain=.likavcan.cz`;
    });
  };

  const disableAnalytics = () => {
    window[disableKey] = true;
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", {analytics_storage:"denied",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
    }
    clearAnalyticsCookies();
  };

  const sanitizeAnalyticsUrl = (rawUrl) => {
    if (!rawUrl) return "";
    try {
      const url = new URL(rawUrl, window.location.href);
      url.search = "";
      url.hash = "";
      return url.href;
    } catch { return ""; }
  };

  const loadAnalytics = () => {
    if (analyticsLoaded || document.querySelector(`script[data-ga4-id="${measurementId}"]`)) return;
    window[disableKey] = false;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };
    window.gtag("consent", "update", {analytics_storage:"granted",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
    window.gtag("js", new Date());
    const pageLocation = sanitizeAnalyticsUrl(window.location.href) || window.location.origin + window.location.pathname;
    const pageReferrer = sanitizeAnalyticsUrl(document.referrer);
    const config = {anonymize_ip:true,allow_google_signals:false,allow_ad_personalization_signals:false,page_location:pageLocation};
    if (pageReferrer) config.page_referrer = pageReferrer;
    window.gtag("config", measurementId, config);
    const script=document.createElement("script"); script.async=true; script.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`; script.dataset.ga4Id=measurementId; document.head.appendChild(script);
  };

  const removeBanner=()=>{ const b=document.querySelector(".cookie-banner"); if(!b)return; b.classList.remove("is-visible"); setTimeout(()=>{ b.remove(); updateBackToTopVisibility(); },200); };

  const saveConsent = (value) => {
    const previous=readConsent();
    writeConsent(value);
    if(value==="all") loadAnalytics();
    else disableAnalytics();
    removeBanner();
    if(previous==="all" && value==="essential") window.setTimeout(()=>window.location.reload(),120);
  };

  function showBanner(immediate=false){
    if(document.querySelector(".cookie-banner"))return;
    const banner=document.createElement("aside"); banner.className="cookie-banner"; banner.setAttribute("role","dialog"); banner.setAttribute("aria-live","polite"); banner.setAttribute("aria-modal","false"); banner.setAttribute("aria-label",t.title);
    banner.innerHTML=`<div class="cookie-banner__top"><div><h2 class="cookie-banner__title">${t.title}</h2><p class="cookie-banner__text">${t.text} <a href="${privacyUrl}">${t.privacy}</a>.</p></div><button class="cookie-banner__close" type="button" aria-label="${t.closeLabel}">×</button></div><div class="cookie-banner__actions"><button class="button button--secondary" type="button" data-consent="all">${t.acceptAll}</button><button class="button button--secondary" type="button" data-consent="essential">${t.essentialOnly}</button></div>`;
    document.body.appendChild(banner); backToTop.classList.remove("is-visible"); backToTop.tabIndex=-1; backToTop.setAttribute("aria-hidden","true"); requestAnimationFrame(()=>setTimeout(()=>banner.classList.add("is-visible"),immediate?0:900));
    banner.querySelector('[data-consent="all"]').addEventListener("click",()=>saveConsent("all")); banner.querySelector('[data-consent="essential"]').addEventListener("click",()=>saveConsent("essential")); banner.querySelector(".cookie-banner__close").addEventListener("click",()=>saveConsent("essential"));
  }

  document.querySelectorAll("[data-open-cookie-settings]").forEach(b=>b.addEventListener("click",()=>showBanner(true)));
  const saved=readConsent();
  if(saved==="all"){ loadAnalytics(); } else if(saved==="essential"){ disableAnalytics(); } else { disableAnalytics(); showBanner(); }


});
