"""Charts and numbers for enrollment-26.md (fall SY27 building use, class size and closure costs).

Part 1: four charts (PNG) from the fall SY27 dashboard data, written to assets/:
  enrollment26_class_size_vs_utilization.png   regression: class size vs. utilization
  enrollment26_utilization_current.png         current utilization by school
  enrollment26_class_size_by_school.png        average class size by elementary school, TWI flagged
  enrollment26_class_size_heatmap.png          class size by school and grade, K-5
Inputs (data/enrollment_26/), exported from the enrollment_fall26 notebook
(https://github.com/jmclip/enrollment_fall26), where classes are estimated:
  class_size_detail_by_school.csv, utilization_current_vs_predicted.csv,
  capacity_comparison.csv, twi_strands.csv

Part 2: closure savings vs. added busing. Compares the district's transportation tables
(students by transportation category, by school) for today's schools and for closure
scenarios, on the same hazard definition within each pair:
  Close Lincolnwood            2FR vs 1A   (data/*_transportation_idot_d65.csv, current year)
  Close Willard                2DR vs 1A   (same)
  Close Lincolnwood+Washington 3D  vs 0    (data/enrollment_26/0_ and 3D_transportation_d65.csv,
                                            last year's tables, Kingsley still open in the baseline)
New general-education riders = Bus + Hazard + program placements (ACC, STEP, TWE/TWS/TWX).
Costs: District 65 Transportation Memo to the Board, Feb 9, 2026 (~$4.2M/yr; general-ed routes
~$2.4M; ~$80K per added single route). Building savings use FY26 salary disclosures; custodian and
office pay are ASSUMED (no salary data) and marked below.
Outputs: data/enrollment_26/closure_transportation_summary.csv and closure_transportation_by_school.csv

Made with help from Claude (an AI model), which can make mistakes. Please verify.
"""
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")
IN_DIR = os.path.join(DATA_DIR, "enrollment_26")
ASSETS_DIR = os.path.join(HERE, "assets")

# ── Chart style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": "#52514e",
    "xtick.color": "#52514e", "ytick.color": "#0b0b0b",
    "axes.grid": True, "axes.grid.axis": "x", "grid.color": "#e8e7e3", "grid.linewidth": 0.8,
    "axes.axisbelow": True, "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
})
INK, MUTED, DARK_BLUE, MID_BLUE, RED = "#0b0b0b", "#52514e", "#184f95", "#3987e5", "#e34948"
STEP = {"Lincoln", "Lincolnwood", "Washington"}      # STEP use affects their capacity


def short(name):
    """'Dawes Elementary School' -> 'Dawes', 'Chute Middle School' -> 'Chute (MS)'."""
    return (name.replace("Dr Martin Luther King Jr Literary & Fine Arts School", "King Arts")
                .replace(" Elementary School", "").replace(" Middle School", " (MS)").replace(" School", ""))


def save(fig, name):
    fig.savefig(os.path.join(ASSETS_DIR, name), dpi=200)
    plt.close(fig)
    print(f"  Saved assets/{name}")


# ── Load inputs ───────────────────────────────────────────────────────────────
detail = pd.read_csv(os.path.join(IN_DIR, "class_size_detail_by_school.csv"))
util = pd.read_csv(os.path.join(IN_DIR, "utilization_current_vs_predicted.csv"))
util = util.dropna(subset=["util_pct_current"]).assign(school=lambda d: d["school"].map(short)).set_index("school")
capcmp = pd.read_csv(os.path.join(IN_DIR, "capacity_comparison.csv")).set_index("school")
twi_schools = set(pd.read_csv(os.path.join(IN_DIR, "twi_strands.csv"))["school"])

elem = detail[~detail["school"].str.contains("MS") & (detail["grade"] <= 5)].copy()   # King Arts: K-5 only
school_avg = (elem.groupby("school")
              .agg(avg_class_size=("avg_class_size", "mean"), students=("students", "sum"), classes=("sections", "sum"))
              .sort_values("avg_class_size"))

