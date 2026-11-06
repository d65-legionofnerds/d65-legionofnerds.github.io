# Legion of Data Nerds website: how to publish, and the house style

This file is for anyone updating the site, and for their AI assistant (Claude Code reads it
automatically; other assistants are pointed here by `AGENTS.md`). **Follow it exactly.** The site is
built so that publishing a new piece is one file, and the homepage, section pages, archive and
search all update themselves.

The site: <https://d65-legionofnerds.github.io>. It is a Jekyll site with its own small theme
("Marked Up": a local data desk). It is built and published by GitHub Actions on every push to
`main` (about two minutes). The repo is **public**: anything committed can be read on GitHub,
even if it is not on the site.

---

## 1. Publish a new analysis (the common case)

1. Put the page in `dataanalysis/<short-name>.md` (lowercase, hyphens). Start from
   `tools/templates/new-analysis.md`.
2. Fill in the front matter (section 2). The required fields are `title`, `date`, `topic`, `type`
   and `summary`.
3. Write the body in Markdown (section 4). Don't repeat the title as a `#` heading: the layout
   prints it. Start sections with `##`.
4. Charts: save Plotly charts to `dataanalysis/assets/` and embed them with an iframe (section 5).
5. Make the picture: render the main chart to a PNG and set `image:` (section 5.3).
6. Add one or two highlights and, if useful, a short version (section 3).
7. Check the build (section 8), then commit and push to `main`.

That is all. **Do not edit the homepage, section pages, `archive.md`, layouts or CSS to list the new
page.** The new page appears automatically:

- at the top of the homepage's **Latest** list, and **as the lead story** if it is the newest
  `type: analysis` (unless another piece is pinned with `lead: true`)
- on its section page (`/topics/<topic>/`) and in **All stories** (`/archive/`), with its filters
- in site search, and in "More on …" at the bottom of related articles

To update an existing analysis, edit its file and add `updated: YYYY-MM-DD`. If the change
alters a finding, add a dated note (section 3.2).

## 2. Front matter

```yaml
---
title: "Did closing Kingsley and Bessie Rhodes save money?"   # the headline
date: 2026-10-29             # first published, YYYY-MM-DD. Decides the order everywhere.
updated: 2026-11-05          # optional: last substantive update
topic: closures              # closures | buildings | budget | admin   (_data/topics.yml)
type: analysis               # see the list below                        (_data/types.yml)
summary: "One or two plain sentences: what we looked at and what we found."
image: /assets/img/lead/closure-savings.png          # analyses: the PNG of the main chart
image_alt: "Bar chart: the District projected $2.90M a year in savings ..."
image_source: dataanalysis/assets/closure_headline.html   # the chart the PNG was made from
takeaways:                   # optional "The short version" box, 2-4 items
  - "First finding, as a full sentence."
  - "Second finding."
featured: true               # optional: the feature at the top of its section page
lead: true                   # optional, rare: pin this analysis as the homepage lead
dek: "..."                   # optional: a longer standfirst under the headline (default: summary)
author: "..."                # optional: byline (default: the Legion of Data Nerds)
published: false             # optional: keep a draft OFF the site (it is still public on GitHub)
---
```

**Topics** (`_data/topics.yml`): `closures` (School Closures), `buildings` (Enrollment &
Buildings), `budget` (Budget & Savings), `admin` (Administration & Staffing). Pick the one a
reader would look under first. A new topic needs a line in `_data/topics.yml` and a page in
`topics/` (copy an existing one).

**Types** (`_data/types.yml`): `analysis`, `explainer`, `memo`, `guest` (guest memo),
`board-letter`, `admin-letter`, `oped`, `tool` (interactive tool), `code` (data & code). Only
`analysis` can lead the homepage. Letters fill "What we've told the District" in the side rail.

**If something is wrong, the build stops** and the GitHub Actions log (and your local build) says
which file and which line, e.g. `dataanalysis/foo.md: topic 'closure' isn't one of: closures,
buildings, budget, admin`. The live site stays as it was until it's fixed. Warnings (missing
picture, too many highlights, long summary) don't stop the build, but fix them.

### Writing the summary, title and short version

- **Title:** a headline, in sentence case or the style of the existing pages. Questions are fine
  ("Did closing Kingsley and Bessie Rhodes save money?"). No "Analysis:" prefixes, no dates.
