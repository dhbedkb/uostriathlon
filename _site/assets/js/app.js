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

    if (window.scrollY > 12) {
      header.classList.add("is-scrolled");
    } else {
      header.classList.remove("is-scrolled");
    }
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
    const storedTheme = window.localStorage.getItem("theme");

    if (storedTheme === "dark" || storedTheme === "light") {
      return storedTheme;
    }

    const systemPrefersLight = window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: light)").matches;

    return systemPrefersLight ? "light" : "dark";
  }

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    window.localStorage.setItem("theme", theme);

    if (themeIcon) {
      themeIcon.textContent = theme === "dark" ? "☾" : "☀";
    }
  }

  function toggleTheme() {
    const currentTheme = root.getAttribute("data-theme") || "dark";
    const nextTheme = currentTheme === "dark" ? "light" : "dark";

    applyTheme(nextTheme);
  }

  if (navToggle) {
    navToggle.addEventListener("click", toggleNavigation);
  }

  if (navPanel) {
    navPanel.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        closeNavigation();
      }
    });
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
    applyTheme(getPreferredTheme());
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeNavigation();
    }
  });

  window.addEventListener("scroll", setHeaderState, { passive: true });

  setHeaderState();
})();
