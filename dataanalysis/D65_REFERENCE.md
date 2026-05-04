# D65 Administrative Growth — Comprehensive Reference Document

Last updated: 2026-05-04

This document is a ground-truth reference for LLMs and researchers working on District 65 (Evanston/Skokie, IL) administrative growth analysis. It consolidates key facts, data sources, personnel rosters, timelines, and access methods so future conversations can start from a complete picture without re-deriving everything.

---

## 1. District Overview

- **District:** Evanston/Skokie Community Consolidated School District 65 (K-8)
- **Location:** Evanston and Skokie, Illinois
- **Superintendent:** Dr. Angel Turner
- **CFO:** Tamara Mitchell
- **Board:** 7 elected members
- **SY2025-26 K-8 Enrollment:** 5,625 (K-8 + PreK with IEP; down from 7,523 in SY2015-16 = **-25%**)
- **Total staff (staff directory):** 1,448
- **FY25 AFR admin compensation pool:** $19.99M (2026 dollars)
- **FY25 total operating fund expenditures:** ~$168.7M

### Schools (SY2025-26)
**Elementary (K-5):** Dawes, Dewey, Dr. Bessie Rhodes, Dr. Martin Luther King Jr., Kingsley (closing after SY25-26), Lincoln, Lincolnwood, Oakton, Orrington, Walker, Washington, Willard
**Middle (6-8):** Chute, Haven, Nichols
**Other:** JEH Early Childhood Center, Park School (special ed), Rice Children's Center
**Central Office:** JEH Administrative Center (86 staff)

---

## 2. Key Findings Summary

| Metric | SY2015-16 / FY16 | SY2025-26 / FY25 | Change |
|--------|-------------------|-------------------|--------|
| K-8 Enrollment | 7,523 | 5,625 | **-25%** |
| TRS Admin headcount | 11 | 24 | **+118%** |
| Principal headcount | 34 | 28 | **-18%** |
| IMRF Support Staff (above threshold) | 30 | 101 | **+237%** |
| Higher-paid admin (CPI-indexed, total) | 75 | 94 | **+25%** |
| Admin per 1,000 students | 10.0 | 16.7 | **+67%** |
| Total admin comp pool (2026 $) | $16.56M | $19.99M | **+21%** |
| General Admin (fn 2300, 2026 $) | $2.40M | $4.88M | **+103%** |
| Per-pupil admin spending (2026 $) | $2,201 | $3,401 | **+55%** |
| Per-pupil central-office excl principals (2026 $) | $1,246 | $2,125 | **+71%** |
| IAR math proficiency (% meeting benchmark) | 44.8% (2018) | 42.3% (2024) | **-2.5 pts** |

**Key conclusion:** The cost growth is driven by adding more positions, not by paying existing administrators more. Per-person compensation has roughly tracked inflation.

---

## 3. Enrollment History

| Year (ending) | Enrollment | Source |
|---------------|----------:|--------|
| 2016 | 7,523 | Opening of Schools 2015-16 (foiagras doc 7213) |
| 2017 | 7,712 | Opening of Schools 2019-20 cross-year table (foiagras doc 4318) |
| 2018 | 7,578 | Opening of Schools 2019-20 (foiagras doc 4318) |
| 2019 | 7,562 | Opening of Schools 2019-20 (foiagras doc 4318) |
| 2020 | 7,483 | Opening of Schools 2019-20 (foiagras doc 4318) |
| 2021 | 6,997 | ISBE state report cards |
| 2022 | 6,481 | ISBE state report cards |
| 2023 | 6,145 | ISBE state report cards |
| 2024 | 6,053 | ISBE state report cards |
| 2025 | 5,877 | ISBE state report cards |
| 2026 | 5,625 | D65 Data Dashboard (data.district65.net) |

**Note:** These are K-8 + PreK-with-IEP figures consistent with D65's Opening of Schools methodology. ISBE's "total served" figure (used by Larry Gavin) is higher (5,941 for SY25-26) because it adds early-childhood, Park School, and Rice Center students.

---

## 4. PA Headcount by Year and Role Class

