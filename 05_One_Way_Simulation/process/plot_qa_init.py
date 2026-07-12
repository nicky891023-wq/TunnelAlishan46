#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_qa_init.py -- presentation QA figures of the INITIAL equilibrium states (07-12 v2,
standard spec: Times New Roman English, large fonts, light-grey plot grid).
Inputs : lg_init_slice.txt / sm_init_slice.txt  (x z szz sxx pp state; console export)
Outputs: 00_Document/method_report_assets/qa_large_init.png / qa_small_init.png
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import thesis_style as TS

TS.apply()
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.color"] = "#d4d4d4"
plt.rcParams["grid.linewidth"] = 0.8
HERE = Path(__file__).parent
OUT = HERE.parent.parent / "00_Document" / "method_report_assets"

def tricf(ax, x, z, v, cmap, label, vmin=None, vmax=None, rmax=None):
    tri = mtri.Triangulation(x, z)
    # mask only extreme sliver triangles (concave terrain boundary), keep interior full
    xt, zt = x[tri.triangles], z[tri.triangles]
    r = np.sqrt((xt.max(1)-xt.min(1))**2 + (zt.max(1)-zt.min(1))**2)
    tri.set_mask(r > (rmax if rmax else np.percentile(r, 99.5) * 2.5))
    im = ax.tricontourf(tri, v, levels=24, cmap=cmap, vmin=vmin, vmax=vmax)
    cb = plt.colorbar(im, ax=ax, shrink=0.92, pad=0.02)
    cb.set_label(label)
    ax.set_xlabel("x (m)"); ax.set_ylabel("z (m)")
    ax.set_aspect("equal")
    return im

# ---------------- LARGE ----------------
d = np.loadtxt(HERE / "lg_init_slice.txt", skiprows=1, ndmin=2)
x, z = d[:, 0], d[:, 1]
szz, sxx, pp = d[:, 2] / 1e6, d[:, 3] / 1e6, d[:, 4] / 1e6
fig, axs = plt.subplots(1, 3, figsize=(27, 8.5), sharey=True)
tricf(axs[0], x, z, szz, "turbo_r", r"$\sigma_{zz}$ (MPa, compression $-$)")
axs[0].set_title("(a) Vertical stress", loc="left")
tricf(axs[1], x, z, sxx, "turbo_r", r"$\sigma_{xx}$ (MPa, compression $-$)")
axs[1].set_title("(b) Horizontal stress", loc="left")
tricf(axs[2], x, z, pp, "viridis", "Pore pressure (MPa)")
axs[2].set_title("(c) Pore pressure (W-110)", loc="left")
fig.suptitle("Slope-scale initial equilibrium - section y = 900 m "
             "(seepage steady state at W-110, then mechanical solve)", y=1.02)
fig.savefig(OUT / "qa_large_init.png", dpi=170, bbox_inches="tight")
plt.close(fig)
print("saved qa_large_init.png")

# ---------------- SMALL ----------------
d = np.loadtxt(HERE / "sm_init_slice.txt", skiprows=1, ndmin=2)
x, z = d[:, 0], d[:, 1]
szz, sxx, pp, st = d[:, 2] / 1e6, d[:, 3] / 1e6, d[:, 4] / 1e6, d[:, 5].astype(int)
win = (x > 1250) & (x < 1350) & (z > 1698) & (z < 1800)
x, z, szz, sxx, pp, st = x[win], z[win], szz[win], sxx[win], pp[win], st[win]
fig, axs = plt.subplots(2, 2, figsize=(20, 17), sharex=True, sharey=True)
tricf(axs[0, 0], x, z, szz, "turbo_r", r"$\sigma_{zz}$ (MPa, compression $-$)", rmax=10)
axs[0, 0].set_title("(a) Vertical stress", loc="left")
tricf(axs[0, 1], x, z, sxx, "turbo_r", r"$\sigma_{xx}$ (MPa, compression $-$)", rmax=10)
axs[0, 1].set_title("(b) Horizontal stress", loc="left")
tricf(axs[1, 0], x, z, pp, "viridis", "Pore pressure (MPa)", rmax=10)
axs[1, 0].set_title("(c) Pore pressure (wall drained)", loc="left")
ax = axs[1, 1]
never = st == 0
ax.plot(x[never], z[never], ".", ms=2.4, color="0.78", label=f"elastic ({never.sum():,})")
# FLAC3D state bitmask: 1=shear-n, 2=tension-n, 4=shear-p, 8=tension-p
shear = (st & 0b0101) > 0
tens = ((st & 0b1010) > 0) & ~shear
ax.plot(x[shear], z[shear], ".", ms=3.2, color="#1f6fe0",
        label=f"shear flag ({shear.sum():,})")
ax.plot(x[tens], z[tens], ".", ms=3.2, color="#e00000",
        label=f"tension flag ({tens.sum():,})")
ax.legend(fontsize=18, loc="lower left", framealpha=0.9)
ax.set_xlabel("x (m)"); ax.set_ylabel("z (m)"); ax.set_aspect("equal")
ax.set_title("(d) Plastic state around the bore", loc="left")
fig.suptitle("Tunnel-scale initial equilibrium - section y = 885 m "
             "(excavation + shell lining + wall drainage, displacements re-zeroed)",
             y=1.0)
fig.savefig(OUT / "qa_small_init.png", dpi=170, bbox_inches="tight")
plt.close(fig)
print("saved qa_small_init.png")
