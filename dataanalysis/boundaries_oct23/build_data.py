# Rebuild the boundary page's line-dependent data (D, MS, D2 parts) on the district's Oct 23, 2026 lines.
# Lines: today's 2026-27 areas and the Oct 23 draft, both from the district's FY28 Proposed Boundaries Google My Map
# (KML, pulled Oct 23), as already placed on this map frame for D65 School Circles. King Arts' neighborhood area is
# drawn on the Oct 23 layer; it is King Arts' area today too, so it is left out of Dewey's 2026-27 area on both maps.
import base64, copy
from geo import *
from landdist import landdist, band
from shapely import contains_xy, voronoi_polygons, MultiPoint

P = loadpage(); D0, MS0, D20 = P['D'], P['MS'], P['D2']
M = json.load(open(B + 'M.json'))
AFF = json.load(open(B + 'aff_D2.json'))          # map frame -> census-tab frame (fitted on the two sets of today's lines)
T = lambda g: affinity.affine_transform(g, AFF)
Tp = lambda x, y: [AFF[0] * x + AFF[1] * y + AFF[4], AFF[2] * x + AFF[3] * y + AFF[5]]

KA = pathgeom(M['z23']['King Arts'])
OLD = {n: largest(pathgeom(M['z'][n]).difference(KA)) for n in SCH}
NEW = {ZK[n]: pathgeom(M['z23'][n]) for n in Z.values()}
FEED_NOW = {"Chute": ["Dawes", "Oakton", "Walker"], "Nichols": ["Dewey", "Washington", "Lincoln"], "Haven": ["Lincolnwood", "Orrington", "Foster", "Willard"]}
FEED_NEW = {"Chute": ["Dawes", "Oakton", "Walker"], "Nichols": ["Washington", "Lincoln"], "Haven": ["Orrington", "Foster", "Willard"]}
schools = D0['schools']

def school_in(n, NEWd):
    p = Point(*schools[n])
    for k, g in NEWd.items():
        if g.contains(p): return k
    return min(NEWd, key=lambda k: NEWd[k].distance(p))

def land_pieces(n, minshare=0.004):
    v = {k: OLD[n].intersection(g) for k, g in NEW.items()}
    v = {k: g for k, g in v.items() if g.area > OLD[n].area * minshare}
    sh = shares({k: g.area for k, g in v.items()})
    out = []
    for k in sorted(v, key=lambda k: -v[k].area):
        lp = largest(v[k]); a = lp.representative_point()
        out.append({"zone": k, "share": sh[k], "anchor": [int(a.x), int(a.y)], "polys": rings_of(v[k], tol=0.6, minarea=30)})
    return out

# ---------------- D: land-area tabs + builder lines ----------------
D = copy.deepcopy(D0)
D['old'] = {n: ring(OLD[n], 0.3) for n in SCH}
D['new'] = {k: ring(largest(g), 0.3) for k, g in NEW.items()}
D['pieces'] = {n: land_pieces(n) for n in SCH}
for n in SCH:
    D['split'][n]['split'] = {p['zone']: p['share'] for p in D['pieces'][n]}
    D['split'][n]['school_in'] = school_in(n, NEW)
dd = landdist(OLD, NEW, schools, Z, step=3)
D['dist'] = dd

# ---------------- MS: middle-school land tabs ----------------
MS = copy.deepcopy(MS0)
MOLD = {m: unary_union([OLD[e] for e in es]).buffer(0.5).buffer(-0.5) for m, es in FEED_NOW.items()}
MNEW = {m: unary_union([NEW[ZK[e]] for e in es]).buffer(0.5).buffer(-0.5) for m, es in FEED_NEW.items()}
MS['old'] = {m: rings_of(g, tol=0.6, minarea=50) for m, g in MOLD.items()}
MS['new'] = {m: rings_of(g, tol=0.6, minarea=50) for m, g in MNEW.items()}
MS['pieces'] = {}
for m in MOLD:
    v = {k: MOLD[m].intersection(g) for k, g in MNEW.items()}
    v = {k: g for k, g in v.items() if g.area > MOLD[m].area * 0.004}
    sh = shares({k: g.area for k, g in v.items()})
    MS['pieces'][m] = [{"zone": k, "share": sh[k], "anchor": [int(largest(v[k]).representative_point().x), int(largest(v[k]).representative_point().y)],
                        "polys": rings_of(v[k], tol=0.6, minarea=30)} for k in sorted(v, key=lambda k: -v[k].area)]
md = landdist(MOLD, MNEW, MS0['schools'], {k: k for k in MNEW}, step=4, with_bands=False)
md.pop('zones', None); MS['dist'] = md

