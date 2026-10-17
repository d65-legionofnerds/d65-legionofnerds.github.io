"""
Builds the data and chart for the SY2025-26 vs SY2026-27 comparison page
(sy26-sy27-changes.md): what changed in District 65's staffing and certified
payroll in the year Kingsley and Bessie Rhodes closed.

Reads:
  - data/d65_fte_by_category_fy26_roundtable.csv  District staff by employee category, SY2025-26,
        as published by the Evanston RoundTable (Nov 2, 2025, Table 2). NOTE: the District's pivot
        is labeled "COUNTA", i.e. a count of employees, not a sum of FTE.
  - data/d65_fte_by_category_fy27_district.csv    District "FTEs by Employee Category" (October 2026),
        a SUM of FTE.
  - data/target_combined_salary_data.csv          SY2025-26 PA 97-0256 rows (Evanston, SchoolYearId 2025)
  - data/d65_admin_comp_pdfs/sy26_27_admin_teacher.md   SY2026-27 PA 97-0256 (convert_pa_pdfs.py)
  - data/staff_directory_20251219.csv             December 2025 staff directory (who worked at Kingsley
        and Bessie Rhodes)

Writes:
  - data/sy26_sy27_fte_by_category.csv
  - data/sy26_sy27_certified_payroll.csv
  - data/sy26_sy27_closed_school_staff.csv        aggregate counts only (no names)
  - assets/sy26_sy27_fte_change.html
"""
import re
import statistics
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).parent
DATA = ROOT / "data"
ASSETS = ROOT / "assets"

CLOSED_SCHOOLS = {
    "Kingsley": "Kingsley Elementary School",
    "Bessie Rhodes": "Dr. Bessie Rhodes School of Global Studies",
}

LABELS = {
    "CERT TEACH": "Teachers", "TA": "Teacher assistants", "TA SIGN": "Teacher assistants (new TA SIGN code)",
    "MISC": "Educational support staff", "SACC": "School-age child care", "CERT": "Other certified staff",
    "ADMIN": "Central-office administrators", "ADMIN SCHOOL": "School administrators",
    "CABINET": "Cabinet", "SUPT": "Superintendent", "CERT GUIDE": "Guidance counselors",
    "FAMCTR": "Family Center staff", "CERT SLP": "Speech-language pathologists",
    "CERT OTPT": "Occupational / physical therapists", "CUST": "Custodians",
    "AA10": "Admin assistants (10-month)", "AA11": "Admin assistants (11-month)",
    "AA12": "Admin assistants (12-month)", "FOOD": "Food service", "FOOD ECC": "Food service (Head Start)",
    "FOOD MGR": "Food service managers", "MISC ECC": "Child-care support staff",
    "MISC ECC 10": "Child-care support staff (10-month)", "CCTA": "Child-care teaching assistants",
    "CERT COACH": "Instructional coaches", "FACE": "Family & community liaisons", "TECH": "11-month techs",
    "SIGN": "SIGN (new code)", "CERT SOCWKR": "Social workers", "CERT PSYCH": "Psychologists",
    "CERT NURSE": "Certified nurse", "NURREG": "Registered nurses", "HEALTH": "Health clerks",
    "INTERN": "Interns", "BEH": "Behavior support technicians", "MISC EXAS": "Executive assistants",
}
ADMIN_CODES = {"ADMIN", "ADMIN SCHOOL", "CABINET", "SUPT"}
GROUP_COLORS = {"Certified": "#2980b9", "Administrators": "#c0392b", "Classified / other": "#7f8c8d"}


def group(code):
    if code in ADMIN_CODES:
        return "Administrators"
    if code.startswith("CERT"):
        return "Certified"
    return "Classified / other"


# ------------------------------------------------------------------
# 1. Staff by employee category
# ------------------------------------------------------------------
fy26 = pd.read_csv(DATA / "d65_fte_by_category_fy26_roundtable.csv")
fy26["emp_category"] = fy26["emp_category"].replace({"COUNCIL": "CABINET"})   # same category, renamed in FY27
fy27 = pd.read_csv(DATA / "d65_fte_by_category_fy27_district.csv")
cat = fy26[["emp_category", "description", "count"]].merge(fy27, on="emp_category", how="outer")
cat["description"] = cat["description"].fillna("(new code in SY2026-27)")
cat = cat.fillna({"count": 0, "sum_of_fte": 0}).rename(columns={"count": "sy26_count", "sum_of_fte": "sy27_fte"})
cat["change"] = (cat["sy27_fte"] - cat["sy26_count"]).round(2)
cat["group"] = cat["emp_category"].map(group)
cat["label"] = cat["emp_category"].map(LABELS)
assert cat["label"].notna().all(), cat.loc[cat["label"].isna(), "emp_category"].tolist()
cat = cat.sort_values("change")
cat.to_csv(DATA / "sy26_sy27_fte_by_category.csv", index=False)

