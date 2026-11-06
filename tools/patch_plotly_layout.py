"""Change the layout of a saved Plotly chart (.html) without touching its data.

Use this for charts that have no build script (notebook-made or hand-made), when a chart needs a
layout fix (legend position, margins, title, height) and re-running the code isn't possible or
would change the numbers. Charts that come from a build_*.py script should be fixed in the script
(the script can use write_html() below to get the same phone layout support).

How it works: the chart file contains one call
    Plotly.newPlot("<div id>", [traces...], {layout...}, {config...})
The script finds that call, parses the layout object as JSON, applies your changes, and writes
back ONLY the layout object (and, if you change layout.height, the height in the chart div's
style attribute). The traces (all x / y / z / values / text arrays) are left byte-for-byte as they
were, and the script checks that before saving.

Phone layout ("narrow"): a few charts have no single layout that works both at full width
(~1,016 px) and on a phone (~350 px). For those, --narrow stores a second set of layout values in
the chart's layout.meta ({"narrow": {...}, "wide": {...}, "below": 560}) and adds a tiny script
(NARROW_JS, identical in every chart that has it). When the chart is narrower than `below` px the
script redraws it with the `narrow` values; when it is wider again it puts back `wide` (the
original values, filled in automatically). Keys use Plotly.relayout syntax: "legend.y",
"margin.l", "annotations[2].x", "xaxis.tickvals"; a whole list can be swapped ("annotations").

Usage (from the repo root):
    python tools/patch_plotly_layout.py CHART.html --set legend.orientation='"h"' --set legend.y=-0.2
    python tools/patch_plotly_layout.py CHART.html --unset width --set margin.r=20
    python tools/patch_plotly_layout.py CHART.html --show            # print the layout, no change
    python tools/patch_plotly_layout.py CHART.html --patch fix.json  # deep-merge a JSON object
    python tools/patch_plotly_layout.py CHART.html --narrow phone.json [--below 560]

--set PATH=VALUE   PATH is dotted (title.font.size); list items by index (annotations.0.y).
                   VALUE is JSON (numbers, true/false, null, "quoted strings", {...}, [...]);
                   anything that isn't valid JSON is taken as a plain string.
--unset PATH       delete a key (e.g. width, so the chart fills its frame).
--patch FILE       deep-merge a JSON object into the layout (a null value deletes the key).
--narrow FILE      JSON object {relayout key: value on phones}; see "Phone layout" above.
                   Applied after --set/--unset/--patch, so "wide" is the patched layout.
--narrow-restyle FILE  JSON {trace attribute: value on phones} for presentation-only trace
                   attributes (e.g. {"textposition": "inside"}); data attributes are refused.
--trace-set I.PATH=VALUE  change a presentation-only attribute of trace I for all widths
                   (e.g. 0.node.pad=26). Data attributes (x, y, text, values, link...) are refused,
                   and everything else in the traces is checked to be unchanged.
--dry-run          show what would change, don't write.

Library use:
    extract(text) -> list of Call(div_id, data, layout, config, spans)
    write_html(fig, path, narrow=None, **write_html_kwargs)   # for build scripts
"""
import argparse
import json
import pathlib
import re
import sys

