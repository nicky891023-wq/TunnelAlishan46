#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_cp_damage_pressure.py -- 圖5-15 襯砌損傷演化歷程 + 圖5-16 襯砌外壓細緻展開圖
5-15: dN bars (phase colors) + water level + cumulative damage density (quant_summary.json)
5-16: per-contact fine pressure (pf_s01/06/11), crown-centred developed maps,
      POLE CORRECTED to ring centre x=1298.85 (verified 07-10).
"""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import thesis_style as TS
import tunnel_frame as tf

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
CX, CZ = 1298.85, 1747.5          # corrected ring centre
GRAYRED = LinearSegmentedColormap.from_list(
    "grayred", ["#e3e3e3", "#f7c9b8", "#f08a63", "#e03020", "#8a0000"])

# ================= 圖5-15 damage history =================
Q = json.loads((HERE.parent / "result" / "quant_summary.json").read_text())
dN = {int(k): v for k, v in Q["dN"].items()}
Ncum = {int(k): v for k, v in Q["N_cum"].items()}
census_total = Ncum[11] / (Q["D_total_pct"] / 100)
PHASE_C = {"dry1": "0.6", "rise": "#4a7fb5", "wet": "#c0392b",
           "fall": "#7fb3d5", "dry2": "0.6"}
fig, ax = plt.subplots(figsize=(19, 10))
ks = list(range(2, 12))                                  # s1 = baseline, excluded
ax.bar(ks, [dN[k] for k in ks],
       color=[PHASE_C[TS.PHASE[k-1]] for k in ks], edgecolor="k", lw=0.8)
ax.set_xlabel("Stage (water level)")
ax.set_ylabel(r"Damage increment $\Delta N$ (bond breaks)")
ax.set_xticks(ks)
ax.set_xticklabels([f"{k}\n{TS.WATER[k-1]}" for k in ks], fontsize=21)
ax.set_xlim(0.35, 11.65)
ax.annotate(f"wet peak\n$\\Delta N$ = {dN[6]:,}\n$A_{{wet}}$ = {Q['A_wet']:.2f}",
            xy=(6, dN[6]), xytext=(7.2, dN[6]*0.86), fontsize=21, color="#7a1d12",
            arrowprops=dict(arrowstyle="->", color="#7a1d12", lw=2))
ax.annotate(f"frozen after recession\n$A_{{frz}}$ = {Q['A_frz']:.3f}",
            xy=(9, dN[9] + 1200), xytext=(8.62, dN[6]*0.50), fontsize=21, color="#0b5394",
            arrowprops=dict(arrowstyle="->", color="#0b5394", lw=2))
ax2 = ax.twinx()
wx_, wy_ = TS.water_steps()
ax2.plot(wx_, wy_, "b-", lw=2.6, alpha=.8)
ax2.plot(range(1, 12), TS.LEVEL, "bo", ms=8, alpha=.7)
ax2.set_ylabel("Water level (m)", color="b")
ax2.tick_params(axis="y", colors="b")
ax2.grid(False)
ax3 = ax.twinx(); ax3.spines.right.set_position(("axes", 1.13))
Dt = [100 * (Ncum[k] - Ncum[1]) / census_total for k in range(1, 12)]
ax3.plot(range(1, 12), Dt, "r--", lw=3)
ax3.set_ylabel("Cumulative water-cycle damage density (%)", color="r")
ax3.tick_params(axis="y", colors="r")
ax3.grid(False)
ax.set_title("Lining damage evolution through the water cycle "
             "(s1 baseline excluded; f = 0.25, trend)")
fig.savefig(OUT / "圖5-15_襯砌損傷演化歷程.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-15")

# ================= 圖5-16 fine pressure =================
SB = np.arange(-tf.SFOOT, tf.SFOOT + 0.001, 0.10)   # perimeter station bins (m)
YF = np.arange(860, 910.001, 0.5)
DS = 0.10; DY = 0.5
CKPT = [("01", "(a) s1  W-110 (dry)"), ("06", "(b) s6  W-10 (wet)"),
        ("11", "(c) s11  W-110 (dry2)")]

def pressure_grid(tag):
    d = np.loadtxt(HERE / f"pf_s{tag}.txt", skiprows=1, ndmin=2)
    x, y, z, fx, fz = d[:, 0], d[:, 1], d[:, 2], d[:, 3], d[:, 5]
    rx, rz = x - tf.cx_of(y), z - tf.z0_of(y)           # LOCAL centre (curve + grade)
    r = np.sqrt(rx*rx + rz*rz); r[r == 0] = 1e-9
    f_in = np.clip(-(fx*rx + fz*rz) / r, 0, None)
    st = tf.station(x, y, z)
    Fs, _, _ = np.histogram2d(st, y, bins=[SB, YF], weights=f_in)
    area = DS * DY                                       # true perimeter-cell area
    return np.divide(Fs, area, out=np.zeros_like(Fs), where=Fs >= 0) / 1000.0

grids = {t: pressure_grid(t) for t, _ in CKPT}
vmax = np.percentile(np.concatenate([g[g > 0].ravel() for g in grids.values()]), 98)
fig, axs = plt.subplots(1, 3, figsize=(28, 10.5), sharey=True)
for ax, (t, title) in zip(axs, CKPT):
    im = ax.pcolormesh(SB, YF, grids[t].T, vmin=0, vmax=vmax, cmap=GRAYRED,
                       shading="flat")
    ax.set_facecolor("#e3e3e3")
    ax.axvline(0, color="0.45", ls="--", lw=1.4)
    ax.axvline(tf.QUART, color="0.6", ls=":", lw=1.2)
    ax.axvline(-tf.QUART, color="0.6", ls=":", lw=1.2)
    ax.set_title(title, loc="left")
    tp, tl = tf.ticks()
    ax.set_xticks(tp)
    ax.set_xticklabels(tl, fontsize=20)
axs[0].set_ylabel("y (m)")
cb = fig.colorbar(im, ax=axs, label="Radial contact pressure (kPa)", shrink=.85,
                  extend="max")
fig.suptitle("Lining external pressure - developed maps along the CURVED axis "
             "(per-contact; x = perimeter station)", y=1.0)
fig.savefig(OUT / "圖5-16_襯砌外壓展開圖.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-16  vmax=%.0f kPa" % vmax)
