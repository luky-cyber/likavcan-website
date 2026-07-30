
document.addEventListener("DOMContentLoaded", () => {
  const storageKey = "likavcan_cookie_consent";
  const lang = (document.documentElement.lang || "sk").toLowerCase();

  const translations = {
    sk: {
      title: "Cookies",
      text: "Táto stránka používa nevyhnutné cookies pre základné fungovanie a voliteľné cookies na zlepšenie používateľského zážitku. Zavretím okna povolíte len nevyhnutné cookies.",
      acceptAll: "Prijať všetko",
      essentialOnly: "Len nevyhnutné",
      closeLabel: "Zavrieť oznámenie o cookies"
    },
    en: {
      title: "Cookies",
      text: "This website uses essential cookies for core functionality and optional cookies to improve the user experience. Closing this banner will keep only essential cookies enabled.",
      acceptAll: "Accept all",
      essentialOnly: "Essential only",
      closeLabel: "Close cookie notice"
    },
    de: {
      title: "Cookies",
      text: "Diese Website verwendet notwendige Cookies für die Grundfunktionalität sowie optionale Cookies zur Verbesserung der Nutzererfahrung. Wenn Sie dieses Fenster schließen, bleiben nur notwendige Cookies aktiviert.",
      acceptAll: "Alle akzeptieren",
      essentialOnly: "Nur notwendige",
      closeLabel: "Cookie-Hinweis schließen"
    }
  };

  const t = translations[lang] || translations.sk;
  const saved = localStorage.getItem(storageKey);
  if (saved) return;

  const banner = document.createElement("aside");
  banner.className = "cookie-banner";
  banner.setAttribute("role", "dialog");
  banner.setAttribute("aria-live", "polite");
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
    setTimeout(() => banner.classList.add("is-visible"), 900);
  });

  const storeConsent = (value) => {
    localStorage.setItem(storageKey, value);
    banner.classList.remove("is-visible");
    setTimeout(() => banner.remove(), 200);
  };

  banner.querySelector('[data-consent="all"]').addEventListener('click', () => storeConsent('all'));
  banner.querySelector('[data-consent="essential"]').addEventListener('click', () => storeConsent('essential'));
  banner.querySelector('.cookie-banner__close').addEventListener('click', () => storeConsent('essential'));
});
