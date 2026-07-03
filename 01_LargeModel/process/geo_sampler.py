"""qc_geo_v2.py -- Alishan #46 LARGE model, NEW geology QC (2026-06-12).

New stratigraphy = F01.stl (colluvium base, old file) + F02_Ssh.stl +
F03_bedrock-up.stl (new delivery).  Wade's geologic logic:
  (a) colluvium (clv, layer1) = between F01 and DEM, ONLY inside F01 footprint;
  (b) outside F01 footprint: DEM directly onto rock;
  (c) rock units: [F01|DEM]~F02_Ssh (ssh, layer2), F02_Ssh~F03 (bed, layer3),
      F03~bottom z=800 (base, layer4);
  (d) rock can never sit above colluvium -> enforce F02<=F01 (where F01 exists),
      F03<=F02, every surface <=DEM; violations are CLIPPED and quantified;
  (e) F02_Ssh / F03_bedrock-up must extend beyond the model bbox in xy.

Outputs (all in this folder):
  geo_surfaces_v2.npz             clean clipped sample fields + masks + meta
  geo_qc_v2_section_x1300.png     N-S section at x=1300
  geo_qc_v2_section_y900.png      E-W section at y=900
  geo_qc_v2_section_tunnel.png    oblique section along tunnel centerline
  geo_qc_v2_f01_footprint.png     F01 footprint plan map
  geo_qc_v2_diff_old_new.png      old F02/F03 vs new surfaces diff maps+hist
"""
from __future__ import annotations
import os, struct, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

HERE = os.path.dirname(os.path.abspath(__file__))
GEO_N = os.path.join(HERE, '..', 'geometry')
X0, X1, Y0, Y1, ZB = 0.0, 2000.0, -100.0, 2000.0, 800.0

# ---------------------------------------------------------------- STL loading
def load_tris(p):
    d = open(p, 'rb').read()
    n = struct.unpack('<I', d[80:84])[0]
    arr = np.frombuffer(d, dtype=np.uint8, count=n * 50, offset=84).reshape(n, 50)
    return arr[:, 12:48].copy().view('<f4').reshape(n, 3, 3).astype(np.float64)


def cross2(ux, uy, vx, vy):
    return ux * vy - uy * vx


