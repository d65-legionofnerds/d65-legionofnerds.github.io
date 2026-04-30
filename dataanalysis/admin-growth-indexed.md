---
title: Admin Growth (Indexed)
layout: default
nav_exclude: true
search_exclude: true
noindex: true
sitemap: false
---

# District 65 Administrative Growth Over Time — Inflation-Indexed Threshold

*This page is the **strict apples-to-apples academic version** of the Legion's admin growth analysis. It applies a CPI-indexed threshold throughout, using only PA public-disclosure data. For the publication-candidate version that combines this CPI-indexed PA analysis with AFR (Annual Financial Report) data to capture admin compensation below $75K, see [Admin Growth (publication candidate)](admin-growth-final.html). For the original analysis using the unindexed $75,000 PA threshold, see [Admin Growth (unindexed)](admin-growth.html).*

## Overview

Public Act 97-0609 requires Illinois school districts to report compensation data for IMRF-participating employees whose total compensation package (salary plus benefits) exceeds **$75,000**. That threshold has not been adjusted for inflation since the statute took effect — meaning that as compensation packages rise with inflation, more employees mechanically cross the threshold each year even when the underlying workforce is unchanged.

This page applies a **CPI-indexed threshold anchored at 2016**: the $75,000 line is inflated each year using BLS CPI-U so that the comparison is consistent in real-dollar terms across years. In 2016 the threshold is $75,000; in 2026 it is approximately **$103,000**. We then count only D65 administrators and support staff whose compensation package exceeded that year-specific indexed threshold.

The headline findings between SY2015-16 and SY2025-26, while K-8 enrollment fell from approximately 7,500 to 5,625 students (a 25% decline):

- **Indexed-eligible administrative headcount grew from 75 to 94 (+25%)**
- **Per-pupil density rose from 10 to 17 administrators per 1,000 students (+67%)**
- **Real per-student spending on indexed-eligible admin rose from $1,851 to $2,640 (+43%)**
- **TRS Admin (the certificated central-office category) more than doubled, 11 → 24 (+118%)** — this signal is independent of the threshold framework
- **Real total comp of indexed-eligible admin grew only $13.9M → $14.8M (+6.7%) — but real avg comp per administrator *fell* from $185K to $158K (-15%)**, indicating the buildup added mid-tier rather than top-tier positions

*All dollar figures on this page are inflation-adjusted to 2026 dollars (BLS CPI-U, US city average).*

We detail the administrative growth below, but first we want to emphasize the savings opportunity presented by right-sizing administration to D65's previously lean levels. The orange bar shows the District's own April 20, 2026 admin-cut proposal — $8.3M in identified savings from 22 administrators and 42 non-union support positions, presented 19 days after the deadline that would have made it actionable for FY27. The red bars show three Legion right-sizing scenarios computed under the indexed framework. The District's proposal sits *above* all three Legion scenarios because the District's math is sized on actual workforce average, including the sub-indexed admin we exclude here.

<iframe src="assets/admin_growth_indexed_right_sizing_comparison.html" width="100%" height="860" frameborder="0"></iframe>

---

## What this analysis includes — and what it excludes

The CPI-indexed threshold is the right tool for measuring how *higher-paid* administrative staffing levels have changed over time on an apples-to-apples basis. But it has a deliberate limitation that readers should understand before evaluating the cost-cutting implications.

**What is included.** This page counts D65 administrators and support staff whose total compensation package — salary plus benefits — met or exceeded the year-specific inflation-adjusted equivalent of $75,000-2016. In 2026, that threshold is approximately $103,000. **94 D65 administrators and support staff met that bar in 2026.**

**What is excluded.** D65 also employs **59 additional administrators and support staff** (in 2026) whose total compensation package falls between the original $75,000 reporting threshold and the inflation-adjusted equivalent of $103,000. These are real D65 employees doing real D65 work, and their combined real compensation in 2026 was approximately **$5.2 million**. Cuts to these positions would also produce real budget savings — but they are not counted in the headline numbers on this page because they fall below our apples-to-apples bar.

**Why this matters for the cost-cutting case.** A reader who only sees this page might conclude that the universe of cuttable admin compensation is just the $14.85M of indexed-eligible spending. That undercounts the actual cuttable pool by roughly $5.2M. The empirical resolution comes from the District itself: the **April 20, 2026 SDRP Phase III deck identifies $8.3M in admin cuts as available** — sized at the actual workforce average ($129K per position × 64 positions) and therefore implicitly including the sub-indexed admin. So the District's own number is the empirical anchor for "what could you save if you also cut the admin we're excluding from the trend analysis here."

