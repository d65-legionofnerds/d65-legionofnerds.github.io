"""Generate Plotly HTML charts for SY27 Enrollment Analysis page."""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "sy27_enrollment")
UTIL_CSV = os.path.join(os.path.dirname(__file__), "data", "0_utilization.csv")
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

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


# ── Load data ──────────────────────────────────────────────────────────────

enrollment = pd.read_csv(os.path.join(DATA_DIR, "enrollment_by_school_grade_program.csv"), dtype=str)
value_cols = ["ACC", "Middle_School_DL", "MonoL", "RISE", "STEP", "TWE", "TWS", "TWX"]
enrollment = back_calculate(enrollment, value_cols, "Total")
enrollment["Short"] = enrollment["School"].map(SHORT_NAMES)

race = pd.read_csv(os.path.join(DATA_DIR, "enrollment_by_race.csv"), dtype=str)
race_cols = ["American_Indian_or_Alaska_Native", "Asian", "Black_or_African_American",
             "Hispanic_or_Latino", "Middle_Eastern_or_North_African", "Multiracial",
             "Native_Hawaiian_Other_Pacific_Islander", "White", "No_Race"]
race = back_calculate(race, race_cols, "Total")
race["Short"] = race["School"].map(SHORT_NAMES)

el = pd.read_csv(os.path.join(DATA_DIR, "enrollment_english_learners.csv"))
el["Short"] = el["School"].map(SHORT_NAMES)

iep = pd.read_csv(os.path.join(DATA_DIR, "enrollment_ieps.csv"))
iep["Short"] = iep["School"].map(SHORT_NAMES)

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

util = pd.read_csv(UTIL_CSV)

# Normalize util school names for matching
util_name_map = {
    "Dawes Elementary School": "Dawes",
    "Dewey Elementary School": "Dewey",
    "Lincoln Elementary School": "Lincoln",
    "Lincolnwood Elementary School": "Lincolnwood",
    "Oakton Elementary School": "Oakton",
    "Orrington Elementary School": "Orrington",
    "Walker Elementary School": "Walker",
    "Washington Elementary School": "Washington",
    "Willard Elementary School": "Willard",
    "Foster School": "Foster",
    "Dr. Martin Luther King Jr. Literary & Fine Arts School": "King Arts",
    "Chute Middle School": "Chute MS",
    "Haven Middle School": "Haven MS",
    "Nichols Middle School": "Nichols MS",
}
util["Short"] = util["Schools"].map(util_name_map)

# ── Chart 1: Building Utilization ──────────────────────────────────────────

print("Generating building utilization chart...")

school_totals = enrollment.groupby("Short")["Total"].sum().reset_index()
school_totals.columns = ["Short", "SY27_Enrollment"]

cap = util[util["Short"].notna()][["Short", "Cap Total"]].copy()
cap.columns = ["Short", "Capacity"]
cap["Capacity"] = pd.to_numeric(cap["Capacity"], errors="coerce")

merged = school_totals.merge(cap, on="Short", how="inner")
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
    name="SY27 Enrollment", orientation="h",
    marker_color=colors,
    text=[f"{int(e)} ({p}%)" for e, p in zip(merged["SY27_Enrollment"], merged["Utilization_Pct"])],
    textposition="inside",
    hovertemplate="%{y}: Enrollment = %{x}<extra></extra>"
))

fig1.update_layout(
    title="SY 2026-27 Building Utilization: Enrollment vs. Capacity",
    xaxis_title="Students",
    barmode="overlay",
    height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=120, r=40, t=80, b=60),
)

save_html(fig1, "sy27_building_utilization.html")

# ── Chart 2: Monolingual Class Size Analysis ────────────────────────────────

print("Generating class size analysis chart...")

elem_data = enrollment[enrollment["Short"].isin(ELEM_SCHOOLS)].copy()
elem_data["Grade"] = pd.Categorical(elem_data["Grade"], categories=GRADE_ORDER, ordered=True)
elem_data = elem_data.sort_values(["Short", "Grade"])

