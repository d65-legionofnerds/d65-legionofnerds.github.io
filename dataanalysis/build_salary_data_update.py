"""
October 2026 update for the Salary Data page (salary-data.md).

Compares District 65's PA 97-0256 Administrator and Teacher report for
SY2025-26 with the one for SY2026-27, classifying positions with the same
role_map the page's notebook (calculations.ipynb) uses for its charts.

  - SY2025-26: the Evanston rows labeled SchoolYearId 2025 in
    data/target_combined_salary_data.csv (taken from the District's FY26 report,
    assets/Administrator and Teacher FY26.pdf)
  - SY2026-27: data/d65_admin_comp_pdfs/sy26_27_admin_teacher.md, converted from
    assets/Administrator and Teacher FY27.pdf by convert_pa_pdfs.py

Total comp for both years = total salary (base + retirement) + dental, health,
vision and life insurance + bonus + retirement annuities, matching the
notebook's TotalComp for the SY2025-26 rows.

Writes data/d65_salary_fy26_fy27_summary.csv and prints the table used on the page.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
DATA = ROOT / "data"

# role_map is defined in the notebook; read it from there so the two never drift.
nb = json.loads((ROOT / "calculations.ipynb").read_text(encoding="utf-8"))
src = next("".join(c["source"]) for c in nb["cells"]
           if "".join(c["source"]).lstrip().startswith("# Define mapping from PositionCodeDescription"))
ns = {}
exec(src, ns)
role_map = dict(ns["role_map"])

# Titles that first appear (or are truncated differently) in the SY2026-27 report.
role_map.update({
    "interim superintendent": "Admin",
    "assistant superintendent of academic": "Admin",
    "assistant superintendent of account": "Admin",
    "director of student specialized servi": "Admin",
    "director of early childhood program": "Admin",
    "director of buildings, grounds & tran": "Admin",
    "senior manager of health services": "Admin",
    "assistant director of student servic": "Admin",
})
TEACHER_WORDS = ("TEACHER", "TEAC", "GRADE T", "DUAL LANGUAGE")


def classify(pos):
    p = (pos or "").strip()
    role = role_map.get(p.lower())
    if role is None and any(w in p.upper() for w in TEACHER_WORDS):
        role = "Teacher"
    return role


def money(s):
    s = str(s).replace("$", "").replace(",", "").strip()
    return 0.0 if s in ("-", "") else float(s)


# SY2025-26
s = pd.read_csv(DATA / "target_combined_salary_data.csv", low_memory=False)
fy26 = s[(s["District"] == "Evanston CCSD 65") & (s["SchoolYearId"] == 2025)].copy()
fy26["Role"] = fy26["PositionCodeDescription"].map(classify)
fy26 = fy26.rename(columns={"PositionCodeDescription": "position", "TotalComp": "total_comp",
                            "BaseSalary": "base_salary"})

# SY2026-27
lines = [l for l in (DATA / "d65_admin_comp_pdfs" / "sy26_27_admin_teacher.md").read_text(encoding="utf-8").splitlines()
         if l.startswith("| ") and not l.startswith("| Last Name")]
cols = ["last", "first", "position", "base_salary", "retirement", "total_salary", "dental", "health",
        "vision", "life", "bonus", "annuities", "sick", "vacation"]
fy27 = pd.DataFrame([[c.strip() for c in l.strip().strip("|").split("|")] for l in lines], columns=cols)
for c in cols[3:12]:
    fy27[c] = fy27[c].map(money)
fy27["total_comp"] = fy27[["total_salary", "dental", "health", "vision", "life", "bonus", "annuities"]].sum(axis=1)
fy27["Role"] = fy27["position"].map(classify)

unmapped = fy27[fy27["Role"].isna()]
assert unmapped.empty, f"unclassified SY2026-27 titles: {sorted(unmapped['position'].unique())}"

out = []
for label, df in [("SY2025-26", fy26), ("SY2026-27", fy27)]:
    for role in ["Admin", "Principal", "Teacher"]:
        sub = df[df["Role"] == role]
        out.append({"school_year": label, "role": role, "headcount": len(sub),
                    "total_comp": round(sub["total_comp"].sum(), 2),
                    "avg_comp": round(sub["total_comp"].mean(), 2),
                    "total_base_salary": round(sub["base_salary"].sum(), 2)})
summary = pd.DataFrame(out)
summary.to_csv(DATA / "d65_salary_fy26_fy27_summary.csv", index=False)
print(summary.to_string(index=False))

# Admin roster changes, for the page text
a26 = set(fy26.loc[fy26["Role"] == "Admin", "position"].str.upper().str.strip())
a27 = set(fy27.loc[fy27["Role"] == "Admin", "position"].str.upper().str.strip())
print("\nAdmin titles counted by position (SY2025-26 -> SY2026-27):")
c26 = fy26[fy26["Role"] == "Admin"]["position"].str.upper().value_counts()
c27 = fy27[fy27["Role"] == "Admin"]["position"].str.upper().value_counts()
print(pd.concat([c26.rename("SY2025-26"), c27.rename("SY2026-27")], axis=1).fillna(0).astype(int).to_string())