**Where this leaves the reader:** The indexed framework is the right tool for *trend rigor* (was administrative staffing actually expanding faster than enrollment, in apples-to-apples terms?). The District's own $8.3M is the right anchor for *policy maximum-savings analysis* (how much could be cut if you treat the full workforce as cuttable?). Both are honest statements of what the data shows.

---

## Methodology — the 2016 anchor and what it implies

The CPI-indexed threshold requires a base year. We use **2016** because:

- It is the start of our administrator compensation dataset.
- It pre-dates the Horton/MIRACLES central-office expansion (2020 onward).
- It pre-dates the SY22-23 surge in IMRF Support Staff headcount.

The 2016 anchor is *one* defensible choice. Other anchors would yield different magnitudes:

- **Anchor at 2011 (statute year).** The $75,000 threshold has been static since PA-97-0609 took effect. Anchoring at 2011 would yield a higher 2016-equivalent threshold (roughly $80,000 in 2016 dollars), capturing fewer 2016 admins. The growth to 2026 would *appear larger* under that anchor.
- **Anchor at 2019 (pre-COVID).** The 2019 threshold in 2026 dollars would be lower than the 2016-anchored equivalent, capturing more 2026 admins. The growth would *appear smaller* under that anchor.

The 2016 choice is therefore conservative relative to the statute-year alternative — it minimizes apparent growth. We disclose this so readers can evaluate the methodological choice.

For the dollar figures on this page, we use real (2026) dollars throughout. The CPI-U series and per-year thresholds are stored in [data/cpi_history.csv](data/cpi_history.csv).

---

### Categories Used

D65 reports administrative staff under two state public-disclosure laws, plus a separate principal track. The same three categories appear here as on the [unindexed page](admin-growth.html); the only difference is that this page filters each category to roster members whose comp package exceeds the year-specific indexed threshold.

- **TRS Admin** *(red)* — Certificated administrators reported under PA 96-0434: superintendent, assistant superintendents, executive directors, directors (Curriculum & Instruction, MTSS & SEL, STEAM, Multilingual Services, Climate & Safety, Programs & Partnerships, etc.), and supervisors. Salaried under the Teachers' Retirement System. TRS Admin compensation is reported in full regardless of the $75K threshold; under the indexed framework, only one TRS Admin (in 2024) falls below the year-specific cutoff. The TRS Admin trend is therefore essentially identical between the unindexed and indexed views.

- **IMRF Support Staff** *(blue)* — IMRF Support Staff are D65 employees who participate in the Illinois Municipal Retirement Fund. This is non-certificated, IMRF-participating administrative and support staff whose compensation package (salary plus benefits) exceeds the year-specific indexed threshold. The IMRF category is the most sensitive to the choice of threshold framework, because PA-97-0609 only reports IMRF members above $75,000 to begin with.

- **Principals** *(green)* — Principals and assistant principals (extracted from the same PA 96-0434 reports as TRS Admin but tracked separately because they fill a distinctly school-level operational role). Principal compensation virtually always exceeds the indexed threshold; this category is essentially unchanged versus the unindexed view.

- **Not included.** As on the [companion page](admin-growth.html), these data do not include paraprofessionals, school counselors, or librarians.

---

## Headcount Growth

### Indexed-Eligible Administrative Staff Over Time

<iframe src="assets/admin_growth_indexed_headcount_stacked.html" width="100%" height="600" frameborder="0"></iframe>

Indexed-eligible admin headcount rose from 75 in SY2015-16 to 94 in SY2025-26 — a 25% increase over a decade in which K-8 enrollment fell 25%. Most of the year-to-year volatility between TRS Admin and IMRF Support Staff reflects positions being reclassified between funding sources rather than net hires or losses (the SY22-23 → SY23-24 transition is the largest example of this; about 11 IMRF Support Staff appear to have been reclassified into TRS Admin that year).

### Indexed-Eligible Headcount Per 1,000 Students

<iframe src="assets/admin_growth_indexed_headcount_per_1000.html" width="100%" height="600" frameborder="0"></iframe>

