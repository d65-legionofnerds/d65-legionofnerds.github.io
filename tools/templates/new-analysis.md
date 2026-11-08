---
# Copy this file to dataanalysis/<short-name>.md and fill it in. Rules: CLAUDE.md.
title: "Headline: what we looked at, or the question we answer"
date: 2026-01-31
topic: closures            # closures | buildings | budget | admin
type: analysis
summary: "One or two plain sentences: what we looked at and what we found."
image: /assets/img/lead/short-name.png            # python tools/chart_image.py <chart.html> <this path>
image_alt: "What the chart shows, with its key numbers."
image_source: dataanalysis/assets/short_name_main.html
takeaways:
  - "First finding, as a full sentence, with the same numbers as the page."
  - "Second finding."
---

Opening paragraph: the question, the data, and the answer in plain words.
**<mark>The one sentence that carries the main finding.</mark>**

<iframe src="assets/short_name_main.html" width="100%" height="520" frameborder="0" title="Describe the chart"></iframe>

> **How to read this chart**
> Optional: one or two sentences, if the chart needs explaining.
{: .note}

## First section

...

## What this can't tell us

...

## Sources

- ...

*Data and code: `dataanalysis/build_short_name.py`*
