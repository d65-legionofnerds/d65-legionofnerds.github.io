"""
Builds visualizations comparing the size of each D65 8th-grade cohort to the
size of the same students' notional ETHS 9th-grade cohort the following year.

The premise: every June, D65 graduates ~700-900 8th-graders. Every August,
ETHS receives a freshman class. If parents trust D65 to deliver good K-8
education, most D65 8th-graders should continue on to ETHS. If they don't
trust D65, they would be more likely to enroll children K-8 in private schools
and bring them BACK to ETHS for high school — visible as ETHS Grade 9 being
*larger* than the D65 8th-grade cohort the year before.

Reads:  data/d65_to_eths_cohorts.csv
Writes: assets/k8_to_hs_*.html
"""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

D65_COLOR  = "#2980b9"   # blue
ETHS_COLOR = "#c0392b"   # red — high contrast vs D65
GAIN_COLOR = "#e67e22"   # orange — the "external gain" portion

# ------------------------------------------------------------
# Load and derive
# ------------------------------------------------------------
df = pd.read_csv(DATA / "d65_to_eths_cohorts.csv")
# Year shown on charts: D65 8th-grade school year (the cohort)
df["d65_end_year"]  = df["d65_grade8_year"].str[-2:].astype(int) + 2000
df["eths_end_year"] = df["eths_grade9_year"].str[-2:].apply(
    lambda s: 2000 + int(s) if s.isdigit() else None)

# Drop rows where ETHS data isn't yet available
plot_df = df.dropna(subset=["eths_grade9_count"]).copy()
plot_df["eths_grade9_count"] = plot_df["eths_grade9_count"].astype(int)
plot_df["external_gain"]     = plot_df["eths_grade9_count"] - plot_df["d65_grade8_count"]
plot_df["gain_pct"]          = plot_df["external_gain"] / plot_df["d65_grade8_count"] * 100
plot_df["ratio"]             = plot_df["eths_grade9_count"] / plot_df["d65_grade8_count"]
plot_df["cohort_label"]      = plot_df["d65_grade8_year"] + " → " + plot_df["eths_grade9_year"]


def base_layout(title, xt="School Year (D65 8th-grade cohort, then ETHS 9th-grade)", yt="", height=550, legend_y=-0.20):
    return dict(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=18)),
        xaxis_title=xt, yaxis_title=yt,
        height=height,
        legend=dict(orientation="h", y=legend_y, x=0.5, xanchor="center"),
        plot_bgcolor="white",
        xaxis=dict(showgrid=True, gridcolor="#eee"),
        yaxis=dict(showgrid=True, gridcolor="#eee"),
        margin=dict(l=70, r=30, t=70, b=110),
    )


def write(fig, name):
    out = ASSETS / f"k8_to_hs_{name}.html"
    fig.write_html(out, include_plotlyjs="cdn", div_id=f"k8_to_hs_{name}")
    print(f"Wrote {out}")


# ------------------------------------------------------------
# Chart 1 — Side-by-side cohort comparison
# ------------------------------------------------------------
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=plot_df["cohort_label"], y=plot_df["d65_grade8_count"],
    name="D65 8th grade<br>(June graduating)",
    marker_color=D65_COLOR,
    text=plot_df["d65_grade8_count"], textposition="outside",
    hovertemplate="<b>%{x}</b><br>D65 8th grade: %{y}<extra></extra>",
))
fig1.add_trace(go.Bar(
    x=plot_df["cohort_label"], y=plot_df["eths_grade9_count"],
    name="ETHS 9th grade<br>(following August)",
    marker_color=ETHS_COLOR,
    text=plot_df["eths_grade9_count"], textposition="outside",
    hovertemplate="<b>%{x}</b><br>ETHS 9th grade: %{y}<extra></extra>",
))
fig1.update_layout(barmode="group", **base_layout(
    "D65 8th-grade Cohort vs. ETHS 9th-grade Cohort (one year later)",
    yt="Students enrolled (Sept 30 / Oct 1)"))
fig1.update_layout(xaxis=dict(tickangle=-45))
write(fig1, "cohort_side_by_side")


