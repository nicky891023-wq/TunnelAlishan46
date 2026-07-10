#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_lg_model.py -- 圖5-2 邊坡尺度模型 v2 (visual review round 1 fixes):
(a) 3D CUTAWAY at tunnel section y=885 (crinkle clip -> true zones on the cut face, layers
    legible) + terrain + BOLD red tunnel-scale box.
(b) matplotlib-native section with real axes: mesh triangles by layer, W-10/W-110 traces,
    tunnel mark + ZOOM INSET around the tunnel-scale box showing the 100 m water swing
    straddling the tunnel horizon (the mechanism).
Out: 00_Document/result/圖5-02_邊坡尺度模型網格與地下水位面.png
"""
from pathlib import Path
import numpy as np
import pyvista as pv
from PIL import Image
import f3grid_io

pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT = Path(r"C:\Users\Wade\Desktop\Tunnel_TX\00_Document\result")
STL = HERE.parent / "input"

LAYC = {1: "#e8d9a0", 2: "#cdae6b", 3: "#a98c4b", 4: "#7c6840"}
W_HI, W_LO = "#1f6fc4", "#7aa8cf"
TUN = (1297.0, 885.0, 1747.5)

grid = f3grid_io.to_unstructured(HERE / "lg_geom.f3grid")
smb = f3grid_io.to_unstructured(HERE / "sm_geom.f3grid").bounds
w10, w110 = pv.read(str(STL / "W-10.stl")), pv.read(str(STL / "W-110.stl"))

# ---------------- (a) 3D cutaway ----------------
def panel_a(png):
    pl = pv.Plotter(off_screen=True, window_size=(2000, 1500))
    pl.set_background("white")
    half = grid.clip(normal=(0, -1, 0), origin=TUN, crinkle=False)  # flat clean cut face
    for k in (1, 2, 3, 4):
        part = half.threshold([k - 0.5, k + 0.5], scalars="layer")
        if part.n_cells:
            pl.add_mesh(part.extract_surface(algorithm=None), color=LAYC[k],
                        show_edges=True, edge_color="#787878", line_width=0.5,
                        lighting=False)                            # GUI-flat colors
    # water sheets on the kept half, lightly translucent
    for w, c, op in ((w10, W_HI, 0.55), (w110, W_LO, 0.50)):
        wc = w.clip_box([0, 2000, 885, 2000, 0, 3000], invert=False)
        pl.add_mesh(wc, color=c, opacity=op)
    box = pv.Box(bounds=smb)
    pl.add_mesh(box.extract_all_edges(), color="#e0231c", line_width=7,
                render_lines_as_tubes=True)
    pl.add_mesh(pv.Sphere(radius=16, center=TUN), color="#e0231c")
    # camera: from south-below-left of the cut, looking at the section face
    pl.camera_position = [(1250, -1650, 3050), (1050, 1000, 1500), (0, 0, 1)]
    pl.camera.zoom(1.35)
    img = pl.screenshot(return_img=True); pl.close()
    Image.fromarray(img).save(png)

# ---------------- (b) matplotlib-native section ----------------
def section_tris():
    sec = grid.slice(normal="y", origin=TUN)                 # triangles on the plane
    sec = sec.triangulate()
    pts = sec.points
    f = sec.faces.reshape(-1, 4)[:, 1:]
    lay = sec.cell_data["layer"]
    return pts, f, lay

def water_trace(w):
    tr = w.slice(normal="y", origin=TUN)
    p = tr.points
    o = np.argsort(p[:, 0])
    return p[o, 0], p[o, 2]

def panel_b(fig_axes):
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    ax, axz = fig_axes
    pts, f, lay = section_tris()
    for k in (1, 2, 3, 4):
        m = lay == k
        if not m.any():
            continue
        polys = pts[f[m]][:, :, [0, 2]]
        for a in (ax, axz):
            a.add_collection(PolyCollection(polys, facecolor=LAYC[k],
                                            edgecolor="#666666", linewidth=0.25))
    for w, c in ((w10, W_HI), (w110, W_LO)):
        wx, wz = water_trace(w)
        m = (wx >= 0) & (wx <= 2000)
        for a, lw in ((ax, 3.2), (axz, 4.0)):
            a.plot(wx[m], wz[m], color=c, lw=lw, zorder=5)
    for a, r in ((ax, 10), (axz, 5)):
        a.add_patch(plt.Circle((TUN[0], TUN[2]), r, fc="none", ec="#e0231c",
                    lw=3 if a is ax else 3.5, zorder=6))
    # small-box outline on section
    for a in (ax, axz):
        a.add_patch(plt.Rectangle((smb[0], smb[4]), smb[1]-smb[0], smb[5]-smb[4],
                    fc="none", ec="#e0231c", lw=2.4, ls="--", zorder=6))
    ax.set_xlim(0, 2000); ax.set_ylim(800, 2060)
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("Elevation z (m)")
    axz.set_xlim(smb[0] - 30, smb[1] + 30); axz.set_ylim(smb[4] - 30, smb[5] + 60)
    axz.set_aspect("equal")
    axz.set_xlabel("x (m)")
    axz.tick_params(labelleft=True)

pa = HERE / "_lg_a.png"
panel_a(str(pa))
# autocrop white margins so panel (a) fills its axes
img = Image.open(pa); g = np.asarray(img.convert("L"))
rows = np.where((g < 250).any(1))[0]; cols = np.where((g < 250).any(0))[0]
img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)).save(pa)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import thesis_style as TS
TS.apply()

fig = plt.figure(figsize=(27, 8.6))
gs = fig.add_gridspec(1, 3, width_ratios=[1.30, 1.28, 0.66], wspace=0.16)
axA = fig.add_subplot(gs[0]); axB = fig.add_subplot(gs[1]); axZ = fig.add_subplot(gs[2])
axA.imshow(plt.imread(str(pa))); axA.axis("off")
axA.set_title("(a) 3D cutaway at tunnel section (y = 885 m)", loc="left", fontsize=28)
panel_b((axB, axZ))
axB.set_title("(b) Geological section y = 885 m", loc="left", fontsize=28)
axZ.set_title("(c) Tunnel-scale box zoom", loc="left", fontsize=28)
axZ.set_ylabel("Elevation z (m)")
axZ.annotate("W-10 (wet)", xy=(smb[0]-22, 1838), fontsize=23, color=W_HI,
             fontweight="bold")
axZ.annotate("W-110 (dry)", xy=(smb[0]+53, 1677), fontsize=23, color="#4d7fae",
             fontweight="bold")
axZ.annotate("tunnel", xy=(TUN[0]-6, TUN[2]+4), xytext=(TUN[0]-46, TUN[2]+22),
             fontsize=23, color="#e0231c",
             arrowprops=dict(arrowstyle="-", color="#e0231c", lw=1.6))

handles = [Patch(fc=LAYC[k], ec="0.3", label=f"Layer {k}") for k in (1, 2, 3, 4)]
handles += [Line2D([0], [0], color=W_HI, lw=6, label="Water table W-10 (wet)"),
            Line2D([0], [0], color=W_LO, lw=6, label="Water table W-110 (dry)"),
            Line2D([0], [0], color="#e0231c", lw=4, label="Tunnel-scale model box / tunnel")]
fig.legend(handles=handles, loc="lower center", ncol=7, frameon=True, fontsize=24,
           bbox_to_anchor=(0.5, -0.01), columnspacing=1.0, handlelength=1.4)
fig.savefig(OUT / "圖5-02_邊坡尺度模型網格與地下水位面.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-02 v2")
