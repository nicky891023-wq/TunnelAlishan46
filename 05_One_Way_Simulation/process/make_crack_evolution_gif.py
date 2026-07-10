#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_crack_evolution_gif.py -- 3D orbiting GIF of coupled-lining CRACK evolution.
CRACK != BOND BREAK: a bond break is a micro-damage event; a macroscopic crack is a
CONTINUOUS LINE where many aligned breaks connect over a minimum length.
Monotonic accumulation: the crack network is clustered ONCE at the final state (s11);
each crack centerline carries a per-point BIRTH AGE (earliest break there), and at stage k
we reveal the sub-segments already born (birth age <= end-of-stage-k age). Cracks therefore
NUCLEATE and PROPAGATE over stages and are never erased. Stage-1 service-history baseline
(age <= AGE1) is excluded, so cracks are the WATER-CYCLE-induced ones (prominent at wet s6).
Each full 360 orbit = one stage; red crack lines grow on the light-gray G4 lining tube.
NB cracks are predominantly LONGITUDINAL (springline, along tunnel axis) = slope-ovalization
physics, matching NO46 field cracks; the few circumferential/oblique ones are also shown.
Inputs: ring3d_G4.txt + cs_s1..11_cracks.txt (x y z type diam age).
Out: ../result/FIG_D_crack_evolution_3D.gif
Usage: python make_crack_evolution_gif.py [--test]
"""
import sys
from pathlib import Path
import numpy as np
import pyvista as pv
import imageio.v2 as imageio
from sklearn.cluster import DBSCAN
from scipy.spatial import cKDTree

pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT  = HERE.parent / "result" / "FIG_D_crack_evolution_3D.gif"
CX, CY, CZ = 1297.0, 885.0, 1747.5
WATER = ["W-110","W-90","W-70","W-50","W-30","W-10","W-30","W-50","W-70","W-90","W-110"]
PHASE = ["dry1","rise","rise","rise","rise","wet","fall","fall","fall","fall","dry2"]
AGE1  = 25855.0          # stage-1 baseline cutoff
SEED_VOX = 0.25          # thin breaks to voxel seeds
SEED_MIN = 2             # min breaks per seed voxel
EPS   = 0.40             # DBSCAN neighbourhood (m)
MINPTS = 3
LMIN  = 0.9             # min crack length (m)
BIN_L = 0.3            # centerline resampling (m)
DENS_N = 5            # a centerline point "is a crack" once >=DENS_N breaks lie within DENS_R
DENS_R = 0.35         # birth age = age of the DENS_N-th such break (crack densifies -> born)
TUBE_R = 0.16
NFRAMES = 44
FPS_DUR = 0.14
RADIUS, ELEV, ZOOM = 52.0, 24.0, 1.05
WIN = (1000, 720)
TEST = "--test" in sys.argv

ring = np.loadtxt(HERE / "ring3d_G4.txt", skiprows=1, ndmin=2)[::5]
raw  = {k: np.loadtxt(HERE / f"cs_s{k}_cracks.txt", skiprows=1, ndmin=2) for k in range(1, 12)}
AGE_END = {k: float(raw[k][:, 5].max()) for k in range(1, 12)}   # end-of-stage age (monotonic)

# ---- cluster the FINAL crack network once; each centerline point carries a birth age ----
def birth_age(pt, tree, ages):
    """age at which >=DENS_N breaks accumulate within DENS_R of pt (crack densifies -> born); inf if never."""
    idx = tree.query_ball_point(pt, DENS_R)
    if len(idx) < DENS_N:
        return np.inf
    return float(np.sort(ages[idx])[DENS_N - 1])

def build_cracks():
    d = raw[11]; d = d[d[:, 5] > AGE1]
    xyz, age = d[:, :3], d[:, 5]
    tree = cKDTree(xyz)
    ijk = np.floor(xyz / SEED_VOX).astype(np.int64)
    uniq, cnt = np.unique(ijk, axis=0, return_counts=True)
    seeds = (uniq[cnt >= SEED_MIN] + 0.5) * SEED_VOX
    labels = DBSCAN(eps=EPS, min_samples=MINPTS).fit_predict(seeds)
    cracks = []
    for lab in set(labels) - {-1}:
        p = seeds[labels == lab]
        if len(p) < 4:
            continue
        c = p.mean(0); axis = np.linalg.svd(p - c, full_matrices=False)[2][0]
        proj = (p - c) @ axis
        length = proj.max() - proj.min()
        if length < LMIN:
            continue
        nb = max(2, int(round(length / BIN_L)))
        edges = np.linspace(proj.min(), proj.max(), nb + 1)
        cpts, cage = [], []
        for i in range(nb):
            m = (proj >= edges[i]) & (proj <= edges[i + 1])
            if m.any():
                pos = p[m].mean(0)
                cpts.append(pos); cage.append(birth_age(pos, tree, age))
        if len(cpts) >= 2:
            cracks.append((np.array(cpts), np.array(cage)))
    return cracks

CRACKS = build_cracks()

def tubes_at(age_max):
    """polylines of crack sub-segments already born (birth age <= age_max) -> tube mesh + total length."""
    pts, cells, off, tot = [], [], 0, 0.0
    for cpts, cage in CRACKS:
        born = cage <= age_max
        i = 0; n = len(born)
        while i < n:
            if not born[i]:
                i += 1; continue
            j = i
            while j + 1 < n and born[j + 1]:
                j += 1
            if j - i + 1 >= 2:
                seg = cpts[i:j + 1]
                tot += np.linalg.norm(np.diff(seg, axis=0), axis=1).sum()
                pts.append(seg)
                cells.append(np.hstack([[len(seg)], np.arange(off, off + len(seg))]))
                off += len(seg)
            i = j + 1
    if not pts:
        return None, 0.0
    poly = pv.PolyData(np.vstack(pts)); poly.lines = np.hstack(cells)
    return poly.tube(radius=TUBE_R), tot

TUBES = {k: tubes_at(AGE_END[k]) for k in range(1, 12)}

def cam_position(az):
    a = np.radians(az)
    return (CX + RADIUS*np.cos(a), CY + RADIUS*np.sin(a), CZ + ELEV)

def render_stage(pl, k, az):
    pl.clear(); pl.set_background("white")
    pl.add_points(ring, color="#9a9a9a", point_size=2.0, opacity=0.35,
                  render_points_as_spheres=False)
    tube, tlen = TUBES[k]
    if tube is not None:
        pl.add_mesh(tube, color="#e00000", smooth_shading=True, show_scalar_bar=False)
    pl.camera.focal_point = (CX, CY, CZ); pl.camera.up = (0, 0, 1)
    pl.camera.position = cam_position(az); pl.reset_camera(); pl.camera.zoom(ZOOM)
    tag = "baseline (water cycle not started)" if tlen < 0.5 else f"total crack length = {tlen:.0f} m"
    pl.add_text(f"Stage {k}  {WATER[k-1]} ({PHASE[k-1]})\n{tag}",
                position="upper_left", font_size=16, color="black")
    return pl.screenshot(return_img=True)

if TEST:
    from PIL import Image
    pl = pv.Plotter(off_screen=True, window_size=(720, 760))
    imgs = [render_stage(pl, k, 35) for k in (1, 4, 6, 11)]
    pl.close()
    Image.fromarray(np.concatenate(imgs, axis=1)).save(HERE / "_FIG_D_gif_preview.png")
    print("preview; total cracks:", len(CRACKS),
          " segs s1/s4/s6/s11:", TUBES[1][1], TUBES[4][1], TUBES[6][1], TUBES[11][1])
    sys.exit(0)

frames = []
pl = pv.Plotter(off_screen=True, window_size=WIN)
for k in range(1, 12):
    for az in np.linspace(0, 360, NFRAMES, endpoint=False):
        frames.append(render_stage(pl, k, az))
pl.close()
imageio.mimsave(OUT, frames, duration=FPS_DUR, loop=0)
print(f"saved {OUT}  frames={len(frames)}")