# For each school-grade, estimate sections and class size
rows = []
for _, row in elem_data.iterrows():
    mono = row["MonoL"]
    grade = row["Grade"]
    school = row["Short"]
    dec_limit = DEC_LIMITS.get(grade, 25)

    if mono == 0:
        continue

    if mono <= dec_limit:
        sections = 1
    elif mono <= 2 * dec_limit:
        sections = 2
    else:
        sections = int(np.ceil(mono / dec_limit))

    class_size = mono / sections
    one_section_size = mono

    rows.append({
        "School": school, "Grade": grade,
        "MonoL": mono, "DEC_Limit": dec_limit,
        "Sections": sections, "Est_Class_Size": round(class_size, 1),
        "One_Section_Size": one_section_size,
        "Over_Limit_1_Section": one_section_size > dec_limit,
    })

cs_df = pd.DataFrame(rows)

# Create a heatmap-style figure: grouped bar chart per school
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
        x=sdf["Grade"], y=sdf["MonoL"],
        marker_color=bar_colors, showlegend=False,
        text=sdf["MonoL"].astype(int), textposition="outside",
        hovertemplate="Grade %{x}: %{y} students<extra></extra>",
    ), row=row_idx, col=col_idx)

    # Add DEC limit lines
    grades_in = sdf["Grade"].tolist()
    for g in grades_in:
        lim = DEC_LIMITS[g]
        g_idx = grades_in.index(g)
        fig2.add_shape(
            type="line",
            x0=g_idx - 0.4, x1=g_idx + 0.4, y0=lim, y1=lim,
            line=dict(color="red", width=2, dash="dash"),
            row=row_idx, col=col_idx,
        )

    fig2.update_yaxes(range=[0, max(sdf["MonoL"].max() * 1.3, 30)], row=row_idx, col=col_idx)

fig2.update_layout(
    title="Monolingual Class Sizes vs. DEC Contract Limits (dashed red line)<br><sup>Red bars exceed limit with 1 section; orange bars are within 15% of limit</sup>",
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

    if mono == 0:
        continue

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
    prob_df = prob_df.sort_values(["School", "Grade"])

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
        title="Class Size Dilemma: Where Splitting Creates Unsustainably Small Classes<br><sup>Red bars exceed DEC limit as 1 class; blue bars show the resulting class size if split. Dashed line = DEC max (K-2: 23, 3-5: 25).</sup>",
        yaxis_title="Students per Class",
        barmode="group",
        height=500,
        xaxis_tickangle=-45,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=40, t=100, b=120),
    )

    save_html(fig2b, "sy27_class_size_dilemma.html")

# ── Chart 3: DL / TWI Program Enrollment ──────────────────────────────────

print("Generating DL/TWI program enrollment chart...")

# Middle school DL
ms_dl = enrollment[enrollment["Short"].isin(MIDDLE_SCHOOLS)].copy()
ms_dl = ms_dl[["Short", "Grade", "Middle_School_DL"]].copy()
ms_dl["Middle_School_DL"] = pd.to_numeric(ms_dl["Middle_School_DL"], errors="coerce")
ms_dl = ms_dl[ms_dl["Middle_School_DL"] > 0]

# Elementary TWI (TWE + TWS + TWX)
twi_schools = ["Dawes", "Dewey", "Foster", "Oakton", "Washington"]
elem_twi = enrollment[enrollment["Short"].isin(twi_schools)].copy()
elem_twi["TWI_Total"] = elem_twi["TWE"] + elem_twi["TWS"] + elem_twi["TWX"]
elem_twi = elem_twi[elem_twi["TWI_Total"] > 0][["Short", "Grade", "TWE", "TWS", "TWX", "TWI_Total"]]

fig3 = make_subplots(
    rows=1, cols=2,
    subplot_titles=["Middle School Dual Language", "Elementary TWI by School"],
    horizontal_spacing=0.12,
)

if not ms_dl.empty:
    for school in ms_dl["Short"].unique():
        sdf = ms_dl[ms_dl["Short"] == school].sort_values("Grade")
        fig3.add_trace(go.Bar(
            x=sdf["Grade"], y=sdf["Middle_School_DL"],
            name=school, text=sdf["Middle_School_DL"].astype(int),
            textposition="outside",
            hovertemplate=f"{school} Grade %{{x}}: %{{y}} DL students<extra></extra>",
        ), row=1, col=1)