class Surf:
    """Heightfield sampler straight from the STL triangles (exact barycentric,
    no Delaunay re-triangulation, honours the real -- possibly non-convex --
    footprint, tolerates xy-folded/overlapping triangles: takes the TOPMOST z)."""

    CELL = 50.0

    def __init__(self, path, sheet='top'):
        # sheet='top'  -> topmost z where xy-folded (default; correct for the
        #                 single-valued heightfields DEM/F02_Ssh/F03).
        # sheet='bottom' -> lowest z.  REQUIRED for the new F01_fix01_edit.stl,
        #                 which is a WATERTIGHT CLOSED colluvium BODY (every
        #                 footprint column has exactly 2 sheets: a base face
        #                 near terrain + a lid face near z~2453).  The colluvium
        #                 BASE is the bottom face; the top sampler would return
        #                 the lid (sits up to +1096 m above DEM -> zero clv).
        assert sheet in ('top', 'bottom')
        self.sheet = sheet
        self.name = os.path.basename(path)
        tris = load_tris(path)
        V = tris.reshape(-1, 3)
        self.bbox = np.array([V.min(0), V.max(0)])
        a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
        cr = cross2(b[:, 0] - a[:, 0], b[:, 1] - a[:, 1],
                    c[:, 0] - a[:, 0], c[:, 1] - a[:, 1])
        keep = np.abs(cr) > 1e-9
        self.ntri_raw, self.ntri = len(tris), int(keep.sum())
        self.T = tris[keep]
        self.cr = cr[keep]
        self.plan_area = float(np.abs(self.cr).sum() / 2.0)  # overlaps double-counted
        # ---- uniform-grid binning of triangle bboxes ----
        self.ox, self.oy = self.bbox[0, 0], self.bbox[0, 1]
        self.ncx = int((self.bbox[1, 0] - self.ox) / self.CELL) + 1
        self.ncy = int((self.bbox[1, 1] - self.oy) / self.CELL) + 1
        i0 = np.floor((self.T[:, :, 0].min(1) - self.ox) / self.CELL).astype(int)
        i1 = np.floor((self.T[:, :, 0].max(1) - self.ox) / self.CELL).astype(int)
        j0 = np.floor((self.T[:, :, 1].min(1) - self.oy) / self.CELL).astype(int)
        j1 = np.floor((self.T[:, :, 1].max(1) - self.oy) / self.CELL).astype(int)
        bins = {}
        for k in range(len(self.T)):
            for i in range(i0[k], i1[k] + 1):
                for j in range(j0[k], j1[k] + 1):
                    bins.setdefault((i, j), []).append(k)
        self.bins = {key: np.array(v, dtype=np.int64) for key, v in bins.items()}
        # vertex xy/z views for fast candidate math
        self.ax, self.ay, self.az = self.T[:, 0, 0], self.T[:, 0, 1], self.T[:, 0, 2]
        self.bx, self.by, self.bz = self.T[:, 1, 0], self.T[:, 1, 1], self.T[:, 1, 2]
        self.cx, self.cy, self.cz = self.T[:, 2, 0], self.T[:, 2, 1], self.T[:, 2, 2]

    def _sample_one(self, px, py):
        key = (int(np.floor((px - self.ox) / self.CELL)),
               int(np.floor((py - self.oy) / self.CELL)))
        cand = self.bins.get(key)
        if cand is None:
            return np.nan
        ax, ay = self.ax[cand], self.ay[cand]
        bx, by = self.bx[cand], self.by[cand]
        cx, cy = self.cx[cand], self.cy[cand]
        d = self.cr[cand]
        w0 = cross2(bx - px, by - py, cx - px, cy - py)
        w1 = cross2(cx - px, cy - py, ax - px, ay - py)
        w2 = cross2(ax - px, ay - py, bx - px, by - py)
        tol = -1e-7 * np.abs(d)
        sgn = np.sign(d)
        hit = (w0 * sgn >= tol) & (w1 * sgn >= tol) & (w2 * sgn >= tol)
        if not hit.any():
            return np.nan
        zc = ((w0 * self.az[cand] + w1 * self.bz[cand] + w2 * self.cz[cand]) / d)[hit]
        return float(zc.min()) if self.sheet == 'bottom' else float(zc.max())

    def sample(self, X, Y):
        """returns (z, valid) -- z is NaN outside the real footprint."""
        Xf, Yf = np.asarray(X, float).ravel(), np.asarray(Y, float).ravel()
        z = np.fromiter((self._sample_one(px, py) for px, py in zip(Xf, Yf)),
                        dtype=np.float64, count=len(Xf)).reshape(np.shape(X))
        return z, ~np.isnan(z)


# ---------------------------------------------------------------- grid
def grid_axes():
    xs = np.unique(np.concatenate([np.arange(X0, X1 + 1, 50.0), [X0 + 25, X1 - 25]]))
    ys = np.unique(np.concatenate([np.arange(Y0, Y1 + 1, 50.0), [Y0 + 25, Y1 - 25]]))
    return xs, ys


def cell_weights(v):
    w = np.empty_like(v)
    w[1:-1] = (v[2:] - v[:-2]) / 2.0
    w[0] = (v[1] - v[0]) / 2.0
    w[-1] = (v[-1] - v[-2]) / 2.0
    return w


def viol_stats(name, excess, valid, A):
    """excess = surface_above - cap (positive = violation), on grid; A = cell areas"""
    bad = valid & (excess > 1e-6)
    area = float(A[bad].sum())
    vmax = float(excess[bad].max()) if bad.any() else 0.0
    vmean = float(excess[bad].mean()) if bad.any() else 0.0
    n = int(bad.sum())
    tot = int(valid.sum())
    print(f"  {name:34s} nodes {n:4d}/{tot:4d} ({100*n/max(tot,1):5.1f}%)  "
          f"area {area/1e6:7.3f} km^2  max +{vmax:7.2f} m  mean +{vmean:6.2f} m")
    return dict(name=name, n_nodes=n, n_valid=tot, area_m2=area,
                max_exceed_m=vmax, mean_exceed_m=vmean)


