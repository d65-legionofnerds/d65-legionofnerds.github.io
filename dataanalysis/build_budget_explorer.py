"""
Parse all D65 AFR files to extract Educational Fund expenditures by ISBE
function code, then generate a standalone interactive HTML budget explorer.

Adapted from build_afr_admin_pool.py — reuses its proven Excel parsing logic
but captures ALL function codes in the Educational Fund (not just admin).

On-behalf / pension payments are excluded.

Output:
  assets/budget_explorer.html — standalone interactive Plotly app

Run:
  python build_budget_explorer.py
"""

import json
import os
import re
import warnings

import openpyxl
import pandas as pd
import xlrd

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.abspath(__file__))
AFR_DIR = os.path.join(ROOT, "data", "afr")
ASSETS_DIR = os.path.join(ROOT, "assets")

FUNCTION_HIERARCHY = {
    "1100": ("Instruction", "Regular Programs", "Regular Programs K-12"),
    "1115": ("Instruction", "Regular Programs", "Charter Schools"),
    "1125": ("Instruction", "Pre-K Programs", "Pre-K Programs"),
    "1200": ("Instruction", "Special Education", "Special Ed K-12"),
    "1225": ("Instruction", "Special Education", "Special Ed Pre-K"),
    "1250": ("Instruction", "Remedial/Supplemental", "Remedial & Supplemental K-12"),
    "1275": ("Instruction", "Remedial/Supplemental", "Remedial & Supplemental Pre-K"),
    "1300": ("Instruction", "Other Instruction", "Adult/Continuing Ed"),
    "1400": ("Instruction", "Other Instruction", "CTE Programs"),
    "1500": ("Instruction", "Co-Curricular", "Interscholastic Programs"),
    "1600": ("Instruction", "Summer & Extended", "Summer School"),
    "1650": ("Instruction", "Gifted", "Gifted Programs"),
    "1700": ("Instruction", "Other Instruction", "Driver's Education"),
    "1800": ("Instruction", "Bilingual", "Bilingual Programs"),
    "1900": ("Instruction", "Other Instruction", "Truant Alt & Optional Programs"),
    "1910": ("Instruction", "Private Tuition", "Private Tuition - Regular Programs"),
    "1911": ("Instruction", "Private Tuition", "Private Tuition - Special Ed"),
    "1912": ("Instruction", "Private Tuition", "Private Tuition - CTE"),
    "1913": ("Instruction", "Private Tuition", "Private Tuition - Other"),
    "1914": ("Instruction", "Private Tuition", "Private Tuition - Interscholastic"),
    "1915": ("Instruction", "Private Tuition", "Private Tuition - Summer School"),
    "1916": ("Instruction", "Private Tuition", "Private Tuition - Gifted"),
    "1917": ("Instruction", "Private Tuition", "Private Tuition - Driver's Ed"),
    "1918": ("Instruction", "Private Tuition", "Private Tuition - Bilingual"),
    "1919": ("Instruction", "Private Tuition", "Private Tuition - Truant Alt"),
    "1920": ("Instruction", "Private Tuition", "Private Tuition - Pre-K"),
    "1921": ("Instruction", "Private Tuition", "Private Tuition - Remedial"),
    "1922": ("Instruction", "Private Tuition", "Private Tuition - Spec Ed Pre-K"),
    "1999": ("Instruction", "Other Instruction", "Student Activity Fund"),
    "2110": ("Student Support", "Student Support", "Attendance & Social Work"),
    "2120": ("Student Support", "Student Support", "Guidance Services"),
    "2130": ("Student Support", "Student Support", "Health Services"),
    "2140": ("Student Support", "Student Support", "Psychological Services"),
    "2150": ("Student Support", "Student Support", "Speech Pathology & Audiology"),
    "2190": ("Student Support", "Student Support", "Other Student Support"),
    "2210": ("Instructional Staff Support", "Instructional Staff Support", "Improvement of Instruction"),
    "2220": ("Instructional Staff Support", "Instructional Staff Support", "Educational Media"),
    "2230": ("Instructional Staff Support", "Instructional Staff Support", "Assessment & Testing"),
    "2310": ("General Administration", "General Administration", "Board of Education"),
    "2320": ("General Administration", "General Administration", "Executive Administration"),
    "2330": ("General Administration", "General Administration", "Special Area Administration"),
    "2361": ("General Administration", "General Administration", "Tort Immunity"),
    "2365": ("General Administration", "General Administration", "Tort/Worker's Comp"),
    "2410": ("School Administration", "School Administration", "Office of the Principal"),
    "2490": ("School Administration", "School Administration", "Other School Admin"),
    "2510": ("Business Services", "Business Services", "Direction of Business Support"),
    "2520": ("Business Services", "Business Services", "Fiscal Services"),
    "2540": ("Business Services", "Business Services", "Operation & Maintenance of Plant"),
    "2550": ("Business Services", "Business Services", "Pupil Transportation"),
    "2560": ("Business Services", "Business Services", "Food Services"),
    "2570": ("Business Services", "Business Services", "Internal Services"),
    "2610": ("Central Support", "Central Support", "Direction of Central Support"),
    "2620": ("Central Support", "Central Support", "Planning, Research & Development"),
    "2630": ("Central Support", "Central Support", "Information Services"),
    "2640": ("Central Support", "Central Support", "Staff Services"),
    "2660": ("Central Support", "Central Support", "Data Processing / IT"),
    "2900": ("Other Support", "Other Support", "Other Support Services"),
    "3000": ("Community Services", "Community Services", "Community Services"),
    "4110": ("Payments to Other Districts", "In-State Payments", "Payments - Regular Programs"),
    "4120": ("Payments to Other Districts", "In-State Payments", "Payments - Special Ed"),
    "4130": ("Payments to Other Districts", "In-State Payments", "Payments - Adult/Continuing Ed"),
    "4140": ("Payments to Other Districts", "In-State Payments", "Payments - CTE"),
    "4170": ("Payments to Other Districts", "In-State Payments", "Payments - Community College"),
    "4190": ("Payments to Other Districts", "In-State Payments", "Other In-State Payments"),
    "4210": ("Payments to Other Districts", "Tuition Payments", "Tuition - Regular Programs"),
    "4220": ("Payments to Other Districts", "Tuition Payments", "Tuition - Special Ed"),
    "4230": ("Payments to Other Districts", "Tuition Payments", "Tuition - Adult/Continuing Ed"),
    "4240": ("Payments to Other Districts", "Tuition Payments", "Tuition - CTE"),
    "4270": ("Payments to Other Districts", "Tuition Payments", "Tuition - Community College"),
    "4280": ("Payments to Other Districts", "Tuition Payments", "Tuition - Other Programs"),
    "4290": ("Payments to Other Districts", "Tuition Payments", "Other Tuition Payments"),
    "4310": ("Payments to Other Districts", "Transfer Payments", "Transfers - Regular Programs"),
    "4320": ("Payments to Other Districts", "Transfer Payments", "Transfers - Special Ed"),
    "4330": ("Payments to Other Districts", "Transfer Payments", "Transfers - Adult/Continuing Ed"),
    "4340": ("Payments to Other Districts", "Transfer Payments", "Transfers - CTE"),
    "4370": ("Payments to Other Districts", "Transfer Payments", "Transfers - Community College"),
    "4380": ("Payments to Other Districts", "Transfer Payments", "Transfers - Other Programs"),
    "4390": ("Payments to Other Districts", "Transfer Payments", "Other Transfer Payments"),
    "4400": ("Payments to Other Districts", "Out-of-State Payments", "Payments to Out-of-State"),
    "5110": ("Debt Service", "Debt Service", "Interest - Tax Anticipation Warrants"),
    "5120": ("Debt Service", "Debt Service", "Interest - Tax Anticipation Notes"),
    "5130": ("Debt Service", "Debt Service", "Interest - CPPRT Anticipation Notes"),
    "5140": ("Debt Service", "Debt Service", "Interest - Other Short-Term"),
    "5150": ("Debt Service", "Debt Service", "Other Interest on Short-Term Debt"),
    "5200": ("Debt Service", "Debt Service", "Interest on Long-Term Debt"),
    "5300": ("Debt Service", "Debt Service", "Principal on Long-Term Debt"),
    "5400": ("Debt Service", "Debt Service", "Debt Service - Other"),
    "6000": ("Contingencies", "Contingencies", "Provisions for Contingencies"),
}

