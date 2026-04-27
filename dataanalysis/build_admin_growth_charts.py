"""
Builds the visualization suite for the D65 Administrator Growth analysis page.

Reads:
  - data/d65_admin_comp_combined.csv  (long-format, all years/categories)
  - data/d65_enrollment_history.csv

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
df = pd.read_csv(DATA / "d65_admin_comp_combined.csv")
enroll = pd.read_csv(DATA / "d65_enrollment_history.csv")[["year", "enrollment"]]

# Aggregate per year x role_class
agg = (df.groupby(["year", "role_class"], as_index=False)
         .agg(headcount=("last_name", "count"),
              total_comp=("total_comp", "sum"),
              total_salary=("total_salary", "sum")))
agg = agg.merge(enroll, on="year", how="left")
agg["headcount_per_1000"] = agg["headcount"] / agg["enrollment"] * 1000
agg["comp_per_1000"]      = agg["total_comp"]   / agg["enrollment"] * 1000
agg["avg_comp"]           = agg["total_comp"]   / agg["headcount"]


def base_layout(title, xt="School Year (ending)", yt="", height=550):
    return dict(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=18)),
        xaxis_title=xt, yaxis_title=yt,
        height=height,
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#eee", dtick=1),
        yaxis=dict(showgrid=True, gridcolor="#eee"),
        margin=dict(l=70, r=30, t=70, b=80),
    )


def write(fig, name):
    out = ASSETS / f"admin_growth_{name}.html"
    fig.write_html(out, include_plotlyjs="cdn", div_id=f"admin_growth_{name}")
    print(f"Wrote {out}")


def add_gap_annotation(fig, y_position=0.92):
    """The Excel + foiagras dataset is complete from 2016-2026, so no gap.
    Helper kept for parity with prior plan, currently unused."""
    return fig


# ------------------------------------------------------------
# Chart 1 — Headcount over time, stacked bar by category
# ------------------------------------------------------------
fig1 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig1.add_trace(go.Bar(
        x=sub["year"], y=sub["headcount"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
fig1.update_layout(barmode="stack", **base_layout(
    "D65 Administrator Headcount Over Time (Stacked by Category)",
    yt="Number of Administrative Staff"))
write(fig1, "headcount_stacked")


# ------------------------------------------------------------
# Chart 2 — Headcount per 1,000 students
# ------------------------------------------------------------
fig2 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig2.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount_per_1000"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y:.2f} per 1k students<extra></extra>",
    ))
# Total
total_per_1k = (agg.groupby("year")
                  .agg(hc=("headcount", "sum"), enroll=("enrollment", "first"))
                  .reset_index())
total_per_1k["per1k"] = total_per_1k["hc"] / total_per_1k["enroll"] * 1000
fig2.add_trace(go.Scatter(
    x=total_per_1k["year"], y=total_per_1k["per1k"], name="<b>All Categories Combined</b>",
    mode="lines+markers",
    line=dict(color="black", width=4, dash="dash"),
    marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: %{y:.2f} per 1k students<extra></extra>",
))
fig2.update_layout(**base_layout(
    "D65 Administrators per 1,000 Students Over Time",
    yt="Administrators per 1,000 Students"))
write(fig2, "headcount_per_1000")


# ------------------------------------------------------------
# Chart 3 — Total compensation over time, stacked
# ------------------------------------------------------------
fig3 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig3.add_trace(go.Bar(
        x=sub["year"], y=sub["total_comp"], name=role,
        marker_color=COLORS[role],
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f}<extra></extra>",
    ))
fig3.update_layout(barmode="stack", **base_layout(
    "D65 Total Administrative Compensation Over Time (Stacked)",
    yt="Total Compensation (Nominal $)"))
fig3.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig3, "comp_stacked")


# ------------------------------------------------------------
# Chart 4 — Total compensation per 1,000 students
# ------------------------------------------------------------
fig4 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig4.add_trace(go.Scatter(
        x=sub["year"], y=sub["comp_per_1000"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} per 1k students<extra></extra>",
    ))
total_comp_per_1k = (agg.groupby("year")
                       .agg(c=("total_comp", "sum"), e=("enrollment", "first"))
                       .reset_index())
total_comp_per_1k["per1k"] = total_comp_per_1k["c"] / total_comp_per_1k["e"] * 1000
fig4.add_trace(go.Scatter(
    x=total_comp_per_1k["year"], y=total_comp_per_1k["per1k"],
    name="<b>All Categories Combined</b>", mode="lines+markers",
    line=dict(color="black", width=4, dash="dash"),
    marker=dict(size=11, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f} per 1k students<extra></extra>",
))
fig4.update_layout(**base_layout(
    "D65 Administrative Compensation per 1,000 Students Over Time",
    yt="Total Comp per 1,000 Students (Nominal $)"))
fig4.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig4, "comp_per_1000")


# ------------------------------------------------------------
# Chart 5 — Average compensation per administrator by category
# ------------------------------------------------------------
fig5 = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig5.add_trace(go.Scatter(
        x=sub["year"], y=sub["avg_comp"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": $%{y:,.0f} avg<extra></extra>",
    ))
fig5.update_layout(**base_layout(
    "Average Total Compensation per Administrator (by Category)",
    yt="Average Total Comp per Person (Nominal $)"))
fig5.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig5, "avg_comp")


# ------------------------------------------------------------
# Chart 6 — Salary vs. benefits composition (TRS Admin only, where we have full breakdown)
#   Stack base salary, TRS contribution, and "everything else" (benefits)
# ------------------------------------------------------------
trs_detail = (df[df["role_class"] == "TRS Admin"]
                .groupby("year", as_index=False)
                .agg(base=("base_salary", "sum"),
                     total_salary=("total_salary", "sum"),
                     total_comp=("total_comp", "sum")))
trs_detail["trs_contribution"] = trs_detail["total_salary"] - trs_detail["base"]
trs_detail["benefits"] = trs_detail["total_comp"] - trs_detail["total_salary"]
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
    "TRS Admin Compensation Breakdown — What's Driving the Cost?",
    yt="Total Cost (Nominal $)"))
fig6.update_yaxes(tickprefix="$", tickformat=",.0f")
write(fig6, "comp_breakdown")


# ------------------------------------------------------------
# Chart 7 — YoY % change: total admin cost vs enrollment (decoupling)
# ------------------------------------------------------------
year_total = (agg.groupby("year")
                 .agg(total_comp=("total_comp", "sum"),
                      headcount=("headcount", "sum"),
                      enrollment=("enrollment", "first"))
                 .reset_index().sort_values("year"))
year_total["comp_yoy_pct"]   = year_total["total_comp"].pct_change() * 100
year_total["hc_yoy_pct"]     = year_total["headcount"].pct_change()  * 100
year_total["enroll_yoy_pct"] = year_total["enrollment"].pct_change() * 100

fig7 = go.Figure()
fig7.add_trace(go.Scatter(
    x=year_total["year"], y=year_total["comp_yoy_pct"], name="Admin Total Comp",
    mode="lines+markers", line=dict(color="#c0392b", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Comp YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_trace(go.Scatter(
    x=year_total["year"], y=year_total["hc_yoy_pct"], name="Admin Headcount",
    mode="lines+markers", line=dict(color="#8e44ad", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Headcount YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_trace(go.Scatter(
    x=year_total["year"], y=year_total["enroll_yoy_pct"], name="Student Enrollment",
    mode="lines+markers", line=dict(color="#16a085", width=3), marker=dict(size=10),
    hovertemplate="<b>%{x}</b><br>Enrollment YoY: %{y:+.1f}%<extra></extra>"))
fig7.add_hline(y=0, line=dict(color="black", width=1, dash="dot"))
fig7.update_layout(**base_layout(
    "Year-over-Year % Change: Admin Costs vs. Student Enrollment",
    yt="YoY % Change"))
fig7.update_yaxes(ticksuffix="%")
write(fig7, "yoy_decoupling")


# ------------------------------------------------------------
# Chart 8 — Year-over-year change in admin comp (delta-only bar chart)
#   Replaces an earlier waterfall: a delta-only chart keeps the y-axis
#   honestly anchored at $0 without large absolute totals dwarfing the
#   year-to-year deltas. The cumulative absolute view is already
#   covered by the comp_stacked chart above on the page.
# ------------------------------------------------------------
yt = year_total[["year", "total_comp"]].sort_values("year").reset_index(drop=True)
yt["delta"] = yt["total_comp"].diff()
deltas = yt.dropna(subset=["delta"]).copy()
deltas["color"] = deltas["delta"].apply(lambda v: "#c0392b" if v >= 0 else "#27ae60")

fig8 = go.Figure()
fig8.add_trace(go.Bar(
    x=deltas["year"], y=deltas["delta"],
    marker_color=deltas["color"],
    text=[f"${v:+,.0f}" for v in deltas["delta"]],
    textposition="outside",
    hovertemplate="<b>SY%{x}</b><br>YoY change: $%{y:+,.0f}<extra></extra>",
    showlegend=False,
))
fig8.add_hline(y=0, line=dict(color="black", width=1))

start_val = yt["total_comp"].iloc[0]
end_val   = yt["total_comp"].iloc[-1]
net       = end_val - start_val
fig8.add_annotation(
    x=yt["year"].iloc[0], y=0,
    text=f"<b>SY{int(yt['year'].iloc[0])-1}-{str(int(yt['year'].iloc[0]))[-2:]} starting total: ${start_val:,.0f}</b>",
    showarrow=False, xanchor="left", yanchor="bottom",
    yshift=-30, bgcolor="#f4f4f4", borderpad=4)
fig8.add_annotation(
    x=yt["year"].iloc[-1], y=0,
    text=(f"<b>SY{int(yt['year'].iloc[-1])-1}-{str(int(yt['year'].iloc[-1]))[-2:]} ending total: ${end_val:,.0f}</b>"
          f"<br>Net change over decade: <b>${net:+,.0f}</b> ({net/start_val*100:+.1f}%)"),
    showarrow=False, xanchor="right", yanchor="bottom",
    yshift=-30, bgcolor="#fdebea", borderpad=4)

fig8.update_layout(**base_layout(
    "Annual Change in Total Administrative Compensation",
    xt="School Year (ending)",
    yt="Year-over-Year Change ($)",
    height=600))
fig8.update_yaxes(tickprefix="$", tickformat=",.0f")
fig8.update_layout(margin=dict(l=70, r=30, t=70, b=160))
write(fig8, "waterfall")


# ------------------------------------------------------------
# Chart 9 — Cabinet trajectory (named individuals)
#   Top-tier cabinet roles tracked across years where they appear
# ------------------------------------------------------------
# Identify cabinet members: roles containing key cabinet titles in TRS Admin
cabinet_keywords = ["SUPERINTENDENT", "CABINET", "ASST SUP", "ASSISTANT SUP",
                    "DEPUTY SUP", "CHIEF FINANCIAL", "CHIEF SCHOOL", "EXECUTIVE DIRECTOR",
                    "EXEC DIRECTOR", "CSBO", "BUSINESS MANAGER", "CHIEF OF",
                    "EXECUTIVE CHIEF"]
df["full_name"] = df["last_name"].str.strip() + ", " + df["first_name"].str.strip()
cab_mask = df["role_class"].isin(["TRS Admin", "IMRF Support Staff"]) & \
    df["position"].astype(str).str.upper().apply(lambda p: any(k in p for k in cabinet_keywords))
cab = df[cab_mask].copy()

# Pick top 8 cabinet members by years-of-presence (so chart isn't overwhelming)
top_cab = (cab.groupby("full_name")["year"].nunique()
              .sort_values(ascending=False).head(10).index.tolist())

fig9 = go.Figure()
palette = ["#c0392b", "#2980b9", "#27ae60", "#e67e22", "#8e44ad",
           "#16a085", "#d35400", "#2c3e50", "#c0c0c0", "#7f8c8d"]
for i, name in enumerate(top_cab):
    sub = cab[cab["full_name"] == name].sort_values("year")
    # Get most recent position for label
    pos = sub.iloc[-1]["position"]
    label = f"{name} — {pos[:40]}"
    fig9.add_trace(go.Scatter(
        x=sub["year"], y=sub["total_comp"], name=label,
        mode="lines+markers",
        line=dict(color=palette[i % len(palette)], width=2.5),
        marker=dict(size=8),
        hovertemplate=f"<b>{name}</b><br>%{{x}}: $%{{y:,.0f}}<br>{pos}<extra></extra>",
    ))
fig9.update_layout(**base_layout(
    "Cabinet & Senior Leadership Compensation Trajectories",
    yt="Total Compensation (Nominal $)",
    height=700))
fig9.update_yaxes(tickprefix="$", tickformat=",.0f")
fig9.update_layout(legend=dict(orientation="h", y=-0.35, x=0, xanchor="left",
                                font=dict(size=10)))
write(fig9, "cabinet_trajectory")


# ------------------------------------------------------------
# Chart 10 — Top 15 highest-paid administrators in SY25-26 (2026)
#   with comparison to their SY21-22 (2022) compensation if present
# ------------------------------------------------------------
y2026 = df[(df["year"] == 2026) & (df["role_class"].isin(["TRS Admin", "IMRF Support Staff"]))].copy()
y2026 = y2026.sort_values("total_comp", ascending=False).head(15).copy()
y2026["full_name"] = y2026["last_name"] + ", " + y2026["first_name"]

# Lookup their 2022 (SY21-22) comp
y2022 = df[df["year"] == 2022].copy()
y2022["full_name"] = y2022["last_name"] + ", " + y2022["first_name"]
lookup = y2022.set_index("full_name")["total_comp"].to_dict()
y2026["comp_2022"] = y2026["full_name"].map(lookup)

# Sort by 2026 comp ascending so largest is at top of horizontal bar
y2026 = y2026.sort_values("total_comp", ascending=True)

fig10 = go.Figure()
fig10.add_trace(go.Bar(
    y=y2026["full_name"] + "<br><span style='color:#888;font-size:10px'>" + y2026["position"].str[:50] + "</span>",
    x=y2026["total_comp"], orientation="h",
    name="SY25-26",
    marker_color="#c0392b",
    text=[f"${v:,.0f}" for v in y2026["total_comp"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>SY25-26: $%{x:,.0f}<extra></extra>",
))
# Overlay markers for 2022 comp
overlay = y2026.dropna(subset=["comp_2022"])
fig10.add_trace(go.Scatter(
    y=overlay["full_name"] + "<br><span style='color:#888;font-size:10px'>" + overlay["position"].str[:50] + "</span>",
    x=overlay["comp_2022"], mode="markers",
    name="SY21-22 (4 yrs prior)",
    marker=dict(color="#34495e", size=14, symbol="diamond",
                line=dict(color="white", width=1)),
    hovertemplate="<b>%{y}</b><br>SY21-22: $%{x:,.0f}<extra></extra>",
))
fig10.update_layout(**base_layout(
    "Top 15 Highest-Paid Administrators in SY25-26 (with SY21-22 Comparison)",
    xt="Total Compensation (Nominal $)", yt="",
    height=750))
fig10.update_xaxes(tickprefix="$", tickformat=",.0f")
fig10.update_layout(margin=dict(l=280, r=80, t=70, b=80))
write(fig10, "top_paid")


# ------------------------------------------------------------
# Bonus Chart — Headcount lines (non-stacked) for direct comparison
# ------------------------------------------------------------
fig_bonus = go.Figure()
for role in ROLE_ORDER:
    sub = agg[agg["role_class"] == role].sort_values("year")
    fig_bonus.add_trace(go.Scatter(
        x=sub["year"], y=sub["headcount"], name=role,
        mode="lines+markers",
        line=dict(color=COLORS[role], width=3),
        marker=dict(size=9),
        hovertemplate="<b>%{x}</b><br>" + role + ": %{y} staff<extra></extra>",
    ))
fig_bonus.update_layout(**base_layout(
    "D65 Administrator Headcount by Category (Lines for Direct Comparison)",
    yt="Number of Administrative Staff"))
write(fig_bonus, "headcount_lines")


# ------------------------------------------------------------
# Print summary
# ------------------------------------------------------------
print("\n=== Summary by Year ===")
print(year_total.to_string(index=False))
print("\nDone.")
