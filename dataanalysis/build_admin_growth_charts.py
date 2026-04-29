"""
Builds the visualization suite for the D65 Administrator Growth analysis page.

Reads:
  - data/d65_admin_comp_combined.csv  (long-format, all years/categories)
  - data/d65_enrollment_history.csv
  - data/cpi_history.csv               (BLS CPI-U for inflation adjustment)
  - data/d65_recent_cuts.csv           (recently-proposed/enacted budget cuts)

Writes HTML files to assets/admin_growth_*.html for embedding in
dataanalysis/admin-growth.md.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

# Consistent colors for the three role classes (used everywhere)
COLORS = {
    "TRS Admin": "#c0392b",            # red — central office admin (PA 96-0434)
    "IMRF Support Staff": "#2980b9",   # blue — non-cert admin/support (PA 097-0609)
    "Principal": "#27ae60",            # green — principals + asst principals
}
ROLE_ORDER = ["TRS Admin", "IMRF Support Staff", "Principal"]

# ------------------------------------------------------------
# Load
# ------------------------------------------------------------
df     = pd.read_csv(DATA / "d65_admin_comp_combined.csv")
enroll = pd.read_csv(DATA / "d65_enrollment_history.csv")[["year", "enrollment"]]
cpi    = pd.read_csv(DATA / "cpi_history.csv")[["year", "cpi_u"]]
cuts   = pd.read_csv(DATA / "d65_recent_cuts.csv")

# Inflation factors: convert nominal $X(year) to 2026 real $: $X * cpi(2026) / cpi(year)
CPI_BASE_YEAR = 2026
cpi_base = cpi.loc[cpi["year"] == CPI_BASE_YEAR, "cpi_u"].iloc[0]
cpi["adj_to_2026"] = cpi_base / cpi["cpi_u"]

# Aggregate per year x role_class
agg = (df.groupby(["year", "role_class"], as_index=False)
         .agg(headcount=("last_name", "count"),
              total_comp=("total_comp", "sum"),
              total_salary=("total_salary", "sum")))
agg = agg.merge(enroll, on="year", how="left")
agg = agg.merge(cpi[["year", "adj_to_2026"]], on="year", how="left")

# Derived metrics — both nominal and real (CPI-adjusted to 2026 dollars)
agg["headcount_per_1000"]      = agg["headcount"] / agg["enrollment"] * 1000
agg["comp_per_1000"]           = agg["total_comp"]   / agg["enrollment"] * 1000
agg["avg_comp"]                = agg["total_comp"]   / agg["headcount"]
agg["total_comp_real"]         = agg["total_comp"]   * agg["adj_to_2026"]
agg["comp_per_1000_real"]      = agg["comp_per_1000"]* agg["adj_to_2026"]
agg["avg_comp_real"]           = agg["avg_comp"]     * agg["adj_to_2026"]


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
    out = ASSETS / f"admin_growth_{name}.html"
    fig.write_html(out, include_plotlyjs="cdn", div_id=f"admin_growth_{name}")
    print(f"Wrote {out}")


def add_nominal_real_buttons(fig, n_traces_nominal, n_traces_real, title_nominal, title_real):
    """Add Plotly buttons that toggle between nominal and real views.
    Assumes the figure has nominal traces first, then real traces."""
    total = n_traces_nominal + n_traces_real
    vis_nominal = [True] * n_traces_nominal + [False] * n_traces_real
    vis_real    = [False] * n_traces_nominal + [True]  * n_traces_real
    fig.update_layout(updatemenus=[dict(
        type="buttons", direction="left",
        x=0.5, xanchor="center", y=1.16, yanchor="top",
        showactive=True, bgcolor="#f4f4f4",
        buttons=[
            dict(label="Nominal $",        method="update",
                 args=[{"visible": vis_nominal}, {"title.text": f"<b>{title_nominal}</b>"}]),
            dict(label="Inflation-Adjusted (2026 $)", method="update",
                 args=[{"visible": vis_real},    {"title.text": f"<b>{title_real}</b>"}]),
        ],
    )])
    fig.update_layout(margin=dict(l=70, r=30, t=110, b=80))


# ============================================================
# Chart 1 — Headcount over time, stacked bar by category
# ============================================================
fig1 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig1.add_trace(go.Bar(
        x=sub["year"], y=sub["headcount"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
fig1.update_layout(barmode="stack", **base_layout(
    "D65 Admin Headcount Over Time (Stacked by Category)",
    yt="Number of Administrative Staff"))
write(fig1, "headcount_stacked")


# ============================================================
# Chart 2 — Headcount per 1,000 students
# ============================================================
fig2 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig2.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount_per_1000"], name=role,
        mode="lines+markers", line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y:.2f} per 1k students<extra></extra>",
    ))
total_per_1k = (agg.groupby("year")
                  .agg(hc=("headcount", "sum"), enroll=("enrollment", "first"))
                  .reset_index())
total_per_1k["per1k"] = total_per_1k["hc"] / total_per_1k["enroll"] * 1000
fig2.add_trace(go.Scatter(
    x=total_per_1k["year"], y=total_per_1k["per1k"], name="<b>All Categories Combined</b>",
    mode="lines+markers", line=dict(color="black", width=4, dash="dash"),
    marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:.2f} per 1k students<extra></extra>",
))
fig2.update_layout(**base_layout(
    "D65 Admin per 1,000 Students Over Time",
    yt="Administrators per 1,000 Students"))
write(fig2, "headcount_per_1000")


# ============================================================
# Chart 3 — Total compensation over time, stacked (inflation-adjusted to 2026 $)
# ============================================================
fig3 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig3.add_trace(go.Bar(
        x=sub["year"], y=sub["total_comp_real"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f}<extra></extra>",
    ))
fig3.update_layout(barmode="stack", **base_layout(
    "D65 Total Admin Comp Over Time (Inflation-Adjusted to 2026 $)",
    yt="Total Compensation (2026 $)"))
fig3.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig3, "comp_stacked")


# ============================================================
# Chart 4 — Total compensation per 1,000 students (inflation-adjusted to 2026 $)
# ============================================================
fig4 = go.Figure()
total_comp_per_1k = (agg.groupby("year")
                       .agg(c=("total_comp", "sum"),
                            e=("enrollment", "first"),
                            adj=("adj_to_2026", "first"))
                       .reset_index())
total_comp_per_1k["per1k"]      = total_comp_per_1k["c"] / total_comp_per_1k["e"] * 1000
total_comp_per_1k["per1k_real"] = total_comp_per_1k["per1k"] * total_comp_per_1k["adj"]

for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig4.add_trace(go.Scatter(
        x=sub["year"], y=sub["comp_per_1000_real"], name=role,
        mode="lines+markers", line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} per 1k students<extra></extra>",
    ))
fig4.add_trace(go.Scatter(
    x=total_comp_per_1k["year"], y=total_comp_per_1k["per1k_real"],
    name="<b>All Categories Combined</b>", mode="lines+markers",
    line=dict(color="black", width=4, dash="dash"), marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f} per 1k students<extra></extra>",
))
fig4.update_layout(**base_layout(
    "D65 Admin Comp per 1,000 Students Over Time (Inflation-Adjusted)",
    yt="Total Comp per 1,000 Students (2026 $)"))
fig4.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig4, "comp_per_1000")


# ============================================================
# Chart 5 — Average comp per administrator, in real (2026) dollars.
# A flat real-dollar line means comp tracked inflation; a rising line means
# real raises; a falling line means lost ground to inflation. The 2016 real
# baseline is shown as a dotted horizontal reference per role.
# ============================================================
fig5 = go.Figure()
years = sorted(agg["year"].unique())
baseline_2016_real = (agg[agg["year"] == 2016]
                      .assign(avg_comp_real=lambda d: d["avg_comp"] * d["adj_to_2026"])
                      .set_index("role_class")["avg_comp_real"])
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig5.add_trace(go.Scatter(
        x=sub["year"], y=sub["avg_comp_real"], name=f"{role}",
        mode="lines+markers", line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} avg (2026 $)<extra></extra>",
    ))
for role in ROLE_ORDER:
    if role not in baseline_2016_real.index:
        continue
    baseline = baseline_2016_real[role]
    fig5.add_trace(go.Scatter(
        x=years, y=[baseline] * len(years),
        name=f"{role} — 2016 real baseline",
        mode="lines",
        line=dict(color=COLORS[role], width=2, dash="dot"),
        opacity=0.55,
        hovertemplate="<b>%{x}</b><br>" + role + " 2016 real baseline: $%{y:,.0f}<extra></extra>",
    ))
fig5.update_layout(**base_layout(
    "Average Comp per Administrator vs. 2016 Real Baseline (2026 $)",
    yt="Average Total Comp per Person (2026 $)"))
fig5.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig5, "avg_comp")


# ============================================================
# Chart 6 — TRS Admin breakdown (inflation-adjusted to 2026 $)
# ============================================================
trs_detail = (df[df["role_class"] == "TRS Admin"]
                .groupby("year", as_index=False)
                .agg(base=("base_salary", "sum"),
                     total_salary=("total_salary", "sum"),
                     total_comp=("total_comp", "sum")))
trs_detail["trs_contribution"] = trs_detail["total_salary"] - trs_detail["base"]
trs_detail["benefits"]         = trs_detail["total_comp"]   - trs_detail["total_salary"]
trs_detail = trs_detail.merge(cpi[["year", "adj_to_2026"]], on="year")
for col in ["base", "trs_contribution", "benefits"]:
    trs_detail[col] = trs_detail[col] * trs_detail["adj_to_2026"]
fig6 = go.Figure()
fig6.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["base"],
                      name="Base Salary", marker_color="#34495e",
                      hovertemplate="<b>%{x}</b><br>Base: $%{y:,.0f}<extra></extra>"))
fig6.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["trs_contribution"],
                      name="TRS / Retirement Contribution", marker_color="#e67e22",
                      hovertemplate="<b>%{x}</b><br>TRS: $%{y:,.0f}<extra></extra>"))
fig6.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["benefits"],
                      name="Health/Dental/Life/Annuity/Car",
                      marker_color="#16a085",
                      hovertemplate="<b>%{x}</b><br>Benefits: $%{y:,.0f}<extra></extra>"))
fig6.update_layout(barmode="stack", **base_layout(
    "TRS Admin Comp Breakdown (2026 $)",
    yt="Total Cost (2026 $)"))
fig6.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig6, "comp_breakdown")


# ============================================================
# Chart 7 — YoY % change: cost vs enrollment vs headcount (decoupling)
# Comp YoY is computed on inflation-adjusted (2026 $) totals so that the
# series shows real cost growth, not inflation.
# ============================================================
year_total = (agg.groupby("year")
                 .agg(total_comp=("total_comp", "sum"),
                      total_comp_real=("total_comp_real", "sum"),
                      headcount=("headcount", "sum"),
                      enrollment=("enrollment", "first"))
                 .reset_index().sort_values("year"))
year_total["comp_yoy_pct"]   = year_total["total_comp_real"].pct_change() * 100
year_total["hc_yoy_pct"]     = year_total["headcount"].pct_change()  * 100
year_total["enroll_yoy_pct"] = year_total["enrollment"].pct_change() * 100

fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=year_total["year"], y=year_total["comp_yoy_pct"],
    name="Admin Total Comp (real)", mode="lines+markers",
    line=dict(color="#c0392b", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Real comp YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_trace(go.Scatter(x=year_total["year"], y=year_total["hc_yoy_pct"],
    name="Admin Headcount", mode="lines+markers",
    line=dict(color="#8e44ad", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Headcount YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_trace(go.Scatter(x=year_total["year"], y=year_total["enroll_yoy_pct"],
    name="Student Enrollment", mode="lines+markers",
    line=dict(color="#16a085", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Enrollment YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_hline(y=0, line=dict(color="black", width=1, dash="dot"))
fig7.update_layout(**base_layout(
    "Year-over-Year % Change: Admin Costs vs. Student Enrollment",
    yt="YoY % Change"))
fig7.update_yaxes(ticksuffix="%")
write(fig7, "yoy_decoupling")


# ============================================================
# Chart 8 — Year-over-year change in admin comp (delta-only bar chart, 2026 $)
#   Annotations moved out of plot area into title subtitle to avoid x-axis overlap.
# ============================================================
yt = year_total[["year", "total_comp_real"]].sort_values("year").reset_index(drop=True)
yt["delta"] = yt["total_comp_real"].diff()
deltas = yt.dropna(subset=["delta"]).copy()
deltas["color"] = deltas["delta"].apply(lambda v: "#c0392b" if v >= 0 else "#27ae60")

start_val = yt["total_comp_real"].iloc[0]
end_val   = yt["total_comp_real"].iloc[-1]
net       = end_val - start_val
start_year_label = f"SY{int(yt['year'].iloc[0])-1}-{str(int(yt['year'].iloc[0]))[-2:]}"
end_year_label   = f"SY{int(yt['year'].iloc[-1])-1}-{str(int(yt['year'].iloc[-1]))[-2:]}"

fig8 = go.Figure()
fig8.add_trace(go.Bar(
    x=deltas["year"], y=deltas["delta"],
    marker_color=deltas["color"],
    text=[f"${v:+,.0f}" for v in deltas["delta"]],
    textposition="outside",
    hovertemplate="<b>SY%{x}</b><br>YoY change: $%{y:+,.0f} (2026 $)<extra></extra>",
    showlegend=False,
))
fig8.add_hline(y=0, line=dict(color="black", width=1))

# Subtitle below main title (in the plot area top), away from x-axis
subtitle = (f"<span style='font-size:13px;color:#444'>"
            f"{start_year_label} starting total: ${start_val:,.0f} (2026 $)"
            f"  •  {end_year_label} ending total: ${end_val:,.0f} (2026 $)"
            f"  •  Net change: ${net:+,.0f} ({net/start_val*100:+.1f}%)"
            f"</span>")

fig8.update_layout(**base_layout(
    f"Annual Change in Total Administrative Compensation (2026 $)<br>{subtitle}",
    xt="School Year (ending)",
    yt="Year-over-Year Change (2026 $)",
    height=600))
fig8.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig8, "waterfall")


# ============================================================
# Chart 9 — IMRF role examples (data view, bar chart of role categories)
# Replaces the cabinet-trajectory chart that named individuals.
# ============================================================
imrf_roles = (df[(df["role_class"] == "IMRF Support Staff") & (df["position"].fillna("").str.len() > 0)]
              .copy())
imrf_roles["pos_clean"] = imrf_roles["position"].str.upper().str.strip()
# Bucket into broad categories for readability
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

# For each year, count IMRF staff per bucket. Restrict to the most recent
# two reporting years (SY24-25 and SY25-26) — earlier years' position
# strings were too inconsistent across PDFs to bucket reliably.
IMRF_CATEGORIES_YEARS = [2025, 2026]
imrf_by_yr = (imrf_roles[imrf_roles["year"].isin(IMRF_CATEGORIES_YEARS)]
              .groupby(["year", "bucket"], as_index=False)
              .size().rename(columns={"size": "n"}))

fig9 = go.Figure()
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
    fig9.add_trace(go.Bar(
        x=sub["year"], y=sub["n"], name=b,
        marker_color=palette[i % len(palette)],
        hovertemplate="<b>%{x}</b><br>" + b + ": %{y}<extra></extra>",
    ))
fig9.update_layout(barmode="stack", **base_layout(
    "IMRF Support Staff by Role Category (SY24-25 and SY25-26)",
    yt="Number of Staff", height=600,
    legend_y=-0.30))
fig9.update_xaxes(type="category")
write(fig9, "imrf_categories")


# ============================================================
# Chart 10 — Right-sizing comparison
# Compare how much money would be saved by various measures, including
# the recently-proposed cuts and a notional "right-size admin" scenario.
# ============================================================
# Compute "right-size admin" savings: bring admin headcount per 1000 down to the
# 2016 ratio (which was already higher than typical peer districts but is the
# District's own baseline before the buildup).
agg_2026 = agg[agg["year"] == 2026].copy()
agg_2016 = agg[agg["year"] == 2016].copy()

current_total_hc = agg_2026["headcount"].sum()                           # 153
current_total_comp = agg_2026["total_comp"].sum()                        # ~$20M
current_enroll = agg_2026["enrollment"].iloc[0]                          # 5717
ratio_2016 = agg_2016["headcount"].sum() / agg_2016["enrollment"].iloc[0] * 1000  # ~9.97
target_hc_at_2016_ratio = ratio_2016 * current_enroll / 1000             # ~57
hc_to_cut = max(current_total_hc - target_hc_at_2016_ratio, 0)
avg_comp_2026 = current_total_comp / current_total_hc                     # ~$131K
right_size_savings = hc_to_cut * avg_comp_2026

# Tom Hayden / community estimate: roughly admin is ~$5-7M too large vs. peer districts
# Use the cleaner formulation: bring admins/1k students down to peer K-8 median (~12)
# from existing salary-data analysis — assume ~12 per 1k as peer benchmark.
PEER_RATIO = 12.0
target_hc_peer = PEER_RATIO * current_enroll / 1000
hc_to_cut_peer = max(current_total_hc - target_hc_peer, 0)
right_size_savings_peer = hc_to_cut_peer * avg_comp_2026

# Build the comparison data. Drop the "no longer active" 4-school row from the
# main chart (it was superseded in Nov 2025) but keep its row in the CSV for
# methodology transparency.
measures = []
for _, r in cuts.iterrows():
    if "no longer active" in (r["notes"] or "").lower() or "Sept 2025 only" in r["measure"]:
        continue  # skip superseded scenarios in the chart
    measures.append({
        "label": r["measure"],
        "savings": r["annual_savings_estimate"],
        "color": "#34495e",
    })
# District's own April 20, 2026 admin-cut proposal (Phase III deck, slide 13).
# 22 administrators + 42 non-union support, $8,287,312 estimated savings.
# Presented 19 days after the April 1, 2026 contractual deadline that would
# have made it actionable for FY27, so deferred to FY28 at the earliest.
DISTRICT_ADMIN_PROPOSAL_SAVINGS = 8_287_312
measures.append({
    "label": ("District's April 20, 2026 admin-cut proposal<br>"
              "(22 admins + 42 non-union support, missed FY27 deadline)"),
    "savings": DISTRICT_ADMIN_PROPOSAL_SAVINGS,
    "color": "#e67e22",
})

# Right-sizing scenarios — separate color so they pop visually
measures.append({
    "label": "Right-size admin to D65's own 2016 ratio<br>(~10/1k students, ~96 cuts)",
    "savings": right_size_savings,
    "color": "#c0392b",
})
measures.append({
    "label": "Right-size admin to peer K-8 median<br>(~12/1k students, ~86 cuts)",
    "savings": right_size_savings_peer,
    "color": "#c0392b",
})

mdf = pd.DataFrame(measures).sort_values("savings", ascending=True).reset_index(drop=True)
# Format dollar labels in millions for readability and use textposition="auto"
# so labels render inside large bars and outside small ones — keeps everything
# inside the plot area regardless of bar size.
mdf["label_fmt"] = mdf["savings"].apply(lambda v: f"${v/1e6:,.2f}M" if v >= 1e6
                                         else (f"${v/1e3:,.0f}K" if v > 0 else "$0"))

fig10 = go.Figure()
fig10.add_trace(go.Bar(
    y=mdf["label"], x=mdf["savings"],
    orientation="h",
    marker_color=mdf["color"],
    text=mdf["label_fmt"],
    textposition="auto",
    insidetextanchor="end",
    textfont=dict(size=13, color="white"),
    cliponaxis=False,
    hovertemplate="<b>%{y}</b><br>Estimated annual savings: $%{x:,.0f}<extra></extra>",
    showlegend=False,
))
# Bar values are already labeled inside/outside each bar, so we hide the
# x-axis ticks (they were overlapping at small bar sizes) and use the
# bottom margin for a single-line caption that won't clip.
fig10.update_layout(**base_layout(
    "Annual Savings: Recent Cuts vs. Admin Right-Sizing",
    xt="",
    yt="",
    height=760))
fig10.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig10.add_annotation(
    text=("<i>Dark grey: District's revised Dec 2025 SDRP figures.<br>"
          "Orange: District's April 20, 2026 admin-cut proposal (deferred to FY28).<br>"
          "Red: Legion right-sizing scenarios.</i>"),
    xref="paper", yref="paper", x=0, y=-0.02,
    showarrow=False, xanchor="left", yanchor="top",
    font=dict(size=11, color="#666"), align="left",
)
fig10.update_layout(margin=dict(l=320, r=80, t=70, b=90))
write(fig10, "right_sizing_comparison")


# ============================================================
# Chart 11 — Bonus headcount lines (non-stacked, for direct comparison)
# ============================================================
fig_bonus = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig_bonus.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
fig_bonus.update_layout(**base_layout(
    "D65 Admin Headcount by Category (Lines for Direct Comparison)",
    yt="Number of Administrative Staff"))
write(fig_bonus, "headcount_lines")


# ============================================================
# Chart 12 — Inflation-adjusted headcount (PA 97-0609 threshold robustness)
# Toggle between nominal headcount ($75K fixed reporting threshold) and
# inflation-adjusted headcount ($75K-equivalent indexed to CPI from 2016).
# Only IMRF Support Staff are clipped at $75K in the source data, but we
# apply the threshold uniformly across role classes for transparency.
# ============================================================
CPI_ANCHOR_YEAR = 2016
cpi_anchor = cpi.loc[cpi["year"] == CPI_ANCHOR_YEAR, "cpi_u"].iloc[0]
cpi["threshold_indexed"] = 75000 * cpi["cpi_u"] / cpi_anchor

df_thr = df.merge(cpi[["year", "threshold_indexed"]], on="year")
df_thr_adj = df_thr[df_thr["total_comp"] >= df_thr["threshold_indexed"]]

agg_adj = (df_thr_adj.groupby(["year", "role_class"], as_index=False)
                     .agg(headcount=("last_name", "count")))

fig12 = go.Figure()
# Nominal traces (visible by default)
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig12.add_trace(go.Bar(
        x=sub["year"], y=sub["headcount"], name=role,
        marker_color=COLORS[role], visible=True,
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} (nominal $75K threshold)<extra></extra>",
    ))
# Inflation-adjusted traces (hidden by default)
for role in ROLE_ORDER:
    sub = agg_adj[agg_adj["role_class"] == role].sort_values("year")
    # Reindex to ensure all years present (fill missing with 0)
    sub = sub.set_index("year").reindex(sorted(agg["year"].unique()), fill_value=0).reset_index()
    fig12.add_trace(go.Bar(
        x=sub["year"], y=sub["headcount"], name=role,
        marker_color=COLORS[role], visible=False,
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} (CPI-indexed threshold)<extra></extra>",
    ))
title_fixed_main = "D65 Admin Headcount"
title_fixed_sub = "Fixed $75K reporting threshold (PA 97-0609)"
title_indexed_main = "D65 Admin Headcount"
title_indexed_sub = (f"CPI-indexed threshold — anchored at $75K in {CPI_ANCHOR_YEAR}, "
                     f"≈$103K in 2026")

def _title_html(main, sub):
    return (f"<b>{main}</b><br>"
            f"<span style='font-size:13px;color:#444;font-weight:normal'>{sub}</span>")

fig12.update_layout(barmode="stack", **base_layout(
    _title_html(title_fixed_main, title_fixed_sub),
    yt="Number of Administrative Staff",
    height=660,
    legend_y=-0.16))
# Stack the toggle buttons ABOVE the title so they don't overlap the subtitle.
# Title sits at the top of the plot area; buttons go above it in the margin.
fig12.update_layout(title=dict(text=_title_html(title_fixed_main, title_fixed_sub),
                                x=0.5, xanchor="center", y=0.93,
                                yanchor="top", font=dict(size=18)))
fig12.update_layout(updatemenus=[dict(
    type="buttons", direction="left",
    x=0.5, xanchor="center", y=1.13, yanchor="top",
    showactive=True, bgcolor="#f4f4f4",
    buttons=[
        dict(label="Fixed $75K threshold", method="update",
             args=[{"visible": [True]*3 + [False]*3},
                   {"title.text": _title_html(title_fixed_main, title_fixed_sub)}]),
        dict(label="CPI-indexed threshold", method="update",
             args=[{"visible": [False]*3 + [True]*3},
                   {"title.text": _title_html(title_indexed_main, title_indexed_sub)}]),
    ],
)])
fig12.add_annotation(
    text=("<i>Robustness check: PA 97-0609's $75K reporting threshold has not been indexed to inflation since the<br>"
          "statute took effect. Toggle to see headcount counting only employees above the CPI-indexed equivalent.</i>"),
    xref="paper", yref="paper", x=0.5, y=-0.30,
    showarrow=False, xanchor="center", yanchor="top",
    font=dict(size=11, color="#666"), align="center",
)
fig12.update_layout(margin=dict(l=70, r=30, t=160, b=140))
write(fig12, "headcount_inflation_adjusted")


# ============================================================
# Print summary
# ============================================================
print("\n=== Summary by Year (with inflation-adjusted) ===")
print(year_total.merge(cpi[["year", "adj_to_2026"]], on="year")
        .assign(total_comp_2026=lambda d: d["total_comp"]*d["adj_to_2026"])
        [["year","total_comp","total_comp_2026","headcount","enrollment"]]
        .to_string(index=False))

print(f"\nRight-sizing scenarios (vs SY25-26 actual ${current_total_comp:,.0f} / {current_total_hc} staff):")
print(f"  D65's own 2016 ratio ({ratio_2016:.2f}/1k):     savings = ${right_size_savings:,.0f} ({hc_to_cut:.0f} fewer staff)")
print(f"  Peer K-8 median ({PEER_RATIO}/1k):           savings = ${right_size_savings_peer:,.0f} ({hc_to_cut_peer:.0f} fewer staff)")
print("\nDone.")
