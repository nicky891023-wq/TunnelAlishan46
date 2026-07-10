#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_sm_model.py -- 圖5-3 隧道圍岩擾動尺度模型：6-layer 網格剖切 + 殼元素襯砌。
(a) 3D cutaway at y=885 (flat GUI colors, 6 layers legible) with tunnel void visible
(b) shell lining close-up (sm_shells.txt triangles) inside translucent rock
(c) section y=885 matplotlib-native: layers + tunnel + shell trace, real axes
Out: 00_Document/result/圖5-03_隧道圍岩擾動尺度模型網格與襯砌.png
"""
from pathlib import Path
import numpy as np
import pyvista as pv
from PIL import Image
import f3grid_io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import thesis_style as TS

TS.apply()
pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT = TS.RESULT
TUN = (1297.0, 885.0, 1747.5)

LAYC = {1: "#efe0b0", 2: "#dcc078", 3: "#c1a15c", 4: "#a08349", 5: "#82683c", 6: "#655232",
        7: "#b8d4e8"}   # 7 = 'lining' group: near-tunnel annulus (k x100), follows the curve
LAYNAME = {1: "Layer 1", 2: "Layer 2", 3: "Layer 3", 4: "Layer 4", 5: "Layer 5",
           6: "Layer 6", 7: "Near-tunnel annulus"}
SHELLC = "#7f8c9b"

grid = f3grid_io.to_unstructured(HERE / "sm_geom.f3grid")
names = list(grid.field_data["layer_names"])
print("sm layers:", names, " cells:", grid.n_cells)

sh = np.loadtxt(HERE / "sm_shells.txt", skiprows=1)
tris = sh[:, 1:10].reshape(-1, 3, 3)
shell_poly = pv.PolyData(tris.reshape(-1, 3),
                         np.hstack([np.full((len(tris), 1), 3),
                                    np.arange(len(tris) * 3).reshape(-1, 3)]).astype(np.int64))

def panel_a(png):
    pl = pv.Plotter(off_screen=True, window_size=(1900, 1500))
    pl.set_background("white")
    half = grid.clip(normal=(0, -1, 0), origin=TUN, crinkle=False)
    nl = int(grid.cell_data["layer"].max())
    for k in range(1, nl + 1):
        part = half.threshold([k - 0.5, k + 0.5], scalars="layer")
        if part.n_cells:
            pl.add_mesh(part.extract_surface(algorithm=None), color=LAYC.get(k, "#888888"),
                        show_edges=True, edge_color="#8a8a8a", line_width=0.3,
                        lighting=False)
    shel = shell_poly.clip(normal=(0, -1, 0), origin=(0, TUN[1], 0))
    pl.add_mesh(shel, color=SHELLC, show_edges=False, lighting=True,
                smooth_shading=True)
    pl.camera_position = [(1207, 745, 1835), (1300, 905, 1745), (0, 0, 1)]
    pl.camera.zoom(1.28)
    img = pl.screenshot(return_img=True); pl.close()
    Image.fromarray(img).save(png)

def panel_b(png):
    pl = pv.Plotter(off_screen=True, window_size=(1700, 1500))
    pl.set_background("white")
    pl.add_mesh(shell_poly, color=SHELLC, show_edges=True, edge_color="#5c6771",
                line_width=0.3, smooth_shading=True)
    pl.camera_position = [(1235, 820, 1800), (1297, 885, 1747.5), (0, 0, 1)]
    pl.camera.zoom(1.5)
    img = pl.screenshot(return_img=True); pl.close()
    Image.fromarray(img).save(png)

def autocrop(p):
    img = Image.open(p); g = np.asarray(img.convert("L"))
    rows = np.where((g < 250).any(1))[0]; cols = np.where((g < 250).any(0))[0]
    img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)).save(p)

pa, pb = HERE / "_sm_a.png", HERE / "_sm_b.png"
panel_a(str(pa)); panel_b(str(pb))
autocrop(pa); autocrop(pb)

# (c) section
g2 = grid.copy(); g2.cell_data["cid"] = np.arange(g2.n_cells)
sec = g2.slice(normal="y", origin=TUN).triangulate()
pts = sec.points; f = sec.faces.reshape(-1, 4)[:, 1:]
lay = grid.cell_data["layer"][sec.cell_data["cid"]]
POLY = pts[f][:, :, [0, 2]]

fig = plt.figure(figsize=(27, 9.5))
gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1.0, 1.05], wspace=0.14)
axA = fig.add_subplot(gs[0]); axB = fig.add_subplot(gs[1]); axC = fig.add_subplot(gs[2])
axA.imshow(plt.imread(str(pa))); axA.axis("off")
axA.set_title("(a) 3D cutaway at y = 885 m (100 m box, 6 layers)", loc="left", fontsize=24)
axB.imshow(plt.imread(str(pb))); axB.axis("off")
axB.set_title("(b) Shell-element lining (69,828 elements)", loc="left", fontsize=24)

nl = int(lay.max())
for k in range(1, nl + 1):
    m = lay == k
    if m.any():
        axC.add_collection(PolyCollection(POLY[m], facecolor=LAYC.get(k, "#888"),
                                          edgecolor="#77777740", linewidth=0.2))
# shell trace on section
mtr = np.abs(tris[:, :, 1].mean(1) - TUN[1]) < 0.6
axC.plot([], [])
for t in tris[mtr]:
    axC.plot(t[[0, 1, 2, 0], 0], t[[0, 1, 2, 0], 2], color="#2c3540", lw=1.0)
axC.set_xlim(1247, 1347); axC.set_ylim(1697, 1797); axC.set_aspect("equal")
axC.set_xlabel("x (m)"); axC.set_ylabel("Elevation z (m)")
axC.set_title("(c) Section y = 885 m: layers + lining", loc="left", fontsize=24)

handles = [Patch(fc=LAYC[k], ec="0.3", label=LAYNAME[k]) for k in range(1, nl + 1)]
handles += [Patch(fc=SHELLC, ec="0.3", label="Shell lining")]
fig.legend(handles=handles, loc="lower center", ncol=8, fontsize=19,
           bbox_to_anchor=(0.5, -0.035))
fig.suptitle("Tunnel-scale model: 6-layer 100 m box with shell-element lining", y=1.0)
fig.savefig(OUT / "圖5-03_隧道圍岩擾動尺度模型網格與襯砌.png", dpi=190, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-03")
