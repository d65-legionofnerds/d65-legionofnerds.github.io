"""
Builds a unified long-format CSV of D65 administrator compensation data
spanning SY2015-16 through SY2025-26, reconciling:
  - Excel workbook 'D65 Comp.xlsx' (provides SY15-16 and SY21-22..SY25-26)
  - 10 markdown files in data/d65_admin_comp_pdfs/ (provide SY16-17..SY20-21,
    extracted from foiagras PDFs of D65 board meeting compensation reports)

Output: data/d65_admin_comp_combined.csv
Columns: year, school_year, role_class, last_name, first_name, position,
         base_salary, total_salary, total_comp, source
"""
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent
DATA = ROOT / "data"
PDF_DIR = DATA / "d65_admin_comp_pdfs"
EXCEL_PATH = Path(r"C:\Users\jkarlin\Downloads\Copy of D65 Comp.xlsx")
OUT_PATH = DATA / "d65_admin_comp_combined.csv"


def money(x):
    """Parse a money cell to float. Returns NaN if unparseable / blank / '#######'."""
    if x is None:
        return float("nan")
    s = str(x).strip()
    if s in ("", "-", "$ -", "$-", "$", "#######", "nan", "NaN"):
        return float("nan")
    s = s.replace("$", "").replace(",", "").replace(" ", "")
    if s in ("", "-"):
        return float("nan")
    try:
        return float(s)
    except ValueError:
        return float("nan")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip and replace newlines in column names so lookups don't depend on PDF/Excel formatting."""
    df.columns = [
        " ".join(str(c).split()) if c is not None else c
        for c in df.columns
    ]
    return df


# Keyword patterns for benefit-like columns. Any column whose name contains one
# of these as a whole word (case-insensitive) is summed into the benefits total.
# Designed to survive Excel schema drift across SY15 -> SY26 — handles both
# "Health Insurance" (older sheets) and "Health" (SY25 uses bare single-word
# column names with the implicit "Insurance" suffix).
BENEFIT_KEYWORDS = [
    r"health",            # matches "Health", "Health Insurance", "Total Health"
    r"dental",
    r"vision",
    r"life insurance",
    r"annual district insurance",   # SY19-20 PDF quirk: their bare "Insurance" column = Health
    r"car allowance",
    r"\bcar\b",           # matches "Car" but not "Career"; combined with above
    r"annuity",
    r"annuities",
    r"vacation payout",
    r"sick / vacation",
    r"sick/vacation",
    r"other benefits",
    r"bonus",
]
_BENEFIT_RE = re.compile("|".join(BENEFIT_KEYWORDS), re.IGNORECASE)

# Columns that look like a benefit but should NOT be counted (they would
# double-count or are non-monetary).
BENEFIT_EXCLUDE_RE = re.compile(
    r"^\s*(sick days?|vacation days?|sick|vacation|change|fte|contract days?|"
    r"years of experience.*|degree.*|2022 salary|search.?key)\s*$",
    re.IGNORECASE,
)


def sum_benefits(rec: dict) -> float:
    """Sum every column whose name matches a benefit keyword. Returns 0.0 if none match."""
    total = 0.0
    seen = set()
    for col, val in rec.items():
        if col is None:
            continue
        col_norm = " ".join(str(col).split())
        col_lower = col_norm.lower()
        if col_lower in seen:
            continue
        seen.add(col_lower)
        if BENEFIT_EXCLUDE_RE.match(col_lower):
            continue
        if _BENEFIT_RE.search(col_lower):
            v = money(val)
            if not pd.isna(v):
                total += v
    return total


def classify_role(position: str, source_file: str) -> str:
    """Map (position string, source file) -> role_class.
    role_class is one of: 'TRS Admin', 'Principal', 'IMRF Support Staff'
    """
    if "imrf" in source_file.lower():
        return "IMRF Support Staff"
    pos = (position or "").upper()
    # Principal-tier roles (from PA 96-0434 admin reports + Excel principals sheets)
    principal_keywords = ("PRINCIPAL", "ASST PRINCIPAL", "ASSISTANT PRINCIPAL",
                          "INTERIM PRINCIPAL", "INTERIM ASSISTANT PRINCIPAL",
                          "INTERIM ASST PRINCIPAL", "10-MONTH ASST PRINCIPAL",
                          "10-MONTH PRINCIPAL", "12-MONTH PRINCIPAL",
                          "PRINCIPAL SPECIAL EDUCATION", "ASST PRINCIPAL OF SPECIAL SERVICES")
    # but exclude things like "ASST DIRECTOR" which doesn't contain PRINCIPAL
    if any(k in pos for k in principal_keywords):
        return "Principal"
    return "TRS Admin"


