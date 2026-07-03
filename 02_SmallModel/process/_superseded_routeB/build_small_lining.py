"""build_small_lining.py -- Alishan #46 SMALL model, STRUCTURED LINING SHELL.

Route B (Wade 2026-06-22): the 0.40 m tunnel lining is a STRUCTURED swept shell,
NR=3 radial layers across the 0.40 m thickness, joined to the tet rock at the
OUTER (excavation) wall by FLAC `zone attach`.  The inner clearance stays open.

Geometry (identical source to the provided tunnel_outter.stl / tunnel_inner.stl,
which were made by regen_tunnel_stl.py with an up=z swept frame):
  * OUTER loop = clean_loop(r=2.5,hw=2.5,spring=2.5,invert=-0.4) -> 5.0W x 5.4H
    horseshoe, recentred on its own centroid (so the centroid rides the CL).
  * INNER loop = shapely inward buffer 0.40 m (round joins, quad_segs=14) -> the
    real 4.2 x 4.6 clearance (matches the provided tunnel_inner.stl).
  * Both loops resampled to M uniform-arc-length points, aligned 1:1, so the
    radial direction outer[i]->inner[i] is clean; NR=3 layers linear between.
  * Swept along centerline_model.csv (deg-4 polyfit x(y),z(y)) with the SAME
    up=z section frame regen used -> the OUTER surface coincides with the rock
    excavation cut (build_small_rock.py uses the same loop + frame) -> attach.

Output: lining.inp (C3D8 hex, ELSET 'lining', positive volume) + lining_outer.stl
+ lining_inner.stl (for coincidence QC vs the provided tunnel_*.stl).

Run with C:/Users/Wade/anaconda3/python.exe (numpy + shapely).  No gmsh, no FLAC.
"""
from __future__ import annotations
import os, struct
import numpy as np
from shapely.geometry import Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
CL   = os.path.join(HERE, 'centerline_model.csv')
INP  = os.path.join(HERE, 'lining.inp')

# box y-range (lining spans the box; rock hole is also clipped to this)
Y0B, Y1B = 850.0, 950.0
LIN_T    = 0.40            # lining thickness (m)
NR       = 3              # radial cell layers across LIN_T  (Wade: 3 cells)
M        = 72             # hoop nodes (uniform arc-length) -> ~0.26 m hoop
DY_ALONG = 0.50          # along-tunnel station spacing (m)


def clean_loop(r=2.5, hw=2.5, spring=2.5, invert=-0.4, na=48, nw=6):
    """Excavation horseshoe profile, section-local (u,v), recentred on centroid
    -- identical to regen_tunnel_stl.py / build_small_tet.py."""
    th = np.linspace(0, np.pi, na)
    arch = [(r*np.cos(t), spring + r*np.sin(t)) for t in th]
    lw = [(-hw, z) for z in np.linspace(spring, invert, nw)]
    fl = [(x, invert) for x in np.linspace(-hw, hw, nw)]
    rw = [(hw, z) for z in np.linspace(invert, spring, nw)]
    loop = arch + lw[1:] + fl[1:] + rw[1:-1]
    L = np.array(loop, float)
    return L - L.mean(0)


def signed_area(P):
    return 0.5*np.sum(P[:, 0]*np.roll(P[:, 1], -1) - np.roll(P[:, 0], -1)*P[:, 1])


def resample_closed(L, m):
    """Uniform arc-length resample of a CLOSED polyline L (n,2) to m points."""
    P = np.vstack([L, L[0]])
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    total = s[-1]
    targ = np.linspace(0.0, total, m, endpoint=False)
    k = np.clip(np.searchsorted(s, targ) - 1, 0, len(seg)-1)
    f = (targ - s[k]) / np.maximum(seg[k], 1e-12)
    return P[k]*(1-f)[:, None] + P[k+1]*f[:, None]


def hex_signed_volume(P8):
    """signed volume of a hex (8,3) with faces (0123) bottom, (4567) top, via a
    6-tet decomposition."""
    tets = [(0,1,2,6),(0,2,3,6),(0,3,7,6),(0,7,4,6),(0,4,5,6),(0,5,1,6)]
    v = 0.0
    for a,b,c,d in tets:
        v += np.dot(np.cross(P8[b]-P8[a], P8[c]-P8[a]), P8[d]-P8[a]) / 6.0
    return v


