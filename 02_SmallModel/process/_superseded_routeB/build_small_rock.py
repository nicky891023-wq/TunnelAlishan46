"""build_small_rock.py -- Alishan #46 SMALL model, ROCK tet (Route B).

The rock continuum for the near-field small model: box x[1250,1350] y[850,950]
z[1700,1800], 6 geological layers conformal to S01..S05, with the EXCAVATION
horseshoe (OUTER wall, clean_loop 2.5/2.5/2.5/-0.4 = 5.0W x 5.4H) carved out as
an empty hole.  The 0.40 m lining shell (build_small_lining.py) fills the outer
ring of that hole and is joined here later by FLAC `zone attach` at the wall;
the inner 4.2 x 4.6 clearance stays open.

Pipeline (OCC, identical to the proven build_small_tet.py):
  box  +  5 S-interface BSpline surfaces  +  excavation swept solid (addPipe)
    -> occ.cut(box, tunnel) -> holed box (empty bore)
    -> occ.fragment(holed, S-surfaces) -> 6 conformal layer bands
    -> classify layer1..6 by centroid z vs the S-surfaces
    -> Distance(cavity wall)+Threshold size field (0.45 m wall -> 4 m far)
    -> tet mesh -> self-write rock.inp (C3D4, ELSET layer1..6, orphan-free)
    -> ALSO export rock_wall.stl (cavity wall triangles) for attach-coincidence
       QC vs lining_outer.stl.

Run with C:/Users/Wade/anaconda3/python.exe (gmsh 4.15.2 + scipy).  No FLAC.
"""
from __future__ import annotations
import os, struct
import numpy as np
import gmsh
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

HERE = os.path.dirname(os.path.abspath(__file__))
CL   = os.path.join(HERE, 'centerline_model.csv')
INP  = os.path.join(HERE, 'rock.inp')
MSH  = os.path.join(HERE, 'rock.msh')
WALL_STL = os.path.join(HERE, 'rock_wall.stl')

X0, X1 = 1250.0, 1350.0
Y0, Y1 =  850.0,  950.0
ZBOT, ZTOP = 1700.0, 1800.0
EPS = 0.25
NG  = 21                          # S-surface BSpline control grid (NG x NG)

SIZE_WALL = 0.40                  # fine size at the tunnel wall (match lining hoop)
SIZE_FAR  = 4.0
DIST_MIN  = 0.0
DIST_MAX  = 35.0
MESH_MIN  = 0.35
MESH_MAX  = 4.5


def verts(p):
    d = open(p, 'rb').read(); n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d, dtype=np.uint8, count=n*50, offset=84).reshape(n, 50)
    return np.frombuffer(a[:, 12:48].tobytes(), dtype='<f4').reshape(n*3, 3).astype(float)


def sample_surfaces():
    S = {k: verts(os.path.join(HERE, k + '.stl')) for k in
         ['S01', 'S02', 'S03', 'S04', 'S05']}
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


def centerline_frame0():
    C = np.loadtxt(CL, delimiter=',', skiprows=1)
    px = np.polyfit(C[:, 1], C[:, 0], 4); pz = np.polyfit(C[:, 1], C[:, 2], 4)
    ys = np.arange(848.0, 952.01, 2.0)
    CX = np.polyval(px, ys); CZ = np.polyval(pz, ys)
    dCX = np.polyval(np.polyder(px), ys); dCZ = np.polyval(np.polyder(pz), ys)
    return ys, CX, CZ, dCX, dCZ