# -----------------------------------------------------------------------------
# PDF (markdown) parsers — one per source schema family
# -----------------------------------------------------------------------------

def parse_md_table(text: str) -> list[list[str]]:
    """Extract table rows from a markdown table block. Returns list of cell-lists."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            # also accept rows that don't lead with | (some PDFs strip them)
            if "|" in line and not line.startswith("#") and not line.startswith("PA"):
                # heuristic: data rows have many | separators
                if line.count("|") >= 5:
                    cells = [c.strip() for c in line.split("|")]
                    rows.append(cells)
            continue
        # Skip header separator rows like |---|---|...
        if re.match(r"^\|\s*[-:|\s]+\|?$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def parse_admin_pdf(filepath: Path, year: int):
    """Parser for the *_admin.md files (PA 96-0434 reports). Schema varies slightly
    across years but all have: Position, Last Name, First Name, ..., Base Salary,
    TRS, ..., Total Salary, ..., insurance/benefits cells."""
    text = filepath.read_text(encoding="utf-8")
    rows = parse_md_table(text)
    if not rows:
        return []
    headers = [" ".join(h.strip().split()) for h in rows[0]]
    out = []
    for r in rows[1:]:
        if len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        rec = dict(zip(headers, r))
        position = rec.get("Position", "").strip()
        last = rec.get("Last Name", "").strip()
        first = rec.get("First Name", "").strip()
        if not last:
            continue
        base = money(rec.get("Full Year Base Salary") or rec.get("Base Salary"))
        total_salary = money(rec.get("Total Salary"))
        benefit_sum = sum_benefits(rec)
        total_comp = total_salary + benefit_sum if not pd.isna(total_salary) else float("nan")
        out.append({
            "year": year,
            "school_year": f"SY{year-1}-{str(year)[-2:]}",
            "role_class": classify_role(position, filepath.name),
            "last_name": last,
            "first_name": first,
            "position": position,
            "base_salary": base,
            "total_salary": total_salary,
            "total_comp": total_comp,
            "source": filepath.name,
        })
    return out


def parse_imrf_pdf(filepath: Path, year: int):
    """Parser for *_imrf.md files (PA 097-0609 reports). Schema:
    Last Name, First Name, Contract/Salary, Health, Dental, Car Allowance, Total Comp, Sick, Vacation"""
    text = filepath.read_text(encoding="utf-8")
    rows = parse_md_table(text)
    if not rows:
        return []
    headers = [h.strip() for h in rows[0]]
    out = []
    for r in rows[1:]:
        if len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        rec = dict(zip(headers, r))
        last = rec.get("Last Name", "").strip()
        first = rec.get("First Name", "").strip()
        if not last:
            continue
        # IMRF salary column is variously named
        salary = money(rec.get("Contract Salary") or rec.get("Full Year Salary") or
                       rec.get("Salary") or rec.get("Total Salary"))
        total_comp = money(rec.get("Total Compensation") or rec.get("Total Comp"))
        out.append({
            "year": year,
            "school_year": f"SY{year-1}-{str(year)[-2:]}",
            "role_class": "IMRF Support Staff",
            "last_name": last,
            "first_name": first,
            "position": "",  # IMRF reports often omit titles in old years
            "base_salary": salary,
            "total_salary": salary,  # IMRF "Contract Salary" already excludes benefits
            "total_comp": total_comp,
            "source": filepath.name,
        })
    return out


# -----------------------------------------------------------------------------
# Excel parsers — one per sheet schema family
# -----------------------------------------------------------------------------

def parse_excel_sy15_admin(df: pd.DataFrame, year: int):
    """SY15-16 admin sheet schema."""
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        position = str(rec.get("Position", "") or "").strip()
        last = str(rec.get("Last Name", "") or "").strip()
        if not last or last.lower() == "nan":
            continue
        first = str(rec.get("First Name", "") or "").strip()
        base = money(rec.get("Base Salary"))
        total_salary = money(rec.get("Total Salary"))
        benefits = sum_benefits(rec)
        total_comp = total_salary + benefits if not pd.isna(total_salary) else float("nan")
        out.append({
            "year": year, "school_year": "SY2015-16",
            "role_class": classify_role(position, "admin"),
            "last_name": last, "first_name": first, "position": position,
            "base_salary": base, "total_salary": total_salary, "total_comp": total_comp,
            "source": "Excel SY2015-16-Admin",
        })
    return out


def parse_excel_sy15_imrf(df: pd.DataFrame, year: int):
    """SY15-16 IMRF sheet schema."""
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        last = str(rec.get("Last Name", "") or "").strip()
        if not last or last.lower() == "nan":
            continue
        first = str(rec.get("First Name", "") or "").strip()
        salary = money(rec.get("Salary"))
        total_comp = money(rec.get("Total Compensation"))
        out.append({
            "year": year, "school_year": "SY2015-16",
            "role_class": "IMRF Support Staff",
            "last_name": last, "first_name": first, "position": "",
            "base_salary": salary, "total_salary": salary, "total_comp": total_comp,
            "source": "Excel SY2015-16 IMRF",
        })
    return out


def parse_excel_sy16_principals(df: pd.DataFrame, year: int):
    """SY2016-Princpals sheet (this is actually SY15-16 principals)."""
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        position = str(rec.get("Position", "") or "").strip()
        last = str(rec.get("Last Name", "") or "").strip()
        if not last or last.lower() == "nan":
            continue
        first = str(rec.get("First Name", "") or "").strip()
        base = money(rec.get("Base Salary"))
        total_salary = money(rec.get("Total Salary"))
        benefits = sum_benefits(rec)
        total_comp = total_salary + benefits if not pd.isna(total_salary) else float("nan")
        out.append({
            "year": year, "school_year": "SY2015-16",
            "role_class": "Principal",
            "last_name": last, "first_name": first, "position": position,
            "base_salary": base, "total_salary": total_salary, "total_comp": total_comp,
            "source": "Excel SY2016-Princpals",
        })
    return out


def _split_name(rec: dict) -> tuple[str, str]:
    """Return (last, first) from rec, handling both two-column and combined-Name layouts."""
    last = str(rec.get("Last Name", "") or "").strip()
    if last and last.lower() != "nan":
        first = str(rec.get("First Name", "") or "").strip()
        return last, first
    # SY25 uses "Name" field with combined "Last, First" format
    name = str(rec.get("Name", "") or "").strip()
    if not name or name.lower() == "nan":
        return "", ""
    parts = [p.strip() for p in name.split(",")]
    return (parts[0] if parts else "", parts[1] if len(parts) > 1 else "")


def parse_excel_sy22_26_admin(df: pd.DataFrame, year: int, school_year: str, sheet_name: str):
    """SY22, SY23, SY24, SY25, SY26 admin sheets. Schemas drift across years
    (column-name newlines, insurance-column splits) but our matching is now
    keyword-based via sum_benefits()."""
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        position = str(rec.get("Position", "") or rec.get("Title", "") or "").strip()
        last, first = _split_name(rec)
        if not last:
            continue
        base = money(rec.get("Base Salary") or rec.get("Full Year Base Salary"))
        total_salary = money(rec.get("Total Salary"))
        # Derive Total Salary if missing: base + TRS (where TRS column exists)
        if pd.isna(total_salary) and not pd.isna(base):
            trs = money(rec.get("TRS"))
            total_salary = base + (trs if not pd.isna(trs) else 0)
        benefits = sum_benefits(rec)
        total_comp = total_salary + benefits if not pd.isna(total_salary) else float("nan")
        out.append({
            "year": year, "school_year": school_year,
            "role_class": classify_role(position, "admin"),
            "last_name": last, "first_name": first, "position": position,
            "base_salary": base, "total_salary": total_salary, "total_comp": total_comp,
            "source": f"Excel {sheet_name}",
        })
    return out


def parse_excel_sy22_26_imrf(df: pd.DataFrame, year: int, school_year: str, sheet_name: str):
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        last, first = _split_name(rec)
        if not last:
            continue
        position = str(rec.get("Position", "") or rec.get("Title", "") or "").strip()
        salary = money(rec.get("Contract Salary") or rec.get("Full Year Salary") or
                       rec.get("Total Salary"))
        total_comp = money(rec.get("Total Comp") or rec.get("Total Compensation"))
        out.append({
            "year": year, "school_year": school_year,
            "role_class": "IMRF Support Staff",
            "last_name": last, "first_name": first, "position": position,
            "base_salary": salary, "total_salary": salary, "total_comp": total_comp,
            "source": f"Excel {sheet_name}",
        })
    return out


def parse_excel_principals(df: pd.DataFrame, year: int, school_year: str, sheet_name: str):
    """Principal-only sheets (SY22-Principals, SY23-Principals, etc.)"""
    df = normalize_columns(df)
    out = []
    for _, row in df.iterrows():
        rec = row.to_dict()
        last, first = _split_name(rec)
        if not last:
            continue
        position = str(rec.get("Title", "") or rec.get("Position", "") or "PRINCIPAL").strip()
        base = money(rec.get("Base Salary") or rec.get("Full Year Base Salary"))
        total_salary = money(rec.get("Total Salary"))
        if pd.isna(total_salary) and not pd.isna(base):
            trs = money(rec.get("TRS"))
            total_salary = base + (trs if not pd.isna(trs) else 0)
        benefits = sum_benefits(rec)
        total_comp = total_salary + benefits if not pd.isna(total_salary) else float("nan")
        out.append({
            "year": year, "school_year": school_year,
            "role_class": "Principal",
            "last_name": last, "first_name": first, "position": position,
            "base_salary": base, "total_salary": total_salary, "total_comp": total_comp,
            "source": f"Excel {sheet_name}",
        })
    return out


# -----------------------------------------------------------------------------
# Driver
# -----------------------------------------------------------------------------

def main():
    records = []

    # Load the foiagras-PDF-derived markdown files
    sources = json.loads((PDF_DIR / "sources.json").read_text())["documents"]
    for src in sources:
        path = PDF_DIR / src["filename"]
        year = src["year"]
        if src["category"] == "admin_principal":
            records.extend(parse_admin_pdf(path, year))
        elif src["category"] == "imrf":
            records.extend(parse_imrf_pdf(path, year))

    # Load Excel sheets
    xl = pd.ExcelFile(EXCEL_PATH)

    # SY2015-16
    if "SY2015-16-Admin" in xl.sheet_names:
        records.extend(parse_excel_sy15_admin(pd.read_excel(xl, "SY2015-16-Admin"), 2016))
    if "SY2015-16 IMRF" in xl.sheet_names:
        records.extend(parse_excel_sy15_imrf(pd.read_excel(xl, "SY2015-16 IMRF"), 2016))
    if "SY2016-Princpals" in xl.sheet_names:
        records.extend(parse_excel_sy16_principals(pd.read_excel(xl, "SY2016-Princpals"), 2016))

    # SY22 (=2022), SY23 (=2023), SY24 (=2024), SY25 (=2025), SY26 (=2026)
    sy_to_year = {"SY22": 2022, "SY23": 2023, "SY24": 2024, "SY25": 2025, "SY26": 2026}
    for sy, year in sy_to_year.items():
        sy_label = f"SY{year-1}-{str(year)[-2:]}"
        admin_sheet = f"{sy}-Admin"
        if admin_sheet in xl.sheet_names:
            records.extend(parse_excel_sy22_26_admin(
                pd.read_excel(xl, admin_sheet), year, sy_label, admin_sheet))
        principals_sheet = f"{sy}-Principals"
        if principals_sheet in xl.sheet_names:
            records.extend(parse_excel_principals(
                pd.read_excel(xl, principals_sheet), year, sy_label, principals_sheet))
        imrf_sheet = f"{sy}-IMRF"
        if imrf_sheet in xl.sheet_names:
            records.extend(parse_excel_sy22_26_imrf(
                pd.read_excel(xl, imrf_sheet), year, sy_label, imrf_sheet))

    df = pd.DataFrame(records)
    # Quick sanity prints
    print(f"Total records: {len(df)}")
    print(df.groupby(["year", "role_class"]).agg(
        n=("last_name", "count"),
        total_comp_sum=("total_comp", "sum"),
        salary_sum=("total_salary", "sum"),
    ).reset_index().to_string())

    df.to_csv(OUT_PATH, index=False)
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
