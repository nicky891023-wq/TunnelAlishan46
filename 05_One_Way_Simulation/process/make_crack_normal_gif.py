#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_crack_normal_gif.py -- 3D orbiting GIF of coupled-lining cracks classified by
CROSS-SECTION (XZ) CONNECTIVITY, per Wade's correction.

WHY this method (the earlier 3D-PCA method was WRONG):
The springline damage is a thin sheet that runs the WHOLE tunnel length along y, so its
global principal axis points along y -> a 3D PCA mislabels the entire sheet "longitudinal".
But in any single cross-section (e.g. coupled_xsection_and_cracks.png @ y=885) the breaks
form an ARC running DOWN THE LEG, i.e. a CIRCUMFERENTIAL crack lying in the XZ plane. The
sheet is a STACK of such arcs, one per chainage -- circumferential, not longitudinal.

Detection (cross-section-first, matching how tunnel cracks are logged per ring/chainage):
  1. CIRCUMFERENTIAL (priority): slice into 1 m XZ slabs along y; inside each slab cluster
     breaks in the (x,z) plane; a connected arc (path length >= LMIN_CIRC, ordered along the
     hoop angle) is a circumferential crack. Claim its breaks.  -> should DOMINATE.
  2. LONGITUDINAL: from the LEFTOVER breaks only, within thin theta columns, connect runs
     along y (length >= LMIN_LONG).  -> should be ALMOST NONE.
  3. OBLIQUE: remaining leftover connected clusters (diagonal on the developed surface).

CRACK != BOND BREAK: micro-breaks are connected into CONTINUOUS lines; each centerline point
carries a BIRTH AGE (monotonic accumulation, never erased). Stage-1 baseline (age<=AGE1) is
excluded, so cracks are water-cycle-induced (prominent at wet s6). Each 360 orbit = one stage.
Colours: circumferential=red, oblique=blue, longitudinal=green.

