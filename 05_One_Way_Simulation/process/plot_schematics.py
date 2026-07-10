#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_schematics.py -- 圖5-1 多尺度數值模擬方法流程圖（賣點圖）+ 圖5-5 物理量傳遞示意
5-1: three model panels (real renders embedded) -> transfer arrows -> 11-stage water
     timeline strip. The one-figure statement of the multi-scale method.
5-5: (a) large->small velocity-boundary mapping (real mean values), (b) small->coupled
     Kabsch rigid-removal + displacement drive (real numbers).
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT

# ================= 圖5-1 =================
fig = plt.figure(figsize=(30, 13))
gs = fig.add_gridspec(2, 3, height_ratios=[3.1, 0.9], hspace=0.24, wspace=0.30)

PANELS = [
    ("_lg_a.png", "Slope scale (FLAC3D)",
     "2 km x 2.1 km, 4 layers, 512k zones\nSeepage + threshold creep\nwater cycle W-110 <-> W-10"),
    ("_sm_a.png", "Tunnel-disturbance scale (FLAC3D)",
     "100 m box, 6 layers, 1.43M zones\nNear-field seepage (k x100 annulus)\ncreep + shell lining"),
    ("_cp_c.png", "Rock-lining interaction scale (FLAC3D-PFC)",
     "40 x 50 x 40 m elastic box\nBPM lining 456k balls\nstatic per stage, cracks + forces"),
]
axes = []
for i, (img, ttl, sub) in enumerate(PANELS):
    ax = fig.add_subplot(gs[0, i])
    ax.imshow(plt.imread(str(HERE / img)))
    ax.axis("off")
    ax.set_title(ttl, fontsize=25, fontweight="bold", pad=12)
    ax.text(0.5, -0.03, sub, transform=ax.transAxes, ha="center", va="top",
            fontsize=18, linespacing=1.45)
    axes.append(ax)

# transfer arrows between panels (figure coords); captions ABOVE the panel tops (clear zone)
for x0, x1, lines in ((0.345, 0.395, "initial stress (IDW)\n+ stage boundary\nvelocities"),
                      (0.655, 0.705, "stage displacement\nfield (rigid-removed\nresidual)")):
    ar = FancyArrowPatch((x0, 0.60), (x1, 0.60), transform=fig.transFigure,
                         arrowstyle="-|>", mutation_scale=55, lw=5, color="#2e6da4")
    fig.add_artist(ar)
    fig.text((x0 + x1) / 2, 0.625, lines, ha="center", va="bottom", fontsize=20,
             color="#2e6da4", linespacing=1.4,
             bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.25))

# one-way note
fig.text(0.5, 0.905, "one-way transfer (large -> small -> coupled); geology model of Ch.4 "
         "feeds every scale", ha="center", fontsize=20, style="italic", color="0.25")

# water-cycle timeline strip
axt = fig.add_subplot(gs[1, :])
ks = np.arange(1, 12)
lv = np.array(TS.LEVEL, float)
cols = {"dry1": "0.65", "rise": "#4a7fb5", "wet": "#c0392b", "fall": "#7fb3d5",
        "dry2": "0.65"}
axt.bar(ks, lv + 120, bottom=-120, color=[cols[TS.PHASE[k-1]] for k in ks],
        edgecolor="k", lw=0.8, width=0.86)
wx_, wy_ = TS.water_steps()
axt.plot(wx_, wy_, "b-", lw=2.5)
axt.plot(ks, lv, "bo", ms=7)
axt.text(6, 6, "wet peak", ha="center", fontsize=20, color="#7a1d12")
axt.set_ylim(-122, 20)
axt.set_xlim(0.3, 11.7)
axt.set_yticks([-110, -60, -10])
axt.set_ylabel("Water level (m)", fontsize=20)
axt.set_xticks(list(ks))
axt.set_xticklabels([f"s{k}\n{TS.WATER[k-1]}" for k in ks], fontsize=17)
axt.set_title("11-stage water-level cycle applied at every scale "
              "(dry 30 d | rise 4 x 5 d | wet 30 d | fall 4 x 5 d | dry 30 d)",
              fontsize=20, pad=8)
fig.suptitle("Multi-scale numerical strategy: from slope hydrology to lining cracking",
             y=0.975, fontsize=30)
