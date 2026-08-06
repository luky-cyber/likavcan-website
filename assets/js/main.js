document.addEventListener("DOMContentLoaded", () => {
  const storageKey = "likavcan_cookie_consent";
  const measurementId = "G-0F00N4385D";
  const lang = (document.documentElement.lang || "sk").toLowerCase();
  let analyticsLoaded = false;

  const translations = {
    sk: {
      title: "Cookies",
      text: "Táto stránka používa nevyhnutné technológie pre základné fungovanie a voliteľné analytické cookies služby Google Analytics na meranie návštevnosti. Analytika sa aktivuje iba po vašom súhlase.",
      acceptAll: "Prijať všetko",
      essentialOnly: "Len nevyhnutné",
      closeLabel: "Zavrieť oznámenie o cookies",
      settings: "Nastavenia cookies"
    },
    en: {
      title: "Cookies",
      text: "This website uses essential technologies for core functionality and optional Google Analytics cookies to measure traffic. Analytics is activated only after your consent.",
      acceptAll: "Accept all",
      essentialOnly: "Essential only",
      closeLabel: "Close cookie notice",
      settings: "Cookie settings"
    },
    de: {
      title: "Cookies",
      text: "Diese Website verwendet notwendige Technologien für die Grundfunktionalität und optionale Google-Analytics-Cookies zur Reichweitenmessung. Analytics wird nur nach Ihrer Einwilligung aktiviert.",
      acceptAll: "Alle akzeptieren",
      essentialOnly: "Nur notwendige",
      closeLabel: "Cookie-Hinweis schließen",
      settings: "Cookie-Einstellungen"
    }
  };

  const t = translations[lang] || translations.sk;

  const loadAnalytics = () => {
    if (analyticsLoaded || document.querySelector(`script[data-ga4-id="${measurementId}"]`)) {
      return;
    }

    analyticsLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function gtag() {
      window.dataLayer.push(arguments);
    };

    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`;
    script.dataset.ga4Id = measurementId;
    document.head.appendChild(script);
  };

  const createSettingsButton = () => {
    if (document.querySelector(".cookie-settings-button")) return;

    const button = document.createElement("button");
    button.className = "cookie-settings-button";
    button.type = "button";
    button.textContent = t.settings;
    button.setAttribute("aria-label", t.settings);
    button.addEventListener("click", () => showBanner(true));
    document.body.appendChild(button);
  };

  const removeBanner = () => {
    const banner = document.querySelector(".cookie-banner");
    if (!banner) return;
    banner.classList.remove("is-visible");
    setTimeout(() => banner.remove(), 200);
  };

  const saveConsent = (value) => {
    localStorage.setItem(storageKey, value);
    if (value === "all") loadAnalytics();
    removeBanner();
    createSettingsButton();
  };

  function showBanner(immediate = false) {
    if (document.querySelector(".cookie-banner")) return;

    const banner = document.createElement("aside");
    banner.className = "cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-live", "polite");
    banner.setAttribute("aria-modal", "false");
    banner.setAttribute("aria-label", t.title);
    banner.innerHTML = `
      <div class="cookie-banner__top">
        <div>
          <h2 class="cookie-banner__title">${t.title}</h2>
          <p class="cookie-banner__text">${t.text}</p>
        </div>
        <button class="cookie-banner__close" type="button" aria-label="${t.closeLabel}">×</button>
      </div>
      <div class="cookie-banner__actions">
        <button class="button button--primary" type="button" data-consent="all">${t.acceptAll}</button>
        <button class="button button--ghost" type="button" data-consent="essential">${t.essentialOnly}</button>
      </div>
    `;

    document.body.appendChild(banner);

    requestAnimationFrame(() => {
      setTimeout(() => banner.classList.add("is-visible"), immediate ? 0 : 900);
    });

    banner.querySelector('[data-consent="all"]').addEventListener("click", () => saveConsent("all"));
    banner.querySelector('[data-consent="essential"]').addEventListener("click", () => saveConsent("essential"));
    banner.querySelector(".cookie-banner__close").addEventListener("click", () => saveConsent("essential"));
  }

  const savedConsent = localStorage.getItem(storageKey);

  if (savedConsent === "all") {
    loadAnalytics();
    createSettingsButton();
  } else if (savedConsent === "essential") {
    createSettingsButton();
  } else {
    showBanner();
  }
});