# TWI totals by school and grade
if not elem_twi.empty:
    for school in sorted(elem_twi["Short"].unique()):
        sdf = elem_twi[elem_twi["Short"] == school].sort_values("Grade")
        fig3.add_trace(go.Bar(
            x=sdf["Grade"], y=sdf["TWI_Total"],
            name=school, text=sdf["TWI_Total"].astype(int),
            textposition="outside",
            hovertemplate=f"{school} Grade %{{x}}: %{{y}} TWI students<extra></extra>",
        ), row=1, col=2)

fig3.update_layout(
    title="Dual Language & TWI Program Enrollment by School and Grade",
    height=450,
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
    margin=dict(l=60, r=40, t=80, b=80),
)
fig3.update_yaxes(title_text="Students", row=1, col=1)
fig3.update_yaxes(title_text="Students", row=1, col=2)

save_html(fig3, "sy27_dl_twi_enrollment.html")

# ── Chart 4: Demographics ────────────────────────────────────────────────

print("Generating demographics chart...")

race_display = {
    "White": "White",
    "Black_or_African_American": "Black",
    "Hispanic_or_Latino": "Hispanic/Latino",
    "Asian": "Asian",
    "Multiracial": "Multiracial",
    "Middle_Eastern_or_North_African": "Middle Eastern/N. African",
    "American_Indian_or_Alaska_Native": "Am. Indian/Alaska Native",
    "Native_Hawaiian_Other_Pacific_Islander": "Native Hawaiian/Pac. Islander",
}

# Sort schools by total enrollment
race_sorted = race.sort_values("Total", ascending=True)

fig4 = go.Figure()

for col, display_name in race_display.items():
    pcts = (race_sorted[col] / race_sorted["Total"] * 100).round(1)
    fig4.add_trace(go.Bar(
        y=race_sorted["Short"], x=pcts,
        name=display_name, orientation="h",
        hovertemplate=f"{display_name}: %{{x:.1f}}%<extra></extra>",
        text=[f"{p:.0f}%" if p >= 5 else "" for p in pcts],
        textposition="inside",
    ))

fig4.update_layout(
    title="Student Racial/Ethnic Composition by School (SY 2026-27)",
    xaxis_title="Percentage of Students",
    barmode="stack",
    height=550,
    legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="center", x=0.5, font=dict(size=10)),
    margin=dict(l=120, r=40, t=80, b=130),
    xaxis=dict(range=[0, 100]),
)

save_html(fig4, "sy27_demographics.html")

# ── Chart 5: EL, IEP, Low Income ──────────────────────────────────────────

print("Generating EL/IEP/Low Income chart...")

fig5 = make_subplots(
    rows=1, cols=3,
    subplot_titles=["English Learners (%)", "Students with IEPs (%)", "Low Income (%)"],
    horizontal_spacing=0.08,
)

for df_data, val_col, total_col, col_idx, color in [
    (el, "EL", "Total", 1, "#1f77b4"),
    (iep, "IEP", "Total", 2, "#ff7f0e"),
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
    title="English Learners, IEPs, and Low Income by School (SY 2026-27)",
    height=500,
    margin=dict(l=120, r=40, t=80, b=40),
)

save_html(fig5, "sy27_el_iep_lowincome.html")

# ── Chart 6: Transfer Sankey ──────────────────────────────────────────────

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
    title="Permissive Transfer Flow: 268 Approved Transfers (SY 2026-27)<br><sup>Foster (red) accounted for 37% of outgoing transfers. Lincolnwood (green) was the top destination.</sup>",
    height=600,
    margin=dict(l=20, r=20, t=80, b=40),
    font_size=11,
)

save_html(fig6, "sy27_transfer_sankey.html")

# ── Chart 7: Kindergarten Registration ──────────────────────────────────────

print("Generating kindergarten chart...")

kinder_valid = kinder.dropna(subset=["Projected_Total_All_Programs", "Actual_Total_All_Programs"])
kinder_valid = kinder_valid.sort_values("Projected_Total_All_Programs", ascending=False)

