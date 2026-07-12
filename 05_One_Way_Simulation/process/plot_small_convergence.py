#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_small_convergence.py -- small-model 11-stage tunnel convergence history.
Parses small_staged_hist_merged.log (SSv2-HIST lines) -> 3-panel result figure.
Styling (Wade 2026-07-08): English, Times New Roman, fonts ~3-4x default.
Out: ../result/small_convergence_history_v2.png
"""
import re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 26, "axes.titlesize": 30, "axes.labelsize": 28,
    "xtick.labelsize": 22, "ytick.labelsize": 22, "legend.fontsize": 22,
    "axes.linewidth": 1.5, "lines.linewidth": 2.5, "savefig.bbox": "tight",
})

HERE = Path(__file__).parent
LOG  = HERE / "small_staged_hist_merged.log"
OUT  = HERE.parent / "result" / "small_convergence_history_v2.png"

# 11-stage schedule: (day_start, day_end, water_level_m)
STAGES = [(0,30,-110),(30,35,-90),(35,40,-70),(40,45,-50),(45,50,-30),
          (50,80,-10),(80,85,-30),(85,90,-50),(90,95,-70),(95,100,-90),(100,130,-110)]

txt = LOG.read_text(encoding="utf-8", errors="replace")
rows = []
for m in re.finditer(
        r"^SSv2-HIST stg=(\d+) day=([-\d.eE+]+) vclose=([-\d.eE+]+) hclose=([-\d.eE+]+) "
        r"dmax=([-\d.eE+]+) active=(\d+) ncap=(\d+) novf=(\d+) maxC=([-\d.eE+]+)MPa", txt, re.M):
    rows.append([float(m.group(2)), float(m.group(3)), float(m.group(4)),
                 int(m.group(6)), int(m.group(7)), float(m.group(9))])
a = np.array(sorted(rows, key=lambda r: r[0]))
day, vcl, hcl, act, ncap, maxc = a[:,0], a[:,1], a[:,2], a[:,3], a[:,4], a[:,5]

fig, axs = plt.subplots(3, 1, figsize=(20, 18), sharex=True)

def bands(ax):
    for d0, d1, wl in STAGES:                       # deeper blue = higher water
        shade = 0.06 + 0.5 * (wl + 110) / 100.0
        ax.axvspan(d0, d1, color=(0.25, 0.45, 0.85), alpha=shade, lw=0)
    for d0, d1, wl in STAGES:
        ax.axvline(d1, color="0.6", ls=":", lw=1.2)

# ---- panel 1: closure ----
ax = axs[0]; bands(ax)
ax.plot(day, hcl, "s-", color="#c0392b", ms=6, label="Horizontal closure (springline)")
ax.plot(day, vcl, "o-", color="#1a3faa", ms=6, label="Vertical closure (crown-invert)")
ax.axhline(0, color="k", lw=1.0)
ax.set_ylabel("Closure (mm; neg = inward)")
ax.legend(loc="lower left")
ax.set_title("Alishan #46 small-model tunnel convergence, 11 water-level stages "
             "(dry flat -> wet accelerate -> retreat freeze)", pad=42)
ylo, yhi = ax.get_ylim()
for d0, d1, wl in STAGES:                            # water label inside top of plot
    ax.text((d0+d1)/2, yhi - 0.06*(yhi-ylo), f"W{wl}", ha="center", va="top",
            fontsize=15, rotation=90, color="0.35")
ax.set_ylim(ylo, yhi)

# ---- panel 2: creep-active zones ----
ax = axs[1]; bands(ax)
ax.plot(day, act/1000.0, "-", color="#1e7d34", lw=2.8)
ax.plot(day, act/1000.0, "s", color="#1e7d34", ms=4)
ax.set_ylabel(r"Creep-active zones ($\times10^3$)")

# ---- panel 3: shell damage ----
ax = axs[2]; bands(ax)
ax.plot(day, ncap/1000.0, "-", color="#7d1e7d", lw=2.8, label=r"Cumulative reduced shells ($\times10^3$)")
ax.plot(day, maxc/100.0, ":", color="0.4", lw=2.5, label="max shell stress /100 (MPa, fictitious)")
ax.set_ylabel("Shell damage")
ax.set_xlabel("Creep day (130 total)")
ax.legend(loc="upper right")

fig.savefig(OUT, dpi=200); plt.close(fig)
print(f"saved {OUT}  points={len(a)}  final hclose={hcl[-1]:.2f}mm vclose={vcl[-1]:.2f}mm")
