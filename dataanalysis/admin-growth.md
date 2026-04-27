---
title: Administrative Growth Over Time
layout: default
parent: Data Analysis
---

# District 65 Administrative Growth Over Time

## Overview

Over the past decade, District 65 has dramatically expanded its administrative workforce while serving a shrinking student population. This page tracks the size and cost of the District 65 administration from school year 2015-16 through 2025-26 using compensation data from the District's annual public salary disclosures (Public Acts 96-0434 and 97-0609).

The headline finding: between SY2015-16 and SY2025-26, **D65's administrative headcount roughly doubled (75 → 153)** while **K-8 enrollment fell from approximately 7,500 to 5,700 students (a 24% decline)**. Total administrative compensation rose from about $10M to $20M (nominal dollars).

### Categories Used

- **TRS Admin** *(red)* — Certificated administrators reported under PA 96-0434 (superintendents, assistant superintendents, directors, executive directors). These are typically salaried under the Teachers' Retirement System.
- **IMRF Support Staff** *(blue)* — Non-certificated administrative and support staff earning over $75,000, reported under PA 97-0609. Salaried through the Illinois Municipal Retirement Fund.
- **Principals** *(green)* — Principals and assistant principals (extracted from the same PA 96-0434 reports as TRS Admin but tracked separately for clarity).

All compensation figures are **nominal dollars** (not adjusted for inflation) and represent **total compensation** including base salary, retirement contributions, health/dental/life insurance, car allowance, retirement annuities, and sick/vacation payouts.

---

## Headcount Growth

### Total Administrative Staff Over Time

<iframe src="assets/admin_growth_headcount_stacked.html" width="100%" height="600" frameborder="0"></iframe>

The total number of administrators (across all three categories) has increased substantially since SY2015-16. Most of the growth has come from the IMRF Support Staff and TRS Admin categories. Note that some apparent year-over-year volatility between the TRS Admin and IMRF categories reflects positions being reclassified between the two funding sources rather than net hires or losses — focus on the total stack height for the underlying trend.

### Headcount Per 1,000 Students

<iframe src="assets/admin_growth_headcount_per_1000.html" width="100%" height="600" frameborder="0"></iframe>

This is the most important headcount chart. Because student enrollment has been declining sharply over the same period, the ratio of administrators to students has grown even faster than the raw headcount. The combined "All Categories" line (dashed black) shows the most striking trend: administrators per 1,000 students has nearly tripled over the decade.

### Headcount by Category (Direct Comparison)

<iframe src="assets/admin_growth_headcount_lines.html" width="100%" height="600" frameborder="0"></iframe>

The same data shown as separate lines (rather than stacked) makes it easier to see the trajectory of each category individually.

---

## Compensation Growth

### Total Administrative Compensation Over Time

<iframe src="assets/admin_growth_comp_stacked.html" width="100%" height="600" frameborder="0"></iframe>

Total annual compensation paid to D65 administrators (all three categories combined) has roughly doubled in nominal dollars since SY2015-16, growing from about $10M to $20M.

### Compensation per 1,000 Students

<iframe src="assets/admin_growth_comp_per_1000.html" width="100%" height="600" frameborder="0"></iframe>

Normalized by enrollment, the picture is even more dramatic. Per 1,000 students, total administrative compensation has grown from roughly $1.3M to $3.5M — an increase of more than 160%.

### Average Compensation per Administrator

<iframe src="assets/admin_growth_avg_comp.html" width="100%" height="600" frameborder="0"></iframe>

Per-person average compensation has also grown across all three categories, though more modestly than the headcount-driven totals. This reflects standard cost-of-living and step increases over the decade.

### What's Driving TRS Admin Cost Growth?

<iframe src="assets/admin_growth_comp_breakdown.html" width="100%" height="600" frameborder="0"></iframe>

Breaking the central-office TRS Admin total into its components — base salary, retirement (TRS) contribution, and benefits (health, dental, life, vision, car, annuities) — shows that growth is roughly proportional across components rather than concentrated in any single category like benefits or retirement.

---

## Decoupling: Costs vs. Enrollment

### Year-over-Year % Change

<iframe src="assets/admin_growth_yoy_decoupling.html" width="100%" height="600" frameborder="0"></iframe>

This chart juxtaposes the year-over-year percentage change in three series: total administrative compensation (red), administrative headcount (purple), and student enrollment (green). In a financially stable district, you would expect these lines to roughly track each other — when enrollment grows, costs grow proportionally; when enrollment shrinks, costs decline. Instead, D65's enrollment line has been consistently negative since 2019 while admin cost and headcount lines have remained positive, often by double digits.

### Annual Change in Administrative Compensation