This is the most consequential headcount chart on this page. Even after restricting to apples-to-apples indexed-eligible administrators, **per-pupil density rose from 10.0 to 16.7 per 1,000 students between 2016 and 2026 — a 67% increase**. The combined "All Categories" line (dashed black) shows that this is true across the full administrative workforce, not concentrated in any single category. By comparison, peer K-8 districts in the surrounding area cluster around 12 per 1,000 students.

### Indexed-Eligible Headcount by Category (Direct Comparison)

<iframe src="assets/admin_growth_indexed_headcount_lines.html" width="100%" height="600" frameborder="0"></iframe>

Same data as the stacked chart, shown as separate lines so each category's trajectory is visible individually. Note that TRS Admin doubled from 11 to 24 — a clean signal that doesn't depend on the threshold framework, because TRS Admin is reported in full under PA 96-0434 regardless of the $75K rule.

---

## Compensation Growth

### Total Real Compensation of Indexed-Eligible Admin

<iframe src="assets/admin_growth_indexed_comp_stacked.html" width="100%" height="600" frameborder="0"></iframe>

Total real compensation paid to *indexed-eligible* administrators rose from approximately $13.9M in SY2015-16 to $14.8M in SY2025-26 — a real increase of only **+6.7%**. This is dramatically smaller than the 44% real growth visible on the unindexed page, and the difference (~$5.2M) is the real compensation of the 59 admin/support staff who fall between the fixed $75K threshold and the inflation-adjusted equivalent in 2026 (i.e., the drift-into-threshold workforce that an apples-to-apples comparison must exclude).

**This is the trade-off in plain numbers.** The indexed framework gives a more conservative cost story over the decade because the comparison is apples-to-apples. The fixed-threshold view gives a larger cost story because it includes drift-into-threshold staff. Neither number is wrong; they answer different questions.

### Real Compensation per 1,000 Students

<iframe src="assets/admin_growth_indexed_comp_per_1000.html" width="100%" height="600" frameborder="0"></iframe>

Normalizing by enrollment tells a sharper story than total compensation alone. Even on the conservative indexed-eligible basis, **real per-student spending on higher-paid admin grew from approximately $1,851 to $2,640 — a 43% real increase per student over the decade.** The mechanism is straightforward: real total cost rose modestly (6.7%) while enrollment fell substantially (25%), so per-student cost rose substantially even after adjusting for inflation.

### Average Compensation per Administrator vs. 2016 Real Baseline

<iframe src="assets/admin_growth_indexed_avg_comp.html" width="100%" height="600" frameborder="0"></iframe>

This chart plots each role-class's average compensation in 2026 dollars against a dotted horizontal line at the 2016 real-dollar baseline. **Most lines stay near or below their 2016 baseline** — meaning per-person compensation has, on average, kept pace with inflation or slightly lost ground. Critically, the indexed-eligible IMRF Support Staff *average comp has fallen substantially in real terms* (from approximately $185K-equivalent in 2016 to $158K-equivalent in 2026, -15%).

The implication is sharper than on the unindexed page: when total real comp of indexed-eligible admin grew 6.7% but per-person real comp dropped 15%, **the new admin positions added during the buildup came in at meaningfully lower comp than the existing average — they are mid-tier roles, not C-suite roles.** The cost growth is driven by adding more positions, and those positions sit just above the inflation-adjusted threshold.

---

## What's Driving TRS Admin Cost Growth?

<iframe src="assets/admin_growth_indexed_comp_breakdown.html" width="100%" height="600" frameborder="0"></iframe>

The TRS Admin total in 2026 dollars, broken into base salary, retirement (TRS) contribution, and benefits (health, dental, life, vision, car, annuities), shows growth roughly proportional across components. The TRS Admin total roughly doubled between 2016 and 2026 in real terms — closely matching the doubling in TRS Admin headcount. As on the unindexed page, this is consistent with the conclusion that TRS Admin cost growth is driven by hiring more administrators rather than by raising existing administrators' pay above inflation.

> **The SY23-24 spike.** The TRS Admin total nearly doubled in SY23-24 because 27 new administrators appear in that year's PA 96-0434 report — about 11 of whom were existing IMRF Support Staff who were reclassified into TRS Admin (Director of College and Career, Director of Science, Diverse Learning Supervisor/Coordinator, Talent Development Coordinator, Executive Director of Technology, etc.). The remaining ~16 were fresh hires. This was the late-Horton peak; SDRP Phase I cuts brought the TRS Admin count back down in SY24-25.

