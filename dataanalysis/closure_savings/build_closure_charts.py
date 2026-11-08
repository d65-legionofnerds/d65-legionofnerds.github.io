"""
Builds the Kingsley / Bessie Rhodes closure-savings charts (Plotly HTML for iframe embedding,
same pattern as admin_growth_v2/).

Run after export_tracker.py, assemble_fy25.py and normalize.py:

    python build_closure_charts.py

Reads  data/normalized.csv, data/monthly.csv
Writes assets/closure_*.html

Palette: dataviz reference palette. Blue = savings, red = costs went up (the diverging pair),
warm grays for context. Status is never colour-only: every verdict carries a symbol and a word,
and low-confidence lines are hollow markers.
"""
import sys
import textwrap
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).parent
DATA, ASSETS = ROOT / "data", ROOT.parent / "assets"
ASSETS.mkdir(exist_ok=True)

# write_html adds each chart's phone layout (layout.meta.narrow); see tools/patch_plotly_layout.py.
sys.path.insert(0, str(ROOT.parent.parent / "tools"))
from patch_plotly_layout import write_html as write_chart_html  # noqa: E402

INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#fcfcfb"
BLUE, RED, ORANGE = "#2a78d6", "#e34948", "#eb6834"
GHOST, GHOST_LINE = "#e6e5de", "#b9b8ae"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

norm = pd.read_csv(DATA / "normalized.csv")
monthly = pd.read_csv(DATA / "monthly.csv")
N27 = monthly[monthly.fy == 27].fiscal_month.nunique()
MONTHS = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]


def k(v):
    """$ thousands with sign, e.g. +$291K / -$134K."""
    s = "+" if v >= 0 else "−"
    return f"{s}${abs(v) / 1000:,.0f}K"


def m(v):
    s = "+" if v >= 0 else "−"
    return f"{s}${abs(v) / 1e6:,.2f}M"


def base_layout(title, subtitle, height, **kw):
    lay = dict(
        title=dict(text=f"<b>{title}</b><br><span style='font-size:13px;color:{INK2}'>{subtitle}</span>",
                   x=0.0, xanchor="left", y=1 - 22 / height, yanchor="top"),
        font=dict(family=FONT, size=13, color=INK),
        paper_bgcolor=SURFACE, plot_bgcolor=SURFACE, height=height,
        hoverlabel=dict(bgcolor="white", font=dict(family=FONT, size=12, color=INK), bordercolor=AXIS),
        margin=dict(l=20, r=20, t=110, b=70),
    )
    lay.update(kw)
    return lay


def save(fig, name, narrow=None, restyle=None):
    write_chart_html(fig, ASSETS / f"closure_{name}.html", narrow=narrow, restyle=restyle,
                     include_plotlyjs="cdn", div_id=f"closure_{name}",
                     config=dict(displaylogo=False, modeBarButtonsToRemove=["lasso2d", "select2d"],
                                 responsive=True))
    print("wrote", f"closure_{name}.html")


def wrap(text, width):
    return "<br>".join(textwrap.wrap(text, width, break_long_words=False))


def phone_title(title, subtitle, height, size=16, sub_width=46):
    """Phone-layout values for the title: smaller, wrapped, with the top margin to match."""
    main = wrap(title, 30)
    sub = wrap(subtitle.replace("<br>", " "), sub_width)
    lines = main.count("<br>") + sub.count("<br>") + 2
    return {"title.text": f"<b>{main}</b><br><span style='font-size:12px;color:{INK2}'>{sub}</span>",
            "title.font.size": size, "title.y": 1 - 18 / height,
            "margin.t": 18 + lines * round(size * 1.3) + 14}


NEUTRAL = "#6e6d68"
VERDICT_COLOR = {"On track or better": BLUE, "Partly there": BLUE, "No sign yet": NEUTRAL, "Costs went up": RED}
VERDICT_ICON = {"On track or better": "✓", "Partly there": "◐", "No sign yet": "–",
                "Costs went up": "▲"}