<iframe src="assets/admin_growth_waterfall.html" width="100%" height="650" frameborder="0"></iframe>

This chart shows how much total administrative compensation changed each year compared to the prior year. Red bars are increases, green bars are decreases. The starting and ending totals are annotated at the bottom corners — total compensation roughly doubled over the decade.

---

## Cabinet & Senior Leadership

### Compensation Trajectories of Cabinet & Senior Staff

<iframe src="assets/admin_growth_cabinet_trajectory.html" width="100%" height="750" frameborder="0"></iframe>

The 10 most-frequently-appearing cabinet and senior leadership positions in the dataset, plotted across all years they appear. Hover over any line to see exact compensation by year.

### Top 15 Highest-Paid Administrators in SY2025-26

<iframe src="assets/admin_growth_top_paid.html" width="100%" height="800" frameborder="0"></iframe>

The 15 highest-paid administrators in the most recent year (SY2025-26), sorted from highest to lowest. The diamond markers show what the same individuals were paid in SY2021-22 (4 years earlier), where they appear in that year's data, allowing you to see compensation growth at the individual level.

---

## Methodology Notes

- **Data sources**: SY2015-16 and SY2021-22 through SY2025-26 are taken from a compensation workbook compiled from D65 board meeting documents on [foiagras](https://foiagras.com). SY2016-17 through SY2020-21 (the gap years) were backfilled from the original PA 96-0434 and PA 97-0609 reports submitted to the D65 Board of Education each September, also available on foiagras.
- **Year labels** show the *ending* school year (e.g., 2026 = SY2025-26).
- **Total Compensation** = Base Salary + TRS/Retirement contribution + Bonus + Health Insurance + Dental Insurance + Life Insurance + Vision Insurance (where reported) + Car Allowance + Retirement Annuity + Sick/Vacation Payout.
- **PA 097-0609 (IMRF) reports include only employees earning $75,000 or more**, so the IMRF Support Staff totals systematically *under-count* lower-paid administrative staff (e.g., entry-level coordinators, assistants). Year-over-year comparisons are valid because the same threshold applies in every year.
- **Some staff appear to move between TRS Admin and IMRF Support Staff categories** across years as positions are reclassified for funding purposes. For year-over-year *category-level* comparisons, the total combined stack is more meaningful than individual category trends.
- **Principals are tracked separately** from TRS Admin even though they appear in the same PA 96-0434 reports, because principals fill a distinctly different operational role from central-office administration.
- **The SY2020-21 PDF** rendered the Health Insurance column as "#######" (an Excel column-too-narrow rendering artifact in the source PDF). This causes Total Comp to be slightly under-counted for that year only.
- **Enrollment** for years not present in the website's existing enrollment dataset (SY2015-16, SY2016-17, SY2025-26) is sourced from the District's annual *Opening of Schools* reports on foiagras. The SY2025-26 enrollment is an extrapolation from the established declining trend (the official Opening of Schools report for SY2025-26 was not yet posted on foiagras as of April 2026).
- All dollar figures are **nominal** (not inflation-adjusted).

---

## Implications

This page presents the data without prescribing a policy response, but a few observations are unavoidable:

1. **The administrative headcount-to-student ratio in D65 has grown to levels that are difficult to justify by ordinary cost-of-doing-business pressures.** Other peer districts of similar or larger size operate with substantially leaner administrative structures (see the [Salary Data](salary-data.html) page for peer comparisons).

2. **The continued addition of administrative positions during a period of significant enrollment decline** suggests that hiring decisions have not been responsive to the underlying scale of operations.

3. **As the District faces well-documented financial difficulties**, the size and growth trajectory of the administrative workforce is a natural area for scrutiny when evaluating budget reduction options.

The Legion of Data Nerds publishes this data to inform public discussion. We encourage residents, board members, and District leadership to consider it alongside other operational and educational priorities.

---

## Acknowledgements

This analysis was prepared by the Legion of Data Nerds with the assistance of [Claude.ai](https://claude.ai) (Anthropic), which helped with extracting and reconciling data across the multi-year compensation reports, building the visualization pipeline, and drafting this page. All source data is from public District 65 board meeting documents indexed on [foiagras](https://foiagras.com); all editorial decisions, methodology choices, and conclusions are the authors'.

*Underlying CSV data is available at [data/d65_admin_comp_combined.csv](data/d65_admin_comp_combined.csv). Source PDFs are saved to [data/d65_admin_comp_pdfs/](data/d65_admin_comp_pdfs/). Build scripts for the dataset and visualizations are in [build_admin_growth_data.py](build_admin_growth_data.py) and [build_admin_growth_charts.py](build_admin_growth_charts.py).*