# The phone-layout script. Identical in every chart that uses it; reads layout.meta.
# It writes the narrow (or wide) values into the layout object (and, for meta.restyle, into each
# trace; an array value there means one value per trace) and redraws with Plotly.newPlot, so the
# result is exactly what a fresh plot of that layout gives (relayout keeps some automatic margins
# from the previous layout). A null value deletes the key, i.e. restores Plotly's default.
NARROW_BELOW = 560
NARROW_MARK_RE = r"lodn-narrow v\d+"
NARROW_MARK = "lodn-narrow v2"
NARROW_JS = (
    '<script type="text/javascript">/* ' + NARROW_MARK + ": below layout.meta.below px wide, draw "
    "the chart with layout.meta.narrow (and meta.restyle.narrow); above it, with the wide values "
    "(tools/patch_plotly_layout.py) */\n"
    "(function(){function set(o,k,v){var p=k.replace(/\\[(\\d+)\\]/g,'.$1').split('.'),i;"
    "for(i=0;i<p.length-1;i++){if(o[p[i]]==null)o[p[i]]=/^\\d+$/.test(p[i+1])?[]:{};o=o[p[i]];}"
    "if(v==null)delete o[p[i]];else o[p[i]]=JSON.parse(JSON.stringify(v));}"
    "function fit(){var gs=document.querySelectorAll('.plotly-graph-div');"
    "for(var i=0;i<gs.length;i++){var g=gs[i],m=g.layout&&g.layout.meta;"
    "if(!m||!m.narrow||!g._fullLayout||!window.Plotly)continue;var n=g.clientWidth<m.below?'1':'0';"
    "if((g.dataset.lodn||'0')===n)continue;g.dataset.lodn=n;var s=n==='1'?m.narrow:m.wide,k,j;"
    "for(k in s)set(g.layout,k,s[k]);if(m.restyle){var r=n==='1'?m.restyle.narrow:m.restyle.wide;"
    "for(k in r)for(j=0;j<g.data.length;j++)set(g.data[j],k,Array.isArray(r[k])?r[k][j]:r[k]);}"
    "Plotly.newPlot(g,g.data,g.layout,g._context);}}"
    "window.addEventListener('resize',fit);"
    "if(document.readyState==='complete')fit();else window.addEventListener('load',fit);})();\n"
    "</script>"
)


class Call:
    def __init__(self, div_id, data, layout, config, spans):
        self.div_id = div_id
        self.data = data
        self.layout = layout
        self.config = config
        self.spans = spans  # dict name -> (start, end) offsets in the text


def _skip_ws_comma(text, i):
    while i < len(text) and text[i] in " \t\r\n,":
        i += 1
    return i


def extract(text):
    """Return every Plotly.newPlot(...) call in the text, parsed."""
    dec = json.JSONDecoder()
    calls = []
    pos = 0
    # The call plotly.py writes is Plotly.newPlot("id", ...). Files with plotly.js inlined also
    # contain "Plotly.newPlot(" inside the library, never followed by a string literal.
    for m in re.finditer(r"Plotly\.newPlot\(\s*\"", text):
        if m.start() < pos:
            continue
        i = m.end() - 1
        spans = {}
        div_id, j = dec.raw_decode(text, i)
        spans["id"] = (i, j)
        i = _skip_ws_comma(text, j)
        data, j = dec.raw_decode(text, i)
        spans["data"] = (i, j)
        i = _skip_ws_comma(text, j)
        layout, j = dec.raw_decode(text, i)
        spans["layout"] = (i, j)
        i = _skip_ws_comma(text, j)
        config = None
        if text[i] == "{":
            config, j = dec.raw_decode(text, i)
            spans["config"] = (i, j)
        calls.append(Call(div_id, data, layout, config, spans))
        pos = j
    return calls


def dumps_like_plotly(obj):
    """Compact JSON with < > / escaped, as plotly.py writes it (safe inside <script>)."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace(">", "\\u003e").replace("/", "\\u002f")


def _parse_value(v):
    try:
        return json.loads(v)
    except ValueError:
        return v


def _walk(obj, parts, create=True):
    for p in parts[:-1]:
        if isinstance(obj, list):
            obj = obj[int(p)]
        else:
            if p not in obj:
                if not create:
                    return None
                obj[p] = {}
            obj = obj[p]
    return obj


def set_path(layout, path, value):
    parts = path.split(".")
    parent = _walk(layout, parts)
    last = parts[-1]
    if isinstance(parent, list):
        parent[int(last)] = value
    else:
        parent[last] = value


def unset_path(layout, path):
    parts = path.split(".")
    parent = _walk(layout, parts, create=False)
    if parent is None:
        return
    last = parts[-1]
    if isinstance(parent, list):
        del parent[int(last)]
    elif last in parent:
        del parent[last]


def deep_merge(dst, patch):
    for k, v in patch.items():
        if v is None:
            dst.pop(k, None)
        elif isinstance(v, dict) and isinstance(dst.get(k), dict):
            deep_merge(dst[k], v)
        else:
            dst[k] = v


def _key_parts(key):
    """'annotations[2].font.size' -> ['annotations', 2, 'font', 'size']"""
    parts = []
    for tok in key.split("."):
        m = re.fullmatch(r"([^\[\]]+)((?:\[\d+\])*)", tok)
        parts.append(m.group(1))
        parts += [int(i) for i in re.findall(r"\[(\d+)\]", m.group(2))]
    return parts


def get_key(layout, key):
    """Value at a relayout-style key, or None if it isn't set."""
    obj = layout
    for p in _key_parts(key):
        try:
            obj = obj[p]
        except (KeyError, IndexError, TypeError):
            return None
    return obj