- **Summary:** one or two sentences, under about 250 characters. It appears on the homepage, the
  section page, All stories, under the headline, and in link previews. It must only say what the
  page itself shows. No adjectives doing the arguing ("shocking", "massive").
- **Takeaways** (`The short version`): two to four findings, each a full sentence taken from the
  page (same numbers, same caveats). Skip it for short pieces and letters.

## 3. The house style ("Marked Up")

The look is a local newsroom's data desk: condensed capitals, a serif body, generous white space.
Its two signature marks only work if they stay rare and consistent.

### 3.1 The highlighter: `<mark>`

Wrap the one or two sentences that carry the piece's main finding:

```markdown
**<mark>It is too early to prove the savings, and the budget shows only part of what was projected.</mark>**
On the data available so far, <mark>the realized staffing savings appear to be a fraction of the $2.0 million stated.</mark>
```

Rules:

- **One or two per piece.** The build warns at more than three. Letters usually need none.
- Highlight a sentence you'd be comfortable seeing **quoted on its own**: it is what people will
  screenshot. It must be precise, sourced in the page, and make sense without the colour.
- Highlight **whole sentences or clauses**, never single words, numbers in tables, or headings.
- Markdown is **not** processed inside `<mark>`. Put bold *outside* it (`**<mark>…</mark>**`) and
  keep links out of highlighted text.
- You can put a `<mark>` in the `summary`; it then shows on the homepage when the piece leads.
- Never use other highlight colours, coloured text, `<span style=…>`, `<font>`, `<big>` or
  `<center>`. Emphasis is **bold**; the key finding is `<mark>`.

### 3.2 Red-pen notes (margin notes): `{: .note}`

A short note from us that sits in the right margin on wide screens and inline on phones. Use it
for **updates and corrections** (always dated), for **how to read a chart**, and for important
caveats. Write a blockquote whose first line is a bold label, then `{: .note}` on the next line:

```markdown
> **Update · Nov 5, 2026**
> The District sent its FY27 position list. Table 2 now uses it; the totals did not change.
{: .note}

> **About this chart**
> Kingsley only. The 2025 scenarios were presented "in addition to" the Bessie Rhodes closure.
{: .note}
```

- Put the note right after the paragraph or chart it is about.
- A long note (over ~60 words), a note holding a table, or several notes in a row would crowd the
  margin and push the next chart down. Keep those in the text column with `{: .note .inline}`.
- Labels: `Update · <date>`, `Correction · <date>`, `About this chart`, `How to read this chart`,
  `What we asked the District`, or a short label of your own. Keep notes under about 60 words.
- Corrections are never silent: fix the text, then add a dated `Correction` note saying what
  changed. Add `updated:` to the front matter.
- A plain blockquote (no `{: .note}`) is for quoting someone else, e.g. a District document.

### 3.3 Colour

Yellow means our key finding (the highlighter). Red means our notes, plus costs and negative
numbers. Nothing else gets colour in text. For a cost or loss in a table, write
`<span class="neg">cost $329,000</span>`.

### 3.4 Big numbers inside an article

For a row of headline figures (instead of hand-styled big coloured text):

```html
<div class="stats">
  <div class="stat"><b>+54%</b><p>growth in administrative FTE, FY16 to FY25</p></div>
  <div class="stat"><b><span class="hl">+59%</span></b><p>real admin spending per pupil</p></div>
</div>
```

At most one figure in the row gets `<span class="hl">` (the one the piece is about).

### 3.5 Homepage pieces kept by hand

These are short data files, not code. Change them when the facts change:

| What | File | Notes |
|---|---|---|
| By the numbers (4 figures) | `_data/numbers.yml` | Each figure must appear in its `source` page. Check it when you update that page. |
| Coming up (navy box) | `_data/upcoming.yml` | Give every entry an `until` date; it hides itself after that. |
| How we got here (closures timeline) | `_data/timeline.yml` | Mark a future date `upcoming: true`. |
| In the news | `_data/news.yml` | Newest first. The three newest show on the homepage. |
| PDFs, outside articles, apps, standalone HTML tools | `_data/links.yml` | Same fields as front matter plus `link:` and optional `format:` (PDF, App, Map). |

## 4. Writing the body

- `##` for sections (three or more `##` sections produce the "In this story" contents list
  automatically), `###` for sub-sections. Never `#`.
