"""build_large_tet_v3.py -- Alishan #46 LARGE model, TET, NEW geology (v3).

Rebuild of large_tet.inp on Wade's v2 geologic logic (clv local to the F01
footprint; F02_Ssh/F03_bedrock-up full-domain; clip rule d).  Mesh route =
the PROVEN conformal box-by-surface fragment of build_large_tet.py:

  OCC box x[0,2000] y[-100,2000] z[800,2300]
    + 4 BSpline surfaces (DEM, S1, S2, S3 from gen_large_geo_v3.py; mutual
      gap >= 12 m POINTWISE by same-basis control-net construction -> no
      surface/surface intersections, conformal shared faces, no voids)
    -> occ.fragment -> removeAllDuplicates -> drop fragments above the DEM
       (COM tested against the *BSpline itself*, Newton-refined vertical
       sample -- robust against linear-interp sag)
    -> Structured 3D background size field large_size_v3.dat
       (<=20 m in export box x[1150,1450] y[750,1050] z[1600,1900];
        gap/curvature-driven near the geology surfaces; ~50 m far)
    -> tet mesh -> weld seam duplicates -> DROP ORPHAN nodes (lesson #15)
    -> label layer1..4 by centroid against the TRUE clipped fields
       (layer1 clv additionally gated by the F01 footprint mask)
    -> large_tet.inp (C3D4, ELSETs layer1..4) + quality report.

Run with C:/Users/Wade/anaconda3/python.exe, SERIALLY (gmsh OOM lesson #12).
"""
from __future__ import annotations
import os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NPZ  = os.path.join(HERE, 'large_geo_v3.npz')
SIZE = os.path.join(HERE, 'large_size_v3.dat')
INP  = os.path.join(HERE, 'large_tet.inp')
MSH  = os.path.join(HERE, 'large_tet.msh')

X0, X1, Y0, Y1, ZB = 0.0, 2000.0, -100.0, 2000.0, 800.0
ZTOP_BOX = 2300.0
NBX, NBY = 41, 43            # BSpline control net (50 m subsample of 25 m grid)
EB = ((1150.0, 1450.0), (750.0, 1050.0), (1600.0, 1900.0))


def bspline_surface(o, xs, ys, Z, nbx, nby):
    """points ordered i(x)-outer / j(y)-inner -> U runs along y: numPointsU=nby
    (verified empirically on gmsh 4.x: corner/mid evaluation exact)."""
    ix = np.linspace(0, len(xs) - 1, nbx).round().astype(int)
    iy = np.linspace(0, len(ys) - 1, nby).round().astype(int)
    pts = [o.addPoint(xs[i], ys[j], Z[i, j]) for i in ix for j in iy]
    return o.addBSplineSurface(pts, nby)


def weld_nodes(ncoord, conn, tol=1e-4):
    from scipy.spatial import cKDTree
    pairs = cKDTree(ncoord).query_pairs(tol)
    if not pairs:
        return ncoord, conn, 0
    parent = np.arange(len(ncoord))
    def find(a):
        r = a
        while parent[r] != r:
            r = parent[r]
        while parent[a] != r:
            parent[a], a = r, parent[a]
        return r
    for i, j in pairs:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[max(ri, rj)] = min(ri, rj)
    root = np.array([find(i) for i in range(len(ncoord))])
    uniq, inv = np.unique(root, return_inverse=True)
    return ncoord[uniq], inv[conn], len(ncoord) - len(uniq)


def bspline_z_at(s_tag, x, y, gm):
    """vertical sample z(x,y) of an OCC surface: 2-var Newton with numerical
    Jacobian on (u,v) -> (x,y).  Mapping-agnostic (u may run along x or y)."""
    lo, hi = gm.model.getParametrizationBounds(2, s_tag)
    u = 0.5 * (lo[0] + hi[0]); v = 0.5 * (lo[1] + hi[1])
    du = (hi[0] - lo[0]) * 1e-4; dv = (hi[1] - lo[1]) * 1e-4
    for _ in range(12):
        p = gm.model.getValue(2, s_tag, [u, v])
        rx, ry = x - p[0], y - p[1]
        if abs(rx) < 1e-6 and abs(ry) < 1e-6:
            break
        pu = gm.model.getValue(2, s_tag, [min(u + du, hi[0]), v])
        pv = gm.model.getValue(2, s_tag, [u, min(v + dv, hi[1])])
        J = np.array([[(pu[0]-p[0])/du, (pv[0]-p[0])/dv],
                      [(pu[1]-p[1])/du, (pv[1]-p[1])/dv]])
        try:
            step = np.linalg.solve(J, [rx, ry])
        except np.linalg.LinAlgError:
            break
        u = min(max(u + step[0], lo[0]), hi[0])
        v = min(max(v + step[1], lo[1]), hi[1])
    p = gm.model.getValue(2, s_tag, [u, v])
    if abs(p[0] - x) > 1.0 or abs(p[1] - y) > 1.0:
        return None
    return p[2]