From `d65_admin_comp_combined.csv`:

| Year | TRS Admin | TRS Admin Comp | Principal | Principal Comp | IMRF Staff | IMRF Comp | Total N | Total Comp |
|------|----------:|---------------:|----------:|---------------:|-----------:|----------:|--------:|-----------:|
| 2016 | 11 | $2.07M | 34 | $4.99M | 30 | $3.04M | 75 | $10.10M |
| 2017 | 16 | $2.63M | 25 | $3.86M | 39 | $3.80M | 80 | $10.29M |
| 2018 | 17 | $2.79M | 28 | $4.27M | 46 | $4.59M | 91 | $11.65M |
| 2019 | 15 | $2.58M | 29 | $4.57M | 48 | $4.69M | 92 | $11.85M |
| 2020 | 21 | $3.20M | 31 | $4.71M | 54 | $5.38M | 106 | $13.29M |
| 2021 | 19 | $3.04M | 34 | $4.58M | 59 | $5.98M | 112 | $13.61M |
| 2022 | 20 | $3.41M | 34 | $5.03M | 48 | $4.72M | 102 | $13.16M |
| 2023 | 23 | $4.13M | 37 | $6.00M | 74 | $7.94M | 134 | $18.08M |
| 2024 | 45 | $6.61M | 32 | $4.93M | 62 | $6.37M | 139 | $17.91M |
| 2025 | 23 | $4.30M | 34 | $5.56M | 96 | $10.11M | 153 | $19.96M |
| 2026 | 24 | $4.46M | 28 | $4.81M | 101 | $10.76M | 153 | $20.04M |

**Notes:**
- Comp figures are NOMINAL (not inflation-adjusted)
- 6 people in 2026 appear in both TRS Admin and IMRF → 147 unique individuals (not 153)
- The SY2023-24 TRS Admin spike (45) reflects a reporting anomaly or reclassification; it corrected back to 23 in SY2024-25
- IMRF counts are affected by the $75K statutory threshold (not CPI-indexed here)
- The SY22-23 → SY23-24 transition saw ~11 IMRF staff reclassified into TRS Admin

---

## 5. AFR Admin Compensation Pool by Function Code (Inflation-Adjusted to 2026 $)

From `afr_admin_pool_summary.csv`:

| Year | 2300 General Admin | 2400 School Admin | 2500 Business | 2600 Central Support | Total Pool | Excl Principals |
|------|-------------------:|------------------:|--------------:|--------------------:|-----------:|----------------:|
| 2012 | $1.98M | $6.33M | $3.91M | $3.15M | $15.36M | $9.03M |
| 2016 | $2.40M | $7.19M | $3.93M | $3.04M | $16.56M | $9.37M |
| 2017 | $3.34M | $7.06M | $3.71M | $3.86M | $17.97M | $10.91M |
| 2018 | $3.77M | $6.91M | $3.53M | $3.74M | $17.94M | $11.03M |
| 2019 | $3.36M | $6.90M | $3.48M | $4.01M | $17.75M | $10.85M |
| 2020 | $4.01M | $6.74M | $3.57M | $4.20M | $18.52M | $11.78M |
| 2021 | $4.36M | $8.21M | $3.38M | $3.75M | $19.69M | $11.48M |
| 2022 | $4.23M | $7.40M | $3.57M | $4.37M | $19.57M | $12.17M |
| 2023 | $5.59M | $7.54M | $3.67M | $4.68M | $21.48M | $13.94M |
| 2024 | $4.87M | $7.63M | $3.61M | $4.64M | $20.75M | $13.12M |
| 2025 | $4.88M | $7.50M | $3.71M | $3.90M | $19.99M | $12.49M |

**Function code definitions:**
- 2300: Superintendent's office, asst superintendents, executive admin, curriculum directors/coordinators
- 2400: Principals, asst principals, school office staff (secretaries, attendance clerks)
- 2500: CFO, fiscal services, payroll, business (EXCLUDES 2540 O&M and 2550 Pupil Transport)
- 2600: Planning/research, IT, staff services, data processing

---

