"""
Builds the visualization suite for the **publication-candidate** D65 admin
growth analysis page (admin-growth-final.md).

This page integrates two complementary data sources:

1. **PA disclosures (96-0434 + 97-0609), CPI-indexed.** Used for headcount
   trend analysis: the only data source that provides year-by-year roster
   counts. The CPI-indexed threshold (anchored at $75K-2016, ≈$103K-2026)
   removes inflation drift so 2016 and 2026 are compared on the same real-
   dollar bar.
2. **AFR (Annual Financial Report, ISBE).** Used for total admin compensation
   pool: function-code aggregates that capture every employee in admin
   functions regardless of salary, including sub-$75K admin support staff
   that the PA disclosures omit. Functions counted: 2300 (General Admin),
   2400 (School Admin), 2500 (Business Services), 2600 (Central Support).

All dollar figures are in 2026 dollars (BLS CPI-U).

Reads:
  - data/d65_admin_comp_combined.csv  (PA disclosure roster)
  - data/afr_admin_pool_summary.csv   (multi-year AFR pool totals)
  - data/d65_enrollment_history.csv
  - data/cpi_history.csv
  - data/d65_recent_cuts.csv

Writes HTML files to assets/admin_growth_final_*.html.
"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

COLORS = {
    "TRS Admin": "#c0392b",
    "IMRF Support Staff": "#2980b9",
    "Principal": "#27ae60",
}
ROLE_ORDER = ["TRS Admin", "IMRF Support Staff", "Principal"]

# AFR function-group colors and order
AFR_COLORS = {
    "2300": "#c0392b",   # General Administration — red
    "2400": "#27ae60",   # School Administration — green (matches Principal)
    "2500": "#34495e",   # Business Services — slate
    "2600": "#2980b9",   # Central Support Services — blue
}
AFR_LABELS = {
    "2300": "General Administration (Supt., Asst Supts, curriculum dirs/coords, board)",
    "2400": "School Administration (principals, asst principals, school office staff)",
    "2500": "Business Services (CFO, fiscal, payroll, business; excludes O&M/transport)",
    "2600": "Central Support Services (planning, IT, staff services, data processing)",
}
AFR_ORDER = ["2300", "2400", "2500", "2600"]

CPI_BASE_YEAR = 2026
CPI_ANCHOR_YEAR = 2016

# ------------------------------------------------------------
# Load and prepare PA-disclosure data (CPI-indexed)
# ------------------------------------------------------------
df_all = pd.read_csv(DATA / "d65_admin_comp_combined.csv")
enroll = pd.read_csv(DATA / "d65_enrollment_history.csv")[["year", "enrollment"]]
cpi    = pd.read_csv(DATA / "cpi_history.csv")[["year", "cpi_u"]]
cuts   = pd.read_csv(DATA / "d65_recent_cuts.csv")
afr    = pd.read_csv(DATA / "afr_admin_pool_summary.csv")

cpi_base   = cpi.loc[cpi["year"] == CPI_BASE_YEAR,   "cpi_u"].iloc[0]
cpi_anchor = cpi.loc[cpi["year"] == CPI_ANCHOR_YEAR, "cpi_u"].iloc[0]
cpi["adj_to_2026"]      = cpi_base / cpi["cpi_u"]
cpi["threshold_indexed"] = 75000 * cpi["cpi_u"] / cpi_anchor

# Indexed-eligible PA roster
df_all = df_all.merge(cpi[["year", "adj_to_2026", "threshold_indexed"]], on="year")
df_all["total_comp_real"] = df_all["total_comp"] * df_all["adj_to_2026"]
df = df_all[df_all["total_comp"] >= df_all["threshold_indexed"]].copy()

# Aggregate per year x role_class (indexed-eligible only)
agg = (df.groupby(["year", "role_class"], as_index=False)
         .agg(headcount=("last_name", "count"),
              total_comp=("total_comp", "sum"),
              total_salary=("total_salary", "sum")))
agg = agg.merge(enroll, on="year", how="left")
agg = agg.merge(cpi[["year", "adj_to_2026"]], on="year", how="left")
agg["headcount_per_1000"] = agg["headcount"] / agg["enrollment"] * 1000
agg["avg_comp"]           = agg["total_comp"] / agg["headcount"]
agg["total_comp_real"]    = agg["total_comp"] * agg["adj_to_2026"]
agg["avg_comp_real"]      = agg["avg_comp"]   * agg["adj_to_2026"]


def base_layout(title, xt="School Year (ending)", yt="", height=550, legend_y=-0.18):
    return dict(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=18)),
        xaxis_title=xt, yaxis_title=yt,
        height=height,
        legend=dict(orientation="h", y=legend_y, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#eee", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#eee"),
        margin=dict(l=70, r=30, t=70, b=80),
    )


def write(fig, name):
    out = ASSETS / f"admin_growth_final_{name}.html"
    fig.write_html(out, include_plotlyjs="cdn", div_id=f"admin_growth_final_{name}")
    print(f"Wrote {out}")


# ============================================================
# Chart A — AFR Admin Pool Over Time (real 2026 $), stacked by function
# This is the marquee chart: dollar pool with no threshold filter.
# ============================================================
afr_long = afr.melt(id_vars=["year"],
                    value_vars=["2300_real","2400_real","2500_real","2600_real"],
                    var_name="func_real", value_name="real_comp")
afr_long["func"] = afr_long["func_real"].str.replace("_real", "")
afr_long = afr_long.dropna(subset=["real_comp"])

figA = go.Figure()
for func in AFR_ORDER:
    sub = afr_long[afr_long["func"] == func].sort_values("year")
    short_label = AFR_LABELS[func].split("(")[0].strip()
    figA.add_trace(go.Bar(
        x=sub["year"], y=sub["real_comp"], name=f"{func} {short_label}",
        marker_color=AFR_COLORS[func],
        hovertemplate="<b>FY%{x}</b><br>" + AFR_LABELS[func] + ": $%{y:,.0f}<extra></extra>",
    ))
figA.update_layout(barmode="stack", **base_layout(
    "D65 Admin Compensation Pool by Function (AFR, 2026 $)",
    yt="Total Compensation (2026 $)",
    height=600,
    legend_y=-0.30))
figA.update_yaxes(tickprefix="$", tickformat=",.0f")
write(figA, "afr_pool_stacked")


# ============================================================
# Chart B — AFR per-pupil admin spend over time (real 2026 $)
# Combines AFR pool with enrollment to show real-cost-per-student trend.
# ============================================================
afr_per_pupil = afr.merge(enroll, on="year", how="left")
afr_per_pupil["pool_per_pupil_real"] = afr_per_pupil["pool_total_real"] / afr_per_pupil["enrollment"]
afr_per_pupil["pool_excl_prin_per_pupil_real"] = afr_per_pupil["pool_excl_principals_real"] / afr_per_pupil["enrollment"]

figB = go.Figure()
figB.add_trace(go.Scatter(
    x=afr_per_pupil["year"], y=afr_per_pupil["pool_per_pupil_real"],
    name="Total admin pool ($19.99M FY25, 2026 $)", mode="lines+markers",
    line=dict(color="black", width=4), marker=dict(size=10),
    hovertemplate="<b>FY%{x}</b><br>Total admin per pupil: $%{y:,.0f}<extra></extra>",
))
figB.add_trace(go.Scatter(
    x=afr_per_pupil["year"], y=afr_per_pupil["pool_excl_prin_per_pupil_real"],
    name="Admin excl. principals ($12.49M FY25, 2026 $)", mode="lines+markers",
    line=dict(color="#c0392b", width=3, dash="dot"), marker=dict(size=9),
    hovertemplate="<b>FY%{x}</b><br>Admin excl principals per pupil: $%{y:,.0f}<extra></extra>",
))
figB.update_layout(**base_layout(
    "D65 Admin Spending Per Pupil Over Time (AFR, 2026 $)",
    yt="Admin Compensation per Pupil (2026 $)"))
figB.update_yaxes(tickprefix="$", tickformat=",.0f")
write(figB, "afr_per_pupil")


# ============================================================
# Chart C — Indexed-eligible headcount stacked (PA, indexed)
# Trend chart: how many higher-paid admin/support has D65 employed each year?
# ============================================================
figC = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    figC.add_trace(go.Bar(
        x=sub["year"], y=sub["headcount"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
figC.update_layout(barmode="stack", **base_layout(
    "Higher-Paid Admin/Support Headcount (CPI-Indexed)",
    yt="Staff Above CPI-Indexed Threshold"))
write(figC, "indexed_headcount_stacked")


# ============================================================
# Chart D — Indexed-eligible per 1,000 students
# ============================================================
figD = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    figD.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount_per_1000"], name=role,
        mode="lines+markers", line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y:.2f} per 1k students<extra></extra>",
    ))
total_per_1k = (agg.groupby("year")
                  .agg(hc=("headcount", "sum"), enroll=("enrollment", "first"))
                  .reset_index())
total_per_1k["per1k"] = total_per_1k["hc"] / total_per_1k["enroll"] * 1000
figD.add_trace(go.Scatter(
    x=total_per_1k["year"], y=total_per_1k["per1k"], name="<b>All Categories Combined</b>",
    mode="lines+markers", line=dict(color="black", width=4, dash="dash"),
    marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:.2f} per 1k students<extra></extra>",
))
figD.update_layout(**base_layout(
    "Higher-Paid Admin/Support per 1,000 Students Over Time",
    yt="Admin/Support per 1,000 Students (indexed-eligible)"))
write(figD, "indexed_per_1000")


# ============================================================
# Chart E — Indexed avg comp per administrator vs 2016 real baseline
# ============================================================
figE = go.Figure()
years = sorted(agg["year"].unique())
baseline_2016_real = (agg[agg["year"] == CPI_ANCHOR_YEAR]
                      .assign(avg_comp_real=lambda d: d["avg_comp"] * d["adj_to_2026"])
                      .set_index("role_class")["avg_comp_real"])
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    figE.add_trace(go.Scatter(
        x=sub["year"], y=sub["avg_comp_real"], name=f"{role}",
        mode="lines+markers", line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} avg<extra></extra>",
    ))
for role in ROLE_ORDER:
    if role not in baseline_2016_real.index:
        continue
    baseline = baseline_2016_real[role]
    figE.add_trace(go.Scatter(
        x=years, y=[baseline] * len(years),
        name=f"{role} — 2016 real baseline",
        mode="lines",
        line=dict(color=COLORS[role], width=2, dash="dot"),
        opacity=0.55,
        hovertemplate="<b>%{x}</b><br>" + role + " 2016 real baseline: $%{y:,.0f}<extra></extra>",
    ))
figE.update_layout(**base_layout(
    "Average Comp per Administrator vs. 2016 Baseline (2026 $)",
    yt="Average Total Comp per Person (2026 $)"))
figE.update_yaxes(tickprefix="$", tickformat=",.0f")
write(figE, "avg_comp")


# ============================================================
# Chart F — YoY % change: AFR pool real comp · indexed headcount · enrollment
# ============================================================
year_total_pa = (agg.groupby("year")
                    .agg(headcount=("headcount", "sum"),
                         enrollment=("enrollment", "first"))
                    .reset_index().sort_values("year"))
afr_yoy = afr[["year", "pool_total_real"]].sort_values("year").reset_index(drop=True)
yoy = afr_yoy.merge(year_total_pa, on="year", how="outer").sort_values("year").reset_index(drop=True)
yoy["comp_yoy_pct"]   = yoy["pool_total_real"].pct_change() * 100
yoy["hc_yoy_pct"]     = yoy["headcount"].pct_change()  * 100
yoy["enroll_yoy_pct"] = yoy["enrollment"].pct_change() * 100

figF = go.Figure()
figF.add_trace(go.Scatter(x=yoy["year"], y=yoy["comp_yoy_pct"],
    name="AFR admin pool (real)", mode="lines+markers",
    line=dict(color="#c0392b", width=3), marker=dict(size=10),
    hovertemplate="<b>FY%{x}</b><br>Real pool YoY: %{y:+.1f}%<extra></extra>"))
figF.add_trace(go.Scatter(x=yoy["year"], y=yoy["hc_yoy_pct"],
    name="Indexed-eligible headcount", mode="lines+markers",
    line=dict(color="#8e44ad", width=3), marker=dict(size=10),
    hovertemplate="<b>FY%{x}</b><br>Headcount YoY: %{y:+.1f}%<extra></extra>"))
figF.add_trace(go.Scatter(x=yoy["year"], y=yoy["enroll_yoy_pct"],
    name="Student Enrollment", mode="lines+markers",
    line=dict(color="#16a085", width=3), marker=dict(size=10),
    hovertemplate="<b>FY%{x}</b><br>Enrollment YoY: %{y:+.1f}%<extra></extra>"))
figF.add_hline(y=0, line=dict(color="black", width=1, dash="dot"))
figF.update_layout(**base_layout(
    "YoY % Change: Admin Spending vs Headcount vs Student Enrollment",
    yt="YoY % Change"))
figF.update_yaxes(ticksuffix="%")
write(figF, "yoy_decoupling")


# ============================================================
# Chart G — Annual change in AFR admin pool (real $)
# ============================================================
yt_afr = afr[["year", "pool_total_real"]].sort_values("year").reset_index(drop=True)
yt_afr["delta"] = yt_afr["pool_total_real"].diff()
deltas = yt_afr.dropna(subset=["delta"]).copy()
deltas["color"] = deltas["delta"].apply(lambda v: "#c0392b" if v >= 0 else "#27ae60")

start_val = yt_afr["pool_total_real"].iloc[0]
end_val   = yt_afr["pool_total_real"].iloc[-1]
net       = end_val - start_val
start_year_label = f"FY{int(yt_afr['year'].iloc[0])}"
end_year_label   = f"FY{int(yt_afr['year'].iloc[-1])}"

figG = go.Figure()
figG.add_trace(go.Bar(
    x=deltas["year"], y=deltas["delta"],
    marker_color=deltas["color"],
    text=[f"${v:+,.0f}" for v in deltas["delta"]],
    textposition="outside",
    hovertemplate="<b>FY%{x}</b><br>YoY change: $%{y:+,.0f}<extra></extra>",
    showlegend=False,
))
figG.add_hline(y=0, line=dict(color="black", width=1))
subtitle = (f"<span style='font-size:13px;color:#444'>"
            f"{start_year_label}: ${start_val/1e6:,.1f}M → {end_year_label}: ${end_val/1e6:,.1f}M"
            f" (net ${net/1e6:+,.1f}M, {net/start_val*100:+.1f}%)"
            f"</span>")
figG.update_layout(**base_layout(
    f"Annual Change in AFR Admin Pool (2026 $)<br>{subtitle}",
    xt="Fiscal Year",
    yt="Year-over-Year Change (2026 $)",
    height=600))
figG.update_yaxes(tickprefix="$", tickformat=",.0f")
write(figG, "afr_waterfall")


# ============================================================
# Chart H — IMRF role categories (FY24-25 and FY25-26 only),
# indexed-eligible only.
# ============================================================
imrf_roles = (df[(df["role_class"] == "IMRF Support Staff") & (df["position"].fillna("").str.len() > 0)]
              .copy())
imrf_roles["pos_clean"] = imrf_roles["position"].str.upper().str.strip()
def bucket(p):
    p = (p or "").upper()
    if any(k in p for k in ["CUSTODIAN", "MAINTENANCE", "ELECTRICIAN", "BUILDINGS", "INFRASTRUCTURE"]): return "Buildings & Maintenance"
    if any(k in p for k in ["TECHNOLOGY", "NETWORK", "CYBERSECURITY", "SYSTEMS ENGINEER", "DATABASE", "MOBILE COMPUTING"]): return "IT / Technology"
    if any(k in p for k in ["NURSE", "OCCUPATIONAL THERAPIST", "PHYSICAL THERAPIST", "HEALTH SERVICES"]): return "Health & Therapy"
    if any(k in p for k in ["NUTRITION", "FOOD"]): return "Nutrition & Food Services"
    if any(k in p for k in ["PAYROLL", "ACCOUNTS PAYABLE", "FINANCIAL", "GRANT", "FINANCE"]): return "Finance & Payroll"
    if any(k in p for k in ["DIRECTOR", "MANAGER", "SUPERVISOR", "COORDINATOR", "EXEC", "CHIEF", "MANAGING"]): return "Directors / Managers / Coordinators"
    if any(k in p for k in ["FACE", "FAMILY CENTER", "WELLNESS", "CULTURE", "CLIMATE", "STUD SAFETY", "STUDENT SAFETY", "SACC"]): return "Student & Family Services"
    if any(k in p for k in ["SECRETARY", "ASSISTANT", "ADMINISTRATIVE"]): return "Administrative Support"
    return "Other"
imrf_roles["bucket"] = imrf_roles["pos_clean"].apply(bucket)
imrf_by_yr = (imrf_roles[imrf_roles["year"].isin([2025, 2026])]
              .groupby(["year", "bucket"], as_index=False)
              .size().rename(columns={"size": "n"}))

figH = go.Figure()
bucket_order = ["Directors / Managers / Coordinators", "Buildings & Maintenance",
                "IT / Technology", "Health & Therapy", "Student & Family Services",
                "Finance & Payroll", "Nutrition & Food Services",
                "Administrative Support", "Other"]
palette = ["#c0392b", "#34495e", "#2980b9", "#16a085", "#e67e22",
           "#8e44ad", "#27ae60", "#7f8c8d", "#bdc3c7"]
for i, b in enumerate(bucket_order):
    sub = imrf_by_yr[imrf_by_yr["bucket"] == b].sort_values("year")
    if sub.empty:
        continue
    figH.add_trace(go.Bar(
        x=sub["year"], y=sub["n"], name=b,
        marker_color=palette[i % len(palette)],
        hovertemplate="<b>%{x}</b><br>" + b + ": %{y}<extra></extra>",
    ))
figH.update_layout(barmode="stack", **base_layout(
    "IMRF Support Staff by Role Category<br><span style='font-size:13px;color:#444'>Indexed-eligible, SY24-25 and SY25-26</span>",
    yt="Number of Staff", height=600,
    legend_y=-0.30))
figH.update_xaxes(type="category")
write(figH, "imrf_categories")


# ============================================================
# Chart I — Right-sizing comparison (AFR pool denominator, %-of-pool framing)
# Every scenario uses the District's per-cut average ($129K) for direct
# comparability with the District's $8.3M proposal.
# ============================================================
# AFR pool denominators (FY25 in 2026 $ - the most recent finalized AFR)
AFR_POOL_TOTAL = afr.loc[afr["year"] == 2025, "pool_total_real"].iloc[0]   # $19.99M
AFR_POOL_EXCL_PRIN = afr.loc[afr["year"] == 2025, "pool_excl_principals_real"].iloc[0]   # $12.49M

# District's per-cut average (their math: $8,287,312 / 64 cuts)
DISTRICT_PER_CUT = 8_287_312 / 64
DISTRICT_PROPOSAL_TOTAL = 8_287_312

# Indexed PA-roster facts in 2026
agg_2026 = agg[agg["year"] == 2026].copy()
agg_2016 = agg[agg["year"] == 2016].copy()
indexed_hc_2026 = int(agg_2026["headcount"].sum())          # 94
indexed_enroll_2026 = int(agg_2026["enrollment"].iloc[0])   # 5625
ratio_2016_indexed = (agg_2016["headcount"].sum()
                      / agg_2016["enrollment"].iloc[0] * 1000)  # ~10.0/1k

# 2016-2019 indexed avg headcount (group member's "moderate" anchor)
hc_2016_19_indexed = (agg.groupby("year")["headcount"].sum()
                        .loc[2016:2019].mean())

# Three Legion right-sizing scenarios using District per-cut math
scenarios = []

# Moderate
target_moderate = round(hc_2016_19_indexed)
cuts_moderate = max(indexed_hc_2026 - target_moderate, 0)
scenarios.append({
    "label": f"Moderate — return to 2016–19 baseline (~{int(cuts_moderate)} cuts)",
    "savings": cuts_moderate * DISTRICT_PER_CUT,
    "color": "#e74c3c",
})

# Peer median 12/1k
PEER_RATIO = 12.0
target_peer = PEER_RATIO * indexed_enroll_2026 / 1000
cuts_peer = max(indexed_hc_2026 - target_peer, 0)
scenarios.append({
    "label": f"Right-size to peer K-8 median (~{int(round(cuts_peer))} cuts)",
    "savings": cuts_peer * DISTRICT_PER_CUT,
    "color": "#c0392b",
})

# D65 2016 ratio
target_2016 = ratio_2016_indexed * indexed_enroll_2026 / 1000
cuts_2016 = max(indexed_hc_2026 - target_2016, 0)
scenarios.append({
    "label": f"Right-size to D65's 2016 ratio (~{int(round(cuts_2016))} cuts)",
    "savings": cuts_2016 * DISTRICT_PER_CUT,
    "color": "#922b21",
})

# District's April 20, 2026 proposal — kept at $8.3M (their actual workforce math)
scenarios.append({
    "label": ("District's April 20, 2026 admin-cut proposal"
              "<br>(22 admins + 42 non-union support, missed FY27 deadline)"),
    "savings": DISTRICT_PROPOSAL_TOTAL,
    "color": "#e67e22",
})

# Recent enacted/proposed cuts from CSV; drop superseded scenarios
measures = []
for _, r in cuts.iterrows():
    if "no longer active" in (r["notes"] or "").lower() or "Sept 2025 only" in r["measure"]:
        continue
    measures.append({
        "label": r["measure"],
        "savings": r["annual_savings_estimate"],
        "color": "#34495e",
    })
measures.extend(scenarios)

mdf = pd.DataFrame(measures).sort_values("savings", ascending=True).reset_index(drop=True)
# Format dollar AND % of AFR pool
mdf["pct_of_pool"] = mdf["savings"] / AFR_POOL_TOTAL * 100
mdf["label_fmt"] = mdf.apply(lambda r:
    (f"${r['savings']/1e6:,.2f}M ({r['pct_of_pool']:.1f}% of pool)"
     if r["savings"] >= 1e6
     else (f"${r['savings']/1e3:,.0f}K ({r['pct_of_pool']:.1f}% of pool)"
           if r["savings"] > 0 else "$0")),
    axis=1)

figI = go.Figure()
figI.add_trace(go.Bar(
    y=mdf["label"], x=mdf["savings"],
    orientation="h",
    marker_color=mdf["color"],
    text=mdf["label_fmt"],
    textposition="auto",
    insidetextanchor="end",
    insidetextfont=dict(size=12, color="white"),
    outsidetextfont=dict(size=12, color="#333"),
    constraintext="none",
    cliponaxis=False,
    hovertemplate="<b>%{y}</b><br>Annual savings: $%{x:,.0f}<br>"
                  + f"% of AFR admin pool ($19.99M FY25): "
                  + "%{customdata:.1f}%<extra></extra>",
    customdata=mdf["pct_of_pool"],
    showlegend=False,
))
figI.update_layout(**base_layout(
    f"Annual Savings: Recent Cuts vs. Admin Right-Sizing<br>"
    f"<span style='font-size:13px;color:#444'>"
    f"% of pool = FY25 AFR admin comp pool (${AFR_POOL_TOTAL/1e6:,.2f}M, 2026 $)</span>",
    xt="",
    yt="",
    height=820))
figI.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
figI.add_annotation(
    text=("<i>Dark grey: District SDRP figures. "
          "Orange: District's April 2026 admin-cut proposal. "
          "Red: Legion right-sizing scenarios.<br>"
          "All admin scenarios sized at $129K/position (District's own avg).</i>"),
    xref="paper", yref="paper", x=0, y=-0.02,
    showarrow=False, xanchor="left", yanchor="top",
    font=dict(size=11, color="#666"), align="left",
)
figI.update_layout(margin=dict(l=320, r=80, t=110, b=110))
write(figI, "right_sizing_comparison")


# ============================================================
# Print summary
# ============================================================
print("\n=== AFR Pool Summary (real $ in 2026) ===")
print(afr[["year","pool_total_real","pool_excl_principals_real",
           "2300_real","2400_real","2500_real","2600_real"]]
        .round(0).to_string(index=False))

print(f"\n=== Right-sizing scenarios (AFR pool denominator) ===")
print(f"  AFR FY25 admin pool: ${AFR_POOL_TOTAL:,.0f} (denominator)")
print(f"  AFR FY25 excl principals: ${AFR_POOL_EXCL_PRIN:,.0f}")
print(f"  District per-cut avg: ${DISTRICT_PER_CUT:,.0f}")
print()
print(f"  Moderate (target {target_moderate}, cut {int(cuts_moderate)}): "
      f"${cuts_moderate*DISTRICT_PER_CUT:,.0f} = "
      f"{cuts_moderate*DISTRICT_PER_CUT/AFR_POOL_TOTAL*100:.1f}% of pool")
print(f"  Peer median (target {int(round(target_peer))}, cut {int(round(cuts_peer))}): "
      f"${cuts_peer*DISTRICT_PER_CUT:,.0f} = "
      f"{cuts_peer*DISTRICT_PER_CUT/AFR_POOL_TOTAL*100:.1f}% of pool")
print(f"  D65 2016 ratio (target {int(round(target_2016))}, cut {int(round(cuts_2016))}): "
      f"${cuts_2016*DISTRICT_PER_CUT:,.0f} = "
      f"{cuts_2016*DISTRICT_PER_CUT/AFR_POOL_TOTAL*100:.1f}% of pool")
print(f"  District proposal: ${DISTRICT_PROPOSAL_TOTAL:,.0f} = "
      f"{DISTRICT_PROPOSAL_TOTAL/AFR_POOL_TOTAL*100:.1f}% of pool")

print("\nDone.")
