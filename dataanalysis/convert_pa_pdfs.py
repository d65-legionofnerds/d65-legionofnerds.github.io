"""
Converts District 65's Public Act compensation-report PDFs into the markdown
tables in data/d65_admin_comp_pdfs/, which build_admin_growth_data.py reads.

Handles the three report layouts the District publishes each fall:
  - PA 96-0434  Administrator salary/compensation report (administrators + principals)
  - PA 97-0256  Administrator and teacher salary/benefits report
  - PA 97-0609  IMRF employees with total compensation of $75,000+

The PDFs are tables printed from Excel. Each word is placed by position:
a row starts at a Last Name in the left-hand column (wrapped position titles
sit a point or so lower, so every word joins the row with the nearest
Last Name), and a column is the header whose left edge the word falls under.
Every row is then checked against the report's own totals (base + retirement
= total salary; salary + benefits = total comp for IMRF), and any row that
fails is printed.

Usage:
    python convert_pa_pdfs.py                # converts every report in REPORTS
    python convert_pa_pdfs.py --check-only   # parse + check, write nothing

Requires PyMuPDF (pip install pymupdf).
"""
import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF

ROOT = Path(__file__).parent
ASSETS = ROOT.parent / "assets"
OUT_DIR = ROOT / "data" / "d65_admin_comp_pdfs"

# Column specs: (output column name, header word, which occurrence of that
# word in the header band, counting left to right).
SPECS = {
    "96-0434": [
        ("Last Name", "Last", 0), ("First Name", "First", 0), ("Position", "Position", 0),
        ("Base Salary", "Base", 0), ("TRS", "TRS", 0), ("Total Salary", "Total", 0),
        ("Dental Insurance", "Dental", 0), ("Health Insurance", "Health", 0),
        ("Vision Insurance", "Vision", 0), ("Life Insurance", "Life", 0),
        ("Bonus", "Bonus", 0), ("Retirement Annuities", "Retire-", 0),
        ("Car Allowance", "Car", 0), ("Sick & Vacation Payout", "Sick", 0),
    ],
    "97-0256": [
        ("Last Name", "Last", 0), ("First Name", "First", 0), ("Position", "Position", 0),
        ("Base Salary", "Base", 0), ("Retirement", "Retirement", 0), ("Total Salary", "Total", 0),
        ("Dental Insurance", "Dental", 0), ("Health Insurance", "Health", 0),
        ("Vision Insurance", "Vision", 0), ("Life Insurance", "Life", 0),
        ("Bonus", "Bonus", 0), ("Retirement Annuities", "Retirement", 1),
        ("Sick Days", "Sick", 0), ("Vacation Days", "Vacation", 0),
    ],
    "97-0609": [
        ("Last Name", "Last", 0), ("First Name", "First", 0), ("Position", "Position", 0),
        ("Total Salary", "Total", 0), ("Dental Insurance", "Dental", 0),
        ("Health Insurance", "Health", 0), ("Vision Insurance", "Vision", 0),
        ("Life Insurance", "Life", 0), ("Car Allowance", "Car", 0),
        ("Total Comp", "Total", 1), ("Sick Days", "Sick", 0), ("Vacation Days", "Vac-", 0),
    ],
}
TEXT_COLS = {"Last Name", "First Name", "Position"}
DAY_COLS = {"Sick Days", "Vacation Days"}

# (report type, source PDF in /assets, output markdown, title line)
REPORTS = [
    ("96-0434", "TRS Administrator FY27.pdf", "sy26_27_admin.md",
     "Public Act 96-0434 Administrator Salary Compensation Report FY 2026-27"),
    ("97-0609", "IMRF 75000+ FY27.pdf", "sy26_27_imrf.md",
     "Public Act 97-0609 IMRF $75,000+ FY 2026-27"),
    ("97-0256", "Administrator and Teacher FY27.pdf", "sy26_27_admin_teacher.md",
     "Public Act 97-0256 Administrator and Teacher Salary and Benefits Report FY 2026-27"),
]

HEADER_TOP = 45          # column headers start below the report title
ROW_SNAP = 8             # max vertical distance (pt) from a word to its row's Last Name


def to_number(tokens):
    """Join a money cell's tokens ('$', '1,234.56' / '-' / '(1.00)') into a float (0 for '-')."""
    s = "".join(t for t in tokens if t != "$").replace(",", "")
    if s in ("", "-"):
        return 0.0
    neg = s.startswith("(") and s.endswith(")")
    v = float(s.strip("()"))
    return -v if neg else v


def header_bottom(words):
    """y of the header's last line (the line holding 'Last Name')."""
    return max(w[1] for w in words if w[4] == "Last" and w[1] >= HEADER_TOP)