# ---------------- D2: census tabs (kids by block, street-network walks) ----------------
K = M['k']; S = [s['n'] for s in M['s']]
DW = {S[i]: np.frombuffer(base64.b64decode(M['w'][i]), dtype=np.uint8) / 100 for i in range(len(S))}
BX = np.array([b[0] for b in K]); BY = np.array([b[1] for b in K])
k510 = np.array([b[4] for b in K], float); k1113 = np.array([b[6] for b in K], float)
home = np.array([None] * len(K), object); newk = np.array([None] * len(K), object)
for n in SCH: home[contains_xy(OLD[n], BX, BY)] = n
for k, g in NEW.items(): newk[contains_xy(g, BX, BY)] = k
# blocks just outside the traced lines (edge blocks) take the nearest area
for j in range(len(K)):
    if home[j] is None and not KA.contains(Point(BX[j], BY[j])) and min(OLD[n].distance(Point(BX[j], BY[j])) for n in SCH) < 8:
        home[j] = min(SCH, key=lambda n: OLD[n].distance(Point(BX[j], BY[j])))
    if home[j] is not None and newk[j] is None:
        newk[j] = min(NEW, key=lambda k: NEW[k].distance(Point(BX[j], BY[j])))
IN = np.array([h is not None for h in home])

def st1(d, w):
    s = stats(d, w)
    w = np.asarray(w, float); d = np.asarray(d, float)
    s['gt15'] = round(float(w[d > 1.5].sum() / w.sum() * 100), 1) if w.sum() else 0
    return s

D2 = copy.deepcopy(D20)
D2['old'] = {n: ring(T(OLD[n]), 0.3, 0) for n in SCH}
D2['new'] = {k: ring(T(largest(g)), 0.3, 0) for k, g in NEW.items()}
D2['pieces'] = {}; D2['dist'] = {"schools": {}, "zones": {}}
befK = np.array([DW[home[j]][j] if IN[j] else 0 for j in range(len(K))])
aftK = np.array([DW[Z[newk[j]]][j] if IN[j] else 0 for j in range(len(K))])
for n in SCH:
    s = (home == n) & IN
    kv = {k: float(k510[s & (newk == k)].sum()) for k in NEW}
    kv = {k: v for k, v in kv.items() if v > 0}
    sh = shares(kv); sh = {k: v for k, v in sh.items() if v >= 1}
    sh = shares({k: kv[k] for k in sh})
    land = {k: OLD[n].intersection(NEW[k]) for k in sh}
    D2['pieces'][n] = [{"zone": k, "share": sh[k], "anchor": [int(v) for v in Tp(largest(land[k]).representative_point().x, largest(land[k]).representative_point().y)] if not land[k].is_empty else Tp(*schools[n]),
                        "polys": rings_of(T(land[k]), tol=0.6, minarea=30)} for k in sorted(sh, key=lambda k: -sh[k])]
    D2['split'][n]['split'] = {p['zone']: p['share'] for p in D2['pieces'][n]}
    D2['split'][n]['school_in'] = school_in(n, NEW)
    w = k510[s]; b = befK[s]; a = aftK[s]
    pcs = []
    for k in sh:
        t = s & (newk == k); ww = k510[t]
        pcs.append({"zone": k, "kids": int(round(ww.sum())), "before": round(float((befK[t] * ww).sum() / ww.sum()), 2), "after": round(float((aftK[t] * ww).sum() / ww.sum()), 2), "share": sh[k]})
    ib = int(np.argmax(np.where(w > 0, b, -1))); ia = int(np.argmax(np.where(w > 0, a, -1)))
    rec = {"before": st1(b, w), "after": st1(a, w), "pieces": pcs, "farBefore": [int(v) for v in Tp(BX[s][ib], BY[s][ib])],
           "farAfter": [int(v) for v in Tp(BX[s][ia], BY[s][ia])], "farAfterTo": Z[newk[s][ia]], "kids": int(round(w.sum()))}
    # walking bands: each block's Voronoi cell, clipped to the area
    pts = MultiPoint(list(zip(BX[s], BY[s])))
    vor = voronoi_polygons(pts, extend_to=OLD[n].buffer(60))
    cells = list(vor.geoms)
    cpt = {}
    for c in cells:
        for j in np.where(s)[0]:
            pass
    # match cells to blocks
    idx = np.where(s)[0]; cb = []
    for c in cells:
        jj = idx[[c.contains(Point(BX[j], BY[j])) for j in idx]]
        cb.append(jj[0] if len(jj) else None)
    for nm, arr in (("bandsBefore", befK), ("bandsAfter", aftK)):
        gs = []
        for bi in range(4):
            g = unary_union([c for c, j in zip(cells, cb) if j is not None and band(arr[j]) == bi])
            gs.append(rings_of(T(g.intersection(OLD[n])), tol=1.2, minarea=20) if not g.is_empty else [])
        rec[nm] = gs
    D2['dist']['schools'][n] = rec
w = k510[IN]; mv = np.array([Z[newk[j]] != home[j] for j in np.where(IN)[0]])
D2['dist']['district'] = {"kids": int(round(w.sum())), "before": st1(befK[IN], w), "after": st1(aftK[IN], w),
                          "histB": hist(befK[IN], w), "histA": hist(aftK[IN], w), "moved": int(round(w[mv].sum()))}
