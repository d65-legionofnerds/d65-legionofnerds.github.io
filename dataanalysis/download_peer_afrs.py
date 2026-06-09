"""
Download Annual Financial Report (AFR) Excel files for D65's comparable
peer districts from districtvitals.com.

Each district has a districtvitals subdomain (resolved from the site sitemap).
All AFR files live under /downloads/AFR/{RCDTS}_{Name}/ on a shared file server,
so any subdomain can serve any district's files; we scrape each district's own
/data page to discover the exact (year -> file) links, then download into
data/afr/peers/{slug}/.

The canonical peer list comes from calculations.ipynb (target_districts) — the
same comparables used in the enrollment analysis (enrollment-data.md).

Run:
  python download_peer_afrs.py
"""

import os
import re
import time
import html as htmllib
from urllib.parse import unquote

import requests

ROOT = os.path.dirname(os.path.abspath(__file__))
PEER_DIR = os.path.join(ROOT, "data", "afr", "peers")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/120.0 Safari/537.36"}

# District display name -> (districtvitals subdomain, folder slug).
# Subdomains verified against https://districtvitals.com/sitemap.xml.
# D65 itself is excluded here (already present in data/afr/).
PEERS = {
    "East Maine SD 63":          "eastmained63",
    "Winnetka SD 36":            "winnetkad36",
    "Northbrook SD 28":          "sd28",
    "Glencoe SD 35":             "sd35",
    "CCSD 62":                   "ccsd62",
    "Park Ridge CCSD 64":        "ccsd64",
    "Lincolnwood SD 74":         "lincolnwoodd74",
    "Arlington Heights SD 25":   "arlingtonheightsd25",
    "Skokie SD 68":              "skokied68",
    "Skokie SD 69":              "skokied69",
    "Skokie SD 73-5":            "sd735",
    "Oak Park ESD 97":           "esd97",
    "Northbrook/Glenview SD 30": "northbrookglenviewd30",
    "Glenview CCSD 34":          "glenviewd34",
    "Wilmette SD 39":            "sd39",
    "Wheeling CCSD 21":          "ccsd21",
    "Palatine CCSD 15":          "palatined15",
    "North Shore SD 112":        "sd112",
}

AFR_HREF_RE = re.compile(
    r'href="(/downloads/AFR/[^"]+\.(?:xls|xlsx|xlsm|XLS|XLSX|XLSM|XLSx))"'
)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def slugify(subdomain):
    return subdomain


def fetch_data_page(subdomain):
    url = f"https://{subdomain}.districtvitals.com/data"
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text


def main():
    os.makedirs(PEER_DIR, exist_ok=True)
    manifest = []

    for name, sub in PEERS.items():
        slug = slugify(sub)
        ddir = os.path.join(PEER_DIR, slug)
        os.makedirs(ddir, exist_ok=True)

        try:
            page = fetch_data_page(sub)
        except Exception as e:
            print(f"!! {name} ({sub}): failed to load /data: {e}")
            continue

        title = TITLE_RE.search(page)
        title = htmllib.unescape(title.group(1).strip()) if title else "?"

        hrefs = []
        seen = set()
        for m in AFR_HREF_RE.finditer(page):
            h = m.group(1)
            if h not in seen:
                seen.add(h)
                hrefs.append(h)

        print(f"\n== {name}  [{sub}]  page-title={title!r}  {len(hrefs)} AFR files")

        for h in hrefs:
            fname = unquote(h.split("/")[-1])
            dest = os.path.join(ddir, fname)
            if os.path.exists(dest) and os.path.getsize(dest) > 0:
                continue
            url = f"https://{sub}.districtvitals.com{h}"
            try:
                rr = requests.get(url, headers=HEADERS, timeout=60)
                rr.raise_for_status()
                with open(dest, "wb") as fh:
                    fh.write(rr.content)
                print(f"   + {fname}  ({len(rr.content):,} bytes)")
                time.sleep(0.3)
            except Exception as e:
                print(f"   !! {fname}: {e}")

        manifest.append((name, sub, title, len(hrefs)))

    print("\n=== SUMMARY ===")
    for name, sub, title, n in manifest:
        print(f"  {name:30s} {sub:24s} {n:2d} files   title={title!r}")


if __name__ == "__main__":
    main()
