document.addEventListener("DOMContentLoaded", () => {
  const updateScrollOffset = () => {
    const header = document.querySelector(".site-header");
    const height = header ? Math.ceil(header.getBoundingClientRect().height) : 64;
    document.documentElement.style.setProperty("--scroll-offset", `${height + 16}px`);
  };
  updateScrollOffset();
  window.addEventListener("resize", updateScrollOffset, {passive:true});
  const storageKey = "likavcan_cookie_consent";
  const measurementId = "G-0F00N4385D";
  const disableKey = `ga-disable-${measurementId}`;
  const lang = (document.documentElement.lang || "sk").toLowerCase();
  let analyticsLoaded = false;

  const readConsent = () => {
    try { return window.localStorage.getItem(storageKey); }
    catch { return null; }
  };

  const writeConsent = (value) => {
    try { window.localStorage.setItem(storageKey, value); return true; }
    catch { return false; }
  };

  const translations = {
    sk: {title:"Cookies",text:"Táto stránka používa nevyhnutné technológie a voliteľnú analytiku Google Analytics. Analytika sa aktivuje iba po súhlase.",acceptAll:"Prijať analytiku",essentialOnly:"Len nevyhnutné",closeLabel:"Zavrieť oznámenie o cookies",settings:"Nastavenia cookies",privacy:"Ochrana súkromia",copy:"Kopírovať odkaz na sekciu",copied:"Odkaz skopírovaný"},
    en: {title:"Cookies",text:"This website uses essential technologies and optional Google Analytics. Analytics is activated only after consent.",acceptAll:"Accept analytics",essentialOnly:"Essential only",closeLabel:"Close cookie notice",settings:"Cookie settings",privacy:"Privacy",copy:"Copy link to section",copied:"Link copied"},
    de: {title:"Cookies",text:"Diese Website verwendet notwendige Technologien und optional Google Analytics. Analytics wird erst nach Einwilligung aktiviert.",acceptAll:"Analytics akzeptieren",essentialOnly:"Nur notwendige",closeLabel:"Cookie-Hinweis schließen",settings:"Cookie-Einstellungen",privacy:"Datenschutz",copy:"Link zum Abschnitt kopieren",copied:"Link kopiert"}
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

  const loadAnalytics = () => {
    if (analyticsLoaded || document.querySelector(`script[data-ga4-id="${measurementId}"]`)) return;
    window[disableKey] = false;
    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };
    window.gtag("consent", "update", {analytics_storage:"granted",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});
    window.gtag("js", new Date());
    window.gtag("config", measurementId, {anonymize_ip:true,allow_google_signals:false,allow_ad_personalization_signals:false});
    const script=document.createElement("script"); script.async=true; script.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`; script.dataset.ga4Id=measurementId; document.head.appendChild(script);
  };

  const createSettingsButton = () => {
    if (document.querySelector(".cookie-settings-button")) return;
    const button=document.createElement("button"); button.className="cookie-settings-button"; button.type="button"; button.textContent=t.settings; button.setAttribute("aria-label",t.settings); button.addEventListener("click",()=>showBanner(true)); document.body.appendChild(button);
  };
  const removeBanner=()=>{ const b=document.querySelector(".cookie-banner"); if(!b)return; b.classList.remove("is-visible"); setTimeout(()=>b.remove(),200); };

  const saveConsent = (value) => {
    const previous=readConsent();
    writeConsent(value);
    if(value==="all") loadAnalytics();
    else disableAnalytics();
    removeBanner(); createSettingsButton();
    if(previous==="all" && value==="essential") window.setTimeout(()=>window.location.reload(),120);
  };

  function showBanner(immediate=false){
    if(document.querySelector(".cookie-banner"))return;
    const banner=document.createElement("aside"); banner.className="cookie-banner"; banner.setAttribute("role","dialog"); banner.setAttribute("aria-live","polite"); banner.setAttribute("aria-modal","false"); banner.setAttribute("aria-label",t.title);
    banner.innerHTML=`<div class="cookie-banner__top"><div><h2 class="cookie-banner__title">${t.title}</h2><p class="cookie-banner__text">${t.text} <a href="${privacyUrl}">${t.privacy}</a>.</p></div><button class="cookie-banner__close" type="button" aria-label="${t.closeLabel}">×</button></div><div class="cookie-banner__actions"><button class="button button--primary" type="button" data-consent="all">${t.acceptAll}</button><button class="button button--ghost" type="button" data-consent="essential">${t.essentialOnly}</button></div>`;
    document.body.appendChild(banner); requestAnimationFrame(()=>setTimeout(()=>banner.classList.add("is-visible"),immediate?0:900));
    banner.querySelector('[data-consent="all"]').addEventListener("click",()=>saveConsent("all")); banner.querySelector('[data-consent="essential"]').addEventListener("click",()=>saveConsent("essential")); banner.querySelector(".cookie-banner__close").addEventListener("click",()=>saveConsent("essential"));
  }

  document.querySelectorAll("[data-open-cookie-settings]").forEach(b=>b.addEventListener("click",()=>showBanner(true)));
  const saved=readConsent();
  if(saved==="all"){ loadAnalytics(); createSettingsButton(); } else if(saved==="essential"){ disableAnalytics(); createSettingsButton(); } else { disableAnalytics(); showBanner(); }

  // Add copyable permalinks to content sections that already have stable IDs.
  document.querySelectorAll("main section[id]").forEach(section => {
    const heading=section.querySelector("h2");
    if(!heading || heading.querySelector(".section-link-copy")) return;
    heading.classList.add("section-heading-with-link");
    const b=document.createElement("button"); b.className="section-link-copy"; b.type="button"; b.textContent="#"; b.title=t.copy; b.setAttribute("aria-label",t.copy);
    b.addEventListener("click", async () => {
      const url=`${location.origin}${location.pathname}#${section.id}`;
      try { await navigator.clipboard.writeText(url); b.dataset.copied="true"; b.setAttribute("aria-label",t.copied); window.setTimeout(()=>{delete b.dataset.copied;b.setAttribute("aria-label",t.copy);},1800); }
      catch { location.hash=section.id; }
    });
    heading.appendChild(b);
  });
});