for k in NEW:
    t = IN & (newk == k)
    if t.any(): D2['dist']['zones'][Z[k]] = {"kids": int(round(k510[t].sum()))} | st1(aftK[t], k510[t])
D2['pop'] = {"schools": {n: {"kids": int(round(k510[(home == n) & IN].sum()))} for n in SCH}}

# heat bands: kids by area, by new zone, moved, by new feeder
FEEDOF = {e: m for m, es in FEED_NEW.items() for e in es}
for bk, wv in (("k5", k510), ("m68", k1113), ("k8", k510 + k1113)):
    b = D2['heat2']['bands'][bk]
    b['old'] = {n: int(round(wv[(home == n) & IN].sum())) for n in SCH}
    b['new'] = {Z[k]: int(round(wv[(newk == k) & IN].sum())) for k in NEW}
    b['moved'] = int(round(sum(wv[j] for j in np.where(IN)[0] if Z[newk[j]] != home[j])))
    b['total'] = int(round(wv[IN].sum()))
    b['feed'] = {m: int(round(sum(wv[j] for j in np.where(IN)[0] if FEEDOF[Z[newk[j]]] == m))) for m in FEED_NEW}
D2['heat2']['feedpolys'] = {m: [[[int(round(v)) for v in Tp(x, y)] for x, y in r] for r in MS['new'][m]] for m in FEED_NEW}
D2['heat2']['feedmap'] = {"Chute": ["Dawes", "Walker", "Oakton"], "Nichols": ["Washington", "Lincoln"], "Haven": ["Orrington", "Willard", "Foster"]}

# race of kids (2020 Census, builder grid cells), by area, new zone and move
RD = P['RD']; CS, NX = 12, int(math.ceil(1324 / 12)); G = RD['groups']
cx = np.array([(int(c) % NX) * CS + CS / 2 for c in RD['cells']['kids']]); cy = np.array([(int(c) // NX) * CS + CS / 2 for c in RD['cells']['kids']])
cv = np.array(list(RD['cells']['kids'].values()))
ch = np.array([None] * len(cx), object); cn = np.array([None] * len(cx), object)
for n in SCH: ch[contains_xy(OLD[n], cx, cy)] = n
for k, g in NEW.items(): cn[contains_xy(g, cx, cy)] = Z[k]
def comp(sel):
    v = cv[sel].sum(0); t = v.sum()
    return {"n": int(round(t))} | {G[i]: round(float(v[i] / t * 100), 1) for i in range(len(G))} if t else {"n": 0}
ok = np.array([h is not None and z is not None for h, z in zip(ch, cn)])
race = {"old": {n: comp(ok & (ch == n)) for n in SCH}, "new": {z: comp(ok & (cn == z)) for z in Z.values()}, "moved": {}}
for a in SCH:
    for z in Z.values():
        if z == a: continue
        sel = ok & (ch == a) & (cn == z)
        if cv[sel].sum() >= 15: race["moved"][f"{a}>{z}"] = comp(sel)
race["allmoved"] = comp(ok & (ch != cn)); race["all"] = comp(ok)
# shares come from the race grid; counts are 2020 Census kids ages 5-10 by block, like the rest of these tabs
def kn(hsel=None, zsel=None, moved=False):
    t = 0.0
    for j in np.where(IN)[0]:
        z = Z[newk[j]]; h = home[j]
        if hsel and h != hsel: continue
        if zsel and z != zsel: continue
        if moved and z == h: continue
        t += k510[j]
    return int(round(t))
for n in race["old"]: race["old"][n]["n"] = kn(hsel=n)
for z in race["new"]: race["new"][z]["n"] = kn(zsel=z)
for key in list(race["moved"]):
    a_, z_ = key.split(">"); race["moved"][key]["n"] = kn(hsel=a_, zsel=z_)
    if race["moved"][key]["n"] < 5: race["moved"].pop(key)
race["allmoved"]["n"] = kn(moved=True); race["all"]["n"] = kn()
D2['race'] = race

json.dump({"D": D, "MS": MS, "D2": D2}, open(B + 'oct23_data.json', 'w'), separators=(',', ':'))
# summary
print('D pieces:'); [print(' ', n, [(Z[p['zone']], p['share']) for p in D['pieces'][n]]) for n in SCH]
print('MS pieces:', {m: [(p['zone'], p['share']) for p in v] for m, v in MS['pieces'].items()})
print('D2 kid shares:'); [print(' ', n, [(Z[p['zone']], p['share']) for p in D2['pieces'][n]]) for n in SCH]
print('land dist district', dd['district']['before'], dd['district']['after'])
print('kid dist district', D2['dist']['district'])
print('MS dist', md['district']['before'], md['district']['after'])
print('heat k5', {k: v for k, v in D2['heat2']['bands']['k5'].items() if k != 'img'})
print('race moved', {k: v['n'] for k, v in race['moved'].items()})
