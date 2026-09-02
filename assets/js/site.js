/* SciRecast page framework: theme switch, reading progress, section rail,
   scroll spy, and two small markdown touch-ups. No dependencies. */
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
    window.dispatchEvent(new Event("scirecast-theme"));
  }
  doc.querySelectorAll(".theme-switch button").forEach(function (b) {
    b.addEventListener("click", function () { setTheme(b.dataset.theme, true); });
  });
  setTheme(currentTheme(), false);

  /* ---------- markdown touch-ups ---------- */
  var prose = doc.querySelector(".prose");
  if (prose) {
    // Every table scrolls inside its own box rather than pushing the page sideways.
    prose.querySelectorAll(":scope > table").forEach(function (t) {
      var wrap = doc.createElement("div");
      wrap.className = "table-wrap";
      t.parentNode.insertBefore(wrap, t);
      wrap.appendChild(t);
    });
    // A "| | |" header row renders as an empty <thead>; drop it.
    prose.querySelectorAll("thead").forEach(function (thead) {
      if (!thead.textContent.trim()) thead.classList.add("empty");
    });
    // Number the h2 sections the way the rail does.
    var pageNo = prose.dataset.pageNo || "";
    var h2s = prose.querySelectorAll("h2");
    h2s.forEach(function (h, i) {
      if (!h.id) h.id = "section-" + (i + 1);
      h.dataset.title = h.textContent.trim();
      var no = doc.createElement("span");
      no.className = "sec-no";
      no.textContent = pageNo + "." + (i + 1);
      h.insertBefore(no, h.firstChild);
    });
    // A blockquote whose first line is "Key idea:", "Honest note:" or
    // "Warning:" becomes a tagged callout.
    prose.querySelectorAll("blockquote").forEach(function (q) {
      var first = q.querySelector("p");
      if (!first) return;
      var m = /^(Key idea|Honest note|Warning|Note)\s*[:：]\s*/i.exec(first.textContent);
      if (!m) return;
      var kind = { "key idea": "note-key", "note": "note-key", "honest note": "note-honest", "warning": "note-warn" }[m[1].toLowerCase()];
      var tag = doc.createElement("span");
      tag.className = "note-tag";
      tag.textContent = m[1];
      first.innerHTML = first.innerHTML.replace(/^[\s\S]*?[:：]\s*/, "");
      q.className = "note " + kind;
      q.insertBefore(tag, q.firstChild);
    });
  }

  /* ---------- section links in the rail ---------- */
  var slot = doc.querySelector(".rail [data-sections]");
  var sectionLinks = [];
  if (slot && prose) {
    prose.querySelectorAll("h2").forEach(function (h) {
      var a = doc.createElement("a");
      a.className = "sub";
      a.href = "#" + h.id;
      a.textContent = h.dataset.title || h.textContent;
      slot.appendChild(a);
      sectionLinks.push([a, h]);
    });
  }

  /* ---------- scroll spy + progress ---------- */
  var bar = doc.querySelector(".progress-bar");
  function onScroll() {
    if (bar) {
      var p = root.scrollTop / Math.max(1, root.scrollHeight - root.clientHeight);
      bar.style.width = (p * 100).toFixed(2) + "%";
    }
    if (sectionLinks.length) {
      var active = -1;
      for (var i = 0; i < sectionLinks.length; i++) {
        if (sectionLinks[i][1].getBoundingClientRect().top <= 96) active = i;
      }
      sectionLinks.forEach(function (pair, i) { pair[0].classList.toggle("active", i === active); });
    }
  }
  doc.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
})();