def tet_quality(P):
    """P (M,4,3) -> vol, gamma(=3*r_in/R_circ, 1=regular), aspect(edge ratio)."""
    a, b, c, d = P[:, 0], P[:, 1], P[:, 2], P[:, 3]
    vol = np.einsum('ij,ij->i', np.cross(b - a, c - a), d - a) / 6.0
    E = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    el = np.stack([np.linalg.norm(P[:, i] - P[:, j], axis=1) for i, j in E], 1)
    aspect = el.max(1) / np.maximum(el.min(1), 1e-12)
    def tri_area(p, q, r):
        return 0.5 * np.linalg.norm(np.cross(q - p, r - p), axis=1)
    A = (tri_area(a, b, c) + tri_area(a, b, d) +
         tri_area(a, c, d) + tri_area(b, c, d))
    r_in = 3.0 * np.abs(vol) / np.maximum(A, 1e-300)
    M = np.stack([b - a, c - a, d - a], axis=1)             # (M,3,3)
    rhs = 0.5 * np.einsum('nij,nij->ni', M, M)
    try:
        cc = np.linalg.solve(M, rhs[..., None])[..., 0]
    except np.linalg.LinAlgError:
        cc = np.zeros_like(rhs)
    R = np.linalg.norm(cc, axis=1)
    gamma = 3.0 * r_in / np.maximum(R, 1e-300)
    return vol, gamma, aspect, el