def main():
    xs, ys_s, surfs = sample_surfaces()
    yspine, CX, CZ, dCX, dCZ = centerline_frame0()

    gmsh.initialize()
    gmsh.option.setNumber('General.Terminal', 1)
    gmsh.model.add('small_rock')
    o = gmsh.model.occ

    box = o.addBox(X0, Y0, ZBOT, X1 - X0, Y1 - Y0, ZTOP - ZBOT)

    isurf = []
    for s in surfs:
        pts = [o.addPoint(xs[i], ys_s[j], s[i, j]) for i in range(NG) for j in range(NG)]
        isurf.append(o.addBSplineSurface(pts, NG))

    # --- excavation swept solid (OUTER wall = clean_loop), up=z start frame ----
    L = clean_loop(); M = len(L)
    spine_pts = [o.addPoint(CX[k], yspine[k], CZ[k]) for k in range(len(yspine))]
    spine = o.addBSpline(spine_pts); wire = o.addWire([spine])
    k = 0
    T = np.array([dCX[k], 1.0, dCZ[k]]); T /= np.linalg.norm(T)
    up = np.array([0, 0, 1.0]); v = up - up.dot(T)*T; v /= np.linalg.norm(v)
    u = np.cross(v, T); u /= np.linalg.norm(u)
    Pc = np.array([CX[k], yspine[k], CZ[k]])
    sp = [o.addPoint(*(Pc + L[p, 0]*u + L[p, 1]*v)) for p in range(M)]
    sl = [o.addLine(sp[p], sp[(p+1) % M]) for p in range(M)]
    sec = o.addPlaneSurface([o.addCurveLoop(sl)])
    o.synchronize()
    tun = o.addPipe([(2, sec)], wire)
    tun_vols = [(3, t) for d, t in tun if d == 3]
    o.synchronize()

    # --- carve hole, then fragment by S-surfaces -> 6 conformal layers ---------
    holed, _ = o.cut([(3, box)], tun_vols, removeObject=True, removeTool=True)
    o.synchronize()
    o.fragment(holed, [(2, t) for t in isurf])
    o.removeAllDuplicates()
    o.synchronize()

    rock_vols = gmsh.model.getEntities(3)
    print(f"after cut+fragment: rock volumes = {len(rock_vols)}")

    Sint = [LinearNDInterpolator(
        np.column_stack([np.repeat(np.linspace(X0, X1, NG), NG),
                         np.tile(np.linspace(Y0, Y1, NG), NG)]), s.ravel())
        for s in surfs]

    def layer_of(cx, cy, cz):
        zs = [float(si(cx, cy)) for si in Sint]
        if cz >= zs[0]: return 1
        if cz >= zs[1]: return 2
        if cz >= zs[2]: return 3
        if cz >= zs[3]: return 4
        if cz >= zs[4]: return 5
        return 6

    vol2lay = {}
    groups = {i: [] for i in range(1, 7)}
    for d, t in rock_vols:
        L6 = layer_of(*o.getCenterOfMass(d, t))
        vol2lay[t] = L6; groups[L6].append(t)
    for i in range(1, 7):
        print(f"  layer{i}: {len(groups[i])} fragment(s)")

    # --- cavity wall faces (Distance anchor + STL export) ----------------------
    C = np.loadtxt(CL, delimiter=',', skiprows=1)
    pcx = np.polyfit(C[:, 1], C[:, 0], 4); pcz = np.polyfit(C[:, 1], C[:, 2], 4)
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
    print(f"  cavity wall faces: {len(wall_faces)}")

    if wall_faces:
        dist = gmsh.model.mesh.field.add('Distance')
        gmsh.model.mesh.field.setNumbers(dist, 'SurfacesList', wall_faces)
        gmsh.model.mesh.field.setNumber(dist, 'Sampling', 500)
        thr = gmsh.model.mesh.field.add('Threshold')
        gmsh.model.mesh.field.setNumber(thr, 'InField', dist)
        gmsh.model.mesh.field.setNumber(thr, 'SizeMin', SIZE_WALL)
        gmsh.model.mesh.field.setNumber(thr, 'SizeMax', SIZE_FAR)
        gmsh.model.mesh.field.setNumber(thr, 'DistMin', DIST_MIN)
        gmsh.model.mesh.field.setNumber(thr, 'DistMax', DIST_MAX)
        gmsh.model.mesh.field.setAsBackgroundMesh(thr)

    gmsh.option.setNumber('Mesh.MeshSizeMin', MESH_MIN)
    gmsh.option.setNumber('Mesh.MeshSizeMax', MESH_MAX)
    gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)
    gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
    gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 0)
    gmsh.option.setNumber('Mesh.Algorithm', 6)
    gmsh.option.setNumber('Mesh.Algorithm3D', 1)
    gmsh.option.setNumber('Mesh.Optimize', 1)
    gmsh.option.setNumber('Mesh.OptimizeNetgen', 1)
    gmsh.option.setNumber('Mesh.SaveAll', 0)
    gmsh.model.mesh.generate(3)

    # --- export cavity wall triangles as STL (coincidence QC) ------------------
    ntags, ncoord, _ = gmsh.model.mesh.getNodes()
    ncoord = ncoord.reshape(-1, 3)
    nmap = {int(t): i for i, t in enumerate(ntags)}
    with open(WALL_STL, 'w') as f:
        f.write('solid wall\n')
        for t in wall_faces:
            ets, etg, enod = gmsh.model.mesh.getElements(2, t)
            for et, nodes in zip(ets, enod):
                if et != 2:
                    continue
                tri = nodes.reshape(-1, 3)
                for a, b, c in tri:
                    P = ncoord[[nmap[int(a)], nmap[int(b)], nmap[int(c)]]]
                    nrm = np.cross(P[1]-P[0], P[2]-P[0]); L2 = np.linalg.norm(nrm)
                    nrm = nrm/L2 if L2 > 0 else nrm
                    f.write(f'facet normal {nrm[0]:.5e} {nrm[1]:.5e} {nrm[2]:.5e}\n outer loop\n')
                    for vv in P:
                        f.write(f'  vertex {vv[0]:.5f} {vv[1]:.5f} {vv[2]:.5f}\n')
                    f.write(' endloop\nendfacet\n')
        f.write('endsolid wall\n')
    print(f"wrote {WALL_STL}")

    # --- self-write rock.inp (C3D4, ELSET layer1..6, orphan-free) --------------
    lay_tets = {i: [] for i in range(1, 7)}
    for d, t in rock_vols:
        ets, etg, enod = gmsh.model.mesh.getElements(3, t)
        for et, nodes in zip(ets, enod):
            if et != 4:
                continue
            conn = nodes.reshape(-1, 4)
            lay_tets[vol2lay[t]].append(conn)
    for i in range(1, 7):
        lay_tets[i] = np.vstack(lay_tets[i]) if lay_tets[i] else np.zeros((0, 4), int)
    gmsh.finalize()

    # global node renumber over USED nodes only
    used = np.unique(np.vstack([lay_tets[i] for i in range(1, 7) if len(lay_tets[i])]))
    remap = {int(t): k+1 for k, t in enumerate(used)}     # 1-based
    print(f"tets total {sum(len(lay_tets[i]) for i in range(1,7))}  "
          f"nodes used {len(used)} (of {len(ntags)})")
    with open(INP, 'w') as f:
        f.write('*Heading\n ' + INP + '\n*NODE\n')
        for t in used:
            p = ncoord[nmap[int(t)]]
            f.write(f'{remap[int(t)]}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        eid = 1
        for i in range(1, 7):
            if not len(lay_tets[i]):
                continue
            f.write(f'*ELEMENT, type=C3D4, ELSET=layer{i}\n')
            for c in lay_tets[i]:
                f.write(f'{eid}, ' + ', '.join(str(remap[int(n)]) for n in c) + '\n')
                eid += 1
        print("layer tet counts:", {i: len(lay_tets[i]) for i in range(1, 7)})
    print('wrote', INP)


if __name__ == '__main__':
    main()