ROLLUP_CODES = {
    "1000", "2000", "2100", "2200", "2300", "2400", "2500", "2600",
    "3000", "4000", "4100", "4200", "4300", "5000", "5100",
}

KNOWN_LEAF_CODES = set(FUNCTION_HIERARCHY.keys())

EXCLUDE_SECTION_KEYWORDS = [
    "MR/SS", "O&M", "TORT FUND", "TRANSPORTATION FUND",
    "CAPITAL PROJECTS", "FIRE PREVENTION", "MUNICIPAL RETIREMENT",
    "OPERATIONS & MAINTENANCE",
]


# ---------------------------------------------------------------------------
# Excel parsing (reused from build_afr_admin_pool.py)
# ---------------------------------------------------------------------------

def fy_from_filename(filename):
    m = re.search(r"AFR\s*(\d{2})", filename, re.IGNORECASE)
    if m:
        return 2000 + int(m.group(1))
    m = re.search(r"Budget\s*(\d{2})", filename, re.IGNORECASE)
    if m:
        return 2000 + int(m.group(1))
    return None


def parse_xlsx(fp):
    wb = openpyxl.load_workbook(fp, data_only=True)
    expsheet = None
    for n in wb.sheetnames:
        if "Expenditures" in n:
            expsheet = wb[n]
            break
    if expsheet is None:
        return None
    rows = []
    for r in range(1, expsheet.max_row + 1):
        rowvals = [expsheet.cell(row=r, column=c).value for c in range(1, 12)]
        rows.append(rowvals)
    return rows