---

## Decoupling: Costs vs. Enrollment

### Year-over-Year % Change

<iframe src="assets/admin_growth_indexed_yoy_decoupling.html" width="100%" height="600" frameborder="0"></iframe>

This chart juxtaposes the year-over-year percentage change in three series: indexed-eligible total administrative compensation in real (2026) dollars (red), indexed-eligible administrative headcount (purple), and student enrollment (green). In a financially stable district you would expect these lines to roughly track each other — when enrollment grows, costs grow proportionally; when enrollment shrinks, costs decline. Instead, D65's enrollment line has been consistently negative since 2019 while real-cost and headcount lines have remained positive in many years, with a substantial single-year jump in SY22-23.

### Annual Change in Indexed-Eligible Administrative Compensation

<iframe src="assets/admin_growth_indexed_waterfall.html" width="100%" height="650" frameborder="0"></iframe>

This chart shows how much real total compensation of indexed-eligible administrators changed each year compared to the prior year. Red bars are increases, green bars are decreases. The starting and ending totals plus the net change appear in the chart subtitle. The largest single-year jump is SY22-23 — Devon Horton's first full year as superintendent — even on the conservative indexed-eligible basis.

---

## IMRF Support Staff: who's actually in this category?

<iframe src="assets/admin_growth_indexed_imrf_categories.html" width="100%" height="650" frameborder="0"></iframe>

This chart breaks the indexed-eligible IMRF Support Staff count down into broad role categories for the two most recent reporting years (SY24-25 and SY25-26). Earlier years are excluded because their IMRF reports either lacked Position strings or used inconsistent terminology that resists reliable bucketing. Note that under the indexed framework the IMRF totals are smaller than on the unindexed page (44 in SY24-25 and 42 in SY25-26 versus 96 and 101 nominally), because the higher real-dollar threshold filters out lower-paid IMRF members. The "Directors / Managers / Coordinators" bucket remains the most administrative-feeling subset.

---

## Comparing Right-Sizing the Admin to the District's Other Cost-Cutting Measures

<iframe src="assets/admin_growth_indexed_right_sizing_comparison.html" width="100%" height="860" frameborder="0"></iframe>

The chart above shows the same recently-enacted and proposed cuts that appear on the [unindexed page](admin-growth.html), recomputed against a set of right-sizing scenarios derived from the indexed framework.

### What's actually happened or been proposed

The school-closure savings figures below use the District's **Dec 1, 2025 revised SDRP III financial model** ([foiagras doc 12033](https://ig.foiagras.com/api/public/chat/documents/12033/view)). See the unindexed page for full per-row sourcing.

