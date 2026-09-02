/* SciRecast page framework: theme switch, reading progress, scroll spy.
   No dependencies. */
(function () {
  "use strict";
  var doc = document;
  var root = doc.documentElement;

  /* ---------- theme (system / light / dark) ---------- */
  var THEME_KEY = "scirecast-theme";
  function currentTheme() {
    return root.dataset.theme === "light" || root.dataset.theme === "dark" ? root.dataset.theme : "system";
  }
  function setTheme(name, persist) {
    if (name === "system") delete root.dataset.theme; else root.dataset.theme = name;
    if (persist) {
      try { name === "system" ? localStorage.removeItem(THEME_KEY) : localStorage.setItem(THEME_KEY, name); } catch (e) {}
    }
    doc.querySelectorAll(".theme-switch button").forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.theme === name ? "true" : "false");
    });
  }
  doc.querySelectorAll(".theme-switch button").forEach(function (b) {
    b.addEventListener("click", function () { setTheme(b.dataset.theme, true); });
  });
  setTheme(currentTheme(), false);

  /* ---------- scroll spy + progress ---------- */
  var bar = doc.querySelector(".progress-bar");
  var railLinks = [].slice.call(doc.querySelectorAll('.rail a[href^="#"]'));
  var topLinks = [].slice.call(doc.querySelectorAll('.topnav a[href^="#"]'));
  function target(a) { return doc.getElementById(a.getAttribute("href").slice(1)); }
  var railTargets = railLinks.map(target);
  var chapters = [].slice.call(doc.querySelectorAll("section.chapter"));

  function onScroll() {
    if (bar) {
      var p = root.scrollTop / Math.max(1, root.scrollHeight - root.clientHeight);
      bar.style.width = (p * 100).toFixed(2) + "%";
    }
    // The rail highlights the last heading that has scrolled past the top bar.
    var active = -1;
    for (var i = 0; i < railTargets.length; i++) {
      if (railTargets[i] && railTargets[i].getBoundingClientRect().top <= 96) active = i;
    }
    railLinks.forEach(function (a, i) { a.classList.toggle("active", i === active); });
    // The top bar highlights the chapter.
    var current = null;
    chapters.forEach(function (c) { if (c.getBoundingClientRect().top <= 96) current = c.id; });
    topLinks.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + current); });
  }
  doc.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
})();
