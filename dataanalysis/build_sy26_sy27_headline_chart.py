"""
Builds the headline chart for "SY26 to SY27: What Changed After Kingsley and Bessie Rhodes Closed"
(dataanalysis/sy26-sy27-changes.md) as a Plotly chart:

    python dataanalysis/build_sy26_sy27_headline_chart.py

Writes dataanalysis/assets/sy26_sy27_claimed_vs_realized.html

The page itself shows the static SVG assets/sy26_sy27_claimed_vs_realized.svg. This is the same
chart, with the same numbers, rebuilt in Plotly so it can be rendered to the page's picture:

    python tools/chart_image.py dataanalysis/assets/sy26_sy27_claimed_vs_realized.html assets/img/lead/sy26-sy27-changes.png

Numbers (per year, Kingsley and Bessie Rhodes combined; $ millions, as shown in the SVG and the page):
  - Staffing: District claims $2.02M ($2,015,337). Likely realized: from a net cost of $0.5M
    (only the added assistant principals and custodians count, about $489,000) to a net saving of
    $0.2M (every district-wide cut credited to the closures, about $622,000, minus about $459,000).
  - Building costs: District claims $0.98M ($980,554). Likely realized while the District still owns
    the buildings: $0.3-0.5M.
  - Total: District claims $3.00M ($2,995,891). Likely realized: from a net cost of $0.2M to a net
    saving of $0.7M.
The low and high ends are the rounded figures the page and the SVG use; change them only together
with the page.
"""
from pathlib import Path

import plotly.graph_objects as go

ROOT = Path(__file__).parent
OUT = ROOT / "assets" / "sy26_sy27_claimed_vs_realized.html"

# Palette: same as the closure-savings charts (dataanalysis/closure_savings/build_closure_charts.py).
# Grey = the District's figure, blue = our estimate, red = a net cost.
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS = "#e1e0d9", "#c3c2b7"
BLUE, RED = "#2a78d6", "#e34948"
GHOST, GHOST_LINE = "#e6e5de", "#b9b8ae"
FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"

# category, District's claim, our likely low end, our likely high end, label for our range
ROWS = [
    ("Staffing", 2.02, -0.5, 0.2, "$0.5M net cost to $0.2M saving"),
    ("Building costs", 0.98, 0.3, 0.5, "$0.3–0.5M"),
    ("Total", 3.00, -0.2, 0.7, "$0.2M net cost to $0.7M saving"),
]
CATS = [r[0] for r in ROWS]
HEIGHT = 470

fig = go.Figure()

# The District's claim: a grey bar from $0.
fig.add_trace(go.Bar(
    y=CATS, x=[r[1] for r in ROWS], orientation="h", offsetgroup="claimed",
    name="Claimed by the District",
    marker=dict(color=GHOST, line=dict(color=GHOST_LINE, width=1)),
    text=[f"<b>${r[1]:.2f}M</b>" for r in ROWS], textposition="outside", cliponaxis=False,
    textfont=dict(size=14, color=INK),
    hovertemplate="<b>%{y}</b><br>Claimed by the District: $%{x:.2f}M a year<extra></extra>",
))

# Our likely range: blue from max(low, 0) to the high end ...
fig.add_trace(go.Bar(
    y=CATS, x=[r[3] - max(r[2], 0) for r in ROWS], base=[max(r[2], 0) for r in ROWS],
    orientation="h", offsetgroup="likely", name="Likely realized (our range)",
    marker=dict(color=BLUE),
    text=[f"<b>{r[4]}</b>" for r in ROWS], textposition="outside", cliponaxis=False,
    textfont=dict(size=14, color=INK),
    customdata=[r[4] for r in ROWS],
    hovertemplate="<b>%{y}</b><br>Likely realized: %{customdata} a year<extra></extra>",
))

# ... and red for the part of the range below $0 (a net cost).
neg = [r for r in ROWS if r[2] < 0]
fig.add_trace(go.Bar(
    y=[r[0] for r in neg], x=[-r[2] for r in neg], base=[r[2] for r in neg],
    orientation="h", offsetgroup="likely", name="Net cost (left of $0)",
    marker=dict(color=RED),
    customdata=[r[4] for r in neg],
    hovertemplate="<b>%{y}</b><br>Likely realized: %{customdata} a year<extra></extra>",
))

fig.add_vline(x=0, line=dict(color=INK2, width=1.2))

fig.update_xaxes(
    range=[-0.75, 3.75], tickvals=[-0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5],
    ticktext=["−$0.5M", "$0", "$0.5M", "$1M", "$1.5M", "$2M", "$2.5M", "$3M", "$3.5M"],
    gridcolor=GRID, linecolor=AXIS, zeroline=False, tickfont=dict(color=MUTED),
    title_text="$ millions per year", title_font=dict(size=12, color=INK2),
)
fig.update_yaxes(autorange="reversed", categoryorder="array", categoryarray=CATS,
                 tickfont=dict(color=INK, size=14), showgrid=False, linecolor=AXIS)

fig.add_annotation(
    xref="paper", yref="paper", x=0, y=-0.36, xanchor="left", yanchor="top", showarrow=False,
    align="left", font=dict(size=11.5, color=INK2),
    text=("Staffing: cuts visible in the state pay reports and FTE file, minus added assistant principals"
          "<br>and custodians. Building: costs that stop while the District still owns the buildings."
          "<br>Source: District 65, “A Sustainable Path Forward” (Oct. 13, 2026); Legion of Data Nerds analysis."),
)

fig.update_layout(
    title=dict(text=("<b>Savings claimed vs. likely realized, per year</b><br>"
                     f"<span style='font-size:13px;color:{INK2}'>Kingsley and Bessie Rhodes combined</span>"),
               x=0.0, xanchor="left", y=1 - 22 / HEIGHT, yanchor="top"),
    font=dict(family=FONT, size=13, color=INK),
    paper_bgcolor="white", plot_bgcolor="white", height=HEIGHT,
    margin=dict(l=20, r=30, t=110, b=140),
    barmode="group", bargap=0.3, bargroupgap=0.12,
    legend=dict(orientation="h", x=0, xanchor="left", y=1.02, yanchor="bottom",
                font=dict(size=12, color=INK2), bgcolor="rgba(0,0,0,0)", traceorder="normal"),
    hoverlabel=dict(bgcolor="white", font=dict(family=FONT, size=12, color=INK), bordercolor=AXIS),
)


if __name__ == "__main__":
    OUT.parent.mkdir(exist_ok=True)
    fig.write_html(OUT, include_plotlyjs="cdn", full_html=True, div_id="sy26_sy27_claimed_vs_realized",
                   config={"responsive": True, "displaylogo": False})
    print("wrote", OUT)
