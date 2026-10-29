"""
Normalizes the closure-savings tracker for raises and inflation.

Question answered per line item: "If Kingsley and Bessie Rhodes had stayed open, what
would FY27 spending on this line plausibly be, and how far below that is the FY27 budget?"

    expected FY27 (no closures) = FY26 actual x (1 + g)
    normalized savings          = expected FY27 - FY27 budget (latest report)

g is a RANGE, never a point, and every input is documented below. FY26 is the baseline
because both buildings were open all year (FY26 actuals contain no closure effect).

Reads  data/source_lines.csv       FY26 + FY27 reports (the tracker's Source Lines sheet)
       data/fy25_source_lines.csv  FY25 baseline (assemble_fy25.py)
       data/projections.csv        district's projected savings per item (tracker)
Writes data/normalized.csv, data/monthly.csv
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent / "data"

# ---- growth assumptions (all sourced; see README for the citations) ---------------------
# Personnel: no FY27 per-bargaining-unit raise was found in FOIAgras. Range is
#   low  = +3.1%  FY27 salary budget ($113.8M) vs FY26 salary budget ($110.4M)  [docs 23995, 4116]
#          (a FLOOR: that growth is already net of the budgeted reductions)
#   high = +6.0%  top of the 4-6% raise range the district budgeted for FY26     [doc 4116]
PERSONNEL_G = (0.031, 0.060)
# Non-personnel: low = CPI-U 2.2% (the site's own forecast, dataanalysis/data/cpi_history.csv);
#   high = the line's own FY25->FY26 growth when the buildings were open (closure-free),
#   floored at CPI and capped at +15% so one lumpy year cannot dominate.
CPI = 0.022
HIGH_CAP = 0.15

# Lines whose FY27 price is driven by something we cannot see (rate shocks, a new building,
# an unexplained budget jump): their normalized savings are shown but flagged low-confidence
# and left out of the headline total.
LOW_CONFIDENCE = {
    "Insurance": "Premium set by the insurance market; a closed building still needs property cover until sold.",
    "Electricity": "Rates and weather dominate; Foster School is a new building on the same line.",
    "Natural gas": "Rates and weather dominate; the heating season has not started.",
    "Water": "Billed irregularly; Foster School is a new building on the same line.",
    "Interventionist": "FY27 budget rose for reasons the reports do not give.",
    "Nutrition": "FY27 budget rose sharply for reasons the reports do not give.",
    "Discretionary supplies": "School-level allocations are not reported; district-wide proxy.",
    "Phone/WAN, security, BAS": "Closest available lines; building automation is not broken out.",
    "Custodial supplies": "Bulk purchases make the budget a poor guide; judge on full-year actual.",
}

fy2627 = pd.read_csv(DATA / "source_lines.csv", dtype={"fund": str, "obj": str})
fy25 = pd.read_csv(DATA / "fy25_source_lines.csv", dtype={"fund": str, "obj": str})
proj = pd.read_csv(DATA / "projections.csv")
cats = proj["category"].tolist()

# ---- monthly series by category, three fiscal years --------------------------------------
m26 = fy2627.groupby(["category", "fy", "fiscal_month"], as_index=False)["month_expended"].sum()
m25 = fy25.assign(fy=25).groupby(["category", "fy", "fiscal_month"], as_index=False)["month_expended"].sum()
monthly = pd.concat([m25, m26], ignore_index=True)
monthly = monthly[monthly["category"].isin(cats)]
reported27 = sorted(fy2627[fy2627.fy == 27].fiscal_month.unique())
monthly = monthly[(monthly.fy != 27) | monthly.fiscal_month.isin(reported27)]
monthly.to_csv(DATA / "monthly.csv", index=False)
n27 = len(reported27)

# ---- per-category annual figures ----------------------------------------------------------
def budget_in(fy, month):
    s = fy2627[(fy2627.fy == fy) & (fy2627.fiscal_month == month)]
    return s.groupby("category")["budget_in_report"].sum()

b26 = budget_in(26, 12)                    # FY26 final budget (Jun 2026 report)
b27 = budget_in(27, max(reported27))       # FY27 budget, latest report
a26 = fy2627[fy2627.fy == 26].groupby("category")["month_expended"].sum()
a25 = fy25.groupby("category")["month_expended"].sum()
ytd27 = fy2627[(fy2627.fy == 27)].groupby("category")["month_expended"].sum()
ytd26 = fy2627[(fy2627.fy == 26) & (fy2627.fiscal_month <= n27)].groupby("category")["month_expended"].sum()

rows = []
for _, p in proj.iterrows():
    c = p["category"]
    personnel = p["kind"] == "Personnel"
    g25_26 = a26[c] / a25[c] - 1 if a25.get(c, 0) > 0 else float("nan")
    if personnel:
        g_lo, g_hi = PERSONNEL_G
    else:
        g_lo = CPI
        g_hi = min(HIGH_CAP, max(CPI, g25_26)) if pd.notna(g25_26) else CPI
    exp_lo, exp_hi = a26[c] * (1 + g_lo), a26[c] * (1 + g_hi)
    sav_lo, sav_hi = exp_lo - b27[c], exp_hi - b27[c]
    mid = (sav_lo + sav_hi) / 2
    ratio = mid / p["combined"]
    if ratio >= 0.75:
        verdict = "On track or better"
    elif ratio >= 0.25:
        verdict = "Partly there"
    elif ratio > -0.10:
        verdict = "No sign yet"
    else:
        verdict = "Costs went up"
    rows.append(dict(
        category=c, kind=p["kind"], proxy=p["proxy"],
        proj_kingsley=p["kingsley"], proj_rhodes=p["rhodes"], projected=p["combined"],
        fy25_actual=a25.get(c), fy26_actual=a26[c], fy26_budget=b26[c], fy27_budget=b27[c],
        fy25_to_fy26_pct=g25_26, g_lo=g_lo, g_hi=g_hi,
        expected_lo=exp_lo, expected_hi=exp_hi,
        raw_savings=b26[c] - b27[c],            # tracker's budget-implied number
        norm_savings_lo=min(sav_lo, sav_hi), norm_savings_hi=max(sav_lo, sav_hi), norm_savings_mid=mid,
        share_of_projection=ratio, verdict=verdict,
        confidence="Low" if c in LOW_CONFIDENCE else "Higher",
        confidence_reason=LOW_CONFIDENCE.get(c, "Dedicated budget lines with few other drivers."),
        ytd27=ytd27.get(c, 0), ytd26=ytd26.get(c, 0),
    ))
out = pd.DataFrame(rows)
out.to_csv(DATA / "normalized.csv", index=False)

# ---- headline totals -----------------------------------------------------------------------
def tot(df, col):
    return df[col].sum()
hi_conf = out[out.confidence == "Higher"]
print(f"FY27 months reported: {n27}")
print(f"projected savings, all 17 items: {tot(out, 'projected'):,.0f}")
print(f"raw budget-implied (tracker):    {tot(out, 'raw_savings'):,.0f}")
print(f"normalized, all items:           {tot(out, 'norm_savings_lo'):,.0f} to {tot(out, 'norm_savings_hi'):,.0f}")
print(f"normalized, higher-confidence:   {tot(hi_conf, 'norm_savings_lo'):,.0f} to {tot(hi_conf, 'norm_savings_hi'):,.0f} "
      f"(projected for those items: {tot(hi_conf, 'projected'):,.0f})")
print(out[["category", "projected", "raw_savings", "norm_savings_lo", "norm_savings_hi", "verdict", "confidence"]]
      .round(0).to_string(index=False))