# ── Chart 1: class size vs. utilization (regression) ─────────────────────────
reg = school_avg[["avg_class_size"]].join(util["util_pct_current"]).dropna()
fit = stats.linregress(reg["util_pct_current"], reg["avg_class_size"])
fig, ax = plt.subplots(figsize=(10, 7))
x = np.linspace(reg["util_pct_current"].min() - 3, reg["util_pct_current"].max() + 3, 50)
ax.plot(x, fit.intercept + fit.slope * x, color=RED, linewidth=2, zorder=2)
ax.scatter(reg["util_pct_current"], reg["avg_class_size"], s=110, color=DARK_BLUE, zorder=3)
for sch, r in reg.iterrows():
    ax.annotate(sch, (r["util_pct_current"], r["avg_class_size"]), xytext=(8, 4), textcoords="offset points", fontsize=11)
ax.set_xlabel("Current utilization (% of capacity used)")
ax.set_ylabel("Estimated average class size (students)")
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}%"))
ax.grid(color="#e8e7e3")
sign = "+" if fit.slope >= 0 else "−"
ax.set_title("Higher utilization buildings don't have bigger classes", loc="left", fontsize=15, fontweight="bold", color=INK, pad=30)
ax.text(0, 1.02, f"Line: class size = {fit.intercept:.1f} {sign} {abs(fit.slope):.3f} × utilization.   "
        f"r = {fit.rvalue:.2f},  R² = {fit.rvalue**2:.2f},  p = {fit.pvalue:.2f},  n = {len(reg)} elementary schools",
        transform=ax.transAxes, fontsize=10.5, color=MUTED, parse_math=False)
fig.text(0.01, 0.005, "Class sizes are estimates (Washington and Oakton 5th grade use reported class counts).\n"
         "Utilization = fall SY27 enrollment ÷ smaller of Cap Total and Cordogan Clark capacity. King Arts utilization is K–8.",
         fontsize=9, color=MUTED, style="italic", parse_math=False)
plt.tight_layout(rect=(0, 0.05, 1, 1))
save(fig, "enrollment26_class_size_vs_utilization.png")

# ── Chart 2: current utilization, with capacity and classrooms in each bar ───
label = lambda s: f"{s}*" if s in STEP else s
cur = util["util_pct_current"].sort_values()
fig, ax = plt.subplots(figsize=(10, 8.2))
ax.barh([label(s) for s in cur.index], cur.values, height=0.85, color=DARK_BLUE)
for yi, sch in enumerate(cur.index):
    rooms = capcmp["classrooms_floor_plan"].get(sch, np.nan)
    extra = f"   classrooms: {rooms:.0f}" if pd.notna(rooms) else ""
    if pd.isna(rooms) and pd.notna(capcmp["cordogan_teaching_stations"].get(sch, np.nan)):
        word = "teaching stations" if "(MS)" in sch else "classrooms"
        extra = f"   {word}: {capcmp['cordogan_teaching_stations'][sch]:.0f}"
    ax.text(cur[sch] + 0.9, yi, f"{cur[sch]:.0f}%", va="center", fontsize=11, color=INK, fontweight="bold")
    ax.text(1.2, yi, f"capacity: {util['capacity_used'][sch]:.0f}{extra}", va="center", fontsize=10.5, color="white")
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 100)
ax.set_xticks(range(0, 101, 20), [f"{t}%" for t in range(0, 101, 20)])
ax.set_xlabel("Utilization (enrollment ÷ capacity)")
ax.set_title(f"Utilization runs from {cur.min():.0f}% to {cur.max():.0f}%", loc="left", fontsize=15,
             fontweight="bold", color=INK, pad=28)
ax.text(0, 1.015, "Fall SY27 enrollment ÷ the smaller of Cap Total and Cordogan Clark capacity.",
        transform=ax.transAxes, fontsize=10, color=MUTED)
plt.tight_layout(rect=(0, 0.05, 1, 1))
fig.text(0.01, 0.01, "* STEP program use affects total capacity at these schools.\nClassrooms = floor-plan count "
         "(Foster: teaching stations); middle schools show Cordogan teaching stations.", fontsize=9.5, color=MUTED, style="italic")
save(fig, "enrollment26_utilization_current.png")

# ── Chart 3: average class size by elementary school, TWI flagged ────────────
sa = school_avg
fig, ax = plt.subplots(figsize=(10, 7))
ax.barh(sa.index, sa["avg_class_size"], height=0.85, color=MID_BLUE)
for yi, (sch, r) in enumerate(sa.iterrows()):
    tag = "   ·   dual-language (TWI)" if sch in twi_schools else ""
    ax.text(r["avg_class_size"] + 0.2, yi, f"{r['avg_class_size']:.1f}", va="center", fontsize=11, color=INK, fontweight="bold")
    ax.text(0.3, yi, f"K–5 students: {r['students']:.0f}   classes: {r['classes']:.0f}{tag}", va="center", fontsize=10.5,
            color="white", fontweight="bold" if tag else "normal")
