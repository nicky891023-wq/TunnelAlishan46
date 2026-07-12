#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_cp_forces.py -- 圖5-17 襯砌內力（PFC 鍵結接觸力網）
(a-c) y=885 ring force chains at s1/s6/s11: bonded ball-ball contact forces drawn as
      oriented segments, linewidth/color ~ |f| (the DEM internal-force picture)
(d)   hoop thrust profile N(theta) (y=885+-5m band): sum of hoop-projected bonded contact
      force per 2-deg sector, s1 vs s6 vs s11 -> thrust redistribution and loss at the
      cracked springline.
Data: cp_cforce_s01/06/11.txt (x y z fx fy fz nx ny nz pbstate).
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import thesis_style as TS
import tunnel_frame as tf

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
CX, CY, CZ = 1298.85, 885.0, 1747.5  # ring centre verified from xsec_G4 (07-10)
STG = {1: ("s1  W-110 (dry)", "01"), 6: ("s6  W-10 (wet)", "06"),
       11: ("s11  W-110 (dry2)", "11")}

def load(tag):
    d = pd.read_csv(HERE / f"cp_cforce_s{tag}.txt", sep=r"\s+").to_numpy()
    return d

D = {k: load(t) for k, (_, t) in STG.items()}
for k, d in D.items():
    print(f"s{k}: contacts={len(d):,}  bonded={(d[:,9]==3).sum():,}")

# ---------- (a-c) ring force chains ----------
fig = plt.figure(figsize=(30, 9.4))
gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1, 1.35], wspace=0.18)
axr = [fig.add_subplot(gs[i]) for i in range(3)]
axp = fig.add_subplot(gs[3])

fmax = None
for ax, k in zip(axr, (1, 6, 11)):
    d = D[k]
    m = (np.abs(d[:, 1] - CY) < 0.6) & (d[:, 9] == 3)
    p = d[m]
    f = np.linalg.norm(p[:, 3:6], axis=1) / 1e3          # kN
    if fmax is None:
        fmax = np.percentile(f, 99)
    L = 0.22
    seg = np.stack([p[:, [0, 2]] - p[:, [6, 8]] * L / 2,
                    p[:, [0, 2]] + p[:, [6, 8]] * L / 2], axis=1)
    lw = 0.3 + 2.8 * np.clip(f / fmax, 0, 1)
    lc = LineCollection(seg, array=np.clip(f, 0, fmax), cmap="inferno_r",
                        linewidths=lw, clim=(0, fmax))
    ax.add_collection(lc)
    ax.set_xlim(CX - 3.1, CX + 3.1); ax.set_ylim(CZ - 3.2, CZ + 3.2)
    ax.set_aspect("equal")
    ax.set_title(f"({'abc'[[1,6,11].index(k)]}) {STG[k][0]}", loc="left", fontsize=26)
    ax.set_xlabel("x (m)", fontsize=24)
    ax.tick_params(labelsize=20)
axr[0].set_ylabel("z (m)")
cb = fig.colorbar(lc, ax=axr, shrink=0.78, pad=0.012, extend="max")
cb.set_label("Bonded contact force (kN)")

# ---------- (d) hoop thrust N(theta) ----------
TH_BINS = np.arange(-6.8, 6.801, 0.12)
thc = 0.5 * (TH_BINS[1:] + TH_BINS[:-1])
YB = 5.0
for k, c in ((1, "0.25"), (6, "#c0392b"), (11, "#2e6da4")):
    d = D[k]
    m = (np.abs(d[:, 1] - CY) < YB) & (d[:, 9] == 3)
    p = d[m]
    th = tf.station(p[:, 0], p[:, 1], p[:, 2])
    # hoop unit vector in x-z plane at each contact (local centre)
    r = np.stack([p[:, 0] - tf.cx_of(p[:, 1]), p[:, 2] - tf.z0_of(p[:, 1])], axis=1)
    r /= np.maximum(np.linalg.norm(r, axis=1, keepdims=True), 1e-9)
    t_hat = np.stack([r[:, 1], -r[:, 0]], axis=1)         # rotate -90deg
    fh = np.abs(p[:, 3] * t_hat[:, 0] + p[:, 5] * t_hat[:, 1]) / 1e3   # kN
    H, _ = np.histogram(th, bins=TH_BINS, weights=fh)
    lw, ls = (3.4, "-") if k != 11 else (2.2, "--")
    axp.plot(thc, H / (2 * YB), color=c, lw=lw, ls=ls, label=STG[k][0])
axp.set_xlabel("Position along lining perimeter")
axp.set_ylabel("Hoop-projected bonded force (kN per m axial)")
axp.set_title("(d) Hoop thrust profile (y = 885$\\pm$5 m)", loc="left", fontsize=23)
tp_, tl_ = tf.ticks()
axp.set_xticks(tp_)
axp.set_xticklabels(tl_, fontsize=20)
axp.axvline(tf.QUART, color="0.7", ls=":", lw=1.5)
axp.axvline(-tf.QUART, color="0.7", ls=":", lw=1.5)
axp.annotate("L-shoulder peak $\\approx$1,030 kN/m\n(s6 $\\approx$ s11, locked in)",
             xy=(-2.06, 1030), xytext=(-5.5, 1180), fontsize=18, color="#7a1d12",
             arrowprops=dict(arrowstyle="->", color="#7a1d12", lw=1.8))
axp.annotate("anchor reaction\n(boundary artifact)",
             xy=(6.58, 1500), xytext=(2.6, 1420), fontsize=18, color="0.35",
             arrowprops=dict(arrowstyle="->", color="0.35", lw=1.8))
axp.legend(fontsize=22, loc="center left")
fig.suptitle("Lining internal forces: bonded contact-force network and hoop thrust "
             "through the water cycle", y=1.01)
fig.savefig(OUT / "圖5-17_襯砌內力分布.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-17")