# =============================================================================================
# 1. Scorecard: promised vs. what the FY27 budget shows, one row per line item
# =============================================================================================
people = norm[norm.kind == "Personnel"].sort_values("projected", ascending=False)
ops = norm[norm.kind != "Personnel"].sort_values("projected", ascending=False)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.07,
                    row_heights=[len(people), len(ops)],
                    subplot_titles=("PEOPLE  (salary lines)", "BUILDINGS, UTILITIES & SUPPLIES"))
fig.update_annotations(font=dict(size=12, color=INK2), xanchor="left", x=0)

for row, df in ((1, people), (2, ops)):
    yref = "y" if row == 1 else "y2"
    fig.add_trace(go.Bar(
        x=df.projected / 1000, y=df.category, orientation="h", width=0.62,
        marker=dict(color=GHOST, line=dict(color=GHOST_LINE, width=1)),
        hoverinfo="skip", showlegend=False), row=row, col=1)
    for _, r in df.iterrows():
        color = VERDICT_COLOR[r.verdict]
        fig.add_trace(go.Scatter(
            x=[r.norm_savings_lo / 1000, r.norm_savings_hi / 1000], y=[r.category, r.category],
            mode="lines", line=dict(color=color, width=9), hoverinfo="skip", showlegend=False),
            row=row, col=1)
        icon = VERDICT_ICON[r.verdict]
        fig.add_annotation(
            xref="paper", x=1.01, yref=yref, y=r.category, xanchor="left", showarrow=False, align="left",
            text=(f"<b>{icon} {r.verdict}</b><br>"
                  f"<span style='color:{INK2}'>{k(r.norm_savings_lo)} to {k(r.norm_savings_hi)}</span>"),
            font=dict(size=12, color=INK))
    hover = [
        (f"<b>{r.category}</b><br>"
         f"District projected savings: ${r.projected:,.0f}  "
         f"(Kingsley ${r.proj_kingsley:,.0f} + Rhodes ${r.proj_rhodes:,.0f})<br>"
         f"FY26 actual spend: ${r.fy26_actual:,.0f}<br>"
         f"FY27 budget: ${r.fy27_budget:,.0f}<br>"
         f"Raw change in budget (FY26 budget − FY27 budget): {k(r.raw_savings)}<br>"
         f"Assumed cost growth with no closures: {r.g_lo * 100:.1f}% to {r.g_hi * 100:.1f}%<br>"
         f"<b>Estimated savings after raises/inflation: {k(r.norm_savings_lo)} to {k(r.norm_savings_hi)}</b><br>"
         f"Confidence in this line: <b>{r.confidence}</b> – {r.confidence_reason}<br>"
         f"Budget line(s): {r.proxy}")
        for _, r in df.iterrows()]
    fig.add_trace(go.Scatter(
        x=df.norm_savings_mid / 1000, y=df.category, mode="markers", text=hover,
        hovertemplate="%{text}<extra></extra>", showlegend=False,
        marker=dict(size=15, symbol="circle",
                    color=[SURFACE if c == "Low" else VERDICT_COLOR[v] for c, v in zip(df.confidence, df.verdict)],
                    line=dict(width=2.5, color=[VERDICT_COLOR[v] for v in df.verdict]))),
        row=row, col=1)

# manual legend (dummy traces)
for name, trace in [
    ("District's projected savings", go.Bar(x=[None], y=[None], marker=dict(color=GHOST, line=dict(color=GHOST_LINE, width=1)))),
    ("Estimated savings after raises & inflation (range)", go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=BLUE, width=9))),
    ("No clear sign either way", go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=NEUTRAL, width=9))),
    ("Costs went up instead", go.Scatter(x=[None], y=[None], mode="lines", line=dict(color=RED, width=9))),
    ("Hollow dot = low-confidence line", go.Scatter(x=[None], y=[None], mode="markers",
                                                    marker=dict(size=13, color=SURFACE, line=dict(color=INK2, width=2.5)))),
]:
    trace.update(name=name, showlegend=True)
    fig.add_trace(trace, row=1, col=1)

