#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_fine_pressure.py -- FINE lining external-pressure maps from per-contact
ball-facet force dumps (pf_s01/06/11.txt: x y z fx fy fz).
Radial (inward/compressive) force is area-normalized to a pressure field [kPa]
and binned on the crown-centred developed-lining grid (fine 1deg x 0.5m).
Styling: English, Times New Roman, large fonts, light-gray bg, red = pressure.
Out: ../result/FIG_G_pressure_fine.png   (checkpoints s01 dry1 / s06 wet / s11 dry2)
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

matplotlib.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 28, "axes.titlesize": 32, "axes.labelsize": 30,
    "xtick.labelsize": 22, "ytick.labelsize": 24, "savefig.bbox": "tight",
})
GRAYRED = LinearSegmentedColormap.from_list(
    "grayred", ["#e3e3e3", "#f7c9b8", "#f08a63", "#e03020", "#8a0000"])

HERE = Path(__file__).parent
OUT  = HERE.parent / "result" / "FIG_G_pressure_fine.png"
CX, CZ = 1297.0, 1747.5
PHI = np.arange(-150, 150.001, 1.0)          # deg
YF  = np.arange(860, 910.001, 0.5)           # m
DPHI = np.radians(1.0); DY = 0.5
CKPT = [("01", "s1  W-110 (dry1)"), ("06", "s6  W-10 (wet)"), ("11", "s11  W-110 (dry2)")]

def pressure_grid(tag):
    d = np.loadtxt(HERE / f"pf_s{tag}.txt", skiprows=1, ndmin=2)
    x, y, z, fx, fz = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 5]
    rx, rz = x - CX, z - CZ
    r = np.sqrt(rx*rx + rz*rz); r[r == 0] = 1e-9
    f_out = (fx*rx + fz*rz) / r               # outward radial component (N)
    f_in  = np.clip(-f_out, 0, None)          # inward = compression (N)
    phi = np.degrees(np.arctan2(rx, rz))
    Fsum, _, _ = np.histogram2d(phi, y, bins=[PHI, YF], weights=f_in)
    Rsum, _, _ = np.histogram2d(phi, y, bins=[PHI, YF], weights=r)
    Cnt,  _, _ = np.histogram2d(phi, y, bins=[PHI, YF])
    Rmean = np.divide(Rsum, Cnt, out=np.full_like(Rsum, 3.5), where=Cnt > 0)
    area = Rmean * DPHI * DY                   # m^2 per cell (arc x axial)
    P = np.divide(Fsum, area, out=np.zeros_like(Fsum), where=area > 0) / 1000.0  # kPa
    return P

grids = {t: pressure_grid(t) for t, _ in CKPT}
vmax = np.percentile(np.concatenate([g[g > 0].ravel() for g in grids.values()]), 98)

fig, axs = plt.subplots(1, 3, figsize=(28, 11), sharey=True)
for ax, (t, title) in zip(axs, CKPT):
    im = ax.pcolormesh(PHI, YF, grids[t].T, vmin=0, vmax=vmax, cmap=GRAYRED, shading="flat")
    ax.set_facecolor("#e3e3e3")
    ax.axvline(0, color="0.45", ls="--", lw=1.4)
    ax.axvline(90, color="0.6", ls=":", lw=1.2); ax.axvline(-90, color="0.6", ls=":", lw=1.2)
    ax.set_title(title)
    ax.set_xlabel("Angle from crown (deg)")
    ax.set_xticks([-135, -90, 0, 90, 135])
    ax.set_xticklabels(["L foot", "L spr", "Crown", "R spr", "R foot"], fontsize=18)
axs[0].set_ylabel("y (m)")
fig.colorbar(im, ax=axs, label="Radial pressure (kPa)", shrink=.85, extend="max")
fig.suptitle("Lining external pressure - fine developed map (per-contact, checkpoints)")
fig.savefig(OUT, dpi=220); plt.close(fig)
print(f"saved {OUT}  vmax={vmax:.1f} kPa")
