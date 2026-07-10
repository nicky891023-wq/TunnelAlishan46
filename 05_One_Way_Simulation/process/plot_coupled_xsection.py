#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_coupled_xsection.py -- coupled lining y=885 cross-section: G4 horseshoe ring geometry
+ final (stage-11) cracks in the slice, COLOURED BY ORIENTATION CLASS via crack_classify
(circumferential=red, oblique=blue, longitudinal=green). In a single cross-section the
connected arc down the leg is a circumferential crack (red), matching the field ring pattern.
Styling: English, Times New Roman, fonts ~3-4x default.
Out: ../result/coupled_xsection_and_cracks.png
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import crack_classify as cc

matplotlib.rcParams.update({
    "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 28, "axes.titlesize": 30, "axes.labelsize": 30,
    "xtick.labelsize": 24, "ytick.labelsize": 24, "legend.fontsize": 22,
    "savefig.bbox": "tight",
})

HERE = Path(__file__).parent
XSEC = HERE.parent.parent / "04_InitialBalance" / "process" / "couple_solve" / "xsec_G4_y885.txt"
OUT  = HERE.parent / "result" / "coupled_xsection_and_cracks.png"
YLO, YHI = 884.5, 885.5

xs = np.loadtxt(XSEC, skiprows=1, ndmin=2)             # ball x z (ring geometry @ y=885)
P, _ = cc.load_breaks(stage=11)
typ, TH, R = cc.classify_breaks(P)
X, Y, Z = P[:, 0], P[:, 1], P[:, 2]
sl = (Y > YLO) & (Y < YHI)                             # cracks in this y-slice

fig, (a1, a2) = plt.subplots(1, 2, figsize=(20, 11))
a1.scatter(xs[:, 0], xs[:, 1], s=6, c="0.55")
a1.set_title("Coupled lining ring @ y=885\n(horseshoe, open invert)")
a1.set_xlabel("x (m)"); a1.set_ylabel("z (m)"); a1.set_aspect("equal")

a2.scatter(xs[:, 0], xs[:, 1], s=6, c="0.82")
counts = {}
for t in (0, 2, 1):                                    # circ, long, oblique on top
    m = sl & (typ == t)
    counts[t] = int(m.sum())
    if m.any():
        a2.scatter(X[m], Z[m], s=14, c=cc.TYPE_COL[t], lw=0)
nslice = int(sl.sum())
a2.set_title(f"Cracks @ y=885 by orientation\n({nslice} breaks in slice)")
a2.set_xlabel("x (m)"); a2.set_ylabel("z (m)"); a2.set_aspect("equal")
handles = [Line2D([0], [0], marker="o", ls="", ms=13, mfc=cc.TYPE_COL[t], mec="none",
                  label=f"{cc.TYPE_NAME[t]}  ({counts.get(t,0)})") for t in (0, 1, 2)]
a2.legend(handles=handles, loc="upper left", framealpha=0.9)

fig.savefig(OUT, dpi=200); plt.close(fig)
print(f"saved {OUT}  slice breaks={nslice}  circ={counts[0]} oblique={counts[1]} longit={counts[2]}")
