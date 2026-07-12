#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_cp_deform.py -- 圖5-18 襯砌變形 v3: FULL-ball displacement dumps (cp_balldisp_s01/06/11,
456,162 balls each -- replaces cwall whose cracked right-mid band was unclassified).
Rigid translation removed per stage; ring centre (1298.85, 1747.5) verified.
(a) ring y=885+-1m centreline deformed x400 (theta-binned, FULL coverage)
(b) developed u_r map (inward +) at s11, 3deg x 1.5m bins
(c) regional mean u_r at the 3 checkpoints (grouped bars): wet jump + frozen dry2.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS
import tunnel_frame as tf

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
CX, CY, CZ = 1298.85, 885.0, 1747.5
MAG = 400
STG = {1: "s1 W-110 (dry)", 6: "s6 W-10 (wet)", 11: "s11 W-110 (dry2)"}

def load(k):
    d = pd.read_csv(HERE / f"cp_balldisp_s{k:02d}.txt", sep=r"\s+").to_numpy()
    u = d[:, 4:7].copy()
    drift = u.mean(0)
    u -= drift
    x0 = d[:, 1] - d[:, 4]; y0 = d[:, 2] - d[:, 5]; z0 = d[:, 3] - d[:, 6]
    return x0, y0, z0, u, drift

DATA = {k: load(k) for k in (1, 6, 11)}
print("drift mm:", {k: np.round(v[4]*1000, 2).tolist() for k, v in DATA.items()})

def ring_line(k, ybw=1.0, thbin=2.0):
    x0, y0, z0, u, _ = DATA[k]
    m = np.abs(y0 - CY) < ybw
    th = np.degrees(np.arctan2(x0[m] - CX, z0[m] - CZ))
    bins = np.arange(-180, 180.1, thbin)
    ib = np.digitize(th, bins)
    P0, PD = [], []
    for b in np.unique(ib):
        s = ib == b
        if s.sum() < 5:
            continue
        P0.append([x0[m][s].mean(), z0[m][s].mean()])
        PD.append([(x0[m][s] + MAG * u[m][:, 0][s]).mean(),
                   (z0[m][s] + MAG * u[m][:, 2][s]).mean()])
    P0, PD = np.array(P0), np.array(PD)
    thc = np.degrees(np.arctan2(P0[:, 0] - CX, P0[:, 1] - CZ))
    o = np.argsort(thc)
    return P0[o], PD[o]

fig = plt.figure(figsize=(30, 9.2))
gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.5, 1.1], wspace=0.24)
ax0 = fig.add_subplot(gs[0]); ax1 = fig.add_subplot(gs[1]); ax2 = fig.add_subplot(gs[2])

# (a)
P0, _ = ring_line(1)
ax0.plot(P0[:, 0], P0[:, 1], color="0.65", lw=2.8, label="original")
for k, c, ls in ((6, "#c0392b", "-"), (11, "#2e6da4", "--")):
    _, PD = ring_line(k)
    lw, dashes = (3.4, None) if k == 6 else (2.2, (4, 3))
    ln = ax0.plot(PD[:, 0], PD[:, 1], color=c, lw=lw, ls=ls, label=f"s{k} (u x{MAG})")
    if dashes:
        ln[0].set_dashes(dashes)
ax0.annotate("ring leans west (racking);\ns6 = s11 (frozen)", xy=(1300.4, 1748.9),
             xytext=(1297.15, 1746.9), fontsize=19, color="#7a1d12",
             arrowprops=dict(arrowstyle="->", color="#7a1d12", lw=2.0))
ax0.set_aspect("equal")
ax0.set_xlabel("x (m)"); ax0.set_ylabel("z (m)")
ax0.set_title(f"(a) Ring y = 885 m centreline, deformed x{MAG}", loc="left", fontsize=21)
ax0.legend(fontsize=18, loc="lower center")

# (b)
x0, y0, z0, u, _ = DATA[11]
rx, rz = x0 - tf.cx_of(y0), z0 - tf.z0_of(y0)
rm = np.sqrt(rx**2 + rz**2); rm[rm == 0] = 1e-9
ur = -(u[:, 0] * rx / rm + u[:, 2] * rz / rm) * 1000
th = tf.station(x0, y0, z0)
PHI = np.arange(-6.8, 6.801, 0.15); YF = np.arange(860, 910.001, 1.5)
S, _, _ = np.histogram2d(th, y0, bins=[PHI, YF], weights=ur)
C, _, _ = np.histogram2d(th, y0, bins=[PHI, YF])
M = np.divide(S, C, out=np.full_like(S, np.nan), where=C > 0)
vmax = np.nanpercentile(np.abs(M), 98)
im = ax1.pcolormesh(PHI, YF, M.T, cmap="RdBu_r", vmin=-vmax, vmax=vmax, shading="flat")
ax1.set_facecolor("#e8e8e8")
ax1.axvline(0, color="0.4", ls="--", lw=1.2)
ax1.axvline(tf.QUART, color="0.55", ls=":", lw=1.1)
ax1.axvline(-tf.QUART, color="0.55", ls=":", lw=1.1)
tp_, tl_ = tf.ticks()
ax1.set_xticks(tp_)
ax1.set_xticklabels(tl_, fontsize=20)
ax1.set_ylabel("y (m)")
ax1.set_title("(b) Radial displacement $u_r$ (inward +), s11, all balls",
              loc="left", fontsize=21)
cb = fig.colorbar(im, ax=ax1, shrink=0.85, pad=0.015)
cb.set_label("$u_r$ (mm)")

# (c)
REG = {"Crown": (-30, 30, "#555555"), "R springline": (60, 120, "#c0392b"),
       "L springline": (-120, -60, "#2e6da4")}
W = 0.24
for j, (nm, (lo, hi, c)) in enumerate(REG.items()):
    vals = []
    for k in (1, 6, 11):
        x0k, y0k, z0k, uk, _ = DATA[k]
        rxk, rzk = x0k - tf.cx_of(y0k), z0k - tf.z0_of(y0k)
        rmk = np.sqrt(rxk**2 + rzk**2); rmk[rmk == 0] = 1e-9
        thk = tf.theta_local(x0k, y0k, z0k)
        urk = -(uk[:, 0] * rxk / rmk + uk[:, 2] * rzk / rmk) * 1000
        m = (thk >= lo) & (thk <= hi)
        vals.append(urk[m].mean())
    ax2.bar(np.arange(3) + (j - 1) * W, vals, W, color=c, edgecolor="k", lw=0.8,
            label=nm)
    for i, v in enumerate(vals):
        ax2.text(i + (j - 1) * W, v + (0.006 if v >= 0 else -0.006),
                 f"{v:.2f}", ha="center", fontsize=18,
                 va="bottom" if v >= 0 else "top")
ax2.axhline(0, color="0.3", lw=1.2)
ax2.set_xticks(range(3))
ax2.set_xticklabels([STG[k] for k in (1, 6, 11)], fontsize=20)
ax2.margins(y=0.18)
ax2.set_ylim(bottom=min(ax2.get_ylim()[0], -0.045))
ax2.set_ylabel("Mean $u_r$ (mm, inward +)")
ax2.set_title("(c) Regional mean $u_r$ at checkpoints", loc="left", fontsize=21)
ax2.legend(fontsize=19)
fig.suptitle("Lining ovalization through the water cycle (all 456k balls, rigid drift "
             "removed; f = 0.25 trend-level)", y=1.01)
fig.savefig(OUT / "圖5-18_襯砌變形.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-18 v3  vmax=%.2f mm" % vmax)