ax.axvline(24, color=MUTED, linewidth=1, linestyle="--")
ax.text(24, len(sa) - 0.35, " cap 24", va="bottom", fontsize=9.5, color=MUTED)
ax.tick_params(axis="y", length=0)
ax.set_xlim(0, 26.5)
ax.set_xlabel("Average class size (average of K–5 grade averages)")
ax.set_title("The smallest classes are at the dual-language schools", loc="left", fontsize=15, fontweight="bold", color=INK, pad=28)
ax.text(0, 1.015, "Estimated average class size per elementary school, fall SY27 (every grade weighted equally).",
        transform=ax.transAxes, fontsize=10, color=MUTED)
plt.tight_layout(rect=(0, 0.05, 1, 1))
fig.text(0.01, 0.01, "Estimate: fewest classes at 24 per class; dual-language strands and Oakton's ACC program count as their "
         "own classes.\nKing Arts K–5 only.", fontsize=9, color=MUTED, style="italic", linespacing=1.3)
save(fig, "enrollment26_class_size_by_school.png")

# ── Chart 4: heatmap of class size by school and grade, sorted by school average ──
K5 = [0, 1, 2, 3, 4, 5]
H = elem.pivot_table(index="school", columns="grade", values="avg_class_size")[K5]
S = elem.pivot_table(index="school", columns="grade", values="sections", aggfunc="sum")[K5]
H["avg"], S["avg"] = H[K5].mean(axis=1), S[K5].sum(axis=1)
order = H.sort_values("avg").index
H, S = H.loc[order], S.loc[order]
fig, ax = plt.subplots(figsize=(10, 7.5))
cmap = LinearSegmentedColormap.from_list("red_purple_blue", ["#e0182d", "#8f3fd1", "#0a3a9e"])
im = ax.imshow(H.values.astype(float), cmap=cmap, norm=TwoSlopeNorm(vmin=14, vcenter=18, vmax=23), aspect="auto")
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        ax.text(j, i - 0.12, f"{H.iat[i, j]:.1f}", ha="center", va="center", fontsize=12.5, fontweight="bold", color="white")
        ax.text(j, i + 0.25, f"{int(S.iat[i, j])} cl.", ha="center", va="center", fontsize=8, color="white")
ax.set_xticks(range(7), ["K", "1", "2", "3", "4", "5", "School\naverage"])
ax.set_yticks(range(len(order)), order)
ax.tick_params(length=0); ax.grid(False)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_xticks(np.arange(-.5, 7, 1), minor=True); ax.set_yticks(np.arange(-.5, len(order), 1), minor=True)
ax.grid(which="minor", color="#fcfcfb", linewidth=2); ax.tick_params(which="minor", length=0)
ax.axvline(5.5, color="#fcfcfb", linewidth=7)
ax.set_xlabel("Grade")
ax.set_title("A third of elementary grades average under 18 students per class", loc="left", fontsize=15,
             fontweight="bold", color=INK, pad=52)
ax.text(0, 1.012, "Big number = students per class; small = estimated classes. School average = average of the six grade averages\n"
        "(small number = total K–5 classes). Fewest classes at 24 per class; TWI and ACC classes counted separately,\n"
        "except Washington (reported: 4 classes per grade, 3 in 1st and 2nd). King Arts: K–5 only.",
        transform=ax.transAxes, fontsize=9.5, color=MUTED)
cb = fig.colorbar(im, ax=ax, fraction=0.03, pad=0.02); cb.outline.set_visible(False)
cb.set_ticks([14, 16, 18, 20, 22, 23]); cb.set_label("Students per class (red = smaller, purple = 18, blue = larger)", color=MUTED)
plt.tight_layout(rect=(0, 0.06, 1, 1))
fig.text(0.01, 0.01, "Estimate: schools may run more, smaller classes. TWI and Oakton ACC students assumed evenly spread across K–5.\n"
         "Cap = district capacity standard (24), not the contract limit. Willard and Washington 2nd grade checked against parent reports.",
         fontsize=9, color=MUTED, style="italic")
save(fig, "enrollment26_class_size_heatmap.png")