def main():
    d = np.load(NPZ, allow_pickle=True)
    xs, ys = d['xs'], d['ys']
    dem, s1z, s2z, s3z = d['dem'], d['s1z'], d['s2z'], d['s3z']
    t1, f02, f03, m01 = d['t1'], d['f02'], d['f03'], d['mask_f01']

    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 1)
    gmsh.model.add('large_v3')
    o = gmsh.model.occ

    box = o.addBox(X0, Y0, ZB, X1 - X0, Y1 - Y0, ZTOP_BOX - ZB)
    dem_s = bspline_surface(o, xs, ys, dem, NBX, NBY)
    rs = [bspline_surface(o, xs, ys, Z, NBX, NBY) for Z in (s1z, s2z, s3z)]
    o.synchronize()

    o.fragment([(3, box)], [(2, dem_s)] + [(2, s) for s in rs])
    o.removeAllDuplicates()
    o.synchronize()

    # ---- drop the above-DEM cap(s) ------------------------------------------
    # the 4 S/DEM surfaces are mutually gap-separated and all BELOW the DEM,
    # so the only volumes touching the raw box top z=2300 are the above-DEM
    # caps; every rock band tops out at the DEM (max 2193).  bbox test = exact.
    from scipy.interpolate import RegularGridInterpolator
    drop, keep = [], []
    for dim, t in gmsh.model.getEntities(3):
        bb = gmsh.model.getBoundingBox(dim, t)
        (drop if bb[5] > ZTOP_BOX - 50.0 else keep).append((dim, t))
    if drop:
        o.remove(drop, recursive=True)
        o.synchronize()
    rock = gmsh.model.getEntities(3)
    print(f"fragment + DEM trim: rock volumes = {len(rock)} (dropped {len(drop)})")
    assert len(rock) == 4, f"expected 4 conformal bands, got {len(rock)}"

    pg = gmsh.model.addPhysicalGroup(3, [t for _, t in rock])
    gmsh.model.setPhysicalName(3, pg, 'rock')

    # ---- background size: Structured grid -----------------------------------
    fid = gmsh.model.mesh.field.add('Structured')
    gmsh.model.mesh.field.setString(fid, 'FileName', SIZE)
    gmsh.model.mesh.field.setNumber(fid, 'TextFormat', 1)
    try:
        gmsh.model.mesh.field.setNumber(fid, 'SetOutsideValue', 1)
        gmsh.model.mesh.field.setNumber(fid, 'OutsideValue', 50.0)
    except Exception:
        pass
    gmsh.model.mesh.field.setAsBackgroundMesh(fid)

    gmsh.option.setNumber('Mesh.MeshSizeMin', 6.0)
    gmsh.option.setNumber('Mesh.MeshSizeMax', 55.0)
    gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)
    gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
    gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 0)
    gmsh.option.setNumber('Mesh.Algorithm', 6)
    gmsh.option.setNumber('Mesh.Algorithm3D', 1)
    gmsh.option.setNumber('Mesh.Optimize', 1)
    gmsh.option.setNumber('Mesh.OptimizeNetgen', 1)
    gmsh.option.setNumber('Mesh.OptimizeThreshold', 0.5)
    gmsh.option.setNumber('Mesh.Smoothing', 20)
    gmsh.option.setNumber('Mesh.SmoothRatio', 1.4)
    gmsh.option.setNumber('Mesh.SaveAll', 0)

    gmsh.model.mesh.generate(3)
    gmsh.write(MSH)

    ntags, ncoord, _ = gmsh.model.mesh.getNodes()
    ncoord = ncoord.reshape(-1, 3)
    nmap = {int(t): i for i, t in enumerate(ntags)}
    etags, enodes = gmsh.model.mesh.getElementsByType(4)
    conn = np.array([nmap[int(t)] for t in enodes]).reshape(-1, 4)

    # ---- band identity per element (volume entity -> stack position) -------
    # band = 1..4 top-down; identified per volume by the MEDIAN of the
    # surface-count rule over its own cells (median cell is interior -> immune
    # to BSpline-vs-interp jitter at the band skins).
    from scipy.interpolate import RegularGridInterpolator as RGI
    mkI = lambda Z: RGI((xs, ys), Z, bounds_error=False, fill_value=None)
    s1I, s2I, s3I = mkI(s1z), mkI(s2z), mkI(s3z)
    tag2row = {int(t): i for i, t in enumerate(etags)}
    band = np.zeros(len(etags), dtype=np.int64)
    cent0 = ncoord[conn].mean(axis=1)
    for dim, vt in rock:
        tps, tgs, _ = gmsh.model.mesh.getElements(3, vt)
        vt_tags = None
        for tp, tg in zip(tps, tgs):
            if tp == 4:
                vt_tags = tg
        rows = np.array([tag2row[int(t)] for t in vt_tags])
        c = cent0[rows]
        q0, cz0 = c[:, :2], c[:, 2]
        bidx = (1 + (s1I(q0) > cz0).astype(int) + (s2I(q0) > cz0).astype(int)
                + (s3I(q0) > cz0).astype(int))
        band[rows] = int(round(float(np.median(bidx))))
    print("band census:", {b: int((band == b).sum()) for b in range(1, 5)})
    assert set(np.unique(band)) == {1, 2, 3, 4}, "band identification failed"
    gmsh.finalize()

    ncoord, conn, nw = weld_nodes(ncoord, conn)
    # ---- orphan-node removal (lesson #15) -----------------------------------
    used = np.unique(conn)
    norph = len(ncoord) - len(used)
    remap = -np.ones(len(ncoord), dtype=np.int64)
    remap[used] = np.arange(len(used))
    ncoord, conn = ncoord[used], remap[conn]
    print(f"tets {len(conn)}  nodes {len(ncoord)}  (welded {nw} dup, "
          f"dropped {norph} orphan nodes)")

    # ---- layer labelling: TRUE clipped fields + fp gate + band hybrid ------
    # base rule = centroid vs TRUE fields (faithful in artificial zones);
    # band info kills interp jitter: clips below S1/S2 are always valid
    # (s1<=t1, s2<=f02, s3<=f03 by construction), and where BOTH bounding
    # fragment surfaces are exact-conformal the whole band is one layer.
    cent = ncoord[conn].mean(axis=1)
    mk = lambda Z: RegularGridInterpolator((xs, ys), Z, bounds_error=False,
                                           fill_value=None)
    t1I, f02I, f03I = mk(t1), mk(f02), mk(f03)
    nrI = lambda Z: RegularGridInterpolator((xs, ys), Z.astype(float),
                                            bounds_error=False, fill_value=0.0,
                                            method='nearest')
    fpI = nrI(m01)
    e1I, e2I, e3I = nrI(d['ex1']), nrI(d['ex2']), nrI(d['ex3'])
    q, cz = cent[:, :2], cent[:, 2]
    infp = fpI(q) > 0.5
    lay = np.full(len(cent), 4, dtype=np.int64)
    lay[cz > f03I(q)] = 3
    lay[cz > f02I(q)] = 2
    lay[(cz > t1I(q)) & infp] = 1
    njit = 0
    m = (band == 2) & (lay == 1); lay[m] = 2; njit += m.sum()
    m = (band >= 3) & (lay <= 2); lay[m] = 3; njit += m.sum()
    e1, e2, e3 = e1I(q) > 0.5, e2I(q) > 0.5, e3I(q) > 0.5
    m = (band == 1) & infp & e1 & (lay != 1); lay[m] = 1; njit += m.sum()
    m = (band == 2) & e1 & e2 & (lay != 2); lay[m] = 2; njit += m.sum()
    m = (band == 3) & e2 & e3 & (lay != 3); lay[m] = 3; njit += m.sum()
    m = (band == 4) & e3 & (lay != 4); lay[m] = 4; njit += m.sum()
    print(f"band-hybrid jitter fixes: {int(njit)} cells")
    counts = {L: int((lay == L).sum()) for L in range(1, 5)}
    print("layer counts:", counts, " total", len(lay))
    assert min(counts.values()) > 0, "empty layer!"

    # ---- quality -------------------------------------------------------------
    P = ncoord[conn]
    vol, gamma, aspect, el = tet_quality(P)
    neg = int((vol <= 0).sum())
    print(f"vol: min {vol.min():.4f}  p1 {np.percentile(vol,1):.2f}  "
          f"median {np.median(vol):.1f}  sum {vol.sum():.6e}  (neg: {neg})")
    print(f"gamma: min {gamma.min():.4f}  p1 {np.percentile(gamma,1):.3f}  "
          f"p10 {np.percentile(gamma,10):.3f}  median {np.median(gamma):.3f}")
    print(f"  gamma<0.05: {(gamma<0.05).sum()}  <0.02: {(gamma<0.02).sum()}  "
          f"<0.01: {(gamma<0.01).sum()}")
    print(f"aspect: median {np.median(aspect):.2f}  p90 {np.percentile(aspect,90):.2f}"
          f"  p99 {np.percentile(aspect,99):.2f}  max {aspect.max():.1f}")
    inb = ((cent[:, 0] >= EB[0][0]) & (cent[:, 0] <= EB[0][1]) &
           (cent[:, 1] >= EB[1][0]) & (cent[:, 1] <= EB[1][1]) &
           (cent[:, 2] >= EB[2][0]) & (cent[:, 2] <= EB[2][1]))
    elb = el[inb]
    print(f"EXPORT BOX: tets {inb.sum()}  edge median {np.median(elb):.1f}  "
          f"p95 {np.percentile(elb,95):.1f}  max {elb.max():.1f}  (spec <= ~20 m)")
    for L in range(1, 5):
        m = lay == L
        print(f"  layer{L}: n {m.sum():7d}  vol {vol[m].sum():.4e} m^3")

    # ---- write inp (orphan-free) --------------------------------------------
    with open(INP, 'w') as f:
        f.write('*Heading\n ' + INP + '\n*NODE\n')
        for i, p in enumerate(ncoord, 1):
            f.write(f'{i}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        eid = 1
        for L in range(1, 5):
            sel = np.where(lay == L)[0]
            if len(sel) == 0:
                continue
            f.write(f'*ELEMENT, type=C3D4, ELSET=layer{L}\n')
            for c in conn[sel]:
                f.write(f'{eid}, ' + ', '.join(str(int(n) + 1) for n in c) + '\n')
                eid += 1
    print('wrote', INP)


def curved_faces_top_z(gm, dim, t, cx, cy):
    """max vertical-sample z(cx,cy) over the volume's curved boundary faces
    (walls / bottom / box-top are planar -> skipped by bbox thinness)."""
    top = None
    for sdim, st in gm.model.getBoundary([(dim, t)], oriented=False):
        bb = gm.model.getBoundingBox(2, st)
        thin = min(bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2])
        if thin < 1e-6:                                 # planar wall/cap
            continue
        try:
            z = bspline_z_at(st, cx, cy, gm)
        except Exception:
            z = None
        if z is not None and (top is None or z > top):
            top = z
    return top


if __name__ == '__main__':
    main()