## 6. TRS Admin Roster — SY2025-26 (24 People)

| Name | Position | Base Salary | Total Comp |
|------|----------|------------:|-----------:|
| Angel Turner | Superintendent | $260,000 | $286,379 |
| Tamara Mitchell | Chief Financial Officer | $216,959 | $259,525 |
| Stacy Beardsley | Asst Superintendent of Accountability | $186,633 | $239,475 |
| Charmekia McCoy | Director of Schools Management | $163,357 | $213,372 |
| Jessica Plaza | Director of MTSS & SEL | $154,283 | $200,953 |
| Tiffany Taylor | Executive Chief of Human Relations | $182,105 | $200,181 |
| Kathleen Speth | Asst Superintendent of Academics | $176,800 | $195,428 |
| Narishea Parham | Director of Early Childhood Programs | $146,218 | $194,808 |
| Heather Smith | Director of Finance | $156,000 | $192,453 |
| Emily Chambers | Manager of Student Specialized Services | $141,365 | $186,905 |
| Regina Colquitt | Director of Humanities | $136,880 | $182,364 |
| Melissa Messinger | Executive Chief of Communications | $152,881 | $181,904 |
| Donna Cross | Executive Director of RAAD | $141,980 | $177,066 |
| Virginia Sulek | Director of Student Specialized Services | $158,550 | $175,972 |
| Soundarya Radhakrishnan | Director of STEAM | $130,000 | $173,684 |
| Elena Caceres | Executive Director of Technology | $145,601 | $170,188 |
| Kirby Callam | Director of Strategic Projects | $130,000 | $167,060 |
| Sabine Champagne | Director of Human Relations | $124,801 | $165,448 |
| Amy Correa | Director of Multilingual Services | $138,935 | $162,675 |
| Bryon Harris | Director of Climate & Safety | $115,000 | $152,407 |
| Omar Whyte | Director of Buildings, Grounds & Transportation | $119,599 | $148,542 |
| Deborah Osher | Director of Programs & Partnerships | $124,801 | $147,453 |
| Theresa Lee | Asst Director of Teaching & Learning | $110,956 | $146,415 |
| Jeanne McCullough | Health Services Director | $120,778 | $143,810 |

**Dual-listed in both TRS Admin and IMRF:** Callam, Champagne, Harris, Messinger, Taylor, Whyte

**Positions that did NOT exist in SY2015-16:** Executive Chief of Communications, Executive Chief of Human Relations, Executive Director of RAAD, Executive Director of Technology, Director of MTSS & SEL, Director of STEAM, Director of Multilingual Services, Director of Climate & Safety, Director of Strategic Projects, Director of Programs & Partnerships, Director of Schools Management, Director of Humanities, Asst Director of Teaching & Learning, Manager of Student Specialized Services

---

## 7. Bargaining Units

D65 has five bargaining units plus non-union staff:

| Code | Full Name | Members |
|------|-----------|---------|
| DEC | District Educators' Council | Teachers (certificated) |
| DESC | District Educational Secretarial and Clerical Association | Secretaries, health clerks, food service, tech assistants |
| ECMA | (Likely) Evanston Council of Management and Administration | Management/admin positions — broader than TRS Admin |
| ETAA | Evanston Teacher Assistants Association | Paraprofessionals / teacher assistants |
| EACCP | Evanston Association of Child Care Professionals | SACC / childcare workers |
| Non-Union | — | Administrative and support staff not in a bargaining unit |

**Important:** The District's SDRP budget presentations break personnel cuts by bargaining unit, NOT by the PA disclosure categories (TRS Admin / IMRF / Principal). The "22 administrators" in the District's April 2026 proposal likely refers to ECMA members or a similar broad admin definition — NOT 22 of the 24 TRS Admin.

**April 1 deadline:** Illinois law requires administrator contract non-renewal notification by April 1. This applies to ECMA-type positions. The District's $8.3M admin-cut proposal was presented on April 13/20, 2026 — 13-19 days after this deadline, making those cuts unactionable for FY27.

---

## 8. SDRP (Structural Deficit Reduction Plan) Timeline

