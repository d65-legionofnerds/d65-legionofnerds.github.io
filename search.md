---
layout: page
title: Search
permalink: /search/
kicker: Search
no_index: true
noindex: true
---
<div class="search-box" id="search"><noscript>Search needs JavaScript. You can also browse <a href="{{ '/archive/' | relative_url }}">all stories</a>.</noscript></div>
<p class="search-fallback" hidden>Search isn’t available in this copy of the site (it is built when the site is published). Browse <a href="{{ '/archive/' | relative_url }}">all stories</a> instead.</p>
<script src="{{ '/pagefind/pagefind-ui.js' | relative_url }}" onerror="document.querySelector('.search-fallback').hidden=false"></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {
    if (!window.PagefindUI) return;
    new PagefindUI({ element: "#search", showSubResults: true, showImages: false, resetStyles: false,
      translations: { placeholder: "Search our analyses, letters and memos" } });
    var q = new URLSearchParams(location.search).get("q");
    if (q) { var i = document.querySelector("#search input"); if (i) { i.value = q; i.dispatchEvent(new Event("input")); } }
  });
</script>
