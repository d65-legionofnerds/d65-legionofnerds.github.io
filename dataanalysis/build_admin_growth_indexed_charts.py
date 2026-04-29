"""
Builds the visualization suite for the **CPI-indexed** D65 Administrator Growth
analysis page (admin-growth-indexed.md).

This is a parallel build to build_admin_growth_charts.py. Where the original
counts every employee whose comp package exceeds the unindexed $75K PA-97-0609
threshold, this script counts only employees above the year-specific
inflation-indexed equivalent of $75K-2016 (≈$103K in 2026). All charts use
real (2026) dollars throughout — there are no nominal-vs-real toggles.

The indexed-eligible filter applies uniformly to every role class for
consistency. TRS Admin and Principals are unaffected in most years (their
comp ranges exceed the indexed threshold), but using the same filter
everywhere keeps the page methodologically consistent.

Reads:
  - data/d65_admin_comp_combined.csv  (long-format, all years/categories)
  - data/d65_enrollment_history.csv
  - data/cpi_history.csv               (BLS CPI-U; 2016 anchor)
  - data/d65_recent_cuts.csv

Writes HTML files to assets/admin_growth_indexed_*.html for embedding in
dataanalysis/admin-growth-indexed.md.
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

CPI_BASE_YEAR = 2026          # all dollars expressed in 2026 $
CPI_ANCHOR_YEAR = 2016        # threshold-indexing anchor

# ------------------------------------------------------------
# Load and prepare
# ------------------------------------------------------------
df_all = pd.read_csv(DATA / "d65_admin_comp_combined.csv")
enroll = pd.read_csv(DATA / "d65_enrollment_history.csv")[["year", "enrollment"]]
cpi    = pd.read_csv(DATA / "cpi_history.csv")[["year", "cpi_u"]]
cuts   = pd.read_csv(DATA / "d65_recent_cuts.csv")

cpi_base   = cpi.loc[cpi["year"] == CPI_BASE_YEAR,   "cpi_u"].iloc[0]
cpi_anchor = cpi.loc[cpi["year"] == CPI_ANCHOR_YEAR, "cpi_u"].iloc[0]
cpi["adj_to_2026"]      = cpi_base / cpi["cpi_u"]
cpi["threshold_indexed"] = 75000 * cpi["cpi_u"] / cpi_anchor

# Tag every row with its year-specific indexed threshold and real comp,
# then keep only rows that meet the indexed threshold.
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
    out = ASSETS / f"admin_growth_indexed_{name}.html"
    fig.write_html(out, include_plotlyjs="cdn", div_id=f"admin_growth_indexed_{name}")
    print(f"Wrote {out}")


# ============================================================
# Chart 1 — Headcount over time, stacked by role class (indexed-eligible)
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
    "D65 Admin Headcount — Indexed Threshold (Stacked by Category)",
    yt="Number of Administrative Staff (above CPI-indexed $75K-2016)"))
write(fig1, "headcount_stacked")


# ============================================================
# Chart 2 — Headcount per 1,000 students (indexed-eligible)
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
    "D65 Admin per 1,000 Students Over Time — Indexed Threshold",
    yt="Administrators per 1,000 Students (indexed-eligible)"))
write(fig2, "headcount_per_1000")


# ============================================================
# Chart 3 — Headcount lines (non-stacked direct comparison)
# ============================================================
fig3 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig3.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
fig3.update_layout(**base_layout(
    "D65 Admin Headcount by Category — Indexed Threshold (Lines for Direct Comparison)",
    yt="Number of Administrative Staff"))
write(fig3, "headcount_lines")


# ============================================================
# Chart 4 — Total real comp over time, stacked (indexed-eligible)
# ============================================================
fig4 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig4.add_trace(go.Bar(
        x=sub["year"], y=sub["total_comp_real"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f}<extra></extra>",
    ))
fig4.update_layout(barmode="stack", **base_layout(
    "Total Admin Compensation Over Time — Indexed Eligible (2026 $)",
    yt="Total Compensation, Indexed-Eligible Only (2026 $)"))
fig4.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig4, "comp_stacked")


# ============================================================
# Chart 5 — Real total comp per 1,000 students (indexed-eligible)
# ============================================================
fig5 = go.Figure()
total_comp_per_1k = (agg.groupby("year")
                       .agg(c=("total_comp", "sum"),
                            e=("enrollment", "first"),
                            adj=("adj_to_2026", "first"))
                       .reset_index())
total_comp_per_1k["per1k_real"] = (total_comp_per_1k["c"] / total_comp_per_1k["e"]
                                   * 1000 * total_comp_per_1k["adj"])

for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig5.add_trace(go.Scatter(
        x=sub["year"], y=sub["comp_per_1000_real"], name=role,
        mode="lines+markers", line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} per 1k students<extra></extra>",
    ))
fig5.add_trace(go.Scatter(
    x=total_comp_per_1k["year"], y=total_comp_per_1k["per1k_real"],
    name="<b>All Categories Combined</b>", mode="lines+markers",
    line=dict(color="black", width=4, dash="dash"), marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f} per 1k students<extra></extra>",
))
fig5.update_layout(**base_layout(
    "Admin Comp per 1,000 Students — Indexed Eligible (2026 $)",
    yt="Total Comp per 1,000 Students (2026 $)"))
fig5.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig5, "comp_per_1000")


# ============================================================
# Chart 6 — Real avg comp per administrator vs 2016 real baseline
# Under indexed framework this should be roughly flat or declining.
# ============================================================
fig6 = go.Figure()
years = sorted(agg["year"].unique())
baseline_2016_real = (agg[agg["year"] == CPI_ANCHOR_YEAR]
                      .assign(avg_comp_real=lambda d: d["avg_comp"] * d["adj_to_2026"])
                      .set_index("role_class")["avg_comp_real"])
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig6.add_trace(go.Scatter(
        x=sub["year"], y=sub["avg_comp_real"], name=f"{role}",
        mode="lines+markers", line=dict(color=COLORS[role], width=3), marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} avg (2026 $)<extra></extra>",
    ))
for role in ROLE_ORDER:
    if role not in baseline_2016_real.index:
        continue
    baseline = baseline_2016_real[role]
    fig6.add_trace(go.Scatter(
        x=years, y=[baseline] * len(years),
        name=f"{role} — 2016 real baseline",
        mode="lines",
        line=dict(color=COLORS[role], width=2, dash="dot"),
        opacity=0.55,
        hovertemplate="<b>%{x}</b><br>" + role + " 2016 real baseline: $%{y:,.0f}<extra></extra>",
    ))
fig6.update_layout(**base_layout(
    "Avg Comp per Administrator (Indexed-Eligible) vs 2016 Real Baseline (2026 $)",
    yt="Average Total Comp per Person (2026 $)"))
fig6.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig6, "avg_comp")


# ============================================================
# Chart 7 — TRS Admin breakdown (2026 $), indexed-eligible only
# Filter applies; in practice almost all TRS admins exceed the indexed
# threshold so the values closely match the parent build, with the
# exception of one outlier in 2024.
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
fig7 = go.Figure()
fig7.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["base"],
                      name="Base Salary", marker_color="#34495e",
                      hovertemplate="<b>%{x}</b><br>Base: $%{y:,.0f}<extra></extra>"))
fig7.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["trs_contribution"],
                      name="TRS / Retirement Contribution", marker_color="#e67e22",
                      hovertemplate="<b>%{x}</b><br>TRS: $%{y:,.0f}<extra></extra>"))
fig7.add_trace(go.Bar(x=trs_detail["year"], y=trs_detail["benefits"],
                      name="Health/Dental/Life/Annuity/Car",
                      marker_color="#16a085",
                      hovertemplate="<b>%{x}</b><br>Benefits: $%{y:,.0f}<extra></extra>"))
fig7.update_layout(barmode="stack", **base_layout(
    "TRS Admin Compensation Breakdown — Indexed Eligible (2026 $)",
    yt="Total Cost (2026 $)"))
fig7.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig7, "comp_breakdown")


# ============================================================
# Chart 8 — YoY % change: indexed real comp · indexed headcount · enrollment
# ============================================================
year_total = (agg.groupby("year")
                 .agg(total_comp_real=("total_comp_real", "sum"),
                      headcount=("headcount", "sum"),
                      enrollment=("enrollment", "first"))
                 .reset_index().sort_values("year"))
year_total["comp_yoy_pct"]   = year_total["total_comp_real"].pct_change() * 100
year_total["hc_yoy_pct"]     = year_total["headcount"].pct_change()  * 100
year_total["enroll_yoy_pct"] = year_total["enrollment"].pct_change() * 100

fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=year_total["year"], y=year_total["comp_yoy_pct"],
    name="Admin Total Comp (real, indexed-eligible)", mode="lines+markers",
    line=dict(color="#c0392b", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Real comp YoY: %{y:+.1f}%<extra></extra>"))
fig8.add_trace(go.Scatter(x=year_total["year"], y=year_total["hc_yoy_pct"],
    name="Admin Headcount (indexed-eligible)", mode="lines+markers",
    line=dict(color="#8e44ad", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Headcount YoY: %{y:+.1f}%<extra></extra>"))
fig8.add_trace(go.Scatter(x=year_total["year"], y=year_total["enroll_yoy_pct"],
    name="Student Enrollment", mode="lines+markers",
    line=dict(color="#16a085", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Enrollment YoY: %{y:+.1f}%<extra></extra>"))
fig8.add_hline(y=0, line=dict(color="black", width=1, dash="dot"))
fig8.update_layout(**base_layout(
    "YoY % Change — Indexed-Eligible Admin vs Student Enrollment",
    yt="YoY % Change"))
fig8.update_yaxes(ticksuffix="%")
write(fig8, "yoy_decoupling")


# ============================================================
# Chart 9 — Annual change in indexed-eligible real total comp
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

fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=deltas["year"], y=deltas["delta"],
    marker_color=deltas["color"],
    text=[f"${v:+,.0f}" for v in deltas["delta"]],
    textposition="outside",
    hovertemplate="<b>SY%{x}</b><br>YoY change: $%{y:+,.0f} (2026 $)<extra></extra>",
    showlegend=False,
))
fig9.add_hline(y=0, line=dict(color="black", width=1))
subtitle = (f"<span style='font-size:13px;color:#444'>"
            f"{start_year_label} starting total: ${start_val:,.0f} (2026 $)"
            f"  •  {end_year_label} ending total: ${end_val:,.0f} (2026 $)"
            f"  •  Net change: ${net:+,.0f} ({net/start_val*100:+.1f}%)"
            f"</span>")
fig9.update_layout(**base_layout(
    f"Annual Change in Indexed-Eligible Admin Compensation (2026 $)<br>{subtitle}",
    xt="School Year (ending)",
    yt="Year-over-Year Change (2026 $)",
    height=600))
fig9.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig9, "waterfall")


# ============================================================
# Chart 10 — IMRF role categories (SY24-25 and SY25-26 only),
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
IMRF_CATEGORIES_YEARS = [2025, 2026]
imrf_by_yr = (imrf_roles[imrf_roles["year"].isin(IMRF_CATEGORIES_YEARS)]
              .groupby(["year", "bucket"], as_index=False)
              .size().rename(columns={"size": "n"}))

fig10 = go.Figure()
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
    fig10.add_trace(go.Bar(
        x=sub["year"], y=sub["n"], name=b,
        marker_color=palette[i % len(palette)],
        hovertemplate="<b>%{x}</b><br>" + b + ": %{y}<extra></extra>",
    ))
fig10.update_layout(barmode="stack", **base_layout(
    "Indexed-Eligible IMRF Support Staff by Role Category (SY24-25 and SY25-26)",
    yt="Number of Staff", height=600,
    legend_y=-0.30))
fig10.update_xaxes(type="category")
write(fig10, "imrf_categories")


# ============================================================
# Chart 11 — Right-sizing comparison (indexed framework)
# ============================================================
agg_2026 = agg[agg["year"] == 2026].copy()
agg_2016 = agg[agg["year"] == 2016].copy()

current_total_hc = agg_2026["headcount"].sum()                    # 94 indexed-eligible
current_total_comp_real = agg_2026["total_comp_real"].sum()       # ~$14.85M
current_enroll = agg_2026["enrollment"].iloc[0]                   # 5625
ratio_2016 = (agg_2016["headcount"].sum()
              / agg_2016["enrollment"].iloc[0] * 1000)            # ~10.0/1k (indexed = fixed in 2016)

# Indexed-eligible avg real comp in 2026 (~$158K)
avg_comp_2026_indexed = current_total_comp_real / current_total_hc

# 2016-2019 indexed avg headcount (group member's "moderate" anchor)
hc_2016_19_indexed = (agg.groupby("year")["headcount"].sum()
                        .loc[2016:2019].mean())

# Scenarios
scenarios = []

# Moderate: 2016-2019 indexed avg
target_moderate = round(hc_2016_19_indexed)
cuts_moderate = max(current_total_hc - target_moderate, 0)
scenarios.append({
    "label": ("Moderate: bring indexed-eligible admin to 2016–19 average"
              "<br>(~81 admin, ~13 cuts)"),
    "savings": cuts_moderate * avg_comp_2026_indexed,
    "color": "#e74c3c",   # lighter red
})

# Peer K-8 median 12/1k applied to indexed framework
PEER_RATIO = 12.0
target_peer = PEER_RATIO * current_enroll / 1000
cuts_peer = max(current_total_hc - target_peer, 0)
scenarios.append({
    "label": ("Right-size to peer K-8 median (~12/1k students)"
              "<br>(~68 admin, ~26 cuts)"),
    "savings": cuts_peer * avg_comp_2026_indexed,
    "color": "#c0392b",   # red
})

# D65's own 2016 indexed ratio
target_2016 = ratio_2016 * current_enroll / 1000
cuts_2016 = max(current_total_hc - target_2016, 0)
scenarios.append({
    "label": (f"Right-size to D65's own 2016 indexed ratio (~{ratio_2016:.0f}/1k students)"
              f"<br>(~{int(round(target_2016))} admin, ~{int(round(cuts_2016))} cuts)"),
    "savings": cuts_2016 * avg_comp_2026_indexed,
    "color": "#922b21",   # darker red
})

# District's April 20, 2026 admin proposal — kept at $8.3M (their actual workforce math).
# This is the "what if you also cut sub-indexed admin" empirical anchor — included for
# context, in orange so it visually reads as separate from Legion's right-sizing scenarios.
DISTRICT_PROPOSAL = 8_287_312
scenarios.append({
    "label": ("District's April 20, 2026 admin-cut proposal"
              "<br>(22 admins + 42 non-union support, missed FY27 deadline)"),
    "savings": DISTRICT_PROPOSAL,
    "color": "#e67e22",
})

# Recent enacted/proposed cuts (from CSV); skip superseded scenarios
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
mdf["label_fmt"] = mdf["savings"].apply(lambda v: f"${v/1e6:,.2f}M" if v >= 1e6
                                         else (f"${v/1e3:,.0f}K" if v > 0 else "$0"))

fig11 = go.Figure()
fig11.add_trace(go.Bar(
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
fig11.update_layout(**base_layout(
    "Annual Savings: Recent Cuts vs. Admin Right-Sizing (Indexed Framework)",
    xt="",
    yt="",
    height=720))
fig11.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
fig11.add_annotation(
    text=("<i>Dark grey: District's revised Dec 2025 SDRP figures.<br>"
          "Orange: District's April 20, 2026 admin-cut proposal (sized at workforce avg, includes sub-indexed staff).<br>"
          "Red shades: Legion right-sizing scenarios under indexed-eligible framework.</i>"),
    xref="paper", yref="paper", x=0, y=-0.02,
    showarrow=False, xanchor="left", yanchor="top",
    font=dict(size=11, color="#666"), align="left",
)
fig11.update_layout(margin=dict(l=320, r=80, t=70, b=110))
write(fig11, "right_sizing_comparison")


# ============================================================
# Print summary
# ============================================================
print("\n=== Summary by year (indexed-eligible) ===")
print(year_total[["year","total_comp_real","headcount","enrollment"]].round(0).to_string(index=False))

print(f"\n=== Right-sizing scenarios (indexed framework) ===")
print(f"  Current (2026): {int(current_total_hc)} indexed-eligible admin, "
      f"${current_total_comp_real:,.0f} total real comp, "
      f"avg ${avg_comp_2026_indexed:,.0f}/person, {current_total_hc/current_enroll*1000:.2f}/1k")
print(f"  Moderate (2016-19 avg, target {target_moderate}): "
      f"cut {int(cuts_moderate)}, save ${cuts_moderate*avg_comp_2026_indexed:,.0f}")
print(f"  Peer median (12/1k, target {int(round(target_peer))}): "
      f"cut {int(round(cuts_peer))}, save ${cuts_peer*avg_comp_2026_indexed:,.0f}")
print(f"  D65 2016 ratio ({ratio_2016:.2f}/1k, target {int(round(target_2016))}): "
      f"cut {int(round(cuts_2016))}, save ${cuts_2016*avg_comp_2026_indexed:,.0f}")
print(f"  District's April 20 proposal: ${DISTRICT_PROPOSAL:,}")

print("\nDone.")