- Short paragraphs. Lead with the finding, then the evidence, then the caveats.
- Tables: plain Markdown tables, numbers right-aligned (`|---:|`). Wide tables scroll sideways on
  phones by themselves. Avoid HTML tables unless you need merged cells; never inline styles.
- Images: `![Alt text that says what the chart shows](../assets/file.svg)` or a path relative to
  the page. Put a caption in a following `*italic line*` or use `<figure>`/`<figcaption>`.
- Links to pages on this site: relative paths (`[FAQ](admin-growth-faq.html)`,
  `[memo](../assets/FinancialLeversMemoV2.pdf)`) or `{{ '/assets/x.pdf' | relative_url }}`.
  **Never** a bare leading slash like `/assets/x.pdf`: it breaks the preview copy of the site.
- Data downloads: link CSVs in `dataanalysis/data/`. Big raw files (`dataanalysis/data/afr/`)
  are not on the site; link them on GitHub.
- End analyses with `## Sources` (and `## Methods` or `## How we did this` if needed), and a line
  pointing to the code: `*Data and code: dataanalysis/build_<name>.py*`.
- No `<style>` or `<script>` blocks in pages, no per-page CSS. If something needs a new visual
  pattern, add it once to `assets/css/site.css` and document it here.

## 5. Charts

### 5.1 Making them

- Build charts with Plotly in a script `dataanalysis/build_<name>.py` (or a notebook) and save
  them as standalone HTML in `dataanalysis/assets/`:
  `fig.write_html(path, include_plotlyjs="cdn", full_html=True, config={"responsive": True, "displaylogo": False})`
- Let the width follow the page: **don't set `layout.width`**. Set a `layout.height` that fits the
  content (usually 420-650).
- Colours: grey for the District's figure or claim, blue for our estimate, red only for costs or
  losses. One accent per chart. White background.
- Put the title and a one-line subtitle in the chart (`title.text` with a `<br><sup>` subtitle).
  Keep titles short enough to fit on a phone (about 60 characters) or they get cut off.
- Legends: horizontal, below or above the plot (`orientation="h"`), not on the right, so they
  don't squeeze the plot on phones.
- Long category labels (school names, budget lines): use a horizontal bar chart, or wrap labels
  with `<br>`.
- Never change the data when you restyle a chart. If you re-run a build script, check the numbers
  in the chart still match the page.
- **Phones.** If no single layout works at both ~1,016 px and ~350 px (a long legend, long labels,
  a grid of small panels), give the chart a phone layout: in a build script use
  `from patch_plotly_layout import write_html` (in `tools/`) and
  `write_html(fig, path, narrow={"legend.y": -0.3, "height": 900, ...})`. Below 560 px the chart
  redraws with the `narrow` values (Plotly relayout keys). For a chart with no script, patch the
  saved file: `python tools/patch_plotly_layout.py CHART.html --narrow phone.json` (also `--set`,
  `--unset width`, `--show`). The tool never touches the data and checks that before saving.
- If a chart's frame is too short at some width, the site grows the frame to fit on its own; you
  don't need a different iframe height for phones.

### 5.2 Embedding them

```html
<iframe src="assets/closure_headline.html" width="100%" height="500" frameborder="0" title="Projected vs. visible closure savings"></iframe>
```

- `width="100%"` always. `height` = the chart's `layout.height` plus about 20.
- Add a `title` describing the chart (screen readers use it).
- On wide screens, charts run the full width of the text plus the margin (about 1,016 px); on
  phones about 350 px. **Check both** (section 8). If the chart is cut off, squashed or its legend
  covers the plot on a phone, fix the chart, not the page.
- Static charts (SVG/PNG) go in `assets/` and are embedded as images.

### 5.3 The picture (`image:`)

Every `analysis` needs a picture: a PNG of its main Plotly chart. It is shown when the piece leads
the homepage and as the preview image when the link is shared.

```bash
python tools/chart_image.py dataanalysis/assets/closure_headline.html assets/img/lead/closure-savings.png
```

Then set `image`, `image_alt` (what the chart shows, with the key numbers) and `image_source`
(the chart file) in the front matter. Re-run the command whenever that chart changes. **Look at
the PNG**: if a title, legend or label is cut off or overlaps, render the chart bigger with the
same 16:9 shape (`--width 1000 --height 562 --scale 2.4`) or drop its title (`--no-title`). If the
page has no Plotly chart, use its main static chart, saved as a PNG in `assets/img/lead/`. No Python?
Open the chart in a browser, click the camera icon ("Download plot as a png") and save it to
`assets/img/lead/`.