def narrow_meta(layout, narrow, below=NARROW_BELOW, restyle=None, data=None):
    """layout.meta for the phone-layout script: the narrow values plus the wide values to restore.

    restyle (optional) = {trace attribute: value on phones} for presentation-only trace attributes
    (textposition, textfont.size, ...), applied to every trace with Plotly.restyle; the wide values
    are each trace's own. Never use it for data (x, y, text, values...).
    """
    wide = {k: get_key(layout, k) for k in narrow}
    meta = {"below": below, "narrow": narrow, "wide": wide}
    if restyle:
        bad = {"x", "y", "z", "text", "values", "labels", "base", "customdata", "ids", "parents"} & set(restyle)
        if bad:
            raise ValueError(f"restyle may not touch data attributes: {sorted(bad)}")
        meta["restyle"] = {"narrow": restyle,
                           "wide": {k: [get_key(t, k) for t in (data or [])] for k in restyle}}
    return meta


def add_narrow_script(text):
    """Insert NARROW_JS before </body> (once); an older version of the script is replaced."""
    if NARROW_MARK in text:
        return text
    old = re.search(r'<script type="text/javascript">/\* ' + NARROW_MARK_RE + r".*?</script>\n?", text, re.S)
    if old:
        text = text[:old.start()] + text[old.end():]
    idx = text.rfind("</body>")
    if idx < 0:
        return text + NARROW_JS
    return text[:idx] + NARROW_JS + "\n" + text[idx:]


def write_html(fig, path, narrow=None, below=NARROW_BELOW, restyle=None, **kw):
    """fig.write_html(path, **kw), plus the phone layout when `narrow` is given."""
    if narrow is not None:
        fig.update_layout(meta=narrow_meta(fig.layout.to_plotly_json(), narrow, below, restyle,
                                           [t.to_plotly_json() for t in fig.data]))
    fig.write_html(path, **kw)
    if narrow is not None:
        p = pathlib.Path(path)
        p.write_bytes(add_narrow_script(p.read_bytes().decode("utf-8")).encode("utf-8"))


DATA_KEYS = {"x", "y", "z", "text", "values", "labels", "label", "base", "customdata", "ids", "parents",
             "source", "target", "value", "hovertext", "texttemplate"}


def trace_set(data, item):
    """'0.node.pad=26' -> data[0]['node']['pad'] = 26. Presentation attributes only."""
    path, _, val = item.partition("=")
    idx, _, rest = path.partition(".")
    if DATA_KEYS & set(rest.split(".")):
        raise SystemExit(f"--trace-set may not change data attributes: {rest}")
    set_path(data[int(idx)], rest, _parse_value(val))
    return int(idx), rest


def _strip(data, changed):
    data = json.loads(json.dumps(data))
    for idx, rest in changed:
        unset_path(data[idx], rest)
    return json.dumps(data, sort_keys=True)