def write_stl(coords, faces, fn):
    with open(os.path.join(HERE, fn), 'w') as f:
        f.write('solid t\n')
        for tri in faces:
            a, b, c = coords[tri[0]], coords[tri[1]], coords[tri[2]]
            n = np.cross(b-a, c-a); nn = np.linalg.norm(n); n = n/nn if nn > 0 else n
            f.write(f'facet normal {n[0]:.5e} {n[1]:.5e} {n[2]:.5e}\n outer loop\n')
            for vv in (a, b, c):
                f.write(f'  vertex {vv[0]:.5f} {vv[1]:.5f} {vv[2]:.5f}\n')
            f.write(' endloop\nendfacet\n')
        f.write('endsolid t\n')


def main():
    C = np.loadtxt(CL, delimiter=',', skiprows=1)
    px = np.polyfit(C[:, 1], C[:, 0], 4); pz = np.polyfit(C[:, 1], C[:, 2], 4)
    dpx = np.polyder(px); dpz = np.polyder(pz)
    # extend stations past the box; normal-swept (tilted) sections spill ~1.6 m
    # in y, so we clip the cells back to [Y0B,Y1B] after building them.
    ys = np.arange(Y0B - 2.0, Y1B + 2.0 + 1e-9, DY_ALONG)
    NS = len(ys)

    # --- section loops (local u,v) ---
    Lout = clean_loop()
    outer = resample_closed(Lout, M)
    if signed_area(outer) < 0: outer = outer[::-1].copy()   # CCW

    # inner = TRUE parallel inward offset via shapely buffer (round joins ->
    # auto-trims the sharp invert corners exactly like the provided
    # tunnel_inner.stl), resampled to M uniform-arc-length points and aligned to
    # the outer ring by the best rotational roll (min sum correspondence
    # distance).  This keeps the radial correspondence MONOTONIC (no crossing ->
    # no inverted cells) and the inner surface faithful to the real 4.2 x 4.6
    # clearance.  (Per-point normal/miter offset crosses itself near the 90 deg
    # invert corners -> inverted cells; projecting nearest-point collapses
    # adjacent nodes -> degenerate cells.  Arc-length buffer resample avoids
    # both; the radial cells are mildly skewed at the corners but valid.)
    inner_poly = Polygon(Lout).buffer(-LIN_T, join_style=1, quad_segs=14)
    inner_full = np.asarray(inner_poly.exterior.coords)[:-1]
    inner_r = resample_closed(inner_full, M)
    if signed_area(inner_r) < 0: inner_r = inner_r[::-1].copy()   # CCW
    best = None
    for sh in range(M):
        d = np.sum(np.linalg.norm(np.roll(inner_r, sh, axis=0) - outer, axis=1))
        if best is None or d < best[0]:
            best = (d, sh)
    inner = np.roll(inner_r, best[1], axis=0)

    # radial node rings (local): r=0 outer ... r=NR inner
    rings = [outer*(1 - r/NR) + inner*(r/NR) for r in range(NR+1)]
    thick = np.linalg.norm(outer - inner, axis=1)
    print(f"section: M={M}  radial layers={NR}  thickness mean {thick.mean():.3f} "
          f"min {thick.min():.3f} max {thick.max():.3f} m")
    print(f"  outer local u[{outer[:,0].min():.2f},{outer[:,0].max():.2f}] "
          f"v[{outer[:,1].min():.2f},{outer[:,1].max():.2f}]  (W x H ~ "
          f"{np.ptp(outer[:,0]):.2f} x {np.ptp(outer[:,1]):.2f})")
    print(f"  inner local u[{inner[:,0].min():.2f},{inner[:,0].max():.2f}] "
          f"v[{inner[:,1].min():.2f},{inner[:,1].max():.2f}]  (W x H ~ "
          f"{np.ptp(inner[:,0]):.2f} x {np.ptp(inner[:,1]):.2f})")

    # --- sweep with up=z frame (regen-identical) ---
    nodes = np.empty((NS, NR+1, M, 3))
    for si, y in enumerate(ys):
        cx = np.polyval(px, y); cz = np.polyval(pz, y)
        T = np.array([np.polyval(dpx, y), 1.0, np.polyval(dpz, y)]); T /= np.linalg.norm(T)
        up = np.array([0, 0, 1.0]); v = up - up.dot(T)*T; v /= np.linalg.norm(v)
        u = np.cross(v, T); u /= np.linalg.norm(u)
        Pc = np.array([cx, y, cz])
        for rad in range(NR+1):
            ring = rings[rad]
            nodes[si, rad] = Pc[None, :] + ring[:, 0:1]*u[None, :] + ring[:, 1:2]*v[None, :]

    coords = nodes.reshape(-1, 3)
    def nid(si, rad, p): return (si*(NR+1) + rad)*M + (p % M)

    hexes = []
    for si in range(NS-1):
        for rad in range(NR):
            for p in range(M):
                hexes.append([nid(si,   rad,   p), nid(si,   rad,   p+1),
                              nid(si,   rad+1, p+1), nid(si,   rad+1, p),
                              nid(si+1, rad,   p), nid(si+1, rad,   p+1),
                              nid(si+1, rad+1, p+1), nid(si+1, rad+1, p)])
    hexes = np.array(hexes, dtype=np.int64)

    # clip to the box y-range: keep only cells whose 8 nodes all lie in [Y0B,Y1B]
    # so every lining node sits in the rock domain (tilted-section spill removed).
    hy = coords[hexes][:, :, 1]
    keep = (hy >= Y0B - 1e-6).all(1) & (hy <= Y1B + 1e-6).all(1)
    hexes = hexes[keep]
    print(f"clip to box y[{Y0B},{Y1B}]: kept {len(hexes)} hexes "
          f"(of {len(keep)} swept)")

    # winding -> positive volume (lesson #3)
    vols = np.array([hex_signed_volume(coords[h]) for h in hexes])
    if np.median(vols) < 0:
        hexes = hexes[:, [4,5,6,7,0,1,2,3]]
        vols = np.array([hex_signed_volume(coords[h]) for h in hexes])
    neg = int((vols <= 0).sum())
    print(f"hexes {len(hexes)}  nodes {len(coords)}  neg-volume {neg}  "
          f"vol[min {vols.min():.4f} med {np.median(vols):.4f} max {vols.max():.4f}] "
          f"sum {vols.sum():.2f} m^3")

    # drop orphan nodes (none expected, structured) + renumber
    used = np.unique(hexes)
    remap = -np.ones(len(coords), dtype=np.int64); remap[used] = np.arange(len(used))
    coords = coords[used]; hexes = remap[hexes]

    # --- write inp (C3D8, ELSET lining) ---
    with open(INP, 'w') as f:
        f.write('*Heading\n ' + INP + '\n*NODE\n')
        for i, p in enumerate(coords, 1):
            f.write(f'{i}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        f.write('*ELEMENT, type=C3D8, ELSET=lining\n')
        for e, h in enumerate(hexes, 1):
            f.write(f'{e}, ' + ', '.join(str(int(n)+1) for n in h) + '\n')
    print('wrote', INP)

    # --- write surface STLs for coincidence QC (outer & inner walls) ---
    def wall_faces(rad):
        F = []
        for si in range(NS-1):
            for p in range(M):
                q = [remap[nid(si, rad, p)],   remap[nid(si, rad, p+1)],
                     remap[nid(si+1, rad, p+1)], remap[nid(si+1, rad, p)]]
                if any(x < 0 for x in q):      # cell clipped out of the box
                    continue
                F.append((q[0], q[1], q[2])); F.append((q[0], q[2], q[3]))
        return F
    write_stl(coords, wall_faces(0),  'lining_outer.stl')
    write_stl(coords, wall_faces(NR), 'lining_inner.stl')
    print('wrote lining_outer.stl + lining_inner.stl')
    print(f"GLOBAL bounds: x[{coords[:,0].min():.2f},{coords[:,0].max():.2f}] "
          f"y[{coords[:,1].min():.2f},{coords[:,1].max():.2f}] "
          f"z[{coords[:,2].min():.2f},{coords[:,2].max():.2f}]")


if __name__ == '__main__':
    main()