print("Totals: SY26 count %.2f  SY27 FTE %.2f  change %.2f"
      % (cat.sy26_count.sum(), cat.sy27_fte.sum(), cat.change.sum()))
print(cat.groupby("group")[["sy26_count", "sy27_fte", "change"]].sum().round(2))

# ------------------------------------------------------------------
# 2. Certified payroll (PA 97-0256), SY26 vs SY27
# ------------------------------------------------------------------
def person(last, first):
    first = str(first).upper().strip()
    return (str(last).upper().strip(), first.split()[0] if first else "")


def money(s):
    s = str(s).replace("$", "").replace(",", "").strip()
    return 0.0 if s in ("-", "") else float(s)


s = pd.read_csv(DATA / "target_combined_salary_data.csv", low_memory=False)
p26 = s[(s["District"] == "Evanston CCSD 65") & (s["SchoolYearId"] == 2025)]
p26 = pd.DataFrame({"key": [person(l, f) for l, f in zip(p26["LastName"], p26["FirstName"])],
                    "position": p26["PositionCodeDescription"].values,
                    "base": p26["BaseSalary"].values, "comp": p26["TotalComp"].values})

lines = [l for l in (DATA / "d65_admin_comp_pdfs" / "sy26_27_admin_teacher.md").read_text(encoding="utf-8").splitlines()
         if l.startswith("| ") and not l.startswith("| Last Name")]
cols = ["last", "first", "position", "base", "retirement", "total_salary", "dental", "health",
        "vision", "life", "bonus", "annuities", "sick", "vacation"]
r27 = pd.DataFrame([[c.strip() for c in l.strip().strip("|").split("|")] for l in lines], columns=cols)
for c in cols[3:12]:
    r27[c] = r27[c].map(money)
p27 = pd.DataFrame({"key": [person(l, f) for l, f in zip(r27["last"], r27["first"])],
                    "position": r27["position"],
                    "base": r27["base"],
                    "comp": r27[["total_salary", "dental", "health", "vision", "life", "bonus", "annuities"]].sum(axis=1)})

k26, k27 = set(p26["key"]), set(p27["key"])


def surname_parts(last):
    return {t for t in re.split(r"[-\s]+", last) if len(t) > 1}


# Link people whose surname changed between the two reports (e.g. a hyphenated
# name added or dropped): same first name, a shared surname part, unmatched on
# both sides, and exactly one candidate each way. Found 4 in SY27, all in the
# same job (incl. the Bessie Rhodes assistant principal, ANTRIM-CAMBIUM -> ANTRIM GRAF).
un26, un27 = k26 - k27, k27 - k26
cands = {a: [b for b in un27 if b[1] == a[1] and surname_parts(a[0]) & surname_parts(b[0])] for a in un26}
alias = {a: c[0] for a, c in cands.items()
         if len(c) == 1 and sum(c[0] in other for other in cands.values()) == 1}
to27 = {k: k for k in k26 & k27} | alias          # SY26 person -> their SY27 key
print("Surname changes linked:", len(alias))

b26, b27 = dict(zip(p26["key"], p26["base"])), dict(zip(p27["key"], p27["base"]))
raises = [b27[k27_] / b26[k] - 1 for k, k27_ in to27.items() if b26[k] > 0 and b27[k27_] > 0]
payroll = pd.DataFrame([
    {"measure": "People on the PA 97-0256 report", "sy26": len(p26), "sy27": len(p27)},
    {"measure": "Total compensation ($)", "sy26": round(p26["comp"].sum(), 2), "sy27": round(p27["comp"].sum(), 2)},
    {"measure": "Base salary ($)", "sy26": round(p26["base"].sum(), 2), "sy27": round(p27["base"].sum(), 2)},
    {"measure": "Average base salary, excluding $0 rows ($)",
     "sy26": round(p26.loc[p26["base"] > 0, "base"].mean(), 2), "sy27": round(p27.loc[p27["base"] > 0, "base"].mean(), 2)},
    {"measure": "SY26 people still on the report in SY27", "sy26": len(k26), "sy27": len(to27)},
    {"measure": "Median base-salary change, same person", "sy26": None, "sy27": round(statistics.median(raises), 4)},
])
payroll.to_csv(DATA / "sy26_sy27_certified_payroll.csv", index=False)
print("\n", payroll.to_string(index=False))
district_retention = len(to27) / len(k26)