fig7 = go.Figure()

fig7.add_trace(go.Bar(
    x=kinder_valid["School"], y=kinder_valid["Projected_Total_All_Programs"],
    name="Projected", marker_color="rgba(31, 119, 180, 0.7)",
    text=kinder_valid["Projected_Total_All_Programs"].astype(int), textposition="outside",
))

fig7.add_trace(go.Bar(
    x=kinder_valid["School"], y=kinder_valid["Actual_Total_All_Programs"],
    name="Actual (as of 5/12/26)", marker_color="rgba(214, 39, 40, 0.7)",
    text=kinder_valid["Actual_Total_All_Programs"].astype(int), textposition="outside",
))

fig7.update_layout(
    title="Kindergarten Enrollment: Projected vs. Actual (SY 2026-27)<br><sup>157 registrations completed districtwide vs. 238 at same point last year (-34%)</sup>",
    yaxis_title="Students",
    barmode="group",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=60, r=40, t=100, b=60),
)

save_html(fig7, "sy27_kindergarten.html")

# ── Chart 8: Total enrollment by school (simple overview) ───────────────────

print("Generating total enrollment overview...")

school_overview = enrollment.groupby("Short").agg(
    Total=("Total", "sum"),
    MonoL=("MonoL", "sum"),
).reset_index()

# Add program students
twi_by_school = enrollment.groupby("Short").agg(
    TWI=("TWE", lambda x: x.sum()),
    TWS_sum=("TWS", "sum"),
    TWX_sum=("TWX", "sum"),
    DL=("Middle_School_DL", "sum"),
    ACC_sum=("ACC", "sum"),
    RISE_sum=("RISE", "sum"),
    STEP_sum=("STEP", "sum"),
).reset_index()

school_overview = school_overview.merge(twi_by_school, on="Short")
school_overview["TWI_Total"] = school_overview["TWI"] + school_overview["TWS_sum"] + school_overview["TWX_sum"]
school_overview["Other"] = school_overview["Total"] - school_overview["MonoL"] - school_overview["TWI_Total"] - school_overview["DL"] - school_overview["ACC_sum"]
school_overview = school_overview.sort_values("Total", ascending=True)

fig8 = go.Figure()

fig8.add_trace(go.Bar(
    y=school_overview["Short"], x=school_overview["MonoL"],
    name="Monolingual", orientation="h", marker_color="#1f77b4",
))
fig8.add_trace(go.Bar(
    y=school_overview["Short"], x=school_overview["TWI_Total"],
    name="TWI (TWE+TWS+TWX)", orientation="h", marker_color="#2ca02c",
))
fig8.add_trace(go.Bar(
    y=school_overview["Short"], x=school_overview["DL"],
    name="Dual Language (MS)", orientation="h", marker_color="#ff7f0e",
))
fig8.add_trace(go.Bar(
    y=school_overview["Short"], x=school_overview["ACC_sum"],
    name="ACC", orientation="h", marker_color="#9467bd",
))
other_cols = school_overview["RISE_sum"] + school_overview["STEP_sum"]
if other_cols.sum() > 0:
    fig8.add_trace(go.Bar(
        y=school_overview["Short"], x=other_cols,
        name="RISE/STEP", orientation="h", marker_color="#d62728",
    ))

fig8.update_layout(
    title="Total Enrollment by School and Program (SY 2026-27)",
    xaxis_title="Students",
    barmode="stack",
    height=550,
    legend=dict(orientation="h", yanchor="top", y=-0.08, xanchor="center", x=0.5),
    margin=dict(l=120, r=40, t=80, b=120),
)

save_html(fig8, "sy27_enrollment_by_program.html")


# ── Chart 9: Middle School DL detail ──────────────────────────────────────

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
    title="Middle School Enrollment by Grade: Monolingual vs. Dual Language<br><sup>Red dashed line = DEC contract max (28 students). Haven DL 7th grade has fewer than 10 students.</sup>",
    height=400,
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
    margin=dict(l=60, r=40, t=100, b=60),
)

save_html(fig9, "sy27_middle_school_detail.html")

print("\nAll charts generated successfully!")