def parse_xls(fp):
    wb = xlrd.open_workbook(fp)
    expsheet = None
    for n in wb.sheet_names():
        if "Expenditures" in n:
            expsheet = wb.sheet_by_name(n)
            break
    if expsheet is None:
        return None
    rows = []
    for r in range(expsheet.nrows):
        rowvals = []
        for c in range(min(11, expsheet.ncols)):
            v = expsheet.cell_value(r, c)
            if v == "":
                v = None
            rowvals.append(v)
        rows.append(rowvals)
    return rows


def normalize_func(v):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return str(int(v))
    s = str(v).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s


def num(v):
    if v is None:
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        v2 = v.replace(",", "").replace("$", "").strip()
        if v2 == "" or v2 == "-":
            return 0.0
        try:
            return float(v2)
        except ValueError:
            return 0.0
    return 0.0


# ---------------------------------------------------------------------------
# AFR parsing — all Ed Fund function codes
# ---------------------------------------------------------------------------

def is_ed_section(section):
    if "(ED)" in section:
        return True
    if "EDUCATIONAL FUND" in section:
        return True
    return False


def is_excluded_section(section):
    s = section.upper()
    for kw in EXCLUDE_SECTION_KEYWORDS:
        if kw in s:
            return True
    return False


FUND_MARKERS = re.compile(
    r"\((ED|O&M|MR/SS|TORT|TR|DS|CP|FP&S|TF)\)", re.IGNORECASE
)


def parse_afr_all(filepath, year):
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        rows = parse_xlsx(filepath)
    elif ext == ".xls":
        rows = parse_xls(filepath)
    else:
        return [], {}

    if rows is None:
        return [], {}

    records = []
    rollups = {}
    current_section = ""

    for row in rows:
        desc = row[0]
        if isinstance(desc, str):
            d = desc.strip().upper()
            if "EDUCATIONAL FUND" in d or "OPERATIONS & MAINTENANCE FUND" in d:
                current_section = d
            elif FUND_MARKERS.search(d):
                current_section = d

        if is_excluded_section(current_section) or not is_ed_section(current_section):
            continue

        if isinstance(desc, str) and ("ON BEHALF" in desc.upper() or "ON-BEHALF" in desc.upper()):
            continue

        func = normalize_func(row[1])
        if func is None:
            continue

        total = num(row[10]) if len(row) > 10 else 0.0
        salaries = num(row[2])
        benefits = num(row[3])

        if func in ROLLUP_CODES and func != "3000":
            rollups[func] = total
            continue

        if func in KNOWN_LEAF_CODES or (func.isdigit() and len(func) == 4):
            records.append({
                "func": func,
                "total": total,
                "salaries": salaries,
                "benefits": benefits,
            })

    return records, rollups