fig.update_xaxes(range=[-450, 760], tickvals=[-400, -200, 0, 200, 400, 600],
                 ticktext=["−$400K", "−$200K", "$0", "$200K", "$400K", "$600K"], gridcolor=GRID, zeroline=True,
                 zerolinecolor=INK2, zerolinewidth=1.2, linecolor=AXIS, tickfont=dict(color=MUTED))
fig.update_xaxes(title_text="$ thousands per year  (right of zero = savings, left = costs went up)",
                 title_font=dict(size=12, color=INK2), row=2, col=1)
fig.update_yaxes(autorange="reversed", showgrid=False, linecolor=AXIS, tickfont=dict(color=INK, size=13))
SC_TITLE = "Kingsley + Rhodes closures: what the FY27 budget shows, line by line"
SC_SUB = ("Per line item, per year. The colored bar is a range because FY27 raises are not published by group;<br>"
          "it assumes spending would have grown with raises/inflation had the schools stayed open.")
fig.update_layout(**base_layout(
    SC_TITLE, SC_SUB,
    1010, margin=dict(l=20, r=235, t=135, b=90),
    legend=dict(orientation="h", x=0, y=-0.085, xanchor="left", font=dict(size=12, color=INK2),
                bgcolor="rgba(0,0,0,0)"),
    bargap=0.25, hovermode="closest"))
# Phone layout: the same chart, compressed: wrapped line-item labels, smaller verdict notes in a
# narrower right margin, three x ticks, and the legend at the bottom of the figure.
SC_TICKS = dict(tickvals=[-400, 0, 400], ticktext=["−$400K", "$0", "$400K"])
sc_phone = {**phone_title(SC_TITLE, SC_SUB, 1010),
            "margin.l": 4, "margin.r": 100, "margin.b": 150,
            "yaxis.tickvals": list(people.category), "yaxis.ticktext": [wrap(c, 14) for c in people.category],
            "yaxis2.tickvals": list(ops.category), "yaxis2.ticktext": [wrap(c, 14) for c in ops.category],
            "yaxis.tickfont.size": 10, "yaxis2.tickfont.size": 10,
            "xaxis.tickvals": SC_TICKS["tickvals"], "xaxis.ticktext": SC_TICKS["ticktext"],
            "xaxis2.tickvals": SC_TICKS["tickvals"], "xaxis2.ticktext": SC_TICKS["ticktext"],
            "xaxis.tickangle": 0, "xaxis2.tickangle": 0,
            "xaxis2.title.text": "$ thousands per year<br>(right of zero = savings, left = costs went up)",
            "legend.yref": "container", "legend.y": 0, "legend.yanchor": "bottom", "legend.font.size": 10}
for i, a in enumerate(fig.layout.annotations):
    if a.x == 1.01:                        # the verdict notes beside each line item
        sc_phone[f"annotations[{i}].font.size"] = 9.5
        sc_phone[f"annotations[{i}].x"] = 1.02
save(fig, "scorecard", narrow=sc_phone)

# =============================================================================================
# 2. Headline: projected vs. visible, all items vs. cleaner-signal items
# =============================================================================================
clean = norm[norm.confidence == "Higher"]
rows = [  # label, kind, lo, hi
    ("District's projection<br>(all 17 line items)", "proj", 0, norm.projected.sum()),
    ("What the FY27 budget shows<br>(all 17 items, after raises & inflation)", "range",
     norm.norm_savings_lo.sum(), norm.norm_savings_hi.sum()),
    (f"Projection for the {len(clean)} items with<br>cleaner budget lines", "proj", 0, clean.projected.sum()),
    (f"What the FY27 budget shows<br>({len(clean)} cleaner items, after raises & inflation)", "range",
     clean.norm_savings_lo.sum(), clean.norm_savings_hi.sum()),
]
fig = go.Figure()
for i, (label, kind, lo, hi) in enumerate(rows):
    if kind == "proj":
        fig.add_trace(go.Bar(y=[label], x=[hi / 1e6], orientation="h", width=0.5,
                             marker=dict(color=GHOST, line=dict(color=GHOST_LINE, width=1)),
                             text=[f"<b>${hi / 1e6:,.2f}M</b>"], textposition="outside", cliponaxis=False,
                             textfont=dict(size=15, color=INK), hoverinfo="skip", showlegend=False))
    else:
        fig.add_trace(go.Bar(y=[label], x=[(hi - lo) / 1e6], base=[lo / 1e6], orientation="h", width=0.5,
                             marker=dict(color=BLUE),
                             text=[f"<b>{m(lo)} to {m(hi)}</b>"], textposition="outside", cliponaxis=False,
                             textfont=dict(size=15, color=INK),
                             hovertemplate=(f"<b>{label.replace('<br>', ' ')}</b><br>Range: {m(lo)} to {m(hi)}"
                                            "<br>(low = FY27 raises at the floor, high = top of the range)<extra></extra>"),
                             showlegend=False))