- **Layoff of 2 middle-school counselors (April 2026)** — ~$200K. *([FOIA Gras post 264](https://foiagras.com/p/d65-firing-librarians); D65 Board action April 14 2026.)*
- **Reassignment of middle-school librarians (April 2026)** — direct salary savings approximately $0 (reassignment, not termination). *([Post 264](https://foiagras.com/p/d65-firing-librarians) and [post 267](https://foiagras.com/p/firing-librarians-bad-idea-letter).)*
- **Bessie Rhodes K-8 closure** — Modeled annual savings ≈ $1.66M.
- **Kingsley Elementary closure** — Modeled annual savings ≈ $1.83M.
- **Lincolnwood Elementary (conditional trigger)** — Estimated incremental savings ~$1.4–1.6M.
- **2-school closure scenario (revised)** — Total recurring annual savings ~$3.24–3.37M.
- **Decline iPad/keyboard purchase (March 2026, one-time)** — On March 23, 2026 the Board approved a **$528,279 purchase of 1,231 iPads and 1,295 keyboard cases** for SY26-27, ignoring a Screen Sense Evanston petition with 1,200+ signatures urging less screen time. Declining the purchase would have produced a one-time $528,279 savings (shown on the chart at full value, not annual recurring). The District's parallel four-year operational lease (approved Dec 2024) runs $750,966 / 4 years = ~$200K/year on a separate stream. *(Source: [FOIA Gras post 249](https://foiagras.com/p/d65-it-department-spend), [post 255](https://foiagras.com/p/d65-tech-hard-to-unwind), [post 262](https://foiagras.com/p/d65-board-preview-march-23-2026), [post 264](https://foiagras.com/p/d65-firing-librarians); D65 Board action March 23, 2026.)*
- **Choose lowest bidder for special ed transport (KalaJu over BriteLift)** — On December 15, 2025 the Board awarded the special ed transportation contract to BriteLift in a 6-1 vote (Opdycke opposed) at $2.04M annual for 55 routes. KalaJu Elite Fleet's headline bid was approximately $1M lower at $1.04M but **only priced 30 of the 55 routes needed**. CFO Tamara Mitchell stated KalaJu's bid reflected their existing fleet capacity, not the 55 routes required; Tom Hayden's analysis notes nothing in the KalaJu bid explicitly stated this limitation. The chart shows the headline $1M figure; **defensible savings range is ~$143K (linear extrapolation of per-route cost across 55 routes) to ~$1M (headline bid difference)**. *(Source: [FOIA Gras post 253](https://foiagras.com/p/kalaju-protest-letter); D65 Board action December 15, 2025.)*

> **The District's own April 20, 2026 admin-cut proposal — and the missed deadline.** At the April 20, 2026 SDRP Phase III board meeting, the administration's deck identified an additional **$8,287,312 in potential annual savings from eliminating 22 administrators and 42 non-union support positions** (slide 13: *"Items for Analysis – Potential Additional Personnel Reduction Considerations"*). The same slide explicitly notes a contractual deadline of "April 1, 2026 for admin to go into effect for FY27." The proposal was presented **19 days after the deadline that would have made it actionable for FY27**; as a result, these cuts are deferred to FY28 at the earliest. **The District's $8.3M is the largest right-sizing bar in the chart above** because the District sized its proposal at the actual workforce average compensation ($129K/position × 64 positions), implicitly including the sub-indexed admin that this page's apples-to-apples analysis excludes. *(Source: D65 Expenditure Reduction Plan: SDRP Phase 3 Reductions, presented April 20, 2026, slide 13.)*

### What right-sizing the admin would save (indexed framework)

Three reference scenarios, all computed against the **indexed-eligible** workforce (94 administrators in 2026, average real compensation $158K/person):

- **Moderate — return indexed-eligible admin to 2016–2019 baseline (~81 admin, ~13 cuts).** Under this scenario, the indexed-eligible admin workforce would return to the pre-Horton average of 81 administrators (about 14/1k students at current enrollment). Estimated annual savings: **~$2.05M**. This is the most conservative scenario and ties directly to D65's own pre-buildup baseline.
- **Match peer K-8 median (~12/1k students; ~68 admin, ~26 cuts).** Estimated annual savings: **~$4.2M**.
- **Match D65's own SY2015-16 indexed ratio (~10/1k students; ~56 admin, ~38 cuts).** Estimated annual savings: **~$6.0M**.

All three Legion scenarios are smaller than the District's own April 20 proposal of $8.3M. That is not a contradiction — the District's $8.3M is sized at workforce average compensation and includes administrators below the indexed threshold, while the Legion scenarios above use the indexed-eligible average ($158K) and apply only to the indexed-eligible workforce. The empirical takeaway: **on the actual cuttable workforce (the District's own framing), $8.3M of admin cuts is available right now**. On the strict apples-to-apples indexed framework (this page's framing), $2M to $6M of cuts is achievable depending on how aggressive the right-sizing target is.

### Putting these in perspective

The two-counselor layoff saves roughly the cost of a single mid-level administrator position. The librarian reassignments save effectively nothing in dollars. **Closing Bessie Rhodes and Kingsley together (the active 2026 plan) saves about $3.5M annually — comparable to the moderate-to-peer-median Legion scenario** ($2M–$4M) computed strictly on the indexed-eligible framework. Even the conservative indexed scenario is bigger than the entire counselor-layoff savings by an order of magnitude, and **the District's own April 20 proposal is bigger than the largest Legion right-sizing scenario on this page.**

This isn't an argument that the school closures are wrong — there are legitimate facility-utilization and capital-cost reasons to close under-utilized buildings. **It is an argument that the District's current cost-cutting efforts focus heavily on student-facing services while a substantial admin-side savings pool exists, the District itself has identified $8.3M of it, and even on the most conservative apples-to-apples measurement the Legion can construct, several million dollars in annual savings remain accessible.**

---

## What Roles Have Been Added?

The TRS Admin roster in SY25-26 includes a number of senior positions that did not exist in the SY15-16 organization, among them:

- Executive Chief of Communications
- Executive Chief of Human Relations
- Executive Director of RAAD (Research, Assessment, Accountability, and Data)
- Executive Director of Technology
- Director of MTSS & SEL (Multi-Tiered System of Supports & Social-Emotional Learning)
- Director of STEAM (formerly Director of STEM)
- Director of Multilingual Services (formerly Bilingual Coordinator)
- Director of Climate & Safety
- Director of Strategic Projects
- Director of Programs & Partnerships
- Director of Schools Management
- Director of Humanities
- Director of College and Career
- Director of Science
- Asst Director of Teaching & Learning
- Diverse Learning Supervisor / Coordinator
- Talent Development Coordinator
- Special Assistant to Cabinet
- Manager of Student Specialized Services

On the IMRF side, the SY25-26 roster includes newer specialized roles such as Sustainability Coordinator, Wellness Coordinator, Network & Cybersecurity Manager, Substitute Staffing Specialist, Family Center Managing Director, Senior Manager of HR Operations, Culture and Climate Manager, and a Science & Sustainability Education Coordinator.

### Were these additions justified?

This is the harder question. The Legion of Data Nerds doesn't have a definitive answer. In his November 2025 *RoundTable* essay, Larry Gavin flagged several specific role-clusters as candidates for review without endorsement: the **9 IES Coordinators**, multiple positions in the **Human Relations department**, a cluster of **director-level roles** created in recent years (Strategic Projects, Workforce Analytics, Communications), and **assistant principals in small elementary schools** with 300–370 students. We don't have an independent basis for naming specific positions, but we agree these clusters warrant scrutiny.

Several questions would help the public — and the Board — evaluate whether these roles are essential, useful, or expendable:

1. **Was each new role created with a documented business case** that included measurable outcomes the role was supposed to deliver?
2. **Are those outcomes being measured today, and what do the results show?** For example, after creating an Executive Director of RAAD several years ago, has the District's research/assessment/accountability/data work measurably improved? Has student achievement responded?
3. **For roles created during a specific initiative** (e.g., Director of Multilingual Services, Director of MTSS & SEL), what is the evidence that the function would deteriorate if the role were eliminated and the work absorbed elsewhere?
4. **For directors and coordinators** whose work is largely internal coordination, what concrete deliverables changed or new programs launched in the past year that would not have happened without them?
5. **Which of these roles have been previously eliminated and re-created**, and what does that history tell us about whether the function is essential?

The District has not made comprehensive answers to these questions publicly available.

---

## External Validation

Two pieces of independent journalism by Larry Gavin in the *Evanston RoundTable* corroborate the trends documented on this page:

- **Gavin, Larry. "Analysis and Viewpoint: District 65 Has 25% Fewer Students but 10% More Staff. Why?"** *Evanston RoundTable*, March 22, 2026. ([paywall](https://evanstonroundtable.com/2026/03/22/analysis-and-viewpoint-district-65-has-25-fewer-students-but-10-more-staff-why/))
  - D65's −25% enrollment decline since FY 2019 is the steepest among 21 nearby K-8 districts; next-largest decline 14.3%
  - Total district FTEs *increased* by approximately 130 (+10%) over the same period
  - Math IAR proficiency declined from 44.8% (2018) to 42.3% (2024) despite the staffing buildup
  - Cross-referencing all three state disclosure lists yields 62 administrators for FY26 — 10 higher than the 52 the District reported under PA 96-0434 alone — raising the question of how many employees are performing administrative functions without being formally classified as administrators

- **Gavin, Larry. "Guest Essay: District 65 Employees and Enrollment."** *Evanston RoundTable*, November 2, 2025. ([paywall](https://evanstonroundtable.com/2025/11/02/guest-essay-district-65-employees-enrollment/))
  - Earlier independent analysis of the staff-to-enrollment ratio problem
  - Identified specific role-clusters (9 IES Coordinators, Human Relations layers, recent director-level positions, assistant principals in small schools) as candidates for review

The District has separately conceded the magnitude of the available admin savings: the April 20, 2026 SDRP Phase III deck identified $8,287,312 in additional admin/support cuts as available — but presented the proposal 19 days after the contractual deadline that would have made it actionable for FY27.

A reader who wants to verify our data has at least three convergent sources to cross-check: this page, Gavin's RoundTable analyses, and the District's own April 20 admission, all backed by underlying D65 board documents on [foiagras](https://foiagras.com).

---

## Methodology Notes

This page uses identical source data to the [unindexed page](admin-growth.html). The differences are:

- **Threshold filter**: every roster row is filtered to total compensation ≥ the year-specific CPI-indexed equivalent of $75,000-2016 (≈$103,000 in 2026). Under the unindexed page, no inflation adjustment is applied to the threshold — every reported PA-97-0609 row is included.
- **Anchor year**: 2016, the start of the dataset. See the methodology section above for how alternative anchors would shift the figures.
- **Dollar figures**: all in 2026 dollars using BLS CPI-U (US city average). No nominal-vs-real toggles.
- **Right-sizing math**: scenarios use the indexed-eligible workforce in 2026 (94 administrators) and the indexed-eligible average real compensation ($158K). The District's $8.3M proposal is left at $8.3M because that is the District's own number, sized at workforce-wide average comp ($129K × 64 cuts).

Other methodology notes that apply equally to both pages:

- **Total Compensation** = Base Salary + TRS/Retirement contribution + Bonus + Health Insurance + Dental Insurance + Life Insurance + Vision Insurance (where reported) + Car Allowance + Retirement Annuity + Sick/Vacation Payout.
- **Inflation adjustment** uses BLS CPI-U All Urban Consumers (US city average) annual averages, with 2026 as the reporting base year. CPI values are stored in [data/cpi_history.csv](data/cpi_history.csv).
- **PA 097-0609 (IMRF) reports include only IMRF-participating employees whose compensation package (salary plus benefits) exceeds $75,000.** This page's indexed filter is *additionally* applied on top of that legal threshold.
- **Some staff appear to move between TRS Admin and IMRF Support Staff categories** across years as positions are reclassified for funding purposes. The SY22-23 → SY23-24 transition is the most prominent example.
- **Principals are tracked separately** from TRS Admin even though they appear in the same PA 96-0434 reports.
- **The SY2020-21 PDF** rendered the Health Insurance column as "#######" (an Excel column-too-narrow rendering artifact in the source PDF). This causes Total Comp to be slightly under-counted for that year only.
- **Enrollment** for years not present in the website's existing enrollment dataset (SY2015-16, SY2016-17, SY2025-26) is sourced from the District's annual *Opening of Schools* reports on foiagras. The SY2025-26 enrollment is from [D65's Data Dashboard](https://data.district65.net/).

### Cross-reference: D65 staff directory

For a workforce snapshot that does not depend on the comp threshold at all, the D65 staff directory at the time of writing showed approximately 297 staff at the JEH Administrative Center, of whom roughly 100 hold director/manager/coordinator/chief titles. Larry Gavin's March 2026 *Evanston RoundTable* analysis reported a similar cut: 80 administrative-titled employees out of ~200 at JEH. The directory and the PA disclosures use different bases (location vs. funding category, full roster vs. above-threshold), but they are directionally consistent: the central-office workforce at JEH is substantially larger than the 94 indexed-eligible admin counted here.

---

### Companion analyses

- **[Admin Growth (publication candidate)](admin-growth-final.html)** — combines this page's CPI-indexed PA headcount analysis with AFR (Annual Financial Report) data to capture every employee in admin functions regardless of salary, including those below $75K. Right-sizing scenarios use the AFR pool as denominator and the District's own per-cut average ($129K) for direct comparability with the District's $8.3M proposal.
- **[Admin Growth (unindexed)](admin-growth.html)** — original analysis using the unindexed $75,000 PA threshold. Larger headline numbers (153 admin, +104% headcount, $11.2M / $12.7M right-sizing) but more vulnerable to the inflation-drift critique that this page addresses.

---

## Acknowledgements

This analysis was prepared by the Legion of Data Nerds with the assistance of [Claude.ai](https://claude.ai) (Anthropic), which helped with extracting and reconciling data across the multi-year compensation reports, building the visualization pipeline, and drafting this page. All source data is from public District 65 board meeting documents indexed on [foiagras](https://foiagras.com); all editorial decisions, methodology choices, and conclusions are the authors'.

*Underlying CSV data is available at [data/d65_admin_comp_combined.csv](data/d65_admin_comp_combined.csv). Source PDFs are saved to [data/d65_admin_comp_pdfs/](data/d65_admin_comp_pdfs/). The build script for the indexed-framework charts is in [build_admin_growth_indexed_charts.py](build_admin_growth_indexed_charts.py).*
