"""
Assembles the FY25 baseline (Jul 2024 - Jun 2025) from the three hand-extracted
Treasurer-report CSVs and writes data/fy25_source_lines.csv in the same shape as
the FY26/FY27 source_lines.csv.

    python assemble_fy25.py part_A.csv part_B.csv part_C.csv

Source: District 65 monthly Treasurer reports obtained through FOIAgras
(Expenditure Summary section, district-wide, funds 10 / 20 / 80).

Known gaps handled here:
  * May 2025 has no line-item report. The June 2025 report gives the June month AND the
    full-year YTD, so May = June YTD - April YTD - June month.
  * Mar 2025 was derived upstream from YTD differences (no standalone report).
  * Where a report's own month column disagreed with the YTD change, the upstream
    extractor used the YTD change; it is flagged in `note`.

Integrity check: for every line, the 12 months must sum to the June full-year YTD.
"""
import sys
from pathlib import Path
import pandas as pd

OUT = Path(__file__).parent / "data"

parts = [pd.read_csv(p) for p in sys.argv[1:4]]
df = pd.concat(parts, ignore_index=True)
df["fund"] = df["fund"].astype(str)
df["obj"] = df["obj"].astype(str)

key = ["category", "fund", "obj", "line_name"]
apr = df[df.fiscal_month == 10].set_index(key)
jun = df[df.fiscal_month == 12].set_index(key)

may = df[df.fiscal_month == 11].copy().set_index(key)
may["month_expended"] = jun["ytd_expended"] - apr["ytd_expended"] - jun["month_expended"]
may["ytd_expended"] = apr["ytd_expended"] + may["month_expended"]
may["budget"] = jun["budget"]
may["source_doc_id"] = jun["source_doc_id"]
may["note"] = "DERIVED: May = Jun full-year YTD - Apr YTD - Jun month (no May line-item report)"
df = pd.concat([df[df.fiscal_month != 11], may.reset_index()], ignore_index=True)
df = df.sort_values(key + ["fiscal_month"]).reset_index(drop=True)

# integrity: months sum to the full-year YTD printed in the June report
chk = df.groupby(key).agg(total=("month_expended", "sum"))
chk["full_year"] = jun["ytd_expended"]
chk["diff"] = (chk["total"] - chk["full_year"]).round(2)
bad = chk[chk["diff"].abs() > 1.0]
print(f"{len(df)} rows, {len(chk)} lines; lines whose months do not sum to the FY total: {len(bad)}")
if len(bad):
    print(bad.to_string())

df.to_csv(OUT / "fy25_source_lines.csv", index=False)
