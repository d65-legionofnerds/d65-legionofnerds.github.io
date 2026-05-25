# AI Coding Agent Instructions for d65-legionofnerds.github.io

## Project Overview

**Legion of Nerds** is a data analysis and advocacy project analyzing Evanston School District 65 (D65) budget, enrollment, and school closure scenarios. The codebase combines:
- **Jekyll documentation site** (`_config.yml`, `/dataanalysis/`, markdown pages) deployed to GitHub Pages
- **Python data pipelines** (pandas, Plotly) for analyzing budget PDFs, enrollment data, and administrative costs
- **Interactive visualizations** (Plotly HTML embeds in Jekyll markdown) presenting findings to stakeholders

## Architecture & Data Flows

### Core Data Pipeline
1. **Source Data**: PDFs (AFR budgets, ISBE reports), CSVs from FOIA requests, public datasets
2. **Processing**: Python scripts in `/dataanalysis/` (e.g., `convert_budget_pdf.py`, `build_budget_explorer.py`) parse/normalize/transform
3. **Output**: Generated CSVs in `/dataanalysis/data/` and HTML charts in `/dataanalysis/assets/`
4. **Publishing**: Jekyll embeds charts in `/dataanalysis/*.md` via `<iframe>` tags; deployed to GitHub Pages

### Key Directory Structure
- `/dataanalysis/` - Python analysis scripts and generated charts
  - `build_budget_explorer.py` - Budget aggregation tool (transforms AFR XLSX → interactive Plotly)
  - `generate_sy27_charts.py` - Enrollment visualizations (school-level grades K-8 analysis)
  - `build_afr_admin_pool.py` - Administrative staffing analysis (parses historical ISBE Annual Financial Reports)
  - `data/afr/` - ISBE budget files (XLSX, hard-coded year-based naming: `05-016-0650-04_AFRxx Evanston CCSD 65.xlsx`)
  - `data/sy27_enrollment/` - Enrollment exports by school/grade
  - `assets/` - Generated Plotly HTML files embedded in markdown
- `/docs/` - **Separate Jekyll site** for school closure scenarios (subdomain: `la-mcnamara.github.io/d65-school-closure-scenarios`)
- `Gemfile` - Jekyll dependencies (pinned `just-the-docs` theme v0.10.1)

## Key Patterns & Conventions

### Data Handling
- **Number cleaning**: Custom `clean_num()` functions handle currency strings, parentheses for negatives: `"(1,234)"` → `-1234.0`
- **Grade ordering**: Explicit `GRADE_ORDER = ["K", "1", "2", ..., "8"]` (string-based for sorting)
- **School name mappings**: Use dict lookups (e.g., `SHORT_NAMES` in charts to replace full names with abbreviations)
- **CSV structure**: DataFrames preserve multi-index columns from AFR; watch for merged cells when parsing XLSX
- **"<10" masking**: Privacy-protected cell counts represented as `"<10"`; convert to `None` or filter out

### Chart Generation
- **Plotly HTML embeds**: All visualizations use `plotly.graph_objects` or `plotly.express`, saved as standalone HTML
- **Subplot layouts**: Use `make_subplots()` for comparative views (e.g., K-5 vs 6-8 enrollment trends)
- **Interactive filters**: Charts often include dropdown buttons or checkboxes for category selection (see `budget_explorer.html`)
- **Asset paths**: Generated charts stored in `/dataanalysis/assets/` with predictable names (e.g., `sy27_building_utilization.html`)

### Jekyll/Documentation
- **Theme**: `just-the-docs` (GitHub Pages compatible, no plugins required)
- **Markdown front matter**: Include `title:`, `layout: default`, `nav_order:` for sidebar navigation
- **IFrame embeds**: Charts embedded via `<iframe src="assets/FILENAME.html" width="100%" height="950" ...></iframe>`
- **Exclude from search**: Use `nav_exclude: true`, `search_exclude: true` for non-essential pages
- **Build process**: `bundle exec jekyll build` outputs to `./_site/`; GitHub Actions deploy to Pages automatically

## Developer Workflows

### Building Data Artifacts
```bash
cd /dataanalysis
# Convert PDF budget to AFR-compatible XLSX (manual step; requires D65 budget PDF)
python convert_budget_pdf.py

# Generate all SY27 enrollment charts
python generate_sy27_charts.py

# Parse AFR XLSX files and generate admin cost analysis
python build_afr_admin_pool.py

# Build budget explorer (aggregates multi-year AFR data → interactive chart)
python build_budget_explorer.py
```

### Local Jekyll Preview
```bash
bundle install  # One-time setup
bundle exec jekyll serve  # Starts local server at http://localhost:4000
```

### CI/CD
- **CI**: GitHub Actions runs `bundle exec jekyll build` on every push/PR (checks YAML/Markdown syntax)
- **Pages Deploy**: `main` branch automatically builds and deploys to `d65-legionofnerds.github.io`
- **Requirements**: Python scripts require `pandas`, `plotly`, `openpyxl`, `pdfplumber`, `xlrd`

## Common Tasks

### Adding a New Analysis
1. Create Python script in `/dataanalysis/build_<analysis_name>.py` with `if __name__ == "__main__":` entry point
2. Generate output CSV → `/dataanalysis/data/<analysis_name>/` and chart HTML → `/dataanalysis/assets/`
3. Create markdown page: `/dataanalysis/<analysis_name>.md` with Jekyll front matter + embedded `<iframe>`
4. Test locally: `bundle exec jekyll serve` and verify chart loads
5. Commit/push; GitHub Actions auto-deploy

### Updating Budget Data
- Obtain latest ISBE Annual Financial Report XLSX from district
- Update filename in `build_budget_explorer.py` (look for `AFR##` pattern)
- Re-run: `python build_budget_explorer.py`
- Charts auto-regenerate with new data

### Fixing Chart Visibility
- Check `/dataanalysis/assets/` for generated HTML files
- Verify `<iframe>` path in markdown matches actual filename (case-sensitive on Linux runners)
- Ensure `width="100%"` for responsive sizing

## External Dependencies & APIs
- **ISBE AFR Data**: Annual reports from `https://www.district65.net/` (manual FOIA/public downloads)
- **IDOT Hazard Data**: School proximity to highways (CSV provided by FOIA)
- **Enrollment Data**: Exported from D65 student information system (manual CSV export)
- **Plotly Hosting**: Charts are self-contained HTML files (no external CDN required beyond Plotly JS bundled in HTML)

## Critical Notes
- **Python version**: Scripts use Python 3.x; compatible with Jupyter notebooks in `/dataanalysis/`
- **File paths**: Hardcoded Windows paths in some legacy scripts (e.g., `convert_budget_pdf.py` references `C:\Users\...`); adapt before running on macOS/Linux
- **Data privacy**: Some cells masked as `<10>` for FERPA compliance; preserve during analysis
- **Theme stability**: `just-the-docs` pinned to v0.10.1 to avoid breaking CSS changes; test before upgrading
