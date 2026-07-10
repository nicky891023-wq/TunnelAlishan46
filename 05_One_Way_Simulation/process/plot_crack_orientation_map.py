#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_crack_orientation_map.py -- developed-lining crack map coloured by ORIENTATION CLASS
(circumferential=red, oblique=blue, longitudinal=green), using the shared crack_classify
three-track method. Crown at centre, feet at the edges. Left panel = raw crack-count density
(context); right panel = orientation-classified breaks.
Styling: English, Times New Roman, large fonts, light-gray background.
Out: ../result/FIG_B_crack_orientation_developed.png
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import crack_classify as cc

matplotlib.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 28, "axes.titlesize": 30, "axes.labelsize": 30,
    "xtick.labelsize": 20, "ytick.labelsize": 24, "legend.fontsize": 22,
    "savefig.bbox": "tight",
})
GRAYRED = LinearSegmentedColormap.from_list(
    "grayred", ["#e3e3e3", "#f7c9b8", "#f08a63", "#e03020", "#8a0000"])

HERE = Path(__file__).parent
OUT  = HERE.parent / "result" / "FIG_B_crack_orientation_developed.png"
PHI  = np.arange(-150, 150.001, 1.0)
YF   = np.arange(860, 910.001, 0.5)

P, _ = cc.load_breaks(stage=11)
typ, TH, R = cc.classify_breaks(P)
Y = P[:, 1]

def annotate(ax):
    ax.axvline(0, color="0.4", ls="--", lw=1.6)
    ax.axvline(90, color="0.55", ls=":", lw=1.3); ax.axvline(-90, color="0.55", ls=":", lw=1.3)
    ax.set_xlim(-150, 150); ax.set_ylim(860, 910)
    ax.set_xticks([-135, -90, 0, 90, 135])
    ax.set_xticklabels(["L foot", "L spr", "Crown", "R spr", "R foot"])

fig, (a0, a1) = plt.subplots(1, 2, figsize=(26, 12), sharey=True)

# ---- left: raw crack-count density (crown-centred developed map) ----
H, _, _ = np.histogram2d(TH, Y, bins=[PHI, YF])
vmax = np.percentile(H[H > 0], 98)
im = a0.pcolormesh(PHI, YF, H.T, vmin=0, vmax=vmax, cmap=GRAYRED, shading="flat")
a0.set_facecolor("#e3e3e3"); annotate(a0)
a0.set_title("Crack density (s11, cumulative)")
a0.set_xlabel("Angle from crown (deg)"); a0.set_ylabel("y (m)")
fig.colorbar(im, ax=a0, label="Crack count / cell", shrink=.85, extend="max")

# ---- right: orientation-classified breaks ----
a1.set_facecolor("#f2f2f2")
a1.scatter(TH[typ == -1], Y[typ == -1], s=3, c="#cfcfcf", alpha=0.5, lw=0)   # context
for t in (0, 2, 1):                                                          # circ, long, oblique on top
    m = typ == t
    a1.scatter(TH[m], Y[m], s=5, c=cc.TYPE_COL[t], alpha=0.65, lw=0)
annotate(a1)
a1.set_title("Cracks classified by orientation")
a1.set_xlabel("Angle from crown (deg)")
counts = {t: int((typ == t).sum()) for t in (0, 1, 2)}
handles = [Line2D([0], [0], marker="o", ls="", ms=13, mfc=cc.TYPE_COL[t], mec="none",
                  label=f"{cc.TYPE_NAME[t]}  ({counts[t]})") for t in (0, 1, 2)]
a1.legend(handles=handles, loc="lower center", ncol=1, framealpha=0.9,
          title="crack orientation (break count)")

fig.suptitle("Developed lining crack map - orientation classification "
             "(crown centre, feet edges)", fontsize=32)
fig.savefig(OUT, dpi=200); plt.close(fig)
print(f"saved {OUT}  circ={counts[0]} oblique={counts[1]} longit={counts[2]} "
      f"unclassified={int((typ==-1).sum())}")
