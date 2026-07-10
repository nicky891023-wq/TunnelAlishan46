#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_cp_model.py -- 圖5-4 圍岩襯砌互制尺度模型：
(a) tunnel-scale shell lining (continuum)  -> (b) PFC bonded-particle lining (456k balls,
    same geometry) : the "shell replaced by BPM" story
(c) assembly: 40x50x40 rock box (wireframe, single elastic medium) + ball lining + anchored
    feet note. Ball data: ring3d_G4.txt (subsampled); shells: sm_shells.txt.
"""
from pathlib import Path
import numpy as np
import pyvista as pv
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS

TS.apply()
pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT = TS.RESULT
CXR, CY, CZ = 1298.85, 885.0, 1747.5

ring = np.loadtxt(HERE / "ring3d_G4.txt", skiprows=1, ndmin=2)
sh = np.loadtxt(HERE / "sm_shells.txt", skiprows=1)
tris = sh[:, 1:10].reshape(-1, 3, 3)
# clip shells to the coupled box axial range (y 860-910) for like-for-like comparison
msh = (tris[:, :, 1].mean(1) > 860) & (tris[:, :, 1].mean(1) < 910)
tris = tris[msh]
shell_poly = pv.PolyData(tris.reshape(-1, 3),
                         np.hstack([np.full((len(tris), 1), 3),
                                    np.arange(len(tris) * 3).reshape(-1, 3)]).astype(np.int64))

CAM = [(1240, 800, 1802), (1298.85, 885, 1747.5), (0, 0, 1)]

def autocrop(p):
    img = Image.open(p); g = np.asarray(img.convert("L"))
    r = np.where((g < 250).any(1))[0]; c = np.where((g < 250).any(0))[0]
    img.crop((c[0], r[0], c[-1] + 1, r[-1] + 1)).save(p)

def panel_a(png):
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1400))
    pl.set_background("white")
    pl.add_mesh(shell_poly, color="#7f8c9b", smooth_shading=True)
    pl.camera_position = CAM; pl.camera.zoom(1.35)
    Image.fromarray(pl.screenshot(return_img=True)).save(png); pl.close()

def panel_b(png):
    pl = pv.Plotter(off_screen=True, window_size=(1600, 1400))
    pl.set_background("white")
    sub = ring[::3]
    cloud = pv.PolyData(sub)
    pl.add_mesh(cloud, color="#a86e3c", point_size=2.6,
                render_points_as_spheres=True)
    pl.camera_position = CAM; pl.camera.zoom(1.35)
    Image.fromarray(pl.screenshot(return_img=True)).save(png); pl.close()

def panel_c(png):
    pl = pv.Plotter(off_screen=True, window_size=(1800, 1400))
    pl.set_background("white")
    box = pv.Box(bounds=(CXR - 20, CXR + 20, 860, 910, CZ - 20, CZ + 20))
    pl.add_mesh(box.extract_all_edges(), color="#4a4a4a", line_width=3)
    pl.add_mesh(box, color="#d9cbb0", opacity=0.16)
    sub = ring[::4]
    pl.add_mesh(pv.PolyData(sub), color="#a86e3c", point_size=2.2,
                render_points_as_spheres=True)
    feet = ring[ring[:, 2] < 1745.4][::2]
    pl.add_mesh(pv.PolyData(feet), color="#e0231c", point_size=3.2,
                render_points_as_spheres=True)
    pl.camera_position = [(1215, 770, 1815), (CXR, CY, CZ), (0, 0, 1)]
    pl.camera.zoom(1.22)
    Image.fromarray(pl.screenshot(return_img=True)).save(png); pl.close()

pa, pb, pc = HERE / "_cp_a.png", HERE / "_cp_b.png", HERE / "_cp_c.png"
panel_a(str(pa)); panel_b(str(pb)); panel_c(str(pc))
for p in (pa, pb, pc):
    autocrop(p)

fig = plt.figure(figsize=(27, 9.6))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.28], wspace=0.06)
titles = ["(a) Tunnel-scale: shell lining (continuum)",
          "(b) Coupled-scale: PFC bonded-particle lining\n(456,163 balls, same horseshoe)",
          "(c) Assembly: 40 x 50 x 40 m elastic rock box\n+ BPM lining (feet anchored, red)"]
for i, (p, t) in enumerate(zip((pa, pb, pc), titles)):
    ax = fig.add_subplot(gs[i])
    ax.imshow(plt.imread(str(p))); ax.axis("off")
    ax.set_title(t, loc="left", fontsize=22)
fig.text(0.345, 0.5, r"$\Longrightarrow$", fontsize=54, ha="center", va="center",
         color="#2e6da4")
fig.suptitle("Rock-lining interaction model: shell lining replaced by a bonded-particle "
             "lining coupled to an elastic rock box", y=1.0)
fig.savefig(OUT / "圖5-04_圍岩襯砌互制尺度模型.png", dpi=190, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-04")
