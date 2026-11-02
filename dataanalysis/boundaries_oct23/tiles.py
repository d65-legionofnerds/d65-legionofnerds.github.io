# Area and boundary-line disruption tiles (land tabs), checked against the page's own Oct 13 numbers first.
from geo import *
ACRE = lambda a: a * MIPX[0] * MIPX[1] * 640
MI = lambda px: px * (MIPX[0] + MIPX[1]) / 2
FT = lambda ft: ft / 5280 / ((MIPX[0] + MIPX[1]) / 2)

def internal_lines(zones, outer, merge_ft=100):
    """Internal edges of a zone map as one merged linework (shared edges once), outer district edge removed."""
    bnds = unary_union([z.boundary for z in zones.values()])
    edge = outer.exterior.buffer(FT(merge_ft))
    lines = bnds.difference(edge)
    # merge near-duplicate traced edges: keep linework, tolerance handled by buffers when comparing
    return lines

def zone_edges(z, outer, merge_ft=100):
    return z.boundary.difference(outer.exterior.buffer(FT(merge_ft)))

def dedup_len(lines, tol_ft=40):
    """Length of linework counting near-parallel duplicates (two tracings of one shared edge) once."""
    g = lines.buffer(FT(tol_ft) / 2)
    # area / width approximates centerline length
    return g.area / (FT(tol_ft))

def tiles(OLD, NEW, feed_now, feed_new, tol_ft=100):
    outer = unary_union(list(OLD.values())).buffer(3).buffer(-3)
    U_old = unary_union(list(OLD.values()))
    tot = 0; elem = 0; both = 0
    feedof_now = {e: m for m, es in feed_now.items() for e in es}; feedof_new = {e: m for m, es in feed_new.items() for e in es}
    covered = 0
    for n, g in OLD.items():
        for k, h in NEW.items():
            a = g.intersection(h).area
            if not a: continue
            covered += a
            if Z.get(k, k) != n:
                elem += a
                if feedof_now[n] != feedof_new[Z.get(k, k)]: both += a
    out = {"acres": ACRE(covered), "change": ACRE(elem), "both": ACRE(both), "elemonly": ACRE(elem - both), "same": ACRE(covered - elem),
           "lakefront": ACRE(U_old.area - covered)}
    lo = internal_lines(OLD, outer); ln = internal_lines(NEW, outer)
    tol = FT(tol_ft)
    Lo = dedup_len(lo); Ln = dedup_len(ln)
    rem = dedup_len(lo.difference(ln.buffer(tol))); new = dedup_len(ln.difference(lo.buffer(tol)))
    same = Lo - rem
    out |= {"Lo": MI(Lo), "Ln": MI(Ln), "removed": MI(rem), "new": MI(new), "unchanged": MI(same), "total": MI(same + rem + new)}
    per = {}
    for n, g in OLD.items():
        e = zone_edges(g, outer); L = e.length
        mv = e.difference(ln.buffer(tol)).length
        rec = {"old": MI(L), "moved": mv / L if L else 0}
        k = ZK.get(n)
        if k and k in NEW:
            e2 = zone_edges(NEW[k], outer); L2 = e2.length
            rec |= {"new": MI(L2), "newshare": e2.difference(lo.buffer(tol)).length / L2 if L2 else 0}
        per[n] = rec
    out["per"] = per
    return out

if __name__ == '__main__':
    P = loadpage(); D = P['D']
    OLD = {n: Polygon(D['old'][n]).buffer(0) for n in SCH}; NEW = {k: Polygon(v).buffer(0) for k, v in D['new'].items()}
    FN = {"Chute": ["Dawes", "Oakton", "Walker"], "Nichols": ["Dewey", "Washington", "Lincoln"], "Haven": ["Lincolnwood", "Orrington", "Foster", "Willard"]}
    FW = {"Chute": ["Dawes", "Oakton", "Walker"], "Nichols": ["Washington", "Lincoln"], "Haven": ["Orrington", "Foster", "Willard"]}
    t = tiles(OLD, NEW, FN, FW)
    print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in t.items() if k != 'per'})
    for n, r in t['per'].items(): print(n, {k: round(v, 2) for k, v in r.items()})
    print('page: 33.7% / 1940 ac, both 1053, elem only 887, same 3805, total 5745, lakefront 83; lines Lo 15.0 Ln 12.6 removed 9.2 new 6.8 unchanged 5.8')