def patch_text(text, sets=(), unsets=(), patch=None, which=0, narrow=None, below=NARROW_BELOW,
               restyle=None, trace_sets=()):
    """Return (new_text, old_layout, new_layout). Data arrays are not touched."""
    calls = extract(text)
    if not calls:
        raise SystemExit("No Plotly.newPlot call found.")
    call = calls[which]
    orig_data = json.loads(json.dumps(call.data))
    old = json.loads(json.dumps(call.layout))
    lay = call.layout
    changed = [trace_set(call.data, item) for item in trace_sets]
    if changed:
        a, b = call.spans["data"]
        text = text[:a] + dumps_like_plotly(call.data) + text[b:]
        call = extract(text)[which]
        lay = call.layout
    for path in unsets:
        unset_path(lay, path)
    for item in sets:
        path, _, val = item.partition("=")
        set_path(lay, path, _parse_value(val))
    if patch:
        deep_merge(lay, patch)
    if narrow is not None:
        lay["meta"] = narrow_meta(lay, narrow, below, restyle, call.data)
    a, b = call.spans["layout"]
    new_text = text[:a] + dumps_like_plotly(lay) + text[b:]

    # Keep the div's CSS height and width in step with layout.height / layout.width
    # (plotly.py writes them into the div's style attribute).
    if lay.get("height") != old.get("height") or lay.get("width") != old.get("width"):
        div_re = re.compile(r'(<div id="%s" class="plotly-graph-div" style=")([^"]*)(")' % re.escape(call.div_id))
        m = div_re.search(new_text)
        if m:
            style = m.group(2)
            h = "%dpx" % lay["height"] if lay.get("height") else "100%"
            w = "%dpx" % lay["width"] if lay.get("width") else "100%"
            style = re.sub(r"(?<![-\w])height:\s*[^;]*;", "height:%s;" % h, style)
            style = re.sub(r"(?<![-\w])width:\s*[^;]*;", "width:%s;" % w, style)
            new_text = new_text[:m.start(2)] + style + new_text[m.end(2):]

    if narrow is not None:
        new_text = add_narrow_script(new_text)

    # Safety: the traces must be identical after the patch (apart from --trace-set attributes).
    after = extract(new_text)[which]
    if _strip(after.data, changed) != _strip(orig_data, changed):
        raise SystemExit("Refusing to write: trace data changed.")
    return new_text, old, lay


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chart")
    ap.add_argument("--set", action="append", default=[], metavar="PATH=VALUE")
    ap.add_argument("--unset", action="append", default=[], metavar="PATH")
    ap.add_argument("--trace-set", action="append", default=[], metavar="I.PATH=VALUE",
                    help="presentation-only trace attribute, e.g. 0.node.pad=26 (data attributes refused)")
    ap.add_argument("--patch", metavar="FILE")
    ap.add_argument("--which", type=int, default=0, help="which newPlot call in the file (default 0)")
    ap.add_argument("--narrow", metavar="FILE")
    ap.add_argument("--below", type=int, default=NARROW_BELOW)
    ap.add_argument("--narrow-restyle", metavar="FILE",
                    help="JSON {trace attribute: value on phones}, presentation only (e.g. textposition)")
    ap.add_argument("--show", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    path = pathlib.Path(a.chart)
    text = path.read_bytes().decode("utf-8")  # keep line endings as they are
    if a.show:
        lay = dict(extract(text)[a.which].layout)
        lay.pop("template", None)
        print(json.dumps(lay, indent=1, ensure_ascii=False))
        return
    patch = json.loads(pathlib.Path(a.patch).read_text(encoding="utf-8")) if a.patch else None
    narrow = json.loads(pathlib.Path(a.narrow).read_text(encoding="utf-8")) if a.narrow else None
    restyle = json.loads(pathlib.Path(a.narrow_restyle).read_text(encoding="utf-8")) if a.narrow_restyle else None
    if restyle and narrow is None:
        narrow = {}
    new_text, old, new = patch_text(text, a.set, a.unset, patch, a.which, narrow, a.below, restyle,
                                    a.trace_set)
    for k in sorted(set(old) | set(new)):
        if k == "template":
            continue
        if old.get(k) != new.get(k):
            print(f"{k}: {json.dumps(old.get(k), ensure_ascii=False)} -> {json.dumps(new.get(k), ensure_ascii=False)}")
    if a.dry_run:
        print("(dry run, not written)")
        return
    if new_text != text:
        path.write_bytes(new_text.encode("utf-8"))
        print(f"Wrote {path}")
    else:
        print("No change.")


if __name__ == "__main__":
    main()
