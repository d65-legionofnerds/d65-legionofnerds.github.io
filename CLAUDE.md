# CLAUDE.md — d65-legionofnerds.github.io

## Project Overview

**Legion of Nerds** is a data analysis and advocacy project examining Evanston School District 65 (D65) budget, enrollment, and school closure scenarios. The site is a Jekyll documentation site deployed to GitHub Pages, with Python data pipelines generating interactive Plotly visualizations embedded in markdown pages.

## Repo Structure

```
/dataanalysis/          Python scripts + generated charts
  build_*.py            Data pipeline scripts (one per analysis)
  data/afr/             ISBE Annual Financial Report XLSX files
  data/sy27_enrollment/ Enrollment CSVs by school/grade
  assets/               Generated Plotly HTML files (embedded in markdown)
/.github/
  instructions/         AI agent instruction files
    copilot-instructions.md
  workflows/            GitHub Actions (CI + Pages deploy)
Gemfile                 Jekyll deps (just-the-docs v0.10.1, pinned)
_config.yml             Jekyll site config
```

## Common Commands

```bash
# Local preview
bundle exec jekyll serve         # http://localhost:4000

# Run a data pipeline
cd dataanalysis
python build_budget_explorer.py
python generate_sy27_charts.py
python build_afr_admin_pool.py

# CI check (what GitHub Actions runs)
bundle exec jekyll build
```

## Key Conventions

- **Charts**: All visualizations are standalone Plotly HTML files saved to `/dataanalysis/assets/`, embedded in markdown via `<iframe>`.
- **Data cleaning**: Use `clean_num()` for currency strings; `"(1,234)"` → `-1234.0`. Cells masked `"<10"` are FERPA-protected — preserve or filter to `None`, never fabricate values.
- **Grade ordering**: Always use `GRADE_ORDER = ["K", "1", ..., "8"]` (string keys) for consistent sort.
- **Jekyll front matter**: Every page needs `title:`, `layout: default`, `nav_order:`.
- **File paths**: Some legacy scripts have hardcoded Windows paths — adapt before running on macOS/Linux.

## Adding a New Analysis

1. Create `/dataanalysis/build_<name>.py` with an `if __name__ == "__main__":` entry point.
2. Write output CSV → `/dataanalysis/data/<name>/` and chart HTML → `/dataanalysis/assets/`.
3. Create `/dataanalysis/<name>.md` with front matter and an `<iframe>` pointing to the chart.
4. Verify locally with `bundle exec jekyll serve`.

## CI/CD

- Every push/PR runs `bundle exec jekyll build` via GitHub Actions.
- Merges to `main` auto-deploy to `d65-legionofnerds.github.io`.
- Python deps needed for pipelines: `pandas`, `plotly`, `openpyxl`, `pdfplumber`, `xlrd`.

## Critical Notes

- `just-the-docs` is pinned to v0.10.1 — test carefully before upgrading.
- IFrame `src` paths are case-sensitive on Linux runners; match filenames exactly.
- Python scripts target Python 3.x and are compatible with Jupyter notebooks.