def main():
    print("=" * 78)
    print("LOAD + BBOX")
    S = {}
    files = {'DEM': 'DEM.stl', 'F01': 'F01.stl',
             'F02n': 'F02_Ssh.stl', 'F03n': 'F03_bedrock-up.stl',
             'F02o': 'F02.stl', 'F03o': 'F03.stl'}
    for k, fn in files.items():
        # F01_fix01_edit.stl is a closed colluvium BODY -> sample its bottom
        # face (the clv base).  All others are single-valued heightfields.
        S[k] = Surf(os.path.join(HERE, fn), sheet='bottom' if k == 'F01' else 'top')
        b = S[k].bbox
        print(f"  {fn:20s} tri {S[k].ntri_raw}->{S[k].ntri}  "
              f"x[{b[0,0]:8.2f},{b[1,0]:8.2f}] y[{b[0,1]:8.2f},{b[1,1]:8.2f}] "
              f"z[{b[0,2]:8.2f},{b[1,2]:8.2f}]  planA {S[k].plan_area/1e6:.3f} km^2")

    # ---------------- (e) boundary coverage of the two NEW rock surfaces ----
    print("-" * 78)
    print("(e) BBOX margin beyond domain x[0,2000] y[-100,2000]  (negative = short)")
    for k in ['F02n', 'F03n']:
        b = S[k].bbox
        mW, mE = X0 - b[0, 0], b[1, 0] - X1
        mS, mN = Y0 - b[0, 1], b[1, 1] - Y1
        ok = all(m > 0 for m in (mW, mE, mS, mN))
        print(f"  {S[k].name:20s} W {mW:+8.2f}  E {mE:+8.2f}  S {mS:+8.2f}  N {mN:+8.2f}"
              f"   -> {'COVERS bbox' if ok else 'SHORT (report!)'}")

    # ---------------- sampling grid ----------------------------------------
    xs, ys = grid_axes()
    Xg, Yg = np.meshgrid(xs, ys, indexing='ij')
    A = np.outer(cell_weights(xs), cell_weights(ys))
    dom_area = A.sum()
    print("-" * 78)
    print(f"GRID {len(xs)}x{len(ys)} = {Xg.size} nodes (50 m + 25 m boundary band), "
          f"cell-area sum {dom_area/1e6:.3f} km^2 (domain 4.410 km^2)")

    smp = {k: S[k].sample(Xg, Yg) for k in S}
    dem, vdem = smp['DEM']
    f01, v01 = smp['F01']
    f02n, v02 = smp['F02n']
    f03n, v03 = smp['F03n']
    f02o, v02o = smp['F02o']
    f03o, v03o = smp['F03o']
    print(f"  DEM valid {vdem.sum()}/{vdem.size}  (holes = {int((~vdem).sum())})")
    for nm, v in [('F02_Ssh', v02), ('F03_bedrock-up', v03)]:
        holes = int((~v).sum())
        print(f"  {nm:15s} in-domain coverage {v.sum()}/{v.size} nodes "
              f"({100*v.sum()/v.size:.2f}%)  uncovered area {A[~v].sum()/1e6:.4f} km^2"
              + ("" if holes == 0 else "  <-- GAPS, do NOT extrapolate, report"))

    # ---------------- (a) F01 footprint locality ----------------------------
    print("-" * 78)
    fp_area = A[v01].sum()
    b = S['F01'].bbox
    print(f"(a) F01 footprint: grid area {fp_area/1e6:.3f} km^2 "
          f"(STL plan area {S['F01'].plan_area/1e6:.3f} km^2) = "
          f"{100*fp_area/dom_area:.1f}% of domain")
    print(f"    extent x[{b[0,0]:.1f},{b[1,0]:.1f}] y[{b[0,1]:.1f},{b[1,1]:.1f}]")
    print(f"    distance to domain edges: W {b[0,0]-X0:.1f}  E {X1-b[1,0]:.1f}  "
          f"S {b[0,1]-Y0:.1f}  N {Y1-b[1,1]:.1f}  m")
    edge_touch = []
    if b[0, 0] - X0 < 25: edge_touch.append('WEST')
    if X1 - b[1, 0] < 25: edge_touch.append('EAST')
    if b[0, 1] - Y0 < 25: edge_touch.append('SOUTH')
    if Y1 - b[1, 1] < 25: edge_touch.append('NORTH')
    print(f"    touches domain boundary: {edge_touch if edge_touch else 'NONE (fully local)'}")

    # ---------------- violations (raw, before clip) -------------------------
    print("-" * 78)
    print("VIOLATION SCAN (raw surfaces, before clip)")
    stats = []
    stats.append(viol_stats('F01 > DEM (clv base above terrain)', f01 - dem, v01 & vdem, A))
    stats.append(viol_stats('F02_Ssh > DEM', f02n - dem, v02 & vdem, A))
    stats.append(viol_stats('F03_bedrock-up > DEM', f03n - dem, v03 & vdem, A))
    f01c = np.where(v01, np.minimum(f01, dem), np.nan)
    stats.append(viol_stats('F02_Ssh > F01 (rock above clv) [in F01 fp]',
                            f02n - f01c, v02 & v01, A))
    stats.append(viol_stats('F03 > F02_Ssh (interpenetration)', f03n - f02n, v03 & v02, A))
    stats.append(viol_stats('F02_Ssh below model base z=800', ZB - f02n, v02, A))
    stats.append(viol_stats('F03_bedrock-up below model base z=800', ZB - f03n, v03, A))

    # ---------------- clip (rule d) -----------------------------------------
    top_rock = np.where(v01, f01c, dem)        # top of layer2 (ssh)
    f02c = np.minimum(f02n, top_rock)
    f03c = np.minimum(f03n, f02c)
    thk_clv = np.where(v01, dem - f01c, 0.0)
    thk_ssh = top_rock - f02c
    thk_bed = f02c - f03c
    thk_bas = f03c - ZB
    print("-" * 78)
    print("CLIPPED layer thickness on grid (m)  [layer1=clv only in F01 fp]")
    for nm, t, m in [('clv (DEM-F01)', thk_clv, v01),
                     ('ssh (top_rock-F02c)', thk_ssh, v02),
                     ('bed (F02c-F03c)', thk_bed, v02 & v03),
                     ('base (F03c-800)', thk_bas, v03)]:
        tt = t[m]
        print(f"  {nm:22s} mean {np.nanmean(tt):7.2f}  min {np.nanmin(tt):8.2f}  "
              f"max {np.nanmax(tt):7.2f}  p5 {np.nanpercentile(tt,5):7.2f}")

    # ---------------- old vs new diff ---------------------------------------
    print("-" * 78)
    print("OLD vs NEW surface diff (new - old), on common valid nodes")
    diffs = {}
    for nm, new, vn, old, vo in [('F02_Ssh - F02_old', f02n, v02, f02o, v02o),
                                 ('F03_bedrock-up - F03_old', f03n, v03, f03o, v03o)]:
        m = vn & vo
        d = (new - old)[m]
        diffs[nm] = dict(n=int(m.sum()), mean=float(d.mean()),
                         mean_abs=float(np.abs(d).mean()), rms=float(np.sqrt((d**2).mean())),
                         dmin=float(d.min()), dmax=float(d.max()),
                         p5=float(np.percentile(d, 5)), p95=float(np.percentile(d, 95)),
                         overlap_area_m2=float(A[m].sum()))
        s = diffs[nm]
        print(f"  {nm:26s} n={s['n']:4d}  mean {s['mean']:+7.2f}  |mean| {s['mean_abs']:6.2f}  "
              f"rms {s['rms']:6.2f}  min {s['dmin']:+8.2f}  max {s['dmax']:+8.2f}  "
              f"p5/p95 {s['p5']:+7.2f}/{s['p95']:+7.2f}")

    # ---------------- F01 footprint polygon (convex hull, reference only) ---
    from scipy.spatial import ConvexHull
    xy01 = np.unique(np.round(S['F01'].T.reshape(-1, 3)[:, :2], 2), axis=0)
    h = ConvexHull(xy01)
    poly_f01 = xy01[h.vertices]

    # ---------------- save npz ----------------------------------------------
    meta = dict(date='2026-06-12', domain=[X0, X1, Y0, Y1, ZB],
                grid='50 m + 25 m boundary band, indexing ij (x first)',
                layers='layer1=clv DEM~F01 (only mask_f01) / layer2=ssh top_rock~f02 / '
                       'layer3=bed f02~f03 / layer4=base f03~800',
                clip_rule='f01=min(F01,DEM); top_rock=f01 in fp else DEM; '
                          'f02=min(F02_Ssh,top_rock); f03=min(F03_bu,f02); '
                          'NO base-clamp, NO eps gaps (mesh builder applies its own EPS)',
                source=['DEM.stl', 'F01.stl', 'F02_Ssh.stl', 'F03_bedrock-up.stl'],
                raw_fields='*_raw are unclipped samples (NaN outside data); '
                           'f02_old_raw/f03_old_raw = old F02.stl/F03.stl for diff')
    out = os.path.join(HERE, 'geo_surfaces_v2.npz')
    np.savez(out, xs=xs, ys=ys, cell_area=A,
             dem=dem,
             f01_raw=f01, f02_raw=f02n, f03_raw=f03n,
             f01=np.where(v01, f01c, np.nan), f02=f02c, f03=f03c,
             top_rock=top_rock,
             mask_f01=v01, mask_f02=v02, mask_f03=v03,
             f02_old_raw=f02o, f03_old_raw=f03o,
             mask_f02_old=v02o, mask_f03_old=v03o,
             poly_f01=poly_f01, zb=np.array(ZB),
             meta=np.array(json.dumps(meta)))
    print(f"wrote {out}")

    # ================= PLOTS ================================================
    CLV, SSH, BED, BAS = '#d2b48c', '#9aa55a', '#8c8c9e', '#5a5a6e'
    cl = np.loadtxt(os.path.join(GEO_N, 'centerline_model.csv'),
                    delimiter=',', skiprows=1)

    def section(P, lab_axis, title, png, tun_proj):
        """P = (n,2) xy points along the section; lab_axis = horizontal coord."""
        zD, mD = S['DEM'].sample(P[:, 0], P[:, 1])
        z1, m1 = S['F01'].sample(P[:, 0], P[:, 1])
        z2, m2 = S['F02n'].sample(P[:, 0], P[:, 1])
        z3, m3 = S['F03n'].sample(P[:, 0], P[:, 1])
        z2o, m2o = S['F02o'].sample(P[:, 0], P[:, 1])
        z3o, m3o = S['F03o'].sample(P[:, 0], P[:, 1])
        z1c = np.where(m1, np.minimum(z1, zD), np.nan)
        tr = np.where(m1, z1c, zD)
        z2c = np.minimum(z2, tr)
        z3c = np.minimum(z3, z2c)
        t = lab_axis
        fig, ax = plt.subplots(figsize=(13, 5.5))
        ax.fill_between(t, np.fmin(z1c, zD), zD, where=m1, color=CLV, label='layer1 clv (F01~DEM)')
        ax.fill_between(t, z2c, tr, color=SSH, label='layer2 ssh')
        ax.fill_between(t, z3c, z2c, color=BED, label='layer3 bed')
        ax.fill_between(t, np.full_like(t, ZB), np.maximum(z3c, ZB), color=BAS, label='layer4 base')
        ax.plot(t, zD, 'k-', lw=1.4, label='DEM')
        ax.plot(t, np.where(m1, z1, np.nan), '-', color='#7a4a12', lw=1.2, label='F01 raw')
        ax.plot(t, z2, '--', color='#3b4a00', lw=1.0, label='F02_Ssh raw')
        ax.plot(t, z3, '--', color='#26263a', lw=1.0, label='F03_bedrock-up raw')
        ax.plot(t, np.where(m2o, z2o, np.nan), ':', color='#3b4a00', lw=1.0, label='F02 old')
        ax.plot(t, np.where(m3o, z3o, np.nan), ':', color='#26263a', lw=1.0, label='F03 old')
        if tun_proj is not None:
            ax.plot(tun_proj[0], tun_proj[1], 'r-', lw=3, label='tunnel CL (proj)')
        ax.axhline(ZB, color='k', lw=0.6)
        ax.set_title(title)
        ax.set_ylabel('z (m)')
        ax.set_ylim(780, 2300)
        ax.legend(loc='lower right', fontsize=7.5, ncol=2)
        ax.grid(alpha=0.25)
        fig.tight_layout()
        fig.savefig(os.path.join(HERE, png), dpi=160)
        plt.close(fig)
        print(f"  wrote {png}")

    # x = 1300 (N-S)
    yy = np.arange(Y0, Y1 + 1, 5.0)
    P = np.column_stack([np.full_like(yy, 1300.0), yy])
    section(P, yy, 'Section x=1300 (N-S)  new geology v2, clipped fill + raw lines',
            'geo_qc_v2_section_x1300.png', (cl[:, 1], cl[:, 2]))
    # y = 900 (E-W)
    xx = np.arange(X0, X1 + 1, 5.0)
    P = np.column_stack([xx, np.full_like(xx, 900.0)])
    section(P, xx, 'Section y=900 (E-W)  new geology v2',
            'geo_qc_v2_section_y900.png', (cl[:, 0], cl[:, 2]))
    # oblique along tunnel
    c0 = cl[:, :2].mean(0)
    dvec = cl[-1, :2] - cl[0, :2]
    dvec = dvec / np.linalg.norm(dvec)
    ss = np.arange(-1100, 1101, 5.0)
    P = c0[None, :] + ss[:, None] * dvec[None, :]
    inside = (P[:, 0] >= X0) & (P[:, 0] <= X1) & (P[:, 1] >= Y0) & (P[:, 1] <= Y1)
    P, ssn = P[inside], ss[inside]
    s_cl = (cl[:, :2] - c0) @ dvec
    section(P, ssn,
            f'Oblique section along tunnel CL  dir=({dvec[0]:+.3f},{dvec[1]:+.3f}) '
            f'through ({c0[0]:.0f},{c0[1]:.0f}); s=0 at CL centroid',
            'geo_qc_v2_section_tunnel.png', (s_cl, cl[:, 2]))

    # footprint plan map
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.pcolormesh(xs, ys, np.where(v01, 1.0, np.nan).T, cmap='Oranges',
                  vmin=0, vmax=1.6, shading='nearest')
    ax.plot(np.append(poly_f01[:, 0], poly_f01[0, 0]),
            np.append(poly_f01[:, 1], poly_f01[0, 1]), 'r-', lw=1.5,
            label='F01 convex hull')
    ax.add_collection(PolyCollection(S['F01'].T[:, :, :2], facecolor='none',
                                     edgecolor='#7a4a12', lw=0.15, alpha=0.5))
    ax.plot([X0, X1, X1, X0, X0], [Y0, Y0, Y1, Y1, Y0], 'k-', lw=2, label='domain')
    ax.plot(cl[:, 0], cl[:, 1], 'b-', lw=2.5, label='tunnel CL')
    ax.plot([1300, 1300], [Y0, Y1], 'g--', lw=1, label='sec x=1300')
    ax.plot([X0, X1], [900, 900], 'm--', lw=1, label='sec y=900')
    Pl = c0[None, :] + np.array([-1100, 1100])[:, None] * dvec[None, :]
    ax.plot(Pl[:, 0], Pl[:, 1], 'c--', lw=1, label='sec tunnel-oblique')
    ax.set_title(f'F01 (colluvium base) footprint  area={fp_area/1e6:.2f} km^2 '
                 f'({100*fp_area/dom_area:.0f}% of domain)\n'
                 f'x[{b[0,0]:.0f},{b[1,0]:.0f}] y[{b[0,1]:.0f},{b[1,1]:.0f}]  '
                 f'edge-touch: {edge_touch if edge_touch else "none"}')
    ax.set_aspect('equal')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'geo_qc_v2_f01_footprint.png'), dpi=160)
    plt.close(fig)
    print("  wrote geo_qc_v2_f01_footprint.png")

    # old vs new diff figure
    fig, axs = plt.subplots(2, 2, figsize=(13, 10))
    for row, (nm, new, vn, old, vo) in enumerate(
            [('F02_Ssh - F02_old', f02n, v02, f02o, v02o),
             ('F03_bedrock-up - F03_old', f03n, v03, f03o, v03o)]):
        m = vn & vo
        D = np.where(m, new - old, np.nan)
        vmax = np.nanpercentile(np.abs(D), 99)
        pc = axs[row, 0].pcolormesh(xs, ys, D.T, cmap='RdBu_r', vmin=-vmax, vmax=vmax,
                                    shading='nearest')
        axs[row, 0].plot(cl[:, 0], cl[:, 1], 'k-', lw=1.5)
        axs[row, 0].set_aspect('equal')
        s = diffs[nm]
        axs[row, 0].set_title(f'{nm} (m)  mean {s["mean"]:+.1f}  rms {s["rms"]:.1f}')
        fig.colorbar(pc, ax=axs[row, 0], shrink=0.85)
        d = (new - old)[m]
        axs[row, 1].hist(d, bins=60, color='#666699', edgecolor='k', lw=0.3)
        axs[row, 1].axvline(0, color='k', lw=1)
        axs[row, 1].set_title(f'{nm}  min {s["dmin"]:+.1f} / max {s["dmax"]:+.1f} / '
                              f'p5 {s["p5"]:+.1f} / p95 {s["p95"]:+.1f}')
        axs[row, 1].set_xlabel('dz (m)')
        axs[row, 1].grid(alpha=0.3)
    fig.suptitle('NEW (F02_Ssh / F03_bedrock-up) minus OLD (F02 / F03), common coverage',
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, 'geo_qc_v2_diff_old_new.png'), dpi=160)
    plt.close(fig)
    print("  wrote geo_qc_v2_diff_old_new.png")
    print("=" * 78)


if __name__ == '__main__':
    main()