share_lo = clean.norm_savings_lo.sum() / clean.projected.sum()
share_hi = clean.norm_savings_hi.sum() / clean.projected.sum()
fig.add_annotation(xref="paper", yref="paper", x=0, y=-0.78, xanchor="left", showarrow=False, align="left",
                   font=dict(size=12, color=INK2),
                   text=(f"On the {len(clean)} items with cleaner budget lines,<br>"
                         f"{share_lo:.0%}–{share_hi:.0%} of the projected savings is visible in the FY27 budget.<br>"
                         f"These are budgets, not spending: only {N27} summer months<br>of FY27 spending have been reported."))
fig.add_vline(x=0, line=dict(color=INK2, width=1.2))
fig.update_xaxes(range=[-0.6, 3.6], tickvals=[-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
                 ticktext=["−$0.5M", "$0", "$0.5M", "$1M", "$1.5M", "$2M", "$2.5M", "$3M", "$3.5M"], gridcolor=GRID, linecolor=AXIS,
                 tickfont=dict(color=MUTED), title_text="$ millions per year", title_font=dict(size=12, color=INK2))
fig.update_yaxes(autorange="reversed", tickfont=dict(color=INK, size=13), showgrid=False, linecolor=AXIS)
HL_TITLE = "Of $2.9M in projected savings, how much can we see?"
HL_SUB = "Annual savings projected by the district for the two closures vs. what the FY27 budget implies."
# 480 tall so that, with the page's own margins, it fits the 500 px frame on the page
fig.update_layout(**base_layout(HL_TITLE, HL_SUB, 480, margin=dict(l=20, r=40, t=100, b=190), bargap=0.45))
fig.update_annotations(y=-0.8)
# Phone layout: no room for a label column, so each row's label sits above its bar (annotations),
# the bars get the full width, and the x axis keeps four ticks.
hl_note = fig.layout.annotations[0].to_plotly_json()
hl_note.update(text=hl_note["text"].replace("<br>", " "), y=-0.24, yanchor="top")
hl_note["text"] = wrap(hl_note["text"], 52)
hl_phone = {**phone_title(HL_TITLE, HL_SUB, 480),
            "yaxis.showticklabels": False, "margin.l": 8, "margin.r": 8, "margin.b": 130,
            "xaxis.range": [-0.6, 4.1], "xaxis.tickvals": [0, 1, 2, 3], "xaxis.ticktext": ["$0", "$1M", "$2M", "$3M"],
            "xaxis.tickangle": 0,
            "annotations": [hl_note] + [
                dict(text=wrap(label.replace("<br>", " "), 50), xref="paper", x=0, xanchor="left", yref="y", y=label,
                     yanchor="bottom", yshift=13, showarrow=False, align="left", font=dict(size=10, color=INK),
                     bgcolor=SURFACE)
                for label, *_ in rows]}
save(fig, "headline", narrow=hl_phone)

# =============================================================================================
# 3. Seasonal small multiples: FY25 / FY26 / FY27 by month (fills in as reports arrive)
# =============================================================================================
PANELS = ["Electricity", "Natural gas", "Water", "Waste removal",
          "Repairs and maintenance", "Custodial support", "Principal / AP", "Administrative assistant"]
fig = make_subplots(rows=2, cols=4, subplot_titles=PANELS, vertical_spacing=0.17, horizontal_spacing=0.06)
SERIES = [(25, "FY25 (2024-25)", "#cfcdc3", 1.8), (26, "FY26 (2025-26, schools open)", "#898781", 2.2),
          (27, "FY27 (2026-27, schools closed)", BLUE, 3.2)]
for i, cat in enumerate(PANELS):
    r, c = divmod(i, 4)
    for fy, name, color, width in SERIES:
        s = monthly[(monthly.category == cat) & (monthly.fy == fy)].sort_values("fiscal_month").copy()
        s["cum"] = s.month_expended.cumsum()
        fig.add_trace(go.Scatter(
            x=[MONTHS[j - 1] for j in s.fiscal_month], y=s.cum, name=name,
            mode="lines+markers" if fy == 27 else "lines", legendgroup=name, showlegend=(i == 0),
            line=dict(color=color, width=width),
            marker=dict(size=8, color=color, line=dict(color=SURFACE, width=2)),
            hovertemplate=f"{cat} – {name}<br>Spent through %{{x}}: $%{{y:,.0f}}<extra></extra>"), row=r + 1, col=c + 1)
fig.add_annotation(xref="x2", yref="y2 domain", x="Jul", y=0.97, text="Heating season<br>(Nov–Mar) not<br>yet reported",
                   showarrow=False, font=dict(size=11, color=INK2), xanchor="left", yanchor="top")
fig.update_xaxes(categoryorder="array", categoryarray=MONTHS, tickvals=["Jul", "Oct", "Jan", "Apr"],
                 tickfont=dict(color=MUTED, size=11), gridcolor=GRID, linecolor=AXIS)
fig.update_yaxes(tickformat="$~s", tickfont=dict(color=MUTED, size=11), gridcolor=GRID,
                 rangemode="tozero", linecolor=AXIS)
for a in fig.layout.annotations[:len(PANELS)]:
    a.update(font=dict(size=13, color=INK))
MO_TITLE = "Year to date: is spending running lower than in the years the schools were open?"
MO_SUB = (f"Cumulative dollars spent since July 1, each fiscal year.<br>The blue line fills in as monthly reports are "
          f"published ({N27} of 12 months so far).")
fig.update_layout(**base_layout(
    MO_TITLE, MO_SUB,
    700, margin=dict(l=20, r=20, t=120, b=60),
    legend=dict(orientation="h", x=0, y=-0.08, xanchor="left", font=dict(size=12, color=INK2),
                bgcolor="rgba(0,0,0,0)"), hovermode="closest"))
# Phone layout: the eight panels as 4 rows x 2 columns instead of 2 x 4, with the panel titles moved
# along, a smaller title, and the legend at the bottom of the figure.
MO_PHONE_H = 1000   # taller on phones: 4 rows of panels need the room
mo_phone = {**phone_title(MO_TITLE, MO_SUB, MO_PHONE_H, size=15, sub_width=50),
            "height": MO_PHONE_H, "margin.l": 40, "margin.r": 6, "margin.b": 70,
            "legend.yref": "container", "legend.y": 0, "legend.yanchor": "bottom", "legend.font.size": 10,
            "annotations[8].font.size": 9}
_area = MO_PHONE_H - mo_phone["margin.t"] - mo_phone["margin.b"]   # px between the top and bottom margins
_band, _title_px, _ticks_px = _area / 4, 18, 24
for i in range(len(PANELS)):
    r, c = divmod(i, 2)
    top = 1 - (r * _band + _title_px) / _area
    bottom = 1 - ((r + 1) * _band - _ticks_px) / _area
    ax = "" if i == 0 else str(i + 1)
    x0, x1 = (0.0, 0.43) if c == 0 else (0.57, 1.0)
    mo_phone[f"xaxis{ax}.domain"] = [x0, x1]
    mo_phone[f"yaxis{ax}.domain"] = [round(bottom, 4), round(top, 4)]
    mo_phone[f"annotations[{i}].x"] = (x0 + x1) / 2
    mo_phone[f"annotations[{i}].y"] = round(top, 4)
    mo_phone[f"annotations[{i}].font.size"] = 11
    mo_phone[f"xaxis{ax}.tickangle"] = 0
save(fig, "monthly", narrow=mo_phone)

# =============================================================================================
# 4. The promise over time (Kingsley): how the savings number was presented
# =============================================================================================
kings = norm
staff_k = kings[kings.kind == "Personnel"].proj_kingsley.sum()
ops_k = kings[kings.kind != "Personnel"].proj_kingsley.sum()
SNAP = [  # label, staff, non-staff, other levers, source
    ("Sep 29, 2025<br>Scenario 1A", 1_132_442, 180_087, -50_000 + 300_000 + 139_905 + 50_000 + 245_000,
     "SDRP Phase III scenario presentation (Sep 29, 2025)"),
    ("Nov–Dec 2025<br>Scenario 1A-R", 1_132_442, 180_087, 150_000 + 150_000 + 50_000,
     "SDRP scenario modeling memo (Dec 1, 2025); the version the Board voted on Jan 22, 2026"),
    ("Oct 7, 2026<br>District closure file", staff_k, ops_k, 0,
     "District closure projections slide 6B, as loaded in the Legion savings tracker"),
]
LEVERS = ["Staff salaries (and benefits, in the 2025 models)", "Non-staff operating costs",
          "Other levers (transportation, sections, leases, Foster)"]
COLS = [BLUE, ORANGE, "#b9b8ae"]
fig = go.Figure()
for j, (name, color) in enumerate(zip(LEVERS, COLS)):
    vals = [s[1 + j] / 1e6 for s in SNAP]
    fig.add_trace(go.Bar(
        x=[s[0] for s in SNAP], y=vals, name=name, marker=dict(color=color, line=dict(color=SURFACE, width=2)),
        text=[f"${v:,.2f}M" if abs(v) > 0.12 else "" for v in vals], textposition="inside",
        insidetextanchor="middle", textfont=dict(color="white" if j < 2 else INK, size=12),
        hovertemplate="%{x}<br>" + name + ": $%{y:,.2f}M<extra></extra>"))
for s in SNAP:
    tot = (s[1] + s[2] + s[3]) / 1e6
    fig.add_annotation(x=s[0], y=max(tot, (s[1] + s[2]) / 1e6) + 0.04, text=f"<b>${tot:,.2f}M</b>", showarrow=False,
                       yanchor="bottom", font=dict(size=15, color=INK))
fig.update_yaxes(range=[0, 2.35], tickprefix="$", ticksuffix="M", gridcolor=GRID, linecolor=AXIS,
                 tickfont=dict(color=MUTED), title_text="$ millions per year", title_font=dict(size=12, color=INK2))
fig.update_xaxes(tickfont=dict(color=INK, size=13), linecolor=AXIS)
PR_TITLE = "The Kingsley savings figure, as presented over time"
PR_SUB = "Annual savings from closing Kingsley, as presented to the Board and the public."
fig.update_layout(**base_layout(
    PR_TITLE, PR_SUB,
    520, margin=dict(l=20, r=20, t=100, b=130), barmode="relative", bargap=0.45,
    legend=dict(orientation="v", x=0, y=-0.14, xanchor="left", yanchor="top", font=dict(size=12, color=INK2),
                bgcolor="rgba(0,0,0,0)")))
# Phone layout: x labels kept horizontal (re-wrapped to fit a column), legend at the bottom.
save(fig, "promise", narrow={
    **phone_title(PR_TITLE, PR_SUB, 520),
    "margin.l": 10, "margin.r": 6, "margin.b": 125,
    "xaxis.tickvals": [s[0] for s in SNAP],
    "xaxis.ticktext": ["Sep 29, 2025<br>Scenario 1A", "Nov–Dec 2025<br>Scenario 1A-R", "Oct 7, 2026<br>District<br>closure file"],
    "xaxis.tickangle": 0, "xaxis.tickfont.size": 10,
    "legend.yref": "container", "legend.y": 0, "legend.yanchor": "bottom", "legend.font.size": 10,
})
