---
layout: page
title: In the news
kicker: SDRP in the news
intro: Press coverage of the District’s Structural Deficit Reduction Plan and the school closures.
description: Press coverage of District 65’s Structural Deficit Reduction Plan and school closures.
no_index: true
---
{%- comment -%} To add an article, edit _data/news.yml. {%- endcomment -%}
<ul class="news-list">
{% for n in site.data.news %}
  <li><a href="{{ n.url }}" target="_blank" rel="noopener">{{ n.title }}</a><small>{{ n.outlet }} · {{ n.date | date: "%B %-d, %Y" }}</small>{% if n.also %}<small>Also: <a href="{{ n.also.url }}" target="_blank" rel="noopener">{{ n.also.title }}</a></small>{% endif %}</li>
{% endfor %}
</ul>