Inputs: ring3d_G4.txt, cs_s1..11_cracks.txt (x y z type diam age).
Out: ../result/FIG_D_crack_normal_evolution_3D.gif
Usage: python make_crack_normal_gif.py [--test]
"""
import sys
from pathlib import Path
import numpy as np
import pyvista as pv
from sklearn.cluster import DBSCAN
from scipy.spatial import cKDTree
from PIL import Image
import tunnel_frame as tf

pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT  = HERE.parent / "result" / "FIG_D_crack_normal_evolution_3D.gif"
CX, CY, CZ = 1298.85, 885.0, 1747.5     # corrected ring centre (07-10)
WATER = ["W-110","W-90","W-70","W-50","W-30","W-10","W-30","W-50","W-70","W-90","W-110"]
PHASE = ["dry1","rise","rise","rise","rise","wet","fall","fall","fall","fall","dry2"]
# stage-1 baseline cutoff = max age in the CURRENT v6 s1 dump (not hardcoded: the rerun
# changed the s1 cycle span)
AGE1 = float(np.loadtxt(HERE / "cs_s1_cracks.txt", skiprows=1, ndmin=2)[:, 5].max())

YMIN, YMAX = 860.0, 910.0
YSTEP  = 1.0            # XZ cross-section slab thickness (Wade: connect every 1 m)
EPS_RING = 0.35        # DBSCAN neighbourhood in the (x,z) cross-section plane (m)
MIN_RING = 4
LMIN_CIRC = 0.8        # min circumferential arc length (m)
# ---- oblique / longitudinal via smoothed orientation field on the developed surface ----
KORI   = 30            # KNN for the local structure tensor
COH_MIN = 0.28         # min smoothed orientation coherence -> a directional (non-isotropic) break
EPS_DIR = 0.60; MIN_DIR = 6   # cluster the directional breaks into candidate lines
BETA_LO, BETA_HI = 25.0, 65.0 # cluster PCA angle from hoop: [LO,HI]->oblique, >HI->longitudinal
LMIN_OBL = 1.0                # min oblique line length (m)
LMIN_LONG = 3.0               # min longitudinal length (m); strict so longitudinal ~ none
BIN_L = 0.3            # centerline resampling (m)
DENS_N = 5            # >=DENS_N breaks within DENS_R -> centerline point born
DENS_R = 0.35
TUBE_R = 0.10          # thinner tubes (Wade: 裂縫細一些)
NFRAMES  = 72          # frames per stage; 360 orbit = one stage
FRAME_MS = 70          # ms/frame -> 72*0.070 = 5.0 s per rotation
RADIUS, ELEV, ZOOM = 52.0, 24.0, 1.42   # measured: side-on ring width 64.5% at 1.05 -> ~92%
WIN = (1280, 800)      # wide letterbox: the low flat ring fills the frame, less blank sky
FONT = "times"         # standard spec (Wade 07-12): TNR English, large fonts
TEST = "--test" in sys.argv
MONTAGE = "--montage" in sys.argv

# crack TYPE: 0 circumferential(red) / 1 oblique(blue) / 2 longitudinal(green)
COL  = {0: "#e00000", 1: "#1f6fe0", 2: "#2ca02c"}
OPAC = {0: 1.00, 1: 0.95, 2: 1.00}
TRAD = {0: TUBE_R, 1: TUBE_R, 2: TUBE_R}
TNAME = {0: "circumf", 1: "oblique", 2: "longit"}

ring = np.loadtxt(HERE / "ring3d_G4.txt", skiprows=1, ndmin=2)[::5]

# ---- water-cycle-induced break cloud (positions + age) ----
cs = np.loadtxt(HERE / "cs_s11_cracks.txt", skiprows=1, ndmin=2)
w  = cs[:, 5] > AGE1
P   = cs[w, :3]
AGE = cs[w, 5]
X, Y, Z = P[:, 0], P[:, 1], P[:, 2]
# hoop angle/radius about the LOCAL ring centre (plan curve cx(y) + 3.74% grade z0(y))
RX, RZ = X - tf.cx_of(Y), Z - tf.z0_of(Y)
THETA = np.degrees(np.arctan2(RX, RZ))                  # hoop angle from crown (deg)
R     = np.sqrt(RX**2 + RZ**2)
AGE_END = {k: float(np.loadtxt(HERE / f"cs_s{k}_cracks.txt", skiprows=1, ndmin=2)[:, 5].max())
           for k in range(1, 12)}

tree = cKDTree(P)

def birth_age(pt):
    idx = tree.query_ball_point(pt, DENS_R)
    if len(idx) < DENS_N:
        return np.inf
    return float(np.sort(AGE[idx])[DENS_N - 1])

def build_centerline(sub, keyvals, length):
    """resample the break subset into a SMOOTH ordered centerline along keyvals.
    nb is set from the (clean, geometric) length and clipped so bins average enough
    breaks to suppress radial jitter -- avoids a zigzag path through the break blob."""
    order = np.argsort(keyvals)
    s = sub[order]; kv = keyvals[order]
    p = np.column_stack([X[s], Y[s], Z[s]])
    nb = int(np.clip(round(length / BIN_L), 2, 40))
    edges = np.linspace(kv[0], kv[-1], nb + 1)
    cpts = []
    for i in range(nb):
        m = (kv >= edges[i]) & (kv <= edges[i + 1])
        if m.any():
            cpts.append(p[m].mean(0))
    if len(cpts) < 2:
        return None
    return np.array(cpts)

def add_crack(cracks, sub, keyvals, length, typ):
    cl = build_centerline(sub, keyvals, length)
    if cl is None:
        return False
    cage = np.array([birth_age(p) for p in cl])
    cracks.append((cl, cage, typ))
    return True

def coherence_field():
    """Smoothed local-orientation coherence on the developed (hoop-arc U, axial y) surface.
    Local structure tensor (KNN) -> principal axis; its anisotropy-weighted double-angle
    vector is averaged over the neighbourhood. Dense isotropic damage -> low coherence;
    only genuinely coherent streaks keep a direction. Returns (coh, U)."""
    U = np.radians(THETA) * R
    D = np.column_stack([U, Y])
    _, idx = cKDTree(D).query(D, k=KORI + 1)
    nb = D[idx[:, 1:]]; q = nb - nb.mean(1, keepdims=True)
    cxx = (q[:, :, 0]**2).mean(1); cyy = (q[:, :, 1]**2).mean(1); cxy = (q[:, :, 0]*q[:, :, 1]).mean(1)
    tr = cxx + cyy; det = cxx*cyy - cxy**2; disc = np.sqrt(np.maximum((tr/2)**2 - det, 0))
    aniso = (disc * 2) / (tr + 1e-12)
    ap = 0.5 * np.arctan2(2*cxy, cxx - cyy)
    c2 = (aniso*np.cos(2*ap))[idx[:, 1:]].mean(1)
    s2 = (aniso*np.sin(2*ap))[idx[:, 1:]].mean(1)
    return np.sqrt(c2**2 + s2**2), U

def build_cracks():
    coh, U = coherence_field()
    D = np.column_stack([U, Y])
    used = np.zeros(len(P), bool)
    cracks = []
    # 1. OBLIQUE (blue) / LONGITUDINAL (green): cluster the DIRECTIONAL breaks, then classify
    #    each cluster by its OWN shape (developed-surface PCA angle from hoop). Circ-shaped
    #    clusters are NOT claimed -> they fall through to the per-slab arcs below.
    sel = np.where(coh >= COH_MIN)[0]
    if len(sel) >= MIN_DIR:
        lab = DBSCAN(eps=EPS_DIR, min_samples=MIN_DIR).fit_predict(D[sel])
        for L in set(lab) - {-1}:
            sub = sel[lab == L]
            d = D[sub]; axis = np.linalg.svd(d - d.mean(0), full_matrices=False)[2][0]
            proj = (d - d.mean(0)) @ axis
            length = proj.max() - proj.min()
            beta = abs(np.degrees(np.arctan2(abs(axis[1]), abs(axis[0]))))   # 0=hoop, 90=axial
            if beta < BETA_LO:                       # circumferential-shaped -> leave for arcs
                continue
            typ = 1 if beta <= BETA_HI else 2
            lmin = LMIN_OBL if typ == 1 else LMIN_LONG
            if length < lmin:
                continue
            if add_crack(cracks, sub, proj, length, typ):
                used[sub] = True
    # 2. CIRCUMFERENTIAL (red): per-1 m XZ slab arcs on everything else (the dominant bulk)
    for y0 in np.arange(YMIN, YMAX, YSTEP):
        idx = np.where((~used) & (Y >= y0) & (Y < y0 + YSTEP))[0]
        if len(idx) < MIN_RING:
            continue
        lab = DBSCAN(eps=EPS_RING, min_samples=MIN_RING).fit_predict(
            np.column_stack([X[idx], Z[idx]]))
        for L in set(lab) - {-1}:
            sub = idx[lab == L]
            length = np.radians(THETA[sub].max() - THETA[sub].min()) * R[sub].mean()
            if length < LMIN_CIRC:
                continue
            if add_crack(cracks, sub, THETA[sub], length, 0):
                used[sub] = True
    return cracks

CRACKS = build_cracks()

def tubes_at(age_max):
    """born sub-segments (birth age <= age_max) grouped by type -> tube per type + length."""
    buckets = {0: [], 1: [], 2: []}; tot = {0: 0.0, 1: 0.0, 2: 0.0}
    for cpts, cage, typ in CRACKS:
        born = cage <= age_max
        i, n = 0, len(born)
        while i < n:
            if not born[i]:
                i += 1; continue
            j = i
            while j + 1 < n and born[j + 1]:
                j += 1
            if j - i + 1 >= 2:
                seg = cpts[i:j + 1]
                tot[typ] += np.linalg.norm(np.diff(seg, axis=0), axis=1).sum()
                buckets[typ].append(seg)
            i = j + 1
    tubes = {}
    for t, segs in buckets.items():
        if not segs:
            tubes[t] = None; continue
        pts, cells, off = [], [], 0
        for seg in segs:
            pts.append(seg); cells.append(np.hstack([[len(seg)], np.arange(off, off + len(seg))])); off += len(seg)
        poly = pv.PolyData(np.vstack(pts)); poly.lines = np.hstack(cells)
        tubes[t] = poly.tube(radius=TRAD[t])
    return tubes, tot

TUBES = {k: tubes_at(AGE_END[k]) for k in range(1, 12)}

def cam_position(az):
    a = np.radians(az)
    return (CX + RADIUS*np.cos(a), CY + RADIUS*np.sin(a), CZ + ELEV)

def render_stage(pl, k, az, annotate=True):
    pl.clear(); pl.set_background("white")
    pl.add_points(ring, color="#c4c4c4", point_size=2.0, opacity=0.24,
                  render_points_as_spheres=False)
    tubes, tot = TUBES[k]
    for t in (2, 1, 0):                     # longit (back) -> oblique -> circ (front)
        tb = tubes[t]
        if tb is not None:
            pl.add_mesh(tb, color=COL[t], opacity=OPAC[t], smooth_shading=True,
                        show_scalar_bar=False)
    pl.camera.focal_point = (CX, CY, CZ); pl.camera.up = (0, 0, 1)
    pl.camera.position = cam_position(az); pl.reset_camera(); pl.camera.zoom(ZOOM)
    if annotate:
        total = sum(tot.values())
        pl.add_text(f"Stage {k}   {WATER[k-1]} ({PHASE[k-1]})",
                    position="upper_left", font_size=22, color="#1a2433", font=FONT)
        tag = ("baseline - water cycle not started" if total < 0.5 else
               f"circumferential {tot[0]:.0f} m    oblique {tot[1]:.0f} m    "
               f"longitudinal {tot[2]:.0f} m")
        pl.add_text(tag, position=(18, WIN[1] - 116), font_size=15,
                    color="#3a4656", font=FONT)
        for i, (t, lab) in enumerate(((0, "circumferential (XZ-section arcs)"),
                                      (1, "oblique (directional streaks)"),
                                      (2, "longitudinal"))):
            pl.add_text(lab, position=(18, 88 - 32 * i), font_size=15,
                        color=COL[t], font=FONT)
    return pl.screenshot(return_img=True)

if TEST:
    n = {0: 0, 1: 0, 2: 0}
    for _, _, t in CRACKS:
        n[t] += 1
    print("cracks:", len(CRACKS),
          f"  circ={n[0]} oblique={n[1]} longit={n[2]}")
    for k in (1, 4, 6, 11):
        t = TUBES[k][1]
        print(f"  s{k}: circ={t[0]:.0f}m oblique={t[1]:.0f}m longit={t[2]:.0f}m")
    pl = pv.Plotter(off_screen=True, window_size=(760, 780))
    imgs = [render_stage(pl, k, 35) for k in (1, 4, 6, 11)]
    pl.close()
    Image.fromarray(np.concatenate(imgs, axis=1)).save(HERE / "_FIG_D_normal_preview.png")
    sys.exit(0)

if MONTAGE:
    # thesis 圖5-20: static 2x2 stage montage (clean frames + TNR typography)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import thesis_style as TS
    TS.apply()
    KS = (1, 4, 6, 11)
    pl = pv.Plotter(off_screen=True, window_size=(1400, 1000))
    frames = {k: render_stage(pl, k, 35, annotate=False) for k in KS}
    pl.close()
    fig, axs = plt.subplots(2, 2, figsize=(22, 15.5))
    for ax, k in zip(axs.ravel(), KS):
        img = frames[k]
        g = img.mean(axis=2)
        rows = np.where((g < 250).any(1))[0]; cols = np.where((g < 250).any(0))[0]
        ax.imshow(img[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1])
        ax.axis("off")
        lab = {1: "(a) s1  W-110 (initial dry) - baseline",
               4: "(b) s4  W-50 (rising)",
               6: "(c) s6  W-10 (wet peak)",
               11: "(d) s11  W-110 (final dry) - frozen"}[k]
        ax.set_title(lab, loc="left", fontsize=24)
    fig.legend(handles=[plt.Line2D([0], [0], color=COL[0], lw=5, label="circumferential"),
                        plt.Line2D([0], [0], color=COL[1], lw=5, label="oblique"),
                        plt.Line2D([0], [0], color=COL[2], lw=5, label="longitudinal")],
               loc="lower center", ncol=3, fontsize=22, frameon=False)
    fig.suptitle("3D crack-trace evolution through the water cycle "
                 "(s1 baseline excluded; classification and statistics follow Fig. 5-19)",
                 y=0.995)
    fig.savefig(HERE.parent / "result" / "圖5-20_襯砌裂縫三維演化.png",
                dpi=170, bbox_inches="tight")
    print("saved 圖5-20 montage")
    sys.exit(0)

frames = []
pl = pv.Plotter(off_screen=True, window_size=WIN)
for k in range(1, 12):
    for az in np.linspace(0, 360, NFRAMES, endpoint=False):
        frames.append(Image.fromarray(render_stage(pl, k, az)))
pl.close()
frames[0].save(OUT, save_all=True, append_images=frames[1:],
               duration=FRAME_MS, loop=0, disposal=2, optimize=False)
print(f"saved {OUT}  frames={len(frames)}  {FRAME_MS} ms/frame  "
      f"rotation={NFRAMES*FRAME_MS/1000:.1f}s/stage")
