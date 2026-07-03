"""build_small_conformal.py (v2) -- Alishan #46 SMALL model, CONFORMAL (Route C).

FAST robust conformal build (the nested 2-solid fragment hung in OCC):
  box  -  INNER clearance solid (cut)  ->  holed box (inner void removed; the
                                            0.40 m lining ring stays SOLID)
       fragmented by 5 S-surfaces       ->  6 conformal geology layers
  -> ONE tet mesh, shared nodes everywhere (NO attach).
  -> POST-HOC grouping: a cell whose section-local centroid is INSIDE the OUTER
     excavation profile (and outside inner, guaranteed since inner is cut) -> 'lining';
     else -> layer1..6 by centroid z.  Lining ring resolved ~0.20 m (~2 cells).

Run with C:/Users/Wade/anaconda3/python.exe (gmsh 4.15.2 + scipy + shapely).
"""
from __future__ import annotations
import os, struct
import numpy as np
import gmsh
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from shapely.geometry import Polygon
import shapely.vectorized as sv

HERE = os.path.dirname(os.path.abspath(__file__))
CL   = os.path.join(HERE, '..', 'input', 'centerline_model.csv')
INP  = os.path.join(HERE, 'small_conformal.inp')

X0, X1 = 1250.0, 1350.0
Y0, Y1 =  850.0,  950.0
ZBOT, ZTOP = 1700.0, 1800.0
EPS = 0.25
NG  = 21
LIN_T = 0.40
SIZE_WALL = 0.20
SIZE_FAR  = 4.0
DIST_MAX  = 35.0
MESH_MIN  = 0.18
MESH_MAX  = 4.5


def verts(p):
    d = open(p, 'rb').read(); n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d, dtype=np.uint8, count=n*50, offset=84).reshape(n, 50)
    return np.frombuffer(a[:, 12:48].tobytes(), dtype='<f4').reshape(n*3, 3).astype(float)


def sample_surfaces():
    S = {k: verts(os.path.join(HERE, '..', 'input', k + '.stl')) for k in ['S01','S02','S03','S04','S05']}
    lin = {k: LinearNDInterpolator(V[:, :2], V[:, 2]) for k, V in S.items()}
    nea = {k: NearestNDInterpolator(V[:, :2], V[:, 2]) for k, V in S.items()}
    xs = np.linspace(X0, X1, NG); ys = np.linspace(Y0, Y1, NG)
    Xg, Yg = np.meshgrid(xs, ys, indexing='ij')
    def s(k):
        z = lin[k](Xg, Yg); m = np.isnan(z)
        if m.any(): z[m] = nea[k](Xg[m], Yg[m])
        return z
    Z = {k: s(k) for k in S}
    s1 = np.minimum(Z['S01'], ZTOP - EPS)
    s2 = np.minimum(Z['S02'], s1 - EPS)
    s3 = np.minimum(Z['S03'], s2 - EPS)
    s4 = np.minimum(Z['S04'], s3 - EPS)
    s5 = np.maximum(np.minimum(Z['S05'], s4 - EPS), ZBOT + EPS)
    return xs, ys, [s1, s2, s3, s4, s5]


def clean_loop(r=2.5, hw=2.5, spring=2.5, invert=-0.4, na=48, nw=6):
    th = np.linspace(0, np.pi, na)
    arch = [(r*np.cos(t), spring + r*np.sin(t)) for t in th]
    lw = [(-hw, z) for z in np.linspace(spring, invert, nw)]
    fl = [(x, invert) for x in np.linspace(-hw, hw, nw)]
    rw = [(hw, z) for z in np.linspace(invert, spring, nw)]
    loop = arch + lw[1:] + fl[1:] + rw[1:-1]
    L = np.array(loop, float); return L - L.mean(0)


