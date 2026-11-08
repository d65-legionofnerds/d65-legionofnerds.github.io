# Shared geometry helpers for rebuilding d65_boundaries.html on the Oct 23, 2026 lines.
import json, re, math
import numpy as np
from shapely.geometry import Polygon, MultiPolygon, Point, LineString, box
from shapely.ops import unary_union, split
from shapely import affinity
from shapely.prepared import prep

B = '/tmp/claude-0/-home-claude/3bffa1f6-baa2-5bdf-9b5a-29944701f712/scratchpad/b23/'
MIPX = [0.003178082769737034, 0.003218098035888021]   # miles per pixel (x, y), from the page
Z = {"purple": "Willard", "red": "Orrington", "brown": "Walker", "maroon": "Foster", "green": "Washington",
     "teal": "Lincoln", "blue": "Dawes", "orange": "Oakton"}
ZK = {v: k for k, v in Z.items()}
SCH = ["Dawes", "Dewey", "Foster", "Lincoln", "Lincolnwood", "Oakton", "Orrington", "Washington", "Walker", "Willard"]
RM = ["Dewey", "Lincolnwood"]

def pathgeom(d):
    g = None
    for sp in re.findall(r'M[^M]*', d):
        pts = [tuple(map(float, x.split(','))) for x in re.findall(r'-?[\d.]+,-?[\d.]+', sp)]
        if len(pts) < 3: continue
        p = Polygon(pts).buffer(0)
        g = p if g is None else g.symmetric_difference(p)
    return g

def parts(g):
    if g is None or g.is_empty: return []
    if g.geom_type == 'Polygon': return [g]
    return [p for p in getattr(g, 'geoms', []) if p.geom_type == 'Polygon' and not p.is_empty]

def largest(g):
    ps = parts(g); return max(ps, key=lambda p: p.area) if ps else None

def ring(p, tol=0.3, nd=1):
    p = p.simplify(tol, preserve_topology=True)
    c = list(p.exterior.coords)[:-1]
    return [[round(x, nd), round(y, nd)] for x, y in c]

def holefree(p):
    """Split a polygon with holes into hole-free polygons (SVG <polygon> can't draw holes)."""
    out, todo = [], [p]
    while todo:
        q = todo.pop()
        if q.is_empty: continue
        if not q.interiors: out.append(q); continue
        h = Polygon(q.interiors[0]); cx, cy = h.centroid.x, h.centroid.y
        x0, y0, x1, y1 = q.bounds
        line = LineString([(x0 - 5, cy), (x1 + 5, cy)])
        try:
            pieces = split(q, line)
            ps = [g for g in pieces.geoms if g.geom_type == 'Polygon']
            if len(ps) < 2: raise ValueError
        except Exception:
            line = LineString([(cx, y0 - 5), (cx, y1 + 5)])
            ps = [g for g in split(q, line).geoms if g.geom_type == 'Polygon']
            if len(ps) < 2: out.append(Polygon(q.exterior)); continue
        todo.extend(ps)
    return out

def rings_of(g, tol=0.6, minarea=4):
    r = []
    for p in parts(g):
        for q in holefree(p):
            if q.area >= minarea: r.append(ring(q, tol))
    return r

def shares(vals):
    """Integer percents that add to 100 (largest remainder)."""
    tot = sum(vals.values())
    if tot <= 0: return {k: 0 for k in vals}
    raw = {k: v * 100 / tot for k, v in vals.items()}
    fl = {k: int(math.floor(v)) for k, v in raw.items()}
    left = 100 - sum(fl.values())
    for k in sorted(raw, key=lambda k: raw[k] - fl[k], reverse=True)[:left]: fl[k] += 1
    return fl

def manh(x, y, s):
    return abs(x - s[0]) * MIPX[0] + abs(y - s[1]) * MIPX[1]

def stats(d, w=None):
    d = np.asarray(d, float)
    if w is None: w = np.ones_like(d)
    w = np.asarray(w, float)
    if d.size == 0 or w.sum() == 0: return {"avg": 0, "p90": 0, "max": 0, "le1": 0, "gt15": 0}
    o = np.argsort(d); cw = np.cumsum(w[o]) / w.sum()
    p90 = d[o][np.searchsorted(cw, 0.9)]
    return {"avg": round(float((d * w).sum() / w.sum()), 2), "p90": round(float(p90), 2), "max": round(float(d[w > 0].max()), 2),
            "le1": round(float(w[d <= 1].sum() / w.sum() * 100)), "gt15": round(float(w[d > 1.5].sum() / w.sum() * 100))}

def hist(d, w=None, nb=12, step=0.25):
    d = np.asarray(d, float); w = np.ones_like(d) if w is None else np.asarray(w, float)
    h = np.zeros(nb)
    for v, ww in zip(d, w): h[min(nb - 1, int(v / step))] += ww
    return [round(float(x / w.sum() * 100), 1) for x in h]

def loadpage():
    s = open(B + 'orig.html').read()
    sc = [m.group(1) for m in re.finditer(r'<script[^>]*>(.*?)</script>', s, re.S)]
    def grab(src, name):
        i = src.index(f'const {name}=') + len(f'const {name}=')
        o, e = json.JSONDecoder().raw_decode(src[i:]); return o
    return {k: grab(sc[1], k) for k in ['D', 'MS', 'CEN']} | {k: grab(sc[2], k) for k in ['D2', 'HZ', 'RD']}
