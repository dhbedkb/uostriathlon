(function () {
  const root = document.documentElement;
  const header = document.querySelector("[data-header]");
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navPanel = document.querySelector("[data-nav-panel]");
  const themeToggle = document.querySelector("[data-theme-toggle]");
  const themeIcon = document.querySelector("[data-theme-icon]");

  root.classList.add("js-enabled");

  function setHeaderState() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 12);
  }

  function closeNavigation() {
    if (!navToggle || !navPanel) return;
    navToggle.setAttribute("aria-expanded", "false");
    navPanel.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }

  function toggleNavigation() {
    if (!navToggle || !navPanel) return;
    const expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    navPanel.classList.toggle("is-open", !expanded);
    document.body.classList.toggle("nav-open", !expanded);
  }

  function getPreferredTheme() {
    const stored = localStorage.getItem("theme");
    if (stored === "dark" || stored === "light") return stored;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    if (themeIcon) themeIcon.textContent = theme === "dark" ? "☾" : "☀";
  }

  if (navToggle) navToggle.addEventListener("click", toggleNavigation);
  if (themeToggle) themeToggle.addEventListener("click", function () {
    applyTheme((root.getAttribute("data-theme") || "dark") === "dark" ? "light" : "dark");
  });

  if (navPanel) {
    navPanel.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeNavigation();
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeNavigation();
  });

  window.addEventListener("scroll", setHeaderState, { passive: true });

  if (themeToggle) applyTheme(getPreferredTheme());
  setHeaderState();
})();