# ------------------------------------------------------------------
# 3. Staff of the two closed schools (Dec 2025 directory) — where are they in SY27?
# ------------------------------------------------------------------
pos27 = dict(zip(p27["key"], p27["position"].str.upper()))
d = pd.read_csv(DATA / "staff_directory_20251219.csv")
d["key"] = [person(" ".join(n.split()[1:]), n.split()[0]) for n in d["name"]]

rows = []
for school, loc in CLOSED_SCHOOLS.items():
    x = d[d["location"] == loc]
    cert = x[x["key"].isin(k26)]                       # certified staff (on SY26 PA 97-0256)
    still = cert[cert["key"].isin(to27)]
    leaders = cert[cert["title"].str.contains("Principal", case=False)]
    rows.append({
        "school": school,
        "directory_staff_dec2025": len(x),
        "certified_on_sy26_report": len(cert),
        "certified_on_sy27_report": len(still),
        "certified_retention_pct": round(len(still) / len(cert) * 100, 1),
        "principals_aps_sy26": len(leaders),
        "principals_aps_still_principal_or_ap_sy27": int(sum("PRINCIPAL" in pos27.get(to27.get(k), "") for k in leaders["key"])),
        "noncertified_staff_dec2025": len(x) - len(cert),   # paras, lunchroom, SACC, custodial: no public roster
    })
closed = pd.DataFrame(rows)
closed.to_csv(DATA / "sy26_sy27_closed_school_staff.csv", index=False)
print("\n", closed.to_string(index=False))
print(f"\nDistrict-wide: {district_retention:.1%} of SY26 PA 97-0256 people are on the SY27 report")

# ------------------------------------------------------------------
# 4. Chart: change by category
# ------------------------------------------------------------------
# Chart nets TA and the new TA SIGN code together: the District moved 7 teacher
# assistants to TA SIGN, so showing -14 and +7 separately would overstate both moves.
plot = cat.copy()
ta = plot["emp_category"].isin(["TA", "TA SIGN"])
plot = pd.concat([plot[~ta], pd.DataFrame([{
    "emp_category": "TA + TA SIGN", "label": "Teacher assistants (TA + new TA SIGN code)", "group": "Classified / other",
    "sy26_count": plot.loc[ta, "sy26_count"].sum(), "sy27_fte": plot.loc[ta, "sy27_fte"].sum(),
    "change": round(plot.loc[ta, "change"].sum(), 2)}])]).sort_values("change")
chg = plot[plot["change"].abs() >= 0.5].copy()
chg["text"] = chg["change"].map(lambda v: f"{v:+g}")
fig = go.Figure()
for g, color in GROUP_COLORS.items():
    sub = chg[chg["group"] == g]
    fig.add_trace(go.Bar(
        y=sub["label"], x=sub["change"], orientation="h", name=g, marker_color=color,
        text=sub["text"], textposition="outside", cliponaxis=False,
        customdata=sub[["sy26_count", "sy27_fte", "emp_category"]],
        hovertemplate="<b>%{y}</b> (%{customdata[2]})<br>SY25-26: %{customdata[0]}<br>"
                      "SY26-27: %{customdata[1]}<br>Change: %{x:+g}<extra></extra>",
    ))
fig.update_layout(
    title=dict(text="<b>District 65 Staff by Category: SY2025-26 to SY2026-27</b><br>"
                    "<span style='font-size:13px;color:#444'>Categories that changed by at least 0.5. "
                    f"Total: {cat.sy26_count.sum():,.0f} → {cat.sy27_fte.sum():,.2f} ({cat.change.sum():+.2f})</span>",
               x=0.5, xanchor="center", font=dict(size=18)),
    height=760, plot_bgcolor="white", bargap=0.25,
    yaxis=dict(categoryorder="array", categoryarray=chg["label"].tolist()[::-1], automargin=True),
    xaxis=dict(title="Change (SY2026-27 FTE minus SY2025-26 count)", showgrid=True, gridcolor="#eee", range=[-27, 10],
               zeroline=True, zerolinecolor="#333"),
    legend=dict(orientation="h", y=-0.13, x=0.5, xanchor="center"),
    margin=dict(l=40, r=40, t=90, b=150),
)
fig.add_annotation(
    text="<i>SY2025-26 is the District's count of employees by category (published by the Evanston RoundTable);<br>"
         "SY2026-27 is the District's sum of FTE. Part-time staff count as 1 in the first and as a fraction in the second.</i>",
    xref="paper", yref="paper", x=0, y=-0.25, showarrow=False, xanchor="left", align="left",
    font=dict(size=11, color="#666"),
)
fig.write_html(ASSETS / "sy26_sy27_fte_change.html", include_plotlyjs="cdn", div_id="sy26_sy27_fte_change")
print("Wrote", ASSETS / "sy26_sy27_fte_change.html")