def main():
    C = np.loadtxt(CL, delimiter=',', skiprows=1)
    pcx = np.polyfit(C[:, 1], C[:, 0], 4); pcz = np.polyfit(C[:, 1], C[:, 2], 4)
    dpcx = np.polyder(pcx); dpcz = np.polyder(pcz)
    yspine = np.arange(848.0, 952.01, 2.0)
    CX = np.polyval(pcx, yspine); CZ = np.polyval(pcz, yspine)
    dCX = np.polyval(dpcx, yspine); dCZ = np.polyval(dpcz, yspine)
    xs, ys_s, surfs = sample_surfaces()

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 1)
    gmsh.model.add('small_conformal')
    o = gmsh.model.occ

    box = o.addBox(X0, Y0, ZBOT, X1 - X0, Y1 - Y0, ZTOP - ZBOT)
    isurf = []
    for s in surfs:
        pts = [o.addPoint(xs[i], ys_s[j], s[i, j]) for i in range(NG) for j in range(NG)]
        isurf.append(o.addBSplineSurface(pts, NG))

    # Wade 2026-06-23: lining must strictly follow BOTH inner & outer geometry.
    # outer = the EXACT design horseshoe expressed with few edges (2 arcs + 3
    # lines) -> the swept tube has only ~5 faces, so fragmenting the box by it is
    # FAST (a 62-line polyline tube made OCC fragment hang).  inner = same profile
    # offset -0.40, kept as a SOLID for a (fast) cut -> clean clearance boundary.
    SPRING, RR, HW, INV = 2.5, 2.5, 2.5, -0.4
    arch = [[RR*np.cos(t), SPRING + RR*np.sin(t)] for t in np.linspace(0, np.pi, 60)]
    poly_pts = np.array(arch + [[-HW, INV], [HW, INV]])   # closed horseshoe (CCW)
    coff = poly_pts.mean(0)
    Lout = poly_pts - coff                                # classification polygon
    Lin = np.asarray(Polygon(Lout).buffer(-LIN_T, join_style=1, quad_segs=16).exterior.coords)[:-1]
    spine_pts = [o.addPoint(CX[k], yspine[k], CZ[k]) for k in range(len(yspine))]
    spine = o.addBSpline(spine_pts); wire = o.addWire([spine])
    k = 0
    T = np.array([dCX[k], 1.0, dCZ[k]]); T /= np.linalg.norm(T)
    up = np.array([0, 0, 1.0]); v = up - up.dot(T)*T; v /= np.linalg.norm(v)
    u = np.cross(v, T); u /= np.linalg.norm(u)
    Pc = np.array([CX[k], yspine[k], CZ[k]])

    def P3(x, z):
        q = np.array([x, z]) - coff
        return Pc + q[0]*u + q[1]*v

    # inner solid (for the cut) -- buffered profile, polyline is fine (cut is cheap)
    Mi = len(Lin)
    spi = [o.addPoint(*(Pc + Lin[p, 0]*u + Lin[p, 1]*v)) for p in range(Mi)]
    sli = [o.addLine(spi[p], spi[(p+1) % Mi]) for p in range(Mi)]
    sec_in = o.addPlaneSurface([o.addCurveLoop(sli)])
    o.synchronize()
    inner_vols = [(3, t) for d, t in o.addPipe([(2, sec_in)], wire) if d == 3]
    o.synchronize()
    # outer tube SURFACE: 2 circular arcs (arch) + 3 lines (walls + floor) -> 5 faces
    pA = o.addPoint(*P3(HW, SPRING)); pT = o.addPoint(*P3(0, SPRING + RR))
    pB = o.addPoint(*P3(-HW, SPRING)); pC = o.addPoint(*P3(-HW, INV))
    pD = o.addPoint(*P3(HW, INV)); pO = o.addPoint(*P3(0, SPRING))
    ed = [o.addCircleArc(pA, pO, pT), o.addCircleArc(pT, pO, pB),
          o.addLine(pB, pC), o.addLine(pC, pD), o.addLine(pD, pA)]
    o.synchronize()
    outer_surf = [(2, t) for d, t in o.addPipe([(1, e) for e in ed], wire) if d == 2]
    o.synchronize()
    print(f"outer tube surface faces: {len(outer_surf)}", flush=True)

    # cut inner clearance out of the box, then fragment by S-surfaces + outer skin
    holed, _ = o.cut([(3, box)], inner_vols, removeObject=True, removeTool=True)
    o.synchronize()
    o.fragment(holed, [(2, t) for t in isurf] + outer_surf)
    o.removeAllDuplicates(); o.synchronize()
    rock_vols = gmsh.model.getEntities(3)
    print(f"after cut(inner)+fragment(S+outer): volumes={len(rock_vols)}", flush=True)

    # cavity-wall faces (inner clearance boundary) -> refinement anchor
    wall_faces = []
    for d, t in gmsh.model.getEntities(2):
        cx, cy, cz = o.getCenterOfMass(2, t)
        if (abs(cx-X0) < 1e-6 or abs(cx-X1) < 1e-6 or abs(cy-Y0) < 1e-6 or
                abs(cy-Y1) < 1e-6 or abs(cz-ZBOT) < 1e-6 or abs(cz-ZTOP) < 1e-6):
            continue
        if Y0-2 <= cy <= Y1+2:
            x0 = np.polyval(pcx, cy); z0 = np.polyval(pcz, cy)
            if np.hypot(cx-x0, cz-z0) < 3.2:
                wall_faces.append(t)
    print(f"cavity wall faces: {len(wall_faces)}", flush=True)
    dist = gmsh.model.mesh.field.add('Distance')
    gmsh.model.mesh.field.setNumbers(dist, 'SurfacesList', wall_faces)
    gmsh.model.mesh.field.setNumber(dist, 'Sampling', 500)
    thr = gmsh.model.mesh.field.add('Threshold')
    gmsh.model.mesh.field.setNumber(thr, 'InField', dist)
    gmsh.model.mesh.field.setNumber(thr, 'SizeMin', SIZE_WALL)
    gmsh.model.mesh.field.setNumber(thr, 'SizeMax', SIZE_FAR)
    gmsh.model.mesh.field.setNumber(thr, 'DistMin', 0.0)
    gmsh.model.mesh.field.setNumber(thr, 'DistMax', DIST_MAX)
    gmsh.model.mesh.field.setAsBackgroundMesh(thr)

    for kk, vv in [('Mesh.MeshSizeMin', MESH_MIN), ('Mesh.MeshSizeMax', MESH_MAX),
                   ('Mesh.MeshSizeExtendFromBoundary', 0), ('Mesh.MeshSizeFromPoints', 0),
                   ('Mesh.MeshSizeFromCurvature', 0), ('Mesh.Algorithm', 6),
                   ('Mesh.Algorithm3D', 1), ('Mesh.Optimize', 1), ('Mesh.OptimizeNetgen', 1),
                   ('Mesh.SaveAll', 0)]:
        gmsh.option.setNumber(kk, vv)
    print("meshing...", flush=True)
    gmsh.model.mesh.generate(3)

    ntags, ncoord, _ = gmsh.model.mesh.getNodes()
    ncoord = ncoord.reshape(-1, 3)
    nmap = {int(t): i for i, t in enumerate(ntags)}

    # ---- classify each fragment VOLUME (NOT per-tet).  The lining/rock boundary
    # is now the conforming outer tube surface, so grouping by whole volumes makes
    # the lining strictly follow that surface; a volume centroid sits mid-region,
    # far from the boundary, so it is robust to the addPipe sweep-frame roll (a
    # per-tet centroid test would re-introduce a saw-tooth at the boundary).
    xs_g = np.linspace(X0, X1, NG); ys_g = np.linspace(Y0, Y1, NG)
    Sint = [LinearNDInterpolator(np.column_stack([np.repeat(xs_g, NG), np.tile(ys_g, NG)]), s.ravel()) for s in surfs]
    outer_poly = Polygon(Lout)
    vols = gmsh.model.getEntities(3)
    vc = np.array([o.getCenterOfMass(3, vt) for d, vt in vols])
    cy = vc[:, 1]; cx0 = np.polyval(pcx, cy); cz0 = np.polyval(pcz, cy)
    Tx = np.polyval(dpcx, cy); Tz = np.polyval(dpcz, cy)
    Tv = np.stack([Tx, np.ones_like(cy), Tz], axis=1); Tv /= np.linalg.norm(Tv, axis=1, keepdims=True)
    upv = np.array([0, 0, 1.0]); vv = upv[None, :] - (Tv @ upv)[:, None]*Tv
    vv /= np.linalg.norm(vv, axis=1, keepdims=True)
    uv = np.cross(vv, Tv); uv /= np.linalg.norm(uv, axis=1, keepdims=True)
    dP = vc - np.stack([cx0, cy, cz0], axis=1)
    lu = np.sum(dP*uv, axis=1); lv = np.sum(dP*vv, axis=1)
    is_lin_v = sv.contains(outer_poly, lu, lv)
    zsv = [Si(vc[:, 0], vc[:, 1]) for Si in Sint]
    layv = np.full(len(vols), 6, dtype=int)
    layv[vc[:, 2] >= zsv[4]] = 5
    layv[vc[:, 2] >= zsv[3]] = 4
    layv[vc[:, 2] >= zsv[2]] = 3
    layv[vc[:, 2] >= zsv[1]] = 2
    layv[vc[:, 2] >= zsv[0]] = 1

    grp_conn = {f'layer{i}': [] for i in range(1, 7)}; grp_conn['lining'] = []
    for i, (d, vt) in enumerate(vols):
        _, enod = gmsh.model.mesh.getElementsByType(4, vt)
        if len(enod) == 0:
            continue
        c = np.array([nmap[int(t)] for t in enod]).reshape(-1, 4)
        g = 'lining' if is_lin_v[i] else f'layer{int(layv[i])}'
        grp_conn[g].append(c)
    gmsh.finalize()
    groups = {g: (np.vstack(v) if v else np.zeros((0, 4), int)) for g, v in grp_conn.items()}
    conn_all = np.vstack([groups[g] for g in groups if len(groups[g])])
    print(f"raw tets {len(conn_all)} ; group counts:", {n: len(groups[n]) for n in groups}, flush=True)

    used = np.unique(conn_all)
    remap = -np.ones(len(ncoord), dtype=np.int64); remap[used] = np.arange(len(used)) + 1
    with open(INP, 'w') as f:
        f.write('*Heading\n ' + INP + '\n*NODE\n')
        for ii in used:
            p = ncoord[ii]
            f.write(f'{remap[ii]}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        eid = 1
        for name in ['layer1','layer2','layer3','layer4','layer5','layer6','lining']:
            c = groups[name]
            if len(c) == 0:
                continue
            f.write(f'*ELEMENT, type=C3D4, ELSET={name}\n')
            for row in c:
                f.write(f'{eid}, ' + ', '.join(str(int(remap[n])) for n in row) + '\n')
                eid += 1
    print('wrote', INP, flush=True)


if __name__ == '__main__':
    main()
