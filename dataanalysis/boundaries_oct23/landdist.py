# Land-based walking distance (street grid = east-west blocks + north-south blocks), every bit of land weighted equally.
import numpy as np
from shapely.geometry import box, Point
from shapely.ops import unary_union
from shapely import contains_xy
from geo import *

BANDS = [0.5, 1.0, 1.5]

def band(v):
    return 0 if v < 0.5 else 1 if v < 1 else 2 if v < 1.5 else 3

def landdist(OLD, NEW, schools, newname, step=3, with_bands=True, nb=12):
    """OLD: name->Polygon (today). NEW: key->Polygon. schools: name->[x,y]. newname: key->school name."""
    U = unary_union(list(OLD.values()))
    x0, y0, x1, y1 = U.bounds
    xs = np.arange(x0 + step / 2, x1, step); ys = np.arange(y0 + step / 2, y1, step)
    X, Y = np.meshgrid(xs, ys); X = X.ravel(); Y = Y.ravel()
    home = np.full(X.size, -1); newk = np.full(X.size, -1)
    on = list(OLD); nk = list(NEW)
    for i, n in enumerate(on): home[contains_xy(OLD[n], X, Y)] = i
    for k, key in enumerate(nk): newk[contains_xy(NEW[key], X, Y)] = k
    m = (home >= 0) & (newk >= 0)          # land with no new zone (lakefront mismatch) is left out
    X, Y, home, newk = X[m], Y[m], home[m], newk[m]
    bef = np.array([manh(x, y, schools[on[h]]) for x, y, h in zip(X, Y, home)])
    aft = np.array([manh(x, y, schools[newname[nk[k]]]) for x, y, k in zip(X, Y, newk)])
    out = {"district": {"before": stats(bef), "after": stats(aft), "histB": hist(bef, nb=nb), "histA": hist(aft, nb=nb)}, "schools": {}, "zones": {}}
    for i, n in enumerate(on):
        s = home == i
        if not s.any(): continue
        b, a = bef[s], aft[s]
        pcs = []
        for k, key in enumerate(nk):
            t = s & (newk == k)
            if t.sum() < 3: continue
            pcs.append({"zone": key, "before": round(float(bef[t].mean()), 2), "after": round(float(aft[t].mean()), 2), "_n": int(t.sum())})
        pcs.sort(key=lambda p: -p["_n"]); [p.pop("_n") for p in pcs]
        ib, ia = int(np.argmax(b)), int(np.argmax(a))
        rec = {"before": stats(b), "after": stats(a), "pieces": pcs,
               "farBefore": [int(X[s][ib]), int(Y[s][ib])], "farAfter": [int(X[s][ia]), int(Y[s][ia])],
               "farAfterTo": newname[nk[int(newk[s][ia])]]}
        if with_bands:
            for nm, v in (("bandsBefore", b), ("bandsAfter", a)):
                bb = np.array([band(q) for q in v]); gs = []
                for j in range(4):
                    sel = bb == j
                    if not sel.any(): gs.append([]); continue
                    g = unary_union([box(x - step / 2, y - step / 2, x + step / 2, y + step / 2) for x, y in zip(X[s][sel], Y[s][sel])]).buffer(0.01)
                    gs.append(rings_of(g.intersection(OLD[n]), tol=1.2, minarea=20))
                rec[nm] = gs
        out["schools"][n] = rec
    for k, key in enumerate(nk):
        s = newk == k
        if s.any(): out["zones"][newname[key]] = stats(aft[s])
    return out