| Date | Phase | Action | Savings |
|------|-------|--------|---------|
| Feb 2024 | Identification | Began SDRP process | — |
| Jul 2024 | Phase I | Hiring freeze, eliminated vacant positions, purchased services reductions | $6.5M (FY25) |
| Jul 2025 | Phase II | ~100 FTE reductions, school-based staffing model, transportation efficiencies | $13.2M (FY26) |
| Jan 9, 2026 | Phase III | Board resolution to close Kingsley + conditional Lincolnwood trigger | $1.66M–$3.24M |
| Mar 23, 2026 | — | Board approved $528K iPad purchase despite petition | — |
| Apr 9, 2026 | — | Superintendent proposed laying off 9 middle school counselors | — |
| Apr 13, 2026 | Phase III | Committee of the Whole: SDRP Expenditure Reduction Plan presented (doc 21784). Shows 55.5 net FTE reductions for $3.83M personnel + $2.1M non-personnel = $5.93M total | $5.93M (FY27) |
| Apr 14, 2026 | — | Board curtailed counselor layoffs to 2 of 9 positions | ~$200K |
| Apr 20, 2026 | Phase III | Regular Board Meeting. Slide 13 reportedly showed "Items for Analysis" with $8.29M in potential admin/non-union cuts (22 admin + 42 non-union = 64 positions). Presented 19 days after April 1 contractual deadline | $8.29M (potential, FY28+) |
| Apr 2026 | — | Superintendent reassigned all 3 middle school librarians to classroom positions | ~$0 direct |

**FY27 position reductions by bargaining unit (April 13 deck):**

| Unit | Reductions | Additions | Net | Savings |
|------|----------:|----------:|----:|--------:|
| DEC (teachers) | -24 | 0 | -24 | $2,258,346 |
| DESC (secretarial) | -5 | 0 | -5 | $170,465 |
| ECMA (management/admin) | -8 | 0 | -8 | $463,760 |
| ETAA (teacher assistants) | -10 | 0 | -10 | $173,520 |
| EACCP (childcare) | -4.5 | 0 | -4.5 | $238,150 |
| Non-Union | -5 | +1 | -4 | $529,217 |
| **Total** | **-56.5** | **+1** | **-55.5** | **$3,833,458** |

---

## 9. Right-Sizing Scenarios

