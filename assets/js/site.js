/* Small progressive enhancements. Every page works without this file. */
(function () {
  "use strict";

  // Hide dated items ("Coming up", the red "upcoming" timeline entry) once their date has passed,
  // even if nobody has rebuilt the site since.
  var today = new Date();
  var todayKey = today.getFullYear() * 10000 + (today.getMonth() + 1) * 100 + today.getDate();
  document.querySelectorAll("[data-until]").forEach(function (el) {
    var k = parseInt(el.getAttribute("data-until").replace(/-/g, ""), 10);
    if (k && k < todayKey) {
      if (el.classList.contains("up")) el.classList.remove("up");
      else el.hidden = true;
    }
  });

  // Copy link button in the article byline.
  document.querySelectorAll(".copy-link").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = b.getAttribute("data-url") || location.href;
      var done = function () { var t = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = t; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, function () { prompt("Copy this link:", url); });
      else prompt("Copy this link:", url);
    });
  });

  // "In this story": built from the article's ## headings when there are at least three.
  var toc = document.querySelector(".instory");
  if (toc) {
    var hs = Array.prototype.filter.call(document.querySelectorAll(".prose > h2"), function (h) { return h.id; });
    if (hs.length >= 3) {
      var ol = toc.querySelector("ol");
      hs.forEach(function (h) {
        var li = document.createElement("li"), a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent.replace(/\s+/g, " ").trim();
        li.appendChild(a);
        ol.appendChild(li);
      });
      toc.hidden = false;
    }
  }

  // Charts: if a chart (same-site iframe) is taller than its frame at this screen width, grow the
  // frame to fit instead of making readers scroll inside it. Never shrinks below the page's height.
  var frames = Array.prototype.slice.call(document.querySelectorAll(".prose iframe"));
  var fit = function (f) {
    try {
      var d = f.contentDocument;
      if (!d || !d.documentElement) return;
      var h = Math.max(d.documentElement.scrollHeight, d.body ? d.body.scrollHeight : 0);
      var base = parseInt(f.getAttribute("height"), 10) || 0;
      if (h > Math.max(base, f.clientHeight) + 2) f.style.height = h + 2 + "px";
    } catch (e) { /* other-site iframe: leave it */ }
  };
  frames.forEach(function (f) {
    var run = function () { fit(f); setTimeout(function () { fit(f); }, 700); setTimeout(function () { fit(f); }, 2000); };
    f.addEventListener("load", run);
    if (f.contentDocument && f.contentDocument.readyState === "complete") run();
  });
  var rt;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () { frames.forEach(function (f) { f.style.height = ""; }); setTimeout(function () { frames.forEach(fit); }, 400); }, 250);
  });

  // All stories: section tabs, kind chips and a word filter.
  var filters = document.querySelector(".filters");
  if (filters) {
    var items = Array.prototype.slice.call(document.querySelectorAll(".arch-item"));
    var months = Array.prototype.slice.call(document.querySelectorAll(".month-group"));
    var count = document.querySelector(".lib-count");
    var empty = document.querySelector(".empty");
    var input = filters.querySelector("input");
    var params = new URLSearchParams(location.search);
    var state = { topic: params.get("topic") || "all", group: params.get("group") || "all", q: params.get("q") || "" };

    var press = function () {
      filters.querySelectorAll("[data-f]").forEach(function (b) {
        b.setAttribute("aria-pressed", String(state[b.getAttribute("data-f")] === b.getAttribute("data-v")));
      });
    };
    var apply = function () {
      var q = state.q.trim().toLowerCase(), n = 0;
      items.forEach(function (it) {
        var s = it.querySelector(".story");
        var ok = (state.topic === "all" || s.getAttribute("data-topic") === state.topic) &&
                 (state.group === "all" || s.getAttribute("data-group") === state.group) &&
                 (!q || it.getAttribute("data-text").indexOf(q) !== -1);
        it.hidden = !ok;
        if (ok) n++;
      });
      months.forEach(function (m) { m.hidden = !m.querySelector(".arch-item:not([hidden])"); });
      count.textContent = n === items.length ? n + " stories" : n + " of " + items.length + " stories";
      empty.hidden = n !== 0;
      var p = new URLSearchParams();
      if (state.topic !== "all") p.set("topic", state.topic);
      if (state.group !== "all") p.set("group", state.group);
      if (state.q) p.set("q", state.q);
      var qs = p.toString();
      history.replaceState(null, "", location.pathname + (qs ? "?" + qs : ""));
    };

    filters.hidden = false;
    input.value = state.q;
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("[data-f]");
      if (!b) return;
      state[b.getAttribute("data-f")] = b.getAttribute("data-v");
      press(); apply();
    });
    input.addEventListener("input", function () { state.q = input.value; apply(); });
    document.querySelectorAll(".reset").forEach(function (r) {
      r.addEventListener("click", function () { state = { topic: "all", group: "all", q: "" }; input.value = ""; press(); apply(); });
    });
    press(); apply();
  }
})();
