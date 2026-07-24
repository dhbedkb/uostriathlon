(function () {
  var root = document.documentElement;
  var header = document.querySelector("[data-header]");
  var navToggle = document.querySelector("[data-nav-toggle]");
  var navPanel = document.querySelector("[data-nav-panel]");
  var themeToggle = document.querySelector("[data-theme-toggle]");
  var themeIcon = document.querySelector("[data-theme-icon]");

  root.classList.add("js-enabled");

  function closeNavigation() {
    if (!navToggle || !navPanel) return;
    navToggle.setAttribute("aria-expanded", "false");
    navPanel.classList.remove("is-open");
    document.body.classList.remove("nav-open");
  }

  function toggleNavigation() {
    if (!navToggle || !navPanel) return;
    var expanded = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!expanded));
    navPanel.classList.toggle("is-open", !expanded);
    document.body.classList.toggle("nav-open", !expanded);
  }

  function getPreferredTheme() {
    var stored = localStorage.getItem("theme");
    if (stored === "dark" || stored === "light") return stored;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    if (themeIcon) themeIcon.textContent = theme === "dark" ? "☾" : "☀";
  }

  if (navToggle) navToggle.addEventListener("click", toggleNavigation);
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      applyTheme((root.getAttribute("data-theme") || "dark") === "dark" ? "light" : "dark");
    });
    applyTheme(getPreferredTheme());
  }

  if (navPanel) {
    navPanel.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeNavigation();
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") closeNavigation();
  });

  window.addEventListener("scroll", function () {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 12);
  }, { passive: true });

  function canHover() {
    return window.matchMedia && window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  }

  document.querySelectorAll('[data-reveal-mode="hover"]').forEach(function (card) {
    if (!canHover()) return;
    card.addEventListener("mouseenter", function () { card.open = true; });
    card.addEventListener("mouseleave", function () { card.open = false; });
  });
})();