## 6. Other kinds of content

- **Letters** to the Board or administration: `letterstoboard/<name>.md` or
  `letterstoadmin/<name>.md`, `type: board-letter` / `admin-letter`, the date it was read or
  sent. No highlights or picture needed.
- **Memos, explainers, op-eds:** a page (`type: memo` / `explainer` / `oped`) or, for a PDF or
  outside article, an entry in `_data/links.yml`. PDFs go in `assets/`.
- **Interactive tools** that are a whole HTML app: put the file in `dataanalysis/` and add a
  `_data/links.yml` entry with `type: tool`.
- **Drafts:** `published: false` keeps a page off the site. The repo is public, so don't commit
  anything that must stay private. Never leave drafts or screenshots in the repo root.

## 7. Don't

- Don't change the address (file name or folder) of a published page: people have shared links.
  If you must, keep the old file as a short page that links to the new one.
- Don't edit `index.md`, `archive.md`, `topics/`, `_layouts/`, `_includes/`, `_plugins/` or
  `assets/css/site.css` to publish a piece. Change them only for a design change, on a branch,
  with a pull request.
- Don't add colours, fonts, inline styles or `<style>` blocks to pages.
- Don't delete data files that pages link to.

## 8. Check before you push

```bash
bundle exec jekyll build      # must finish with no "problem(s)"; read any "Check:" warnings
bundle exec jekyll serve      # preview at http://localhost:4000
```

Look at the new page at full width and at phone width (browser dev tools, about 390 px):
headline, summary, highlights, notes in the margin (wide) or inline (phone), every chart fully
visible, no sideways scrolling. Then look at the homepage: is the right piece leading, with its
picture? An assistant can do this with Playwright screenshots of `_site` served locally.

No Ruby installed? Push to a branch and open a pull request: the CI check builds the site and
reports the same problems. Merging to `main` publishes.

Commit messages: say what changed for readers ("Add analysis: ...", "Update SY27 building use
with Oct 1 data").

## 9. How the site works (for design changes)

| Path | What |
|---|---|
| `_config.yml` | Site settings and the list of files kept off the site (`exclude`) |
| `_plugins/stories.rb` | Collects every page with `topic:` plus `_data/links.yml` into `site.data.stories`, picks the lead, checks front matter |
| `_layouts/` | `base` (masthead, nav, footer), `home`, `article` (default for every page), `topic`, `archive`, `page` |
| `_includes/` | `story.html` (a list entry), `kicker.html`, `story-link.html` |
| `assets/css/site.css`, `assets/js/site.js` | The whole design; small progressive enhancements |
| `topics/*.md`, `archive.md`, `letterstoboard.md`, `letterstoadmin.md`, `publications.md`, `dataanalysis.md` | Listing pages, generated from the stories |
| `sdrpnews.md`, `resources.md`, `about.md`, `search.md` | Plain pages |
| `tools/chart_image.py` | Renders a Plotly chart to the lead PNG |
| `tools/patch_plotly_layout.py` | Changes a saved chart's layout without touching its data; adds phone layouts |
| `.github/workflows/pages.yml` | Builds with Jekyll, adds Pagefind search, deploys |
| `_config_preview.yml` | Settings for a preview copy published somewhere else (adds a banner, hides it from search engines) |

Search is built by [Pagefind](https://pagefind.app) after Jekyll, in the deploy workflow; it
indexes article text only (`data-pagefind-body`). It doesn't exist in a plain local build.

## 10. Data conventions (from the analysis scripts)

- Scripts live in `dataanalysis/build_<name>.py` with an `if __name__ == "__main__":` entry point;
  outputs go to `dataanalysis/data/<name>/` (CSV) and `dataanalysis/assets/` (chart HTML).
  Python deps: `dataanalysis/requirements.txt` (pandas, plotly, openpyxl, pdfplumber, xlrd).
- Currency strings: use the scripts' `clean_num()`; `"(1,234)"` means `-1234.0`.
- Counts masked as `"<10"` are FERPA-protected: keep them masked or set them to missing. Never
  estimate or fill them in.
- Grade order: `GRADE_ORDER = ["K", "1", "2", "3", "4", "5", "6", "7", "8"]` (strings).
- Some older scripts have hard-coded Windows paths; make them relative before running elsewhere.
- File paths are case-sensitive on the build server: match iframe `src` to the file name exactly.
