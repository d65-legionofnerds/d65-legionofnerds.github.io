---
title: Did the Kingsley and Bessie Rhodes closures save money?
layout: default
nav_exclude: true
search_exclude: true
noindex: true
sitemap: false
---

# Did closing Kingsley and Bessie Rhodes save money?

*DRAFT. District 65 closed both schools after SY2025-26 and projected about **$2.9M a year** in savings across 17 budget lines. The district does not report costs by school, so we tracked each of those 17 lines in the monthly Treasurer's reports and compared FY27 (2026-27) against FY26 (2025-26, schools open) and FY25. Reports through September 2026 (3 of 12 months) are included.*

## The short answer

**It is too early to prove the savings, and the budget shows only part of what was projected.** Across the 8 line items where the budget lines are clean enough to read, roughly **24%-52%** of the projected savings is visible in the FY27 budget once we account for raises and inflation. The other 9 lines are too noisy to judge: insurance, electricity, gas and water are driven by prices and by the new Foster School, and others rose for reasons the reports do not give.

<iframe src="assets/closure_headline.html" width="100%" height="500" frameborder="0"></iframe>

## Line by line

Hover over any dot for the numbers behind it. A hollow dot means we do not trust that budget line as a measure of the closures.

<iframe src="assets/closure_scorecard.html" width="100%" height="1030" frameborder="0"></iframe>

## Is spending actually running lower?

Budgets are plans. Spending is the evidence. Only July-September 2026 has been reported, mostly summer months with no school in session, so this chart is mostly empty on purpose. It fills in each month, and the winter heating bills and the October-June payroll are the real test. FY25 is shown in light gray so you can see how much these lines normally move from year to year.

<iframe src="assets/closure_monthly.html" width="100%" height="720" frameborder="0"></iframe>

## How the savings number has changed

<iframe src="assets/closure_promise.html" width="100%" height="540" frameborder="0"></iframe>

*Kingsley only. The 2025 scenarios were presented "in addition to the Board approved closure of Bessie Rhodes." The Oct 2026 file does not itemize the other levers, so part of the drop from $1.66M to $1.56M is missing detail, not a lower estimate. Staff figures in the 2025 models include benefits; the tracker's staff lines are salary objects only.*

## How we corrected for raises and inflation

A line item can look "flat" in FY27 and still hide a saving, because everything else got more expensive. For each line we ask: **if the schools had stayed open, what would FY27 spending plausibly be?** We start from FY26 actual spending, when both schools were open all year, and grow it by a range:

| Type of line | Low end | High end | Source |
|---|---|---|---|
| Salary lines | +3.1% | +6.0% | Low: FY27 salary budget ($113.8M) vs FY26 budget ($110.4M), which is already net of the budgeted cuts, so it is a floor. High: the 4-6% raises budgeted for FY26. FY27 raises by union are not in the documents we found. |
| Everything else | +2.2% (CPI) | That line's own FY25-to-FY26 growth, floored at CPI and capped at 15% | CPI forecast in the Legion's data; FY25 and FY26 are both years the schools were open. |

Estimated savings = that expected FY27 cost minus the FY27 budget. Because the growth rate is a range, the answer is a range.

## What this cannot tell you

- **Budget is not spending.** FY27 figures are the budget adopted in the September 2026 report, not what has been spent.
- **No school-level costs.** The reports are by fund and object, so each projected item is matched to the closest district-wide line. Moves that happen to land on the same line (such as raises) cannot be separated from the closures.
- **Foster School opened in FY27.** Bessie Rhodes students moved into it, so the new building's staff, utilities, custodians and insurance sit on the same district-wide lines. The district's own 2025 model credited Foster with only $50K of net savings.
- **Closed buildings still cost money until they are sold.** In June 2026 the Board reached a general consensus (no formal vote) to sell both properties, and neither is sold. Insurance and some maintenance continue.
- **The district's budget already assumes the cuts.** The FY27 budget memo states it reflects "$6.3 million in expenditure reductions," including staffing reductions and school closures. Comparing budget to budget measures what the district planned, not what happens.
- **Not every projected saving is on these lines.** The 2025 models also counted transportation, fewer class sections and leases. The tracker does not.

## Sources

- Monthly Treasurer's financial reports, July 2024 through September 2026 (District 65, via FOIAgras). Months with no line-item report (March and May 2025) were derived from year-to-date differences.
- FY27 Final Budget Memo and FY27 Tentative Budget Memo (Sept 28 and Aug 31, 2026); FY26 Budget Workbook (Sept 29, 2025).
- SDRP Phase III scenario presentations (Sept 29 and Nov 17, 2025) and the Dec 1, 2025 scenario modeling memo.
- District closure projections (Oct 7, 2026), as loaded in the Legion savings tracker built by Scot.

*Data and code: `closure_savings/` (`export_tracker.py`, `assemble_fy25.py`, `normalize.py`, `build_closure_charts.py`).*