fig.savefig(OUT / "圖5-01_多尺度數值模擬方法流程圖.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-01")

# ================= 圖5-5 =================
fig, (a1, a2) = plt.subplots(1, 2, figsize=(26, 10))
for a in (a1, a2):
    a.set_xlim(0, 10); a.set_ylim(0, 10); a.axis("off")

# (a) large -> small
a1.add_patch(FancyBboxPatch((0.4, 1.2), 5.4, 7.4, boxstyle="round,pad=0.15",
             fc="#f3ead6", ec="0.4", lw=2))
a1.text(3.1, 8.95, "Slope-scale model", ha="center", fontsize=21, fontweight="bold")
a1.add_patch(plt.Rectangle((2.15, 3.4), 1.9, 1.9, fc="#ffffff", ec="#e0231c", lw=3,
             ls="--"))
a1.text(3.1, 4.35, "100 m\nbox", ha="center", va="center", fontsize=16, color="#e0231c")
arrows = [((5.6, 4.35), (4.15, 4.35), "mean dx = -319 mm (E->W)"),
          ((3.1, 1.55), (3.1, 3.3), "mean dy = +329 mm (S->N)"),
          ((1.15, 5.9), (2.35, 5.0), "dz = -40 mm")]
for (x0, y0), (x1, y1), lbl in arrows:
    a1.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                 mutation_scale=42, lw=4.2, color="#2e6da4"))
a1.text(6.35, 4.9, "stage-average boundary\nvelocities from node\ndisplacement fields\n"
        "(s6 means shown)", fontsize=18, color="#2e6da4", linespacing=1.5)
a1.text(6.35, 2.4, "initial stress: IDW\ninterpolation of the\nslope in-situ field",
        fontsize=18, color="0.3", linespacing=1.5)
a1.set_title("(a) Slope -> tunnel scale: velocity boundary drive", loc="left", fontsize=23)

# (b) small -> coupled (Kabsch)
a2.add_patch(FancyBboxPatch((0.4, 5.6), 4.2, 3.2, boxstyle="round,pad=0.15",
             fc="#e8eef5", ec="0.4", lw=2))
a2.text(2.5, 8.35, "Tunnel-scale stage field $u$", ha="center", fontsize=19,
        fontweight="bold")
a2.text(2.5, 6.9, r"$u = u_{rigid} + u_{residual}$", ha="center", fontsize=22)
a2.add_patch(FancyArrowPatch((2.5, 5.5), (2.5, 4.3), arrowstyle="-|>",
             mutation_scale=42, lw=4.2, color="#2e6da4"))
a2.text(2.85, 4.85, "Kabsch fit removes rigid\ntranslation + rotation", fontsize=17,
        color="#2e6da4", linespacing=1.4)
a2.add_patch(FancyBboxPatch((0.4, 1.0), 4.2, 3.0, boxstyle="round,pad=0.15",
             fc="#f6e8e6", ec="0.4", lw=2))
a2.text(2.5, 3.55, "Coupled-box boundary drive", ha="center", fontsize=19,
        fontweight="bold")
a2.text(2.5, 2.15, "residual only (median ~3-5 mm/stage)\nx f = 0.25 scale factor\n"
        "-> discrete lining stays in the\ncrack-development regime", ha="center",
        fontsize=17, linespacing=1.5)
a2.text(7.4, 6.3, "strain gate check:\nresidual strains << rock\nelastic limit "
        "(all stages pass)", fontsize=18, color="0.3", linespacing=1.5,
        bbox=dict(fc="white", ec="0.5", boxstyle="round,pad=0.4"))
a2.text(7.4, 3.2, "magnitudes are\ntrend-level (f = 0.25);\npattern + relative\n"
        "evolution preserved", fontsize=18, color="#7a1d12", linespacing=1.5,
        bbox=dict(fc="#fdf3f2", ec="#c0392b", boxstyle="round,pad=0.4"))
a2.set_title("(b) Tunnel -> coupled scale: displacement drive", loc="left", fontsize=23)
fig.suptitle("Boundary-condition transfer between scales", y=0.99)
fig.savefig(OUT / "圖5-05_物理量傳遞示意.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-05")