def bucket_unknown_code(code):
    prefix = code[0]
    if prefix == "1":
        return ("Instruction", "Other Instruction", f"Function {code}")
    elif prefix == "2":
        c2 = int(code[:2])
        if c2 == 21:
            return ("Student Support", "Student Support", f"Function {code}")
        elif c2 == 22:
            return ("Instructional Staff Support", "Instructional Staff Support", f"Function {code}")
        elif c2 == 23:
            return ("General Administration", "General Administration", f"Function {code}")
        elif c2 == 24:
            return ("School Administration", "School Administration", f"Function {code}")
        elif c2 == 25:
            return ("Business Services", "Business Services", f"Function {code}")
        elif c2 == 26:
            return ("Central Support", "Central Support", f"Function {code}")
        else:
            return ("Other", "Other", f"Function {code}")
    elif prefix == "3":
        return ("Community Services", "Community Services", f"Function {code}")
    elif prefix == "4":
        return ("Payments to Other Districts", "Payments to Other Districts", f"Function {code}")
    elif prefix == "5":
        return ("Debt Service", "Debt Service", f"Function {code}")
    elif prefix == "6":
        return ("Contingencies", "Contingencies", f"Function {code}")
    return ("Other", "Other", f"Function {code}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    files = sorted(os.listdir(AFR_DIR))
    all_data = {}
    all_rollups = {}
    all_codes_seen = set()

    for f in files:
        fy = fy_from_filename(f)
        if fy is None:
            continue
        if f == "AFR25_d65.xlsx":
            continue
        if "Budget" in f:
            continue

        fp = os.path.join(AFR_DIR, f)
        records, rollups = parse_afr_all(fp, fy)
        print(f"{f:80s}  FY{fy}  {len(records):3d} Ed Fund rows")

        year_data = {}
        for rec in records:
            code = rec["func"]
            all_codes_seen.add(code)
            if code in year_data:
                year_data[code]["total"] += rec["total"]
                year_data[code]["salaries"] += rec["salaries"]
                year_data[code]["benefits"] += rec["benefits"]
            else:
                year_data[code] = {
                    "total": rec["total"],
                    "salaries": rec["salaries"],
                    "benefits": rec["benefits"],
                }
        all_data[fy] = year_data
        all_rollups[fy] = rollups

    years = sorted(all_data.keys())
    print(f"\nYears: {years}")
    print(f"Unique function codes seen: {sorted(all_codes_seen)}")

    full_hierarchy = dict(FUNCTION_HIERARCHY)
    for code in all_codes_seen:
        if code not in full_hierarchy and code not in ROLLUP_CODES:
            full_hierarchy[code] = bucket_unknown_code(code)
            print(f"  Unknown code {code} -> bucketed as {full_hierarchy[code]}")

    categories = {}
    for code in sorted(full_hierarchy.keys()):
        group, subgroup, label = full_hierarchy[code]
        values = {}
        for yr in years:
            yd = all_data.get(yr, {})
            if code in yd:
                values[str(yr)] = round(yd[code]["total"], 2)
            else:
                values[str(yr)] = None
        categories[code] = {
            "label": label,
            "group": group,
            "subgroup": subgroup,
            "values": values,
        }

    totals = {}
    for yr in years:
        t = sum(
            yd["total"]
            for code, yd in all_data.get(yr, {}).items()
            if code in full_hierarchy
        )
        totals[str(yr)] = round(t, 2)

    hierarchy = {}
    for code, (group, subgroup, _label) in full_hierarchy.items():
        if group not in hierarchy:
            hierarchy[group] = {}
        if subgroup not in hierarchy[group]:
            hierarchy[group][subgroup] = []
        if code not in hierarchy[group][subgroup]:
            hierarchy[group][subgroup].append(code)

    for group in hierarchy:
        for subgroup in hierarchy[group]:
            hierarchy[group][subgroup].sort()

    # --- Validation ---
    print("\n=== Validation ===")

    admin_csv = os.path.join(ROOT, "data", "afr_admin_pool_summary.csv")
    if os.path.exists(admin_csv):
        admin = pd.read_csv(admin_csv)
        admin_group_prefixes = {"2300": "23", "2400": "24", "2500": "25", "2600": "26"}
        print("\nAdmin pool cross-check (our total col vs admin sal+ben; expect ours >= admin):")
        for _, row in admin.iterrows():
            yr = int(row["year"])
            if yr not in all_data:
                continue
            for func, prefix in admin_group_prefixes.items():
                admin_val = row.get(func, 0)
                our_val = sum(
                    rec["total"] for code, rec in all_data[yr].items()
                    if code.startswith(prefix) and code not in ROLLUP_CODES
                )
                ratio = our_val / admin_val if admin_val > 0 else 0
                flag = "" if 0.8 < ratio < 2.0 else " *** CHECK"
                if flag:
                    print(f"  FY{yr} {func}: ours={our_val:>12,.0f}  admin(sal+ben)={admin_val:>12,.0f}  ratio={ratio:.2f}{flag}")
        print("  (only suspicious ratios shown)")

    print("\nPer-year totals:")
    for yr in years:
        leaf_sum = totals[str(yr)]
        print(f"  FY{yr}: ${leaf_sum:>14,.0f}")

    json_data = {
        "years": [str(y) for y in years],
        "categories": categories,
        "totals": totals,
        "hierarchy": hierarchy,
    }

    html = build_html(json_data)
    out_path = os.path.join(ASSETS_DIR, "budget_explorer.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nWrote {out_path}")


def build_html(json_data):
    data_json = json.dumps(json_data, indent=None)
    return HTML_TEMPLATE.replace("__BUDGET_DATA__", data_json)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>D65 Budget Explorer</title>
<script src="https://cdn.plot.ly/plotly-3.3.0.min.js"></script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #333; background: #fff; padding: 16px; max-width: 1100px; margin: 0 auto;
}
h1 { font-size: 1.5em; font-weight: 700; margin-bottom: 2px; }
.subtitle { font-size: 0.95em; color: #666; margin-bottom: 14px; }

.controls { margin-bottom: 12px; }
.controls-row { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-bottom: 8px; }
.controls-label { font-size: 0.82em; font-weight: 600; color: #555; margin-right: 4px; white-space: nowrap; }

.preset-btn {
  display: inline-block; padding: 5px 12px; font-size: 0.82em; font-weight: 500;
  border: 1px solid #ccc; border-radius: 4px; background: #f8f8f8; color: #333;
  cursor: pointer; transition: all 0.15s; white-space: nowrap;
}
.preset-btn:hover { background: #e8e8f8; border-color: #99a; }
.preset-btn.active { background: #5e5eb5; color: #fff; border-color: #5e5eb5; }

.toggle-group { display: inline-flex; border: 1px solid #ccc; border-radius: 4px; overflow: hidden; }
.toggle-btn {
  padding: 4px 12px; font-size: 0.82em; font-weight: 500; border: none;
  background: #f8f8f8; color: #555; cursor: pointer; transition: all 0.15s;
  border-right: 1px solid #ccc;
}
.toggle-btn:last-child { border-right: none; }
.toggle-btn:hover { background: #e8e8f8; }
.toggle-btn.active { background: #5e5eb5; color: #fff; }

#chart { width: 100%; height: 500px; margin-bottom: 16px; }

.tree-header {
  font-size: 0.95em; font-weight: 600; margin-bottom: 8px; color: #333;
  display: flex; align-items: center; gap: 12px;
}
.tree-actions { display: flex; gap: 6px; }
.tree-action-btn {
  font-size: 0.78em; padding: 2px 8px; border: 1px solid #ccc; border-radius: 3px;
  background: #f8f8f8; color: #555; cursor: pointer;
}
.tree-action-btn:hover { background: #e8e8f8; }

.tree-container {
  border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px 14px;
  max-height: 420px; overflow-y: auto; background: #fafafa;
}

.tree-group { margin-bottom: 2px; }
.tree-group-header {
  display: flex; align-items: center; gap: 4px; padding: 3px 0; cursor: pointer;
  font-weight: 600; font-size: 0.88em;
}
.tree-toggle {
  width: 16px; text-align: center; font-size: 0.7em; color: #888;
  cursor: pointer; user-select: none; flex-shrink: 0;
}
.tree-subgroup { margin-left: 20px; margin-bottom: 1px; }
.tree-subgroup-header {
  display: flex; align-items: center; gap: 4px; padding: 2px 0; cursor: pointer;
  font-weight: 500; font-size: 0.85em; color: #444;
}
.tree-leaf {
  display: flex; align-items: center; gap: 4px; padding: 1px 0 1px 20px;
  font-size: 0.83em; color: #555;
}
.tree-leaf .code { color: #999; font-size: 0.9em; }
.tree-children { overflow: hidden; }
.tree-children.collapsed { display: none; }

input[type="checkbox"] { cursor: pointer; accent-color: #5e5eb5; flex-shrink: 0; }

.color-swatch {
  display: inline-block; width: 10px; height: 10px; border-radius: 2px;
  flex-shrink: 0; border: 1px solid rgba(0,0,0,0.1);
}

.footer {
  margin-top: 16px; padding-top: 10px; border-top: 1px solid #e0e0e0;
  font-size: 0.78em; color: #888; line-height: 1.5;
}

.grouping-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

@media (max-width: 768px) {
  body { padding: 10px; }
  h1 { font-size: 1.2em; }
  #chart { height: 350px; }
  .tree-container { max-height: 300px; }
}
</style>
</head>
<body>

<h1>D65 Budget Explorer</h1>
<p class="subtitle">Educational Fund Expenditures FY2012–FY2026 (on-behalf/pension payments excluded; FY2026 is adopted budget)</p>

<div class="controls">
  <div class="controls-row">
    <span class="controls-label">Presets:</span>
    <button class="preset-btn active" data-preset="where-money-goes">Where the Money Goes</button>
    <button class="preset-btn" data-preset="instruction">Instruction Breakdown</button>
    <button class="preset-btn" data-preset="classroom-vs-non">Classroom vs Non-Classroom</button>
    <button class="preset-btn" data-preset="admin">All Administration</button>
    <button class="preset-btn" data-preset="special-ed">Special Ed Total</button>
    <button class="preset-btn" data-preset="student-support">Student Support</button>
    <button class="preset-btn" data-preset="community-payments">Community & Payments</button>
  </div>
  <div class="controls-row">
    <div class="grouping-row">
      <span class="controls-label">Chart:</span>
      <div class="toggle-group" id="chart-type-toggle">
        <button class="toggle-btn active" data-type="area">Area</button>
        <button class="toggle-btn" data-type="line">Line</button>
        <button class="toggle-btn" data-type="bar">Bar</button>
      </div>
    </div>
    <div class="grouping-row">
      <span class="controls-label">Y-Axis:</span>
      <div class="toggle-group" id="yaxis-toggle">
        <button class="toggle-btn active" data-yaxis="percent">% of Budget</button>
        <button class="toggle-btn" data-yaxis="dollars">Dollars</button>
      </div>
    </div>
  </div>
</div>

<div id="chart"></div>

<div class="tree-header">
  <span>Category Selection</span>
  <div class="tree-actions">
    <button class="tree-action-btn" id="select-all-btn">Select All</button>
    <button class="tree-action-btn" id="clear-all-btn">Clear All</button>
  </div>
</div>
<div class="tree-container" id="tree"></div>

<div class="footer">
  <strong>Source:</strong> District 65 ISBE Annual Financial Reports (FY2012–FY2025) and Adopted Budget (FY2026).<br>
  Educational Fund only. On-behalf/pension payments excluded.
  Category codes follow the Illinois State Board of Education function code structure.
</div>

<script>
const DATA = __BUDGET_DATA__;

const GROUP_ORDER = [
  "Instruction", "Student Support", "Instructional Staff Support",
  "General Administration", "School Administration", "Business Services",
  "Central Support", "Other Support", "Community Services",
  "Payments to Other Districts", "Debt Service", "Contingencies", "Other"
];

const COLORS = [
  "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
  "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52",
  "#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD",
  "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF",
  "#AEC7E8", "#FFBB78", "#98DF8A", "#FF9896", "#C5B0D5"
];

const GROUP_COLORS = {};
GROUP_ORDER.forEach((g, i) => { GROUP_COLORS[g] = COLORS[i % COLORS.length]; });

const state = {
  chartType: "area",
  yAxis: "percent",
  activePreset: "where-money-goes",
  customTraces: null,
};

function getCodesForGroup(group) {
  const subs = DATA.hierarchy[group] || {};
  const codes = [];
  for (const sg in subs) codes.push(...subs[sg]);
  return codes;
}

function getAllLeafCodes() {
  return Object.keys(DATA.categories);
}

function getCheckedCodes() {
  const codes = [];
  document.querySelectorAll('.leaf-cb:checked').forEach(cb => codes.push(cb.dataset.code));
  return codes;
}

// --- Presets ---

const PRESETS = {
  "where-money-goes": {
    label: "Where the Money Goes",
    mode: "grouped",
    groups: function() {
      const g = {};
      GROUP_ORDER.forEach(grp => {
        const codes = getCodesForGroup(grp);
        if (codes.length > 0) g[grp] = codes;
      });
      return g;
    }
  },
  "instruction": {
    label: "Instruction Breakdown",
    mode: "grouped",
    groups: function() {
      const subs = DATA.hierarchy["Instruction"] || {};
      const g = {};
      for (const sg in subs) g[sg] = subs[sg];
      return g;
    }
  },
  "classroom-vs-non": {
    label: "Classroom vs Non-Classroom",
    mode: "grouped",
    groups: function() {
      const classroomGroups = ["Instruction", "Instructional Staff Support"];
      const classroom = [];
      const nonClassroom = [];
      GROUP_ORDER.forEach(grp => {
        const codes = getCodesForGroup(grp);
        if (classroomGroups.includes(grp)) classroom.push(...codes);
        else nonClassroom.push(...codes);
      });
      return { "Classroom (Instruction + Instructional Staff)": classroom, "Non-Classroom": nonClassroom };
    }
  },
  "admin": {
    label: "All Administration",
    mode: "grouped",
    groups: function() {
      const g = {};
      ["General Administration", "School Administration", "Business Services", "Central Support"].forEach(grp => {
        const subs = DATA.hierarchy[grp] || {};
        for (const sg in subs) g[sg] = subs[sg];
      });
      return g;
    }
  },
  "special-ed": {
    label: "Special Ed Total",
    mode: "individual",
    codes: function() { return ["1200", "1225", "1911", "1922", "4120", "4220", "4320"].filter(c => c in DATA.categories); }
  },
  "student-support": {
    label: "Student Support",
    mode: "individual",
    codes: function() { return getCodesForGroup("Student Support"); }
  },
  "community-payments": {
    label: "Community & Payments",
    mode: "individual",
    codes: function() {
      return [...getCodesForGroup("Community Services"), ...getCodesForGroup("Payments to Other Districts")];
    }
  },
};

function applyPreset(name) {
  state.activePreset = name;
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.toggle('active', b.dataset.preset === name));

  const preset = PRESETS[name];
  const allLeaf = getAllLeafCodes();

  if (preset.mode === "grouped") {
    const groups = preset.groups();
    const codesInPreset = new Set();
    for (const g in groups) groups[g].forEach(c => codesInPreset.add(c));
    allLeaf.forEach(code => {
      const cb = document.querySelector(`.leaf-cb[data-code="${code}"]`);
      if (cb) cb.checked = codesInPreset.has(code);
    });
    updateParentCheckboxes();
    state.customTraces = buildGroupedTraces(groups);
  } else {
    const activeCodes = new Set(preset.codes());
    allLeaf.forEach(code => {
      const cb = document.querySelector(`.leaf-cb[data-code="${code}"]`);
      if (cb) cb.checked = activeCodes.has(code);
    });
    updateParentCheckboxes();
    state.customTraces = null;
  }
  updateChart();
}

// --- Trace building ---

function buildGroupedTraces(groups) {
  const years = DATA.years;
  const traces = [];
  const groupNames = Object.keys(groups);
  groupNames.forEach((name, i) => {
    const codes = groups[name];
    const vals = years.map(yr => {
      let sum = 0;
      let hasData = false;
      codes.forEach(c => {
        const v = (DATA.categories[c] || {values:{}}).values[yr];
        if (v !== null && v !== undefined) { sum += v; hasData = true; }
      });
      return hasData ? sum : null;
    });
    traces.push({ name, values: vals, color: COLORS[i % COLORS.length] });
  });
  return traces;
}

function buildIndividualTraces(codes) {
  const years = DATA.years;
  const traces = [];
  let colorIdx = 0;
  codes.forEach(code => {
    const cat = DATA.categories[code];
    if (!cat) return;
    const vals = years.map(yr => {
      const v = cat.values[yr];
      return (v !== null && v !== undefined) ? v : null;
    });
    const hasAnyData = vals.some(v => v !== null && v > 0);
    if (!hasAnyData) return;
    traces.push({
      name: cat.label + " (" + code + ")",
      values: vals,
      color: GROUP_COLORS[cat.group] || COLORS[colorIdx % COLORS.length],
    });
    colorIdx++;
  });
  return traces;
}

function updateChart() {
  const years = DATA.years;
  const yearLabels = years.map(y => "FY" + y);
  let traces;

  if (state.customTraces) {
    traces = state.customTraces;
  } else {
    const checked = getCheckedCodes();
    traces = buildIndividualTraces(checked);
  }

  if (traces.length === 0) {
    Plotly.react("chart", [], {
      annotations: [{
        text: "Select categories below to display data",
        xref: "paper", yref: "paper", x: 0.5, y: 0.5,
        showarrow: false, font: { size: 16, color: "#999" }
      }],
      xaxis: { visible: false }, yaxis: { visible: false },
      plot_bgcolor: "white", paper_bgcolor: "white", height: 500,
    });
    return;
  }

  const plotTraces = traces.map((t, i) => {
    let yvals;
    if (state.yAxis === "percent") {
      yvals = t.values.map((v, j) => {
        if (v === null) return null;
        const total = DATA.totals[years[j]];
        return total > 0 ? (v / total * 100) : 0;
      });
    } else {
      yvals = t.values;
    }

    const base = {
      x: yearLabels,
      y: yvals,
      name: t.name,
      marker: { color: t.color },
      line: { color: t.color },
    };

    const dollarVals = t.values;
    const pctVals = t.values.map((v, j) => {
      if (v === null) return null;
      const total = DATA.totals[years[j]];
      return total > 0 ? (v / total * 100) : 0;
    });

    base.customdata = years.map((yr, j) => ({
      dollars: dollarVals[j],
      pct: pctVals[j],
      year: yr,
    }));

    if (state.chartType === "area") {
      base.type = "scatter";
      base.mode = "lines";
      base.stackgroup = "one";
      base.hovertemplate = "<b>FY%{customdata.year}</b><br>%{data.name}<br>" +
        "%{customdata.pct:.1f}% ($%{customdata.dollars:,.0f})<extra></extra>";
    } else if (state.chartType === "line") {
      base.type = "scatter";
      base.mode = "lines+markers";
      base.hovertemplate = "<b>FY%{customdata.year}</b><br>%{data.name}<br>" +
        "%{customdata.pct:.1f}% ($%{customdata.dollars:,.0f})<extra></extra>";
    } else {
      base.type = "bar";
      base.hovertemplate = "<b>FY%{customdata.year}</b><br>%{data.name}<br>" +
        "%{customdata.pct:.1f}% ($%{customdata.dollars:,.0f})<extra></extra>";
    }
    return base;
  });

  const layout = {
    plot_bgcolor: "white",
    paper_bgcolor: "white",
    height: 500,
    margin: { l: 70, r: 30, t: 30, b: 80 },
    xaxis: {
      showgrid: true, gridcolor: "#eee",
      tickangle: -45,
    },
    yaxis: {
      showgrid: true, gridcolor: "#eee",
      title: state.yAxis === "percent" ? "% of Total Budget" : "Dollars ($)",
      tickformat: state.yAxis === "percent" ? ".1f" : "$,.0f",
    },
    legend: {
      orientation: "h", y: -0.25, x: 0.5, xanchor: "center",
      font: { size: 11 },
    },
    hovermode: "x unified",
  };

  if (state.chartType === "bar") {
    layout.barmode = "stack";
  }

  Plotly.react("chart", plotTraces, layout, { responsive: true });
}

// --- Checkbox tree ---

function buildTree() {
  const container = document.getElementById("tree");
  container.innerHTML = "";

  GROUP_ORDER.forEach(group => {
    const subs = DATA.hierarchy[group];
    if (!subs) return;

    const allGroupCodes = getCodesForGroup(group);
    if (allGroupCodes.length === 0) return;

    const groupDiv = document.createElement("div");
    groupDiv.className = "tree-group";

    const header = document.createElement("div");
    header.className = "tree-group-header";
    const toggle = document.createElement("span");
    toggle.className = "tree-toggle";
    toggle.textContent = "▼";
    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.className = "group-cb";
    cb.dataset.group = group;
    const label = document.createElement("span");
    label.textContent = group;

    header.appendChild(toggle);
    header.appendChild(cb);
    header.appendChild(label);
    groupDiv.appendChild(header);

    const childrenDiv = document.createElement("div");
    childrenDiv.className = "tree-children";

    const subNames = Object.keys(subs);
    const hasMidLevel = subNames.length > 1 || (subNames.length === 1 && subNames[0] !== group);

    if (hasMidLevel) {
      subNames.forEach(sg => {
        const codes = subs[sg];
        if (codes.length === 1 && !hasMidLevel) {
          appendLeaf(childrenDiv, codes[0]);
        } else if (codes.length === 1 && sg === codes[0]) {
          appendLeaf(childrenDiv, codes[0]);
        } else {
          const subDiv = document.createElement("div");
          subDiv.className = "tree-subgroup";

          if (codes.length === 1) {
            appendLeaf(subDiv, codes[0]);
          } else {
            const subHeader = document.createElement("div");
            subHeader.className = "tree-subgroup-header";
            const subToggle = document.createElement("span");
            subToggle.className = "tree-toggle";
            subToggle.textContent = "▼";
            const subCb = document.createElement("input");
            subCb.type = "checkbox";
            subCb.className = "subgroup-cb";
            subCb.dataset.group = group;
            subCb.dataset.subgroup = sg;
            const subLabel = document.createElement("span");
            subLabel.textContent = sg;

            subHeader.appendChild(subToggle);
            subHeader.appendChild(subCb);
            subHeader.appendChild(subLabel);
            subDiv.appendChild(subHeader);

            const subChildren = document.createElement("div");
            subChildren.className = "tree-children collapsed";
            codes.forEach(code => appendLeaf(subChildren, code));
            subDiv.appendChild(subChildren);

            subToggle.addEventListener("click", () => {
              subChildren.classList.toggle("collapsed");
              subToggle.textContent = subChildren.classList.contains("collapsed") ? "▶" : "▼";
            });
          }
          childrenDiv.appendChild(subDiv);
        }
      });
    } else {
      const sg = subNames[0];
      subs[sg].forEach(code => appendLeaf(childrenDiv, code));
    }

    groupDiv.appendChild(childrenDiv);
    container.appendChild(groupDiv);

    toggle.addEventListener("click", () => {
      childrenDiv.classList.toggle("collapsed");
      toggle.textContent = childrenDiv.classList.contains("collapsed") ? "▶" : "▼";
    });

    cb.addEventListener("change", () => {
      const checked = cb.checked;
      groupDiv.querySelectorAll(".leaf-cb").forEach(lcb => { lcb.checked = checked; });
      groupDiv.querySelectorAll(".subgroup-cb").forEach(scb => { scb.checked = checked; scb.indeterminate = false; });
      onManualChange();
    });
  });

  document.querySelectorAll(".subgroup-cb").forEach(scb => {
    scb.addEventListener("change", () => {
      const group = scb.dataset.group;
      const subgroup = scb.dataset.subgroup;
      const checked = scb.checked;
      const parent = scb.closest(".tree-subgroup");
      parent.querySelectorAll(".leaf-cb").forEach(lcb => { lcb.checked = checked; });
      updateParentCheckboxes();
      onManualChange();
    });
  });

  document.querySelectorAll(".leaf-cb").forEach(lcb => {
    lcb.addEventListener("change", () => {
      updateParentCheckboxes();
      onManualChange();
    });
  });
}

function appendLeaf(container, code) {
  const cat = DATA.categories[code];
  if (!cat) return;
  const div = document.createElement("div");
  div.className = "tree-leaf";
  const cb = document.createElement("input");
  cb.type = "checkbox";
  cb.className = "leaf-cb";
  cb.dataset.code = code;
  const lbl = document.createElement("span");
  lbl.textContent = cat.label;
  const codeSpan = document.createElement("span");
  codeSpan.className = "code";
  codeSpan.textContent = " (" + code + ")";
  div.appendChild(cb);
  div.appendChild(lbl);
  div.appendChild(codeSpan);
  container.appendChild(div);
}

function updateParentCheckboxes() {
  document.querySelectorAll(".subgroup-cb").forEach(scb => {
    const parent = scb.closest(".tree-subgroup");
    const leaves = parent.querySelectorAll(".leaf-cb");
    const checked = parent.querySelectorAll(".leaf-cb:checked");
    scb.checked = checked.length === leaves.length && leaves.length > 0;
    scb.indeterminate = checked.length > 0 && checked.length < leaves.length;
  });

  document.querySelectorAll(".group-cb").forEach(gcb => {
    const group = gcb.closest(".tree-group");
    const leaves = group.querySelectorAll(".leaf-cb");
    const checked = group.querySelectorAll(".leaf-cb:checked");
    gcb.checked = checked.length === leaves.length && leaves.length > 0;
    gcb.indeterminate = checked.length > 0 && checked.length < leaves.length;
  });
}

let debounceTimer = null;
function onManualChange() {
  state.activePreset = null;
  state.customTraces = null;
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
  if (debounceTimer) clearTimeout(debounceTimer);
  debounceTimer = setTimeout(updateChart, 100);
}

// --- Toggle handlers ---

document.querySelectorAll('#chart-type-toggle .toggle-btn').forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll('#chart-type-toggle .toggle-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.chartType = btn.dataset.type;
    updateChart();
  });
});

document.querySelectorAll('#yaxis-toggle .toggle-btn').forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll('#yaxis-toggle .toggle-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    state.yAxis = btn.dataset.yaxis;
    updateChart();
  });
});

document.querySelectorAll('.preset-btn').forEach(btn => {
  btn.addEventListener("click", () => applyPreset(btn.dataset.preset));
});

document.getElementById("select-all-btn").addEventListener("click", () => {
  document.querySelectorAll(".leaf-cb").forEach(cb => { cb.checked = true; });
  updateParentCheckboxes();
  onManualChange();
});

document.getElementById("clear-all-btn").addEventListener("click", () => {
  document.querySelectorAll(".leaf-cb").forEach(cb => { cb.checked = false; });
  updateParentCheckboxes();
  onManualChange();
});

// --- Init ---
buildTree();
applyPreset("where-money-goes");
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