All use $129,489 per-cut (District's own figure: $8,287,312 ÷ 64 positions).

| Scenario | Target | Cuts | Annual Savings | % of AFR Pool |
|----------|--------|-----:|---------------:|--------------:|
| Legion Moderate (return to 2016-2019 baseline) | ~81 admin | ~13 | $1.68M | 8.4% |
| Legion Peer Median (~12/1k students) | ~68 admin | ~26 | $3.43M | 17.2% |
| Legion Match SY2015-16 ratio (~10/1k) | ~56 admin | ~38 | $4.91M | 24.6% |
| **District's own April 2026 proposal** | — | **64** | **$8.29M** | **41.5%** |

---

## 10. Student-Facing Cuts for Comparison

| Measure | Annual Savings | Source |
|---------|---------------:|--------|
| 2 middle school counselors laid off | ~$200K | Board action 4/14/2026 |
| Middle school librarians reassigned | ~$0 | Superintendent memo, April 2026 |
| Close Kingsley Elementary | ~$1.66M | SDRP III revised model (foiagras doc 12033) |
| Close Lincolnwood (conditional) | ~$1.57M incremental | Resolution 1/9/2026 (foiagras doc 13846) |
| Both closures combined | ~$3.24M | SDRP III Scenario 2D |
| Decline iPad purchase (one-time) | $528K one-time | Board action 3/23/2026 |

---

## 11. Staff Directory Profile (SY2025-26)

Scraped from D65 public website. File: `C:\Users\jkarlin\Documents\Code\github_files\D65\district65_staff_complete.csv`
Columns: name, title, location, department, phone, extension, email

**Totals:**
- 1,448 total staff
- 455 teachers
- 268 paraprofessionals
- 63 custodians
- 28 principals/APs
- 86 at JEH Administrative Center (22 senior leadership, 19 mid-level admin, ~45 support)

**JEH Senior Leadership (22):** Superintendent (1), Asst Superintendents (2), Chiefs (2), Executive Directors (2), Directors (13), Health Services Director (1), Executive Assistants (2 — technically support but titled "Executive")

**JEH Mid-Level Admin (19):** Various managers, coordinators, supervisors

**Cross-reference with PA data:**
- 24/24 TRS Admin matched in staff directory (100%)
- 27/28 Principals matched (Carlos Mendez not found)
- 99/101 IMRF matched (2 name discrepancies: Manuel/Jose Aleman, China/Rosalba Saria)
- ~21 JEH staff NOT in PA data (below $75K threshold)

---

## 12. "How Many Central Administrators?" — The Denominator Question

Different sources give different counts depending on definition:

| Definition | Count | Source |
|-----------|------:|--------|
| TRS Admin only (PA 96-0434) | 24 | State filing |
| TRS Admin + Principals (PA 96-0434) | 52 | State filing |
| Cross-referencing all 3 state lists | 62 | Larry Gavin, RoundTable March 2026 |
| Staff directory admin titles (excl principals) | 41-49 | Legion analysis of D65 website |
| Board member internal figure (uncitable) | 64 | Off-record |
| CPI-indexed higher-paid admin (all categories) | 94 | Legion analysis |
| All PA-disclosed unique individuals | 147 | State filings |

The District's "22 administrators" in the $8.3M proposal is ~35% of the ~62 central admin pool (Gavin), NOT 92% of the 24 TRS Admin.

---

## 13. CPI-U Index Values (for Inflation Adjustment)

Base year: 2026. All dollar figures in the analysis are adjusted to 2026 dollars.

| Year | CPI-U | Multiplier to 2026 |
|------|------:|--------------------:|
| 2012 | 229.594 | 1.4351 |
| 2016 | 240.007 | 1.3729 |
| 2017 | 245.120 | 1.3442 |
| 2018 | 251.107 | 1.3122 |
| 2019 | 255.657 | 1.2888 |
| 2020 | 258.811 | 1.2731 |
| 2021 | 270.970 | 1.2160 |
| 2022 | 292.655 | 1.1259 |
| 2023 | 304.702 | 1.0814 |
| 2024 | 313.689 | 1.0504 |
| 2025 | 322.350 | 1.0222 |
| 2026 | 329.500 | 1.0000 |

CPI-indexed threshold: $75,000 × (year CPI ÷ 240.007) → ~$103,000 in 2026.

---

## 14. External Validation

### Larry Gavin, Evanston RoundTable

- **March 22, 2026:** "District 65 Has 25% Fewer Students but 10% More Staff. Why?"
  - D65's -25% enrollment decline is steepest of 21 nearby K-8 districts (next-largest: 14.3%)
  - Total FTEs increased ~130 (+10%)
  - Cross-referencing all 3 disclosure lists → 62 administrators (10 more than PA 96-0434 alone)
  - Math IAR: 44.8% → 42.3%
  - URL: `https://evanstonroundtable.com/2026/03/22/analysis-and-viewpoint-district-65-has-25-fewer-students-but-10-more-staff-why/`

- **November 2, 2025:** "Guest Essay: District 65 Employees and Enrollment"
  - Flagged IES Coordinators (9), Human Relations layers, recent director-level positions, APs in small schools
  - URL: `https://evanstonroundtable.com/2025/11/02/guest-essay-district-65-employees-enrollment/`

### FOIA Gras (Tom Hayden)

Blog and document archive at foiagras.com. Key posts:
- Post 249 (2026-03-09): D65 IT department spending
- Post 253 (2026-03-07): KalaJu protest letter (special ed transport)
- Post 255 (2026-03-10): D65 tech hard to unwind
- Post 262 (2026-03-22): D65 board preview March 23
- Post 264 (2026-04-18): D65 firing librarians
- Post 267 (April 2026): Firing librarians bad idea letter

---

## 15. Data Sources and Access Methods

### FOIA Gras (MCP Tool Available)

**Website:** https://foiagras.com (blog) and https://ig.foiagras.com (document viewer)
**MCP entity slug:** `district-65`
**Direct document URL pattern:** `https://ig.foiagras.com/api/public/chat/documents/{doc_id}/view`

**Available MCP tools:**
- `mcp__foiagras__search_documents` — Full-text search across all indexed D65 board documents. Supports quoted phrases, +required, -excluded, after:/before: date filters.
- `mcp__foiagras__get_document_details` — Get full text of a document by ID
- `mcp__foiagras__get_raw_text` — Read long documents in chunks (offset/limit)
- `mcp__foiagras__search_document_text` — Search within a specific document
- `mcp__foiagras__list_meetings` — List all indexed board meetings
- `mcp__foiagras__get_meeting_details` — Get agenda/documents for a specific meeting
- `mcp__foiagras__get_meeting_transcript` — Get meeting transcript if available
- `mcp__foiagras__search_newsletters` — Search FOIA Gras blog posts

**Key document IDs:**
- 4133: PA 96-0434 TRS Administrator report FY26
- 21784: April 13, 2026 SDRP Phase III Expenditure Reduction Plan presentation
- 12033: SDRP III revised financial model (Dec 1, 2025) — school closure savings
- 13846: Board resolution for Kingsley closure + Lincolnwood trigger (Jan 9, 2026)
- 7213: Opening of Schools 2015-16 (enrollment)
- 4318: Opening of Schools 2019-20 (cross-year enrollment table)

### DistrictVitals

**URL:** https://ccsd65.districtvitals.com/data#sec-afr-excel
**Contains:** Annual Financial Reports (AFR) filed with ISBE. Excel downloads with expenditure breakdowns by function code. This is the source for the AFR admin pool data.

### D65 Official Sources

- **Board documents (BoardBook):** https://meetings.boardbook.org/Public/Organization/1247
- **D65 Data Dashboard:** https://data.district65.net/ — enrollment, demographics, assessment data
- **D65 Staff Directory:** https://www.district65.net/ (public staff listing with name, title, location, department)
- **D65 SDRP Hub:** https://www.district65.net/about/budget-finance/structural-deficit-reduction-plan/phase-iii-school-closures-hub

### ISBE (Illinois State Board of Education)

- State report cards with enrollment and assessment data
- PA 96-0434 administrator salary filings
- PA 97-0609 IMRF compensation filings
- AFR filings

### Evanston RoundTable

**URL:** https://evanstonroundtable.com/
Independent local journalism. Larry Gavin's analyses are the primary external validation of the Legion's findings.

---

## 16. Local Data Files

All paths relative to the nerds site repo: `C:\Users\jkarlin\Documents\Code\nerds_site\d65-legionofnerds.github.io\dataanalysis\`

| File | Description |
|------|-------------|
| `data/d65_admin_comp_combined.csv` | PA disclosure data: individual-level comp for all TRS Admin, Principals, IMRF Support Staff, SY2016-17 through SY2025-26. Columns: year, school_year, role_class, last_name, first_name, position, base_salary, total_salary, total_comp, source |
| `data/afr_admin_pool_summary.csv` | AFR data: total compensation by function code (2300/2400/2500/2600), FY12-FY25, nominal and inflation-adjusted |
| `data/afr_admin_pool.csv` | Detailed AFR breakdown (sub-codes) |
| `data/d65_enrollment_history.csv` | Enrollment by year with sources |
| `data/cpi_history.csv` | BLS CPI-U values for inflation adjustment |
| `data/d65_recent_cuts.csv` | Student-facing and other recent cost-cutting measures with sources |
| `data/afr/` | Raw AFR Excel files from ISBE |
| `data/d65_admin_comp_pdfs/` | Markdown conversions of PA disclosure PDFs |
| `data/d65_admin_comp_pdfs/sources.json` | Metadata for PDF sources |
| `build_admin_growth_data.py` | Script to build d65_admin_comp_combined.csv from PDFs + Excel |
| `build_afr_admin_pool.py` | Script to build afr_admin_pool_summary.csv from AFR Excel files |
| `build_admin_growth_final_charts.py` | Script to build all Plotly HTML charts |
| `admin-growth-final.md` | Main analysis page (Jekyll/Just the Docs) |
| `admin-growth-faq.md` | FAQ page |

**Staff directory (separate repo):** `C:\Users\jkarlin\Documents\Code\github_files\D65\district65_staff_complete.csv`
Columns: name, title, location, department, phone, extension, email (1,448 rows)

**Excel source for PA data:** `C:\Users\jkarlin\Downloads\Copy of D65 Comp.xlsx`
Sheets: SY2015-16-Admin, SY2015-16 IMRF, SY2016-Princpals, SY22-Admin through SY26-Admin, SY22-Principals through SY26-Principals, SY22-IMRF through SY26-IMRF

---

## 17. Methodology Notes

- **Year labels** show the ending school year (2026 = SY2025-26 = FY26)
- **Total Compensation (PA)** = Base Salary + TRS/Retirement + Bonus + Health/Dental/Life/Vision Insurance + Car Allowance + Retirement Annuity + Sick/Vacation Payout
- **Total Compensation (AFR)** = Salaries (object 100) + Benefits (object 200) + MR/SS pension by function
- **CPI-indexed threshold** anchored at $75K in 2016 → ~$103K in 2026. Conservative: earlier anchor year would show larger growth.
- **TRS Admin is threshold-independent:** PA 96-0434 reports all TRS administrators regardless of salary. The "11 to 24" trend is a clean count.
- **Right-sizing per-cut: $129,489** = District's own figure ($8,287,312 ÷ 64 positions)
- **SY2020-21 data quality:** Health Insurance column rendered as "#######" in source PDF (Excel column-too-narrow artifact). Total comp slightly undercounted for that year.
- **Peer district benchmark:** ~12 admin per 1,000 students (from Gavin's RoundTable analysis of 21 nearby K-8 districts)

---

## 18. Key People

| Name | Role | Notes |
|------|------|-------|
| Dr. Angel Turner | Superintendent | $260K base, $286K total comp |
| Tamara Mitchell | CFO/CSBO | $217K base, $260K total comp; presented SDRP financial models |
| Dr. Stacy Beardsley | Asst Supt of Accountability | |
| Dr. Kathleen Speth | Asst Supt of Academics | |
| Larry Gavin | Independent journalist | RoundTable; primary external validator of admin growth data |
| Tom Hayden | FOIA Gras founder | Indexes D65 board documents; blog posts analyzing D65 spending |
| Maria Opdycke | Board member | Sole dissent on BriteLift transport contract (6-1 vote) |

---

## 19. Common Misunderstandings

1. **"22 administrators" ≠ 22 of the 24 TRS Admin.** The District uses "administrator" broadly (likely ECMA bargaining unit members). Against ~62 central admin (Gavin), 22 = ~35%.

2. **The $103K threshold applies only to headcount trend charts**, not to the dollar analysis, the TRS Admin count, or the right-sizing proposals.

3. **IMRF counts include operational staff**, not just administrators. IMRF Support Staff includes head custodians, nutrition services managers, IT staff, etc. alongside directors and managers.

4. **Per-person compensation has NOT grown beyond inflation.** The cost growth is from adding positions, not from raises.

5. **The Legion's right-sizing proposals are all SMALLER than the District's own proposal.** The District identified $8.3M; the Legion's most aggressive scenario is $4.9M.

6. **School closures and admin right-sizing are independent levers.** The District's admin proposal ($8.3M) is larger than both Kingsley + Lincolnwood closures combined ($3.24M).

7. **Principal headcount has declined** (34 → 28). The growth is entirely in central-office roles.

---

## 20. Legion of Data Nerds

- **Website:** https://d65-legionofnerds.github.io
- **GitHub:** https://github.com/d65-legionofnerds
- **Email:** d65.legionofnerds@gmail.com
- **Site framework:** Jekyll with Just the Docs theme
- **Repo location:** `C:\Users\jkarlin\Documents\Code\nerds_site\d65-legionofnerds.github.io`