print(f"Regression: slope {fit.slope:.3f}, r = {fit.rvalue:.2f}, R² = {fit.rvalue**2:.2f}, p = {fit.pvalue:.2f}, n = {len(reg)}")
print(f"School-grades under 18: {(elem['avg_class_size'] < 18).sum()} of {len(elem)}")

# ══ Part 2: closure savings vs. added busing ══════════════════════════════════
GEN_ED = ["Bus", "Hazard", "ACC Placement", "STEP Placement",
          "TWE Placement", "TWS Placement", "TWX Placement"]

GEN_ED_ROUTE_COST = 2_400_000      # memo: 20 double (~$1.8M) + 7 single (~$0.6M)
DOUBLE_ROUTE_COST = 90_000         # $1.8M / 20
RIDERS_PER_DOUBLE_ROUTE = 110      # ~55 riders per run, two runs (assumption)

PRINCIPAL = 180_753                # FY26 PA 96-0434 average, salary + benefits
ASSISTANT_PRINCIPAL = 160_129      # same report; only if a school has one
LIBRARIAN = 132_861                # FY26 PA 97-0256 average; only if the position is cut
OFFICE = 60_000                    # ASSUMED: school secretary / health clerk
CUSTODIAN = 65_000                 # ASSUMED
CUSTODIANS_PER_BUILDING = 2.5      # 64 custodians district-wide, ~4 per building; ~2.5 go away
UTILITIES_2025 = {"Lincolnwood": 50_293, "Willard": 62_350, "Washington": 89_559}

SCENARIOS = [
    # label, closed schools, baseline file, scenario file
    ("Close Lincolnwood (2FR)", ["Lincolnwood"], "1A_transportation_idot_d65.csv", "2FR_transportation_idot_d65.csv"),
    ("Close Willard (2DR)", ["Willard"], "1A_transportation_idot_d65.csv", "2DR_transportation_idot_d65.csv"),
    ("Close Lincolnwood + Washington (3D)", ["Lincolnwood", "Washington"],
     "enrollment_26/0_transportation_d65.csv", "enrollment_26/3D_transportation_d65.csv"),
]


def load_transport(fname):
    d = pd.read_csv(os.path.join(DATA_DIR, fname))
    d = d.rename(columns={d.columns[0]: "school"})
    d = d[d["school"].notna()].copy()
    d["school"] = (d["school"].str.replace(".", "", regex=False)
                   .str.replace(" Elementary School", "", regex=False)
                   .str.replace(" Middle School", " MS", regex=False)
                   .str.replace(" School", "", regex=False))
    return d.set_index("school")


def riders(d):
    return d[GEN_ED].sum(axis=1)


current_riders = riders(load_transport("1A_transportation_idot_d65.csv")).sum()
cost_per_rider = GEN_ED_ROUTE_COST / current_riders

rows, by_school = [], []
for label_, closed, base_f, scen_f in SCENARIOS:
    b, s = riders(load_transport(base_f)), riders(load_transport(scen_f))
    idx = b.index.union(s.index)
    change = s.reindex(idx).fillna(0) - b.reindex(idx).fillna(0)
    added = int(change.sum())
    for sch, v in change[change != 0].items():
        by_school.append({"scenario": label_, "school": sch, "change": int(v)})

    routes = math.ceil(added / RIDERS_PER_DOUBLE_ROUTE)
    transport_low, transport_high = routes * DOUBLE_ROUTE_COST, added * cost_per_rider

    n = len(closed)
    bldg_low = n * (PRINCIPAL + OFFICE + CUSTODIANS_PER_BUILDING * CUSTODIAN) + sum(UTILITIES_2025[c] for c in closed)
    bldg_high = bldg_low + n * LIBRARIAN + ASSISTANT_PRINCIPAL + OFFICE   # plus one AP and one health clerk
    rows.append({"scenario": label_, "added_riders": added, "routes": routes,
                 "transport_low": transport_low, "transport_high": transport_high,
                 "building_low": bldg_low, "building_high": bldg_high,
                 "net_low": bldg_low - transport_high, "net_high": bldg_high - transport_low})

summary = pd.DataFrame(rows)
pd.DataFrame(rows).round(0).to_csv(os.path.join(IN_DIR, "closure_transportation_summary.csv"), index=False)
pd.DataFrame(by_school).to_csv(os.path.join(IN_DIR, "closure_transportation_by_school.csv"), index=False)
print(summary.round(0).to_string())
print(f"Current general-ed riders: {current_riders:,}; average cost per rider ${cost_per_rider:,.0f}")
