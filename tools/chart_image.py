"""Make the picture for an analysis: render a Plotly chart (.html) to a PNG.

The PNG is used when the analysis leads the homepage, and as the preview image when someone
shares the link (Facebook, texts, Slack). Put it in assets/img/lead/ and point the page's
front matter at it:  image: /assets/img/lead/<page-name>.png

Usage (from the repo root):
    python tools/chart_image.py dataanalysis/assets/closure_headline.html assets/img/lead/closure-savings.png

Options:
    --width 800 --height 450     size of the chart in CSS pixels (16:9 suits both uses)
    --scale 3                   pixel density (3 = 2400x1350 output, sharp everywhere)
    --no-title                  drop the chart's own title (kept by default: link previews are
                                seen on their own, so the title helps there)

Needs: pip install playwright pillow && python -m playwright install chromium
No Python? Open the chart in a browser, hover it, and click the camera icon ("Download plot as
a png") in its toolbar. Then save it in assets/img/lead/.
"""
import argparse
import pathlib
import sys

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chart", help="Plotly chart .html file")
    ap.add_argument("out", help="output .png path")
    ap.add_argument("--width", type=int, default=800)
    ap.add_argument("--height", type=int, default=450)
    ap.add_argument("--scale", type=float, default=3)
    ap.add_argument("--no-title", action="store_true")
    a = ap.parse_args()

    chart = pathlib.Path(a.chart).resolve()
    if not chart.exists():
        sys.exit(f"Chart not found: {chart}")
    out = pathlib.Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": a.width + 40, "height": a.height + 40},
                                device_scale_factor=a.scale)
        page.goto(chart.as_uri(), wait_until="networkidle")
        page.wait_for_selector(".js-plotly-plot .main-svg", timeout=30000)
        n = page.evaluate("document.querySelectorAll('.js-plotly-plot').length")
        if n != 1:
            print(f"Note: {n} charts in this file; using the first.", file=sys.stderr)
        page.evaluate(
            """([w, h, noTitle]) => {
                const gd = document.querySelector('.js-plotly-plot');
                document.body.style.margin = '0';
                document.body.style.background = '#fff';
                gd.style.width = w + 'px';
                gd.style.height = h + 'px';
                const upd = {width: w, height: h, autosize: false, paper_bgcolor: '#fff'};
                // Titles and legends placed relative to the whole figure ("container") keep their
                // distance from the top in pixels, so a resized chart doesn't overlap them.
                const H0 = gd._fullLayout.height;
                const keep = (key, o) => {
                    if (o && o.yref === 'container' && typeof o.y === 'number') upd[key + '.y'] = 1 - (1 - o.y) * H0 / h;
                };
                keep('title', gd.layout.title);
                keep('legend', gd.layout.legend);
                if (noTitle) { upd['title.text'] = ''; upd['margin.t'] = Math.min((gd.layout.margin || {}).t || 60, 40); }
                return Plotly.relayout(gd, upd);
            }""",
            [a.width, a.height, a.no_title],
        )
        page.add_style_tag(content=".modebar-container{display:none!important}")
        page.wait_for_timeout(500)
        page.locator(".js-plotly-plot").first.screenshot(path=str(out))
        browser.close()

    try:
        from PIL import Image
        im = Image.open(out)
        im.save(out, optimize=True)
        print(f"Wrote {out} ({im.size[0]}x{im.size[1]}, {out.stat().st_size // 1024} KB)")
    except ImportError:
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
