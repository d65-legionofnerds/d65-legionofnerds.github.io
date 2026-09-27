"""Generate Plotly HTML charts for SY27 Enrollment Analysis page.

Two data sources:
  - Fall (data/sy27_fall/): the district dashboard pulled 2026-09-23, snapshot
    of Jean's jmclip/enrollment_fall26 repo. Primary source for every chart it
    covers.
  - May (data/sy27_enrollment/): the district's May 18, 2026 memo (registrations
    as of May 12). Used only where the fall dashboard has no equivalent: low
    income, middle school Dual Language, permissive transfers, and as the
    projection/registration baseline for kindergarten.
"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import numpy as np

HERE = os.path.dirname(__file__)
DATA_DIR = os.path.join(HERE, "data", "sy27_enrollment")
FALL_DIR = os.path.join(HERE, "data", "sy27_fall")
ASSETS_DIR = os.path.join(HERE, "assets")

SHORT_NAMES = {
    "Chute Middle School": "Chute MS",
    "Dawes Elementary School": "Dawes",
    "Dewey Elementary School": "Dewey",
    "Dr Martin Luther King Jr Literary & Fine Arts School": "King Arts",
    "Foster School": "Foster",
    "Haven Middle School": "Haven MS",
    "Lincoln Elementary School": "Lincoln",
    "Lincolnwood Elementary School": "Lincolnwood",
    "Nichols Middle School": "Nichols MS",
    "Oakton Elementary School": "Oakton",
    "Orrington Elementary School": "Orrington",
    "Walker Elementary School": "Walker",
    "Washington Elementary School": "Washington",
    "Willard Elementary School": "Willard",
}

GRADE_ORDER = ["K", "1", "2", "3", "4", "5", "6", "7", "8"]

DEC_LIMITS = {"K": 23, "1": 23, "2": 23, "3": 25, "4": 25, "5": 25, "6": 28, "7": 28, "8": 28}

ELEM_SCHOOLS = ["Dawes", "Dewey", "Foster", "King Arts", "Lincoln", "Lincolnwood",
                "Oakton", "Orrington", "Walker", "Washington", "Willard"]
MIDDLE_SCHOOLS = ["Chute MS", "Haven MS", "Nichols MS"]
TWI_SCHOOLS = ["Dawes", "Dewey", "Foster", "Oakton", "Washington"]

FALL_LABEL = "Fall SY27 (dashboard, 9/23/26)"
MAY_LABEL = "May memo (5/12/26 registrations)"


def parse_val(v):
    if isinstance(v, str) and v.strip() == "<10":
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def back_calculate(df, value_cols, total_col="Total"):
    rows = []
    for _, row in df.iterrows():
        total = parse_val(row[total_col])
        if total is None:
            # Total itself is suppressed; use sum of knowns + 5 per unknown
            _ks = sum(parse_val(row[c]) or 0 for c in value_cols)
            _uk = sum(1 for c in value_cols if parse_val(row[c]) is None)
            total = _ks + _uk * 5
        known_sum = 0
        unknowns = []
        for col in value_cols:
            val = parse_val(row[col])
            if val is not None:
                known_sum += val
            else:
                unknowns.append(col)
        residual = total - known_sum
        new_row = {c: row[c] for c in df.columns if c not in value_cols and c != total_col}
        new_row[total_col] = total
        for col in value_cols:
            val = parse_val(row[col])
            if val is not None:
                new_row[col] = val
            elif len(unknowns) == 1:
                new_row[col] = residual
            elif len(unknowns) > 1:
                new_row[col] = max(1, residual // len(unknowns))
        rows.append(new_row)
    return pd.DataFrame(rows)


def save_html(fig, filename, div_id=None):
    if div_id is None:
        div_id = filename.replace(".html", "").replace("-", "_")
    html = fig.to_html(
        full_html=True, include_plotlyjs="cdn", div_id=div_id,
        config={"responsive": True, "displayModeBar": False}
    )
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Saved {path}")


# ── Load fall data ─────────────────────────────────────────────────────────

fall_grade = pd.read_csv(os.path.join(FALL_DIR, "enrollment_by_school_grade.csv"))
fall_grade["Short"] = fall_grade["school"].map(SHORT_NAMES)

fall_util = pd.read_csv(os.path.join(FALL_DIR, "utilization_current_vs_predicted.csv"))
fall_util = fall_util[fall_util["dashboard_sy27"].notna()].copy()  # drops Kingsley
fall_util["Short"] = fall_util["school"].map(SHORT_NAMES)

# enroll_total here is the 1A table's projection (Scenario 1A, Kingsley closed)
fall_proj = pd.read_csv(os.path.join(FALL_DIR, "enrollment_vs_utilization.csv"))
fall_proj["Short"] = fall_proj["school"].map(SHORT_NAMES)

twi = pd.read_csv(os.path.join(FALL_DIR, "twi_strands.csv"))

cs_detail = pd.read_csv(os.path.join(FALL_DIR, "class_size_detail_by_school.csv"), dtype={"grade_label": str})
cs_detail["Short"] = cs_detail["school"].str.replace(" (MS)", " MS", regex=False)

demo = pd.read_csv(os.path.join(FALL_DIR, "students_home_demographics.csv"))
demo = demo[demo["school"] != "District"].copy()
demo["Short"] = demo["school"].map(SHORT_NAMES)


def demo_pivot(chart_id):
    return demo[demo["chart_id"] == chart_id].pivot_table(
        index="Short", columns="category", values="value", aggfunc="sum").fillna(0)


# ── Load May data ──────────────────────────────────────────────────────────

enrollment = pd.read_csv(os.path.join(DATA_DIR, "enrollment_by_school_grade_program.csv"), dtype=str)
value_cols = ["ACC", "Middle_School_DL", "MonoL", "RISE", "STEP", "TWE", "TWS", "TWX"]
enrollment = back_calculate(enrollment, value_cols, "Total")
enrollment["Short"] = enrollment["School"].map(SHORT_NAMES)

lowinc = pd.read_csv(os.path.join(DATA_DIR, "enrollment_low_income.csv"))
lowinc["Short"] = lowinc["School"].map(SHORT_NAMES)

transfers_out = pd.read_csv(os.path.join(DATA_DIR, "transfers_out_by_school.csv"))
transfers_out["Short"] = transfers_out["Assigned_School"].map(SHORT_NAMES)

transfers_in = pd.read_csv(os.path.join(DATA_DIR, "transfers_in_by_school.csv"))
transfers_in["Short"] = transfers_in["Receiving_School"].map(SHORT_NAMES)

kinder = pd.read_csv(os.path.join(DATA_DIR, "kindergarten_projected_vs_actual.csv"), dtype=str)
kinder_cols_proj = ["Projected_Total_All_Programs", "Projected_Monolingual"]
kinder_cols_act = ["Actual_Total_All_Programs", "Actual_Monolingual"]
for col in kinder_cols_proj + kinder_cols_act:
    kinder[col] = kinder[col].apply(lambda x: parse_val(x) if pd.notna(x) else None)

# ── Chart 1: Building Utilization (fall) ───────────────────────────────────

print("Generating building utilization chart...")

merged = fall_util[["Short", "dashboard_sy27", "capacity_used"]].copy()
merged.columns = ["Short", "SY27_Enrollment", "Capacity"]
merged["Utilization_Pct"] = (merged["SY27_Enrollment"] / merged["Capacity"] * 100).round(1)
merged = merged.sort_values("Utilization_Pct", ascending=True)

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    y=merged["Short"], x=merged["Capacity"],
    name="Building Capacity", orientation="h",
    marker_color="rgba(200, 200, 200, 0.7)",
    text=merged["Capacity"].astype(int), textposition="inside",
    hovertemplate="%{y}: Capacity = %{x}<extra></extra>"
))

colors = []
for _, row in merged.iterrows():
    pct = row["Utilization_Pct"]
    if pct >= 85:
        colors.append("#d62728")
    elif pct >= 70:
        colors.append("#ff7f0e")
    elif pct >= 50:
        colors.append("#2ca02c")
    else:
        colors.append("#1f77b4")

fig1.add_trace(go.Bar(
    y=merged["Short"], x=merged["SY27_Enrollment"],
    name="Fall SY27 Enrollment", orientation="h",
    marker_color=colors,
    text=[f"{int(e)} ({p:.0f}%)" for e, p in zip(merged["SY27_Enrollment"], merged["Utilization_Pct"])],
    textposition="inside",
    hovertemplate="%{y}: Enrollment = %{x}<extra></extra>"
))

fig1.update_layout(
    title="Fall SY 2026-27 Building Utilization: Enrollment vs. Capacity<br><sup>Capacity = smaller of the district's Cap Total and Cordogan Clark's capacity</sup>",
    xaxis_title="Students",
    barmode="overlay",
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=120, r=40, t=100, b=60),
)

save_html(fig1, "sy27_building_utilization.html")

# ── Chart 1b: Fall enrollment vs. 1A projection ────────────────────────────

print("Generating enrollment vs. projection chart...")

proj = fall_proj[["Short", "enroll_total", "dashboard_sy27"]].copy()
proj["Diff"] = (proj["dashboard_sy27"] - proj["enroll_total"]).astype(int)
proj = proj.sort_values("Diff", ascending=False)

fig1b = go.Figure(go.Bar(
    y=proj["Short"], x=proj["Diff"], orientation="h",
    marker_color=["#1f77b4" if d >= 0 else "#d62728" for d in proj["Diff"]],
    text=[f"{d:+d}" for d in proj["Diff"]], textposition="outside",
    customdata=np.stack([proj["enroll_total"], proj["dashboard_sy27"]], axis=-1),
    hovertemplate="%{y}: %{customdata[1]:.0f} enrolled vs. %{customdata[0]:.0f} projected (%{x:+d})<extra></extra>",
))

tot_proj = int(proj["enroll_total"].sum())
tot_fall = int(proj["dashboard_sy27"].sum())
fig1b.update_layout(
    title=(f"Fall SY27 Enrollment minus Scenario 1A Projection<br><sup>All 14 schools: {tot_fall:,} enrolled vs. "
           f"{tot_proj:,} projected ({tot_fall - tot_proj:+,d}, {(tot_fall - tot_proj) / tot_proj * 100:+.1f}%)</sup>"),
    xaxis_title="Students (fall enrollment minus projection)",
    yaxis=dict(autorange="reversed"),
    height=550,
    margin=dict(l=120, r=40, t=100, b=60),
)
lim = proj["Diff"].abs().max() * 1.25
fig1b.update_xaxes(range=[-lim, lim], zeroline=True, zerolinecolor="#888")

save_html(fig1b, "sy27_enrollment_vs_projection.html")

# ── Chart 2: Mainstream Class Size Analysis (fall, estimated) ──────────────

print("Generating class size analysis chart...")

# Jean's per-grade estimate of monolingual/mainstream students: grade total minus
# TWI (even split of the school's TWI count) minus ACC (Oakton, 73 projected).
rows = []
for _, r in cs_detail[cs_detail["Short"].isin(ELEM_SCHOOLS)].iterrows():
    grade = r["grade_label"]
    mono = int(round(r["mainstream_students"]))
    if mono == 0:
        continue
    dec_limit = DEC_LIMITS.get(grade, 25)
    sections = max(1, int(np.ceil(mono / dec_limit)))
    rows.append({
        "School": r["Short"], "Grade": grade,
        "MonoL": mono, "DEC_Limit": dec_limit,
        "Sections": sections, "Est_Class_Size": round(mono / sections, 1),
        "One_Section_Size": mono,
        "Over_Limit_1_Section": mono > dec_limit,
    })

cs_df = pd.DataFrame(rows)
cs_df["Grade"] = pd.Categorical(cs_df["Grade"], categories=GRADE_ORDER, ordered=True)

fig2 = make_subplots(
    rows=4, cols=3,
    subplot_titles=sorted(ELEM_SCHOOLS),
    vertical_spacing=0.08, horizontal_spacing=0.06,
)

for idx, school in enumerate(sorted(ELEM_SCHOOLS)):
    row_idx = idx // 3 + 1
    col_idx = idx % 3 + 1
    sdf = cs_df[cs_df["School"] == school].copy()
    sdf = sdf.sort_values("Grade")

    bar_colors = []
    for _, r in sdf.iterrows():
        mono = r["MonoL"]
        limit = r["DEC_Limit"]
        if mono > limit:
            bar_colors.append("#d62728")  # over limit
        elif mono > limit * 0.85:
            bar_colors.append("#ff7f0e")  # near limit
        else:
            bar_colors.append("#2ca02c")  # safe

    fig2.add_trace(go.Bar(
        x=sdf["Grade"].astype(str), y=sdf["MonoL"],
        marker_color=bar_colors, showlegend=False,
        text=sdf["MonoL"].astype(int), textposition="outside",
        hovertemplate="Grade %{x}: ~%{y} mainstream students<extra></extra>",
    ), row=row_idx, col=col_idx)

    # Add DEC limit lines
    grades_in = sdf["Grade"].astype(str).tolist()
    for g_idx, g in enumerate(grades_in):
        lim = DEC_LIMITS[g]
        fig2.add_shape(
            type="line",
            x0=g_idx - 0.4, x1=g_idx + 0.4, y0=lim, y1=lim,
            line=dict(color="red", width=2, dash="dash"),
            row=row_idx, col=col_idx,
        )

    fig2.update_yaxes(range=[0, max(sdf["MonoL"].max() * 1.3, 30)], row=row_idx, col=col_idx)

fig2.update_layout(
    title="Estimated Monolingual/Mainstream Students per Grade vs. DEC Contract Limits (dashed red line)<br><sup>Fall SY27. Red bars exceed the limit as 1 class; orange bars are within 15% of it. TWI/ACC students are subtracted using estimates.</sup>",
    height=900,
    showlegend=False,
    margin=dict(l=60, r=40, t=100, b=40),
)

save_html(fig2, "sy27_class_size_elementary.html")

# ── Chart 2b: Class size problem summary ─────────────────────────────────

print("Generating class size problem summary...")

problem_rows = []
for _, r in cs_df.iterrows():
    mono = r["MonoL"]
    limit = r["DEC_Limit"]
    school = r["School"]
    grade = r["Grade"]

    min_sections = int(np.ceil(mono / limit))
    class_size_if_split = round(mono / min_sections, 1)

    # Case 1: Over limit AND splitting creates classes under 16
    if mono > limit and class_size_if_split < 16:
        problem_rows.append({
            "School": school, "Grade": grade, "MonoL": int(mono),
            "DEC_Limit": limit, "1_Section": int(mono),
            "Split_Size": class_size_if_split, "Sections_Needed": min_sections,
            "Status": "Over limit, split too small"
        })
    # Case 2: Exactly at the DEC limit boundary
    elif limit - 1 <= mono <= limit:
        problem_rows.append({
            "School": school, "Grade": grade, "MonoL": int(mono),
            "DEC_Limit": limit, "1_Section": int(mono),
            "Split_Size": class_size_if_split, "Sections_Needed": 1,
            "Status": "At DEC limit"
        })

prob_df = pd.DataFrame(problem_rows)
if not prob_df.empty:
    prob_df["Grade"] = pd.Categorical(prob_df["Grade"], categories=GRADE_ORDER, ordered=True)
    prob_df = prob_df.sort_values(["School", "Grade"])
    print(prob_df.to_string(index=False))

    fig2b = go.Figure()

    colors_1 = ["#d62728" if "too small" in s else "#ff7f0e" for s in prob_df["Status"]]

    fig2b.add_trace(go.Bar(
        x=[f"{r['School']} Gr {r['Grade']}" for _, r in prob_df.iterrows()],
        y=prob_df["1_Section"],
        name="1 Section (class size)",
        marker_color=colors_1,
        text=prob_df["1_Section"], textposition="outside",
    ))

    fig2b.add_trace(go.Bar(
        x=[f"{r['School']} Gr {r['Grade']}" for _, r in prob_df.iterrows()],
        y=prob_df["Split_Size"],
        name="If split into required sections",
        marker_color="#1f77b4",
        text=prob_df["Split_Size"], textposition="outside",
    ))

    for i, (_, r) in enumerate(prob_df.iterrows()):
        fig2b.add_shape(
            type="line", x0=i - 0.4, x1=i + 0.4,
            y0=r["DEC_Limit"], y1=r["DEC_Limit"],
            line=dict(color="red", width=2, dash="dash"),
        )

    fig2b.update_layout(
        title="Class Size Dilemma: Where Splitting Creates Unsustainably Small Classes (Fall SY27, estimated)<br><sup>Red bars exceed DEC limit as 1 class; blue bars show the resulting class size if split. Dashed line = DEC max (K-2: 23, 3-5: 25).</sup>",
        yaxis_title="Students per Class",
        barmode="group",
        height=500,
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=40, t=100, b=120),
    )

    save_html(fig2b, "sy27_class_size_dilemma.html")

# ── Chart 3: Elementary TWI enrollment vs. seats (fall) ─────────────────────

print("Generating TWI enrollment chart...")

twi_sorted = twi.sort_values("twi_now", ascending=False)

fig3 = go.Figure()
for col, name, color in [("TWE", "TWE", "#1f77b4"), ("TWS", "TWS", "#2ca02c"), ("TWX", "TWX", "#9467bd")]:
    fig3.add_trace(go.Bar(
        x=twi_sorted["school"], y=twi_sorted[col], name=name, marker_color=color,
        text=twi_sorted[col].astype(int), textposition="inside",
        hovertemplate=f"%{{x}}: %{{y}} {name} students<extra></extra>",
    ))
fig3.add_trace(go.Scatter(
    x=twi_sorted["school"], y=twi_sorted["cap_twi"], name="TWI seats",
    mode="markers+text", marker=dict(symbol="line-ew-open", size=40, color="#d62728", line=dict(width=3, color="#d62728")),
    text=[f"{int(c)} seats ({p:.0f}% full)" for c, p in zip(twi_sorted["cap_twi"], twi_sorted["fill_pct"])],
    textposition="top center",
    hovertemplate="%{x}: %{y} TWI seats<extra></extra>",
))

fig3.update_layout(
    title="Elementary TWI Enrollment vs. TWI Seats (Fall SY27)<br><sup>144 seats per strand (1 class per grade K-5 × 24). Foster and Washington run 2 strands.</sup>",
    yaxis_title="Students",
    barmode="stack",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    margin=dict(l=60, r=40, t=100, b=80),
)
fig3.update_yaxes(range=[0, twi_sorted["cap_twi"].max() * 1.3])

save_html(fig3, "sy27_dl_twi_enrollment.html")

# ── Chart 4: Demographics (fall) ────────────────────────────────────────────

print("Generating demographics chart...")

race = demo_pivot("home-race")
race_display = {
    "White": "White",
    "Black or African American": "Black",
    "Hispanic or Latino": "Hispanic/Latino",
    "Asian": "Asian",
    "Multi-racial": "Multiracial",
    "Middle Eastern or North African": "Middle Eastern/N. African",
    "Other*": "Other* (groups under 10)",
}
race = race[[c for c in race_display if c in race.columns]]
race_total = race.sum(axis=1)
race_pct = race.div(race_total, axis=0) * 100
race_pct = race_pct.loc[race_total.sort_values().index]

fig4 = go.Figure()

for col, display_name in race_display.items():
    if col not in race_pct.columns:
        continue
    pcts = race_pct[col].round(1)
    fig4.add_trace(go.Bar(
        y=race_pct.index, x=pcts,
        name=display_name, orientation="h",
        hovertemplate=f"{display_name}: %{{x:.1f}}%<extra></extra>",
        text=[f"{p:.0f}%" if p >= 5 else "" for p in pcts],
        textposition="inside",
    ))

fig4.update_layout(
    title="Student Racial/Ethnic Composition by School (Fall SY27)<br><sup>The dashboard merges any group under 10 students at a school into Other*</sup>",
    xaxis_title="Percentage of Students",
    barmode="stack",
    height=550,
    legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="center", x=0.5, font=dict(size=10)),
    margin=dict(l=120, r=40, t=100, b=130),
    xaxis=dict(range=[0, 100]),
)

save_html(fig4, "sy27_demographics.html")

# ── Chart 5: EL, IEP (fall), Low Income (May) ───────────────────────────────

print("Generating EL/IEP/Low Income chart...")

iep_p = demo_pivot("home-iep")
el_p = demo_pivot("home-lep")
el_fall = pd.DataFrame({"Short": el_p.index, "EL": el_p["EL"].values,
                        "Total": (el_p["EL"] + el_p["Not EL"]).values})
iep_fall = pd.DataFrame({"Short": iep_p.index, "IEP": iep_p["Has IEP"].values,
                         "Total": (iep_p["Has IEP"] + iep_p["No IEP"]).values})

fig5 = make_subplots(
    rows=1, cols=3,
    subplot_titles=["English Learners (%) - Fall", "Students with IEPs (%) - Fall", "Low Income (%) - May memo"],
    horizontal_spacing=0.08,
)

for df_data, val_col, total_col, col_idx, color in [
    (el_fall, "EL", "Total", 1, "#1f77b4"),
    (iep_fall, "IEP", "Total", 2, "#ff7f0e"),
    (lowinc, "Low_Income", "Total", 3, "#2ca02c"),
]:
    df_data = df_data.copy()
    df_data["Pct"] = (df_data[val_col] / df_data[total_col] * 100).round(1)
    df_data = df_data.sort_values("Pct", ascending=True)
    fig5.add_trace(go.Bar(
        y=df_data["Short"], x=df_data["Pct"],
        orientation="h", marker_color=color, showlegend=False,
        text=[f"{p:.0f}%" for p in df_data["Pct"]], textposition="outside",
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ), row=1, col=col_idx)
    fig5.update_xaxes(range=[0, df_data["Pct"].max() * 1.2], row=1, col=col_idx)

fig5.update_layout(
    title="English Learners, IEPs, and Low Income by School (SY 2026-27)<br><sup>EL and IEP from the fall dashboard; the dashboard does not report low income, so that panel is the May memo</sup>",
    height=500,
    margin=dict(l=120, r=40, t=100, b=40),
)

save_html(fig5, "sy27_el_iep_lowincome.html")

# ── Chart 6: Transfer Sankey (May) ──────────────────────────────────────────

print("Generating transfer Sankey diagram...")

out = transfers_out.sort_values("Transfer_Out_Count", ascending=False)
inp = transfers_in.sort_values("Transfer_In_Count", ascending=False)

# Build Sankey: Source schools → Pool → Destination schools
labels = []
# Source nodes (school names with " (out)" suffix)
source_labels = [f"{s} (out)" for s in out["Short"]]
labels.extend(source_labels)
# Pool node
pool_idx = len(labels)
labels.append("Transfer Pool (268)")
# Destination nodes
dest_labels = [f"{s} (in)" for s in inp["Short"]]
labels.extend(dest_labels)

sources = []
targets = []
values = []
colors = []

# Outgoing flows → pool
out_color_map = {
    "Foster": "rgba(214, 39, 40, 0.5)",
    "Dewey": "rgba(255, 127, 14, 0.5)",
}
for i, (_, row) in enumerate(out.iterrows()):
    sources.append(i)
    targets.append(pool_idx)
    values.append(row["Transfer_Out_Count"])
    colors.append(out_color_map.get(row["Short"], "rgba(100, 100, 100, 0.3)"))

# Pool → incoming flows
dest_color_map = {
    "Lincolnwood": "rgba(44, 160, 44, 0.5)",
    "Walker": "rgba(31, 119, 180, 0.5)",
    "Willard": "rgba(31, 119, 180, 0.5)",
}
for i, (_, row) in enumerate(inp.iterrows()):
    sources.append(pool_idx)
    targets.append(pool_idx + 1 + i)
    values.append(row["Transfer_In_Count"])
    colors.append(dest_color_map.get(row["Short"], "rgba(100, 100, 100, 0.3)"))

# Node colors
node_colors = []
for lbl in labels:
    if "(out)" in lbl:
        if "Foster" in lbl:
            node_colors.append("#d62728")
        elif "Dewey" in lbl:
            node_colors.append("#ff7f0e")
        else:
            node_colors.append("#aaaaaa")
    elif "Pool" in lbl:
        node_colors.append("#888888")
    elif "(in)" in lbl:
        if "Lincolnwood" in lbl:
            node_colors.append("#2ca02c")
        elif "Walker" in lbl or "Willard" in lbl:
            node_colors.append("#1f77b4")
        else:
            node_colors.append("#aaaaaa")
    else:
        node_colors.append("#888888")

fig6 = go.Figure(go.Sankey(
    node=dict(
        pad=15, thickness=20,
        label=labels, color=node_colors,
    ),
    link=dict(
        source=sources, target=targets, value=values,
        color=colors,
    ),
))

fig6.update_layout(
    title="Permissive Transfer Flow: 268 Approved Transfers (May memo, SY 2026-27)<br><sup>Foster (red) accounted for 37% of outgoing transfers. Lincolnwood (green) was the top destination.</sup>",
    height=600,
    margin=dict(l=20, r=20, t=80, b=40),
    font_size=11,
)

save_html(fig6, "sy27_transfer_sankey.html")

# ── Chart 7: Kindergarten: projected vs. May registrations vs. fall ─────────

print("Generating kindergarten chart...")

fall_k = fall_grade.set_index("Short")["grade_0"]
kinder["Fall_K"] = kinder["School"].map(fall_k)
kinder_valid = kinder.dropna(subset=["Projected_Total_All_Programs", "Fall_K"]).copy()
kinder_valid = kinder_valid.sort_values("Projected_Total_All_Programs", ascending=False)

k_proj = int(kinder_valid["Projected_Total_All_Programs"].sum())
k_fall = int(kinder_valid["Fall_K"].sum())

fig7 = go.Figure()

fig7.add_trace(go.Bar(
    x=kinder_valid["School"], y=kinder_valid["Projected_Total_All_Programs"],
    name="Projected (May memo)", marker_color="rgba(31, 119, 180, 0.7)",
    text=kinder_valid["Projected_Total_All_Programs"].astype(int), textposition="outside",
))

fig7.add_trace(go.Bar(
    x=kinder_valid["School"], y=kinder_valid["Actual_Total_All_Programs"],
    name="Registered as of 5/12/26", marker_color="rgba(200, 200, 200, 0.9)",
    text=[f"{int(v)}" if pd.notna(v) else "<10" for v in kinder_valid["Actual_Total_All_Programs"]],
    textposition="outside",
))

fig7.add_trace(go.Bar(
    x=kinder_valid["School"], y=kinder_valid["Fall_K"],
    name="Enrolled, fall (9/23/26)", marker_color="rgba(214, 39, 40, 0.7)",
    text=kinder_valid["Fall_K"].astype(int), textposition="outside",
))

fig7.update_layout(
    title=(f"Kindergarten: Projected vs. May Registrations vs. Fall Enrollment (SY 2026-27)<br><sup>Fall kindergarten: {k_fall} "
           f"enrolled vs. {k_proj} projected ({k_fall - k_proj:+d}, {(k_fall - k_proj) / k_proj * 100:+.0f}%)</sup>"),
    yaxis_title="Students",
    barmode="group",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=60, r=40, t=100, b=60),
)

save_html(fig7, "sy27_kindergarten.html")

# ── Chart 8: Total enrollment by school and program (fall) ──────────────────

print("Generating total enrollment overview...")

twi_by_school = twi.set_index("school")[["TWE", "TWS", "TWX"]]
school_overview = fall_grade.set_index("Short")[["total"]].join(twi_by_school).fillna(0)
school_overview["TWI_Total"] = school_overview[["TWE", "TWS", "TWX"]].sum(axis=1)
school_overview["Non_TWI"] = school_overview["total"] - school_overview["TWI_Total"]
school_overview = school_overview.sort_values("total", ascending=True)

fig8 = go.Figure()

fig8.add_trace(go.Bar(
    y=school_overview.index, x=school_overview["Non_TWI"],
    name="Monolingual/mainstream and other programs", orientation="h", marker_color="#1f77b4",
))
for col, color in [("TWE", "#2ca02c"), ("TWS", "#98df8a"), ("TWX", "#9467bd")]:
    fig8.add_trace(go.Bar(
        y=school_overview.index, x=school_overview[col],
        name=f"TWI: {col}", orientation="h", marker_color=color,
    ))
fig8.add_trace(go.Scatter(
    y=school_overview.index, x=school_overview["total"] + 20, mode="text",
    text=school_overview["total"].astype(int), showlegend=False, hoverinfo="skip",
))

fig8.update_layout(
    title="Total Enrollment by School and TWI Program (Fall SY27)<br><sup>The fall dashboard reports TWI by school only; ACC (Oakton), middle school Dual Language, RISE and STEP are not broken out</sup>",
    xaxis_title="Students",
    barmode="stack",
    height=550,
    legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5),
    margin=dict(l=120, r=40, t=100, b=120),
)

save_html(fig8, "sy27_enrollment_by_program.html")


# ── Chart 9: Middle School DL detail (May) ──────────────────────────────────

print("Generating middle school DL detail chart...")

ms_all = enrollment[enrollment["Short"].isin(MIDDLE_SCHOOLS)].copy()
ms_all["Grade"] = pd.Categorical(ms_all["Grade"], categories=["6", "7", "8"], ordered=True)
ms_all = ms_all.sort_values(["Short", "Grade"])

fig9 = make_subplots(
    rows=1, cols=3,
    subplot_titles=["Chute MS", "Haven MS", "Nichols MS"],
    horizontal_spacing=0.08,
)

for idx, school in enumerate(["Chute MS", "Haven MS", "Nichols MS"]):
    sdf = ms_all[ms_all["Short"] == school].sort_values("Grade")
    col_idx = idx + 1

    fig9.add_trace(go.Bar(
        x=sdf["Grade"], y=sdf["MonoL"], name="Monolingual",
        marker_color="#1f77b4", showlegend=(idx == 0),
        text=sdf["MonoL"].astype(int), textposition="outside",
    ), row=1, col=col_idx)

    if sdf["Middle_School_DL"].sum() > 0:
        fig9.add_trace(go.Bar(
            x=sdf["Grade"], y=sdf["Middle_School_DL"], name="Dual Language",
            marker_color="#ff7f0e", showlegend=(idx == 0),
            text=sdf["Middle_School_DL"].astype(int), textposition="outside",
        ), row=1, col=col_idx)

    # DEC limit line at 28
    for g_idx in range(len(sdf)):
        fig9.add_shape(
            type="line", x0=g_idx - 0.4, x1=g_idx + 0.4, y0=28, y1=28,
            line=dict(color="red", width=2, dash="dash"),
            row=1, col=col_idx,
        )

fig9.update_layout(
    title="Middle School Enrollment by Grade: Monolingual vs. Dual Language (May memo)<br><sup>Red dashed line = DEC contract max (28 students). Haven DL 7th grade has fewer than 10 students.</sup>",
    height=400,
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    margin=dict(l=60, r=40, t=100, b=60),
)

save_html(fig9, "sy27_middle_school_detail.html")

print("\nAll charts generated successfully!")