def column_edges(words, spec):
    """Left x of each spec column, read from the header band of one page."""
    band = sorted((w for w in words if HEADER_TOP <= w[1] <= header_bottom(words)), key=lambda w: w[0])
    edges = []
    for name, word, nth in spec:
        hits = [w for w in band if w[4] == word]
        if len(hits) <= nth:
            raise ValueError(f"header word {word!r} (#{nth}) not found")
        edges.append((hits[nth][0], name))
    edges.sort()
    return edges


def parse_report(pdf_path, kind):
    spec = SPECS[kind]
    records = []
    for page in fitz.open(pdf_path):
        words = page.get_text("words")
        edges = column_edges(words, spec)
        first_x = dict((n, x) for x, n in edges)["First Name"]
        body = [w for w in words if w[1] > header_bottom(words) + 4]
        # Row anchors: words in the Last Name column, grouped by line
        anchors = []
        for w in sorted((w for w in body if w[0] < first_x - 2), key=lambda w: w[1]):
            if anchors and abs(w[1] - anchors[-1]) < 2:
                continue
            anchors.append(w[1])
        rows = [[] for _ in anchors]
        for w in body:
            if not anchors:
                break
            i = min(range(len(anchors)), key=lambda k: abs(anchors[k] - w[1]))
            if abs(anchors[i] - w[1]) <= ROW_SNAP:
                rows[i].append(w)
        edge_x = dict((n, x) for x, n in edges)
        money_cols = [n for n, _, _ in spec if n not in TEXT_COLS | DAY_COLS]
        day_cols = [n for n, _, _ in spec if n in DAY_COLS]
        for r in rows:
            r.sort(key=lambda w: (w[0], w[1]))
            rec = {n: [] for n, _, _ in spec}
            money_groups = []
            for w in r:
                x, t = w[0], w[4]
                if day_cols and x + 5 >= edge_x[day_cols[0]]:
                    # sick / vacation day counts: plain numbers, no '$'
                    rec[day_cols[0] if x + 5 < edge_x[day_cols[-1]] else day_cols[-1]].append(t)
                elif t == "$":
                    # Money is right-aligned under left-aligned headers, so cells are
                    # identified by their leading '$', in order, not by x position.
                    money_groups.append([])
                elif money_groups:
                    money_groups[-1].append(t)
                else:
                    col = None
                    for ex, name in edges:     # rightmost text header edge left of the word
                        if name in TEXT_COLS and x + 5 >= ex:
                            col = name
                    rec[col or "Last Name"].append(t)
            if len(money_groups) != len(money_cols):
                raise ValueError(f"{pdf_path.name}: {len(money_groups)} money cells, expected "
                                 f"{len(money_cols)} in row {' '.join(w[4] for w in r)[:80]}")
            out = {}
            for name, _, _ in spec:
                if name in TEXT_COLS:
                    out[name] = " ".join(rec[name])
                elif name in DAY_COLS:
                    out[name] = " ".join(rec[name])
            for name, toks in zip(money_cols, money_groups):
                out[name] = to_number(toks)
            records.append(out)
    return records


def check(records, kind):
    """Return rows whose own totals don't add up."""
    bad = []
    for r in records:
        if kind == "96-0434":
            diff = r["Base Salary"] + r["TRS"] - r["Total Salary"]
        elif kind == "97-0256":
            diff = r["Base Salary"] + r["Retirement"] - r["Total Salary"]
        else:
            diff = (r["Total Salary"] + r["Dental Insurance"] + r["Health Insurance"]
                    + r["Vision Insurance"] + r["Life Insurance"] + r["Car Allowance"]
                    - r["Total Comp"])
        if abs(diff) > 0.05 or not r["Last Name"] or not r["Position"]:
            bad.append((r["Last Name"], r["First Name"], r["Position"], round(diff, 2)))
    return bad


def fmt(v):
    if v == 0:
        return "$ -"
    return f"$ {v:,.2f}" if v > 0 else f"$ -{-v:,.2f}"


def to_markdown(records, kind, title):
    cols = [name for name, _, _ in SPECS[kind]]
    lines = [title, "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in records:
        cells = [r[c] if (c in TEXT_COLS or c in DAY_COLS) else fmt(r[c]) for c in cols]
        lines.append("| " + " | ".join(str(c) for c in cells) + " |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    failed = False
    for kind, pdf, out, title in REPORTS:
        recs = parse_report(ASSETS / pdf, kind)
        bad = check(recs, kind)
        print(f"{pdf}: {len(recs)} rows, {len(bad)} failing checks")
        for b in bad:
            print("   ", b)
        failed |= bool(bad)
        if not args.check_only:
            (OUT_DIR / out).write_text(to_markdown(recs, kind, title), encoding="utf-8")
            print(f"    wrote {OUT_DIR / out}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