# ------------------------------------------------------------
# Chart 2 — External gain (ETHS 9th – D65 8th) over time
#   absolute counts, with a secondary y-axis for percentage
# ------------------------------------------------------------
fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(go.Bar(
    x=plot_df["cohort_label"], y=plot_df["external_gain"],
    name="Net external gain (students)",
    marker_color=GAIN_COLOR,
    text=[f"+{v}" for v in plot_df["external_gain"]],
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>External gain: +%{y} students<extra></extra>",
), secondary_y=False)
fig2.add_trace(go.Scatter(
    x=plot_df["cohort_label"], y=plot_df["gain_pct"],
    name="Gain as % of D65 8th-grade cohort",
    mode="lines+markers",
    line=dict(color="#34495e", width=3, dash="dot"),
    marker=dict(size=10, symbol="diamond"),
    hovertemplate="<b>%{x}</b><br>Gain as %% of D65 cohort: %{y:.1f}%<extra></extra>",
), secondary_y=True)
fig2.update_yaxes(title_text="Net external gain (students)", secondary_y=False)
fig2.update_yaxes(title_text="Gain as % of D65 cohort", ticksuffix="%", secondary_y=True)
fig2.update_layout(**base_layout(
    "Net External Gain at the K-8 → High School Transition",
    yt=""))
fig2.update_layout(xaxis=dict(tickangle=-45),
                   legend=dict(orientation="h", y=-0.25, x=0.5, xanchor="center"))
write(fig2, "external_gain_trend")


# ------------------------------------------------------------
# Chart 3 — Stacked composition of ETHS 9th grade
#   "Came from D65 (estimate)" + "External gain" = ETHS 9th total
# ------------------------------------------------------------
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=plot_df["cohort_label"], y=plot_df["d65_grade8_count"],
    name="Implied D65→ETHS continuers",
    marker_color=D65_COLOR,
    hovertemplate="<b>%{x}</b><br>D65→ETHS continuers (assumed): %{y}<extra></extra>",
))
fig3.add_trace(go.Bar(
    x=plot_df["cohort_label"], y=plot_df["external_gain"],
    name="External gain (private K-8 returners + transfers)",
    marker_color=GAIN_COLOR,
    text=[f"+{v}" for v in plot_df["external_gain"]],
    textposition="inside",
    hovertemplate="<b>%{x}</b><br>External gain: +%{y}<extra></extra>",
))
# Add total labels on top of each stack
totals = plot_df["eths_grade9_count"].tolist()
fig3.add_trace(go.Scatter(
    x=plot_df["cohort_label"], y=totals,
    mode="text",
    text=[str(v) for v in totals],
    textposition="top center",
    textfont=dict(size=12, color="#222"),
    showlegend=False,
    hoverinfo="skip",
))
fig3.update_layout(barmode="stack", **base_layout(
    "Composition of Each ETHS Freshman Class",
    yt="ETHS 9th-grade enrollment"))
fig3.update_layout(xaxis=dict(tickangle=-45))
write(fig3, "eths_composition")


# ------------------------------------------------------------
# Chart 4 — Trend in the gap (regression-style line chart)
# ------------------------------------------------------------
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=plot_df["cohort_label"], y=plot_df["gain_pct"],
    mode="lines+markers",
    line=dict(color=GAIN_COLOR, width=4),
    marker=dict(size=12, color=GAIN_COLOR),
    name="External gain as % of D65 cohort",
    hovertemplate="<b>%{x}</b><br>%{y:.1f}%<extra></extra>",
))
# Mean line for reference
mean_pct = plot_df["gain_pct"].mean()
fig4.add_hline(y=mean_pct, line=dict(color="#999", width=1, dash="dash"),
               annotation_text=f"10-yr mean: {mean_pct:.1f}%",
               annotation_position="right")
fig4.update_layout(**base_layout(
    "Has the K-8 Trust Gap Grown? — External Gain as % of D65 Cohort, by Year",
    yt="External gain as % of D65 cohort",
    height=550))
fig4.update_yaxes(ticksuffix="%")
fig4.update_layout(xaxis=dict(tickangle=-45))
write(fig4, "trend_pct")


# ------------------------------------------------------------
# Print summary (ASCII-only labels for Windows console safety)
# ------------------------------------------------------------
ascii_summary = plot_df.copy()
ascii_summary["cohort_label"] = ascii_summary["cohort_label"].str.replace("→", "->", regex=False)
print("\n=== Cohort summary ===")
print(ascii_summary[["cohort_label", "d65_grade8_count", "eths_grade9_count",
                     "external_gain", "gain_pct"]].to_string(index=False))
print(f"\n10-year mean external gain: {plot_df['external_gain'].mean():.0f} students "
      f"({mean_pct:.1f}% of D65 cohort)")
min_label = ascii_summary.loc[plot_df['external_gain'].idxmin(), 'cohort_label']
max_label = ascii_summary.loc[plot_df['external_gain'].idxmax(), 'cohort_label']
print(f"Min: {plot_df['external_gain'].min()} ({plot_df['gain_pct'].min():.1f}%) in {min_label}")
print(f"Max: {plot_df['external_gain'].max()} ({plot_df['gain_pct'].max():.1f}%) in {max_label}")
print("Done.")
