#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_cp_cracks.py -- 圖5-19 襯砌裂縫發展與分類三合一（極點 1298.85 已修正）
(a) developed-surface crack TRACE line art at s11 (field-survey style): red circumferential /
    blue oblique / green longitudinal lines over a pale break-density underlay
(b) y=885 cross-section: ring + classified breaks (arc down the right leg = circumferential)
(c) crack length by class vs stage: circumferential grows at wet, others negligible.
Method = crack_classify three-track (single source of truth), lines built per class.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import DBSCAN
import crack_classify as cc
import tunnel_frame as tf
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
CX, CZ = cc.CX, cc.CZ

def build_lines(P, typ, ST, R):
    """per-class polylines in developed coords (station m, y). returns
    {cls: [Nx2 arrays]}, and per-class total length."""
    U = ST
    Y = P[:, 1]
    lines = {0: [], 1: [], 2: []}
    tot = {0: 0.0, 1: 0.0, 2: 0.0}
    # circumferential: per 1 m slab, cluster in XZ, order by theta
    for y0 in np.arange(cc.YMIN, cc.YMAX, cc.YSTEP):
        idx = np.where((typ == 0) & (Y >= y0) & (Y < y0 + cc.YSTEP))[0]
        if len(idx) < cc.MIN_RING:
            continue
        lab = DBSCAN(eps=cc.EPS_RING, min_samples=cc.MIN_RING).fit_predict(P[idx][:, [0, 2]])
        for L in set(lab) - {-1}:
            sub = idx[lab == L]
            o = np.argsort(ST[sub])
            th, yy = ST[sub][o], Y[sub][o]
            nb = max(2, int((th[-1] - th[0]) / 0.09))
            eb = np.linspace(th[0], th[-1], nb + 1)
            pts = []
            for i in range(nb):
                m = (th >= eb[i]) & (th <= eb[i + 1])
                if m.any():
                    pts.append([th[m].mean(), yy[m].mean()])
            if len(pts) >= 2:
                lines[0].append(np.array(pts))
                tot[0] += th[-1] - th[0]
    # oblique / longitudinal: cluster in (U, y), PCA-ordered centerline
    for t in (1, 2):
        sel = np.where(typ == t)[0]
        if len(sel) < cc.MIN_DIR:
            continue
        D = np.column_stack([U[sel], Y[sel]])
        lab = DBSCAN(eps=cc.EPS_DIR, min_samples=cc.MIN_DIR).fit_predict(D)
        for L in set(lab) - {-1}:
            sub = sel[lab == L]
            d = np.column_stack([U[sub], Y[sub]])
            ax_ = np.linalg.svd(d - d.mean(0), full_matrices=False)[2][0]
            proj = (d - d.mean(0)) @ ax_
            o = np.argsort(proj)
            length = proj.max() - proj.min()
            nb = max(2, int(length / 0.4))
            eb = np.linspace(proj[o][0], proj[o][-1], nb + 1)
            pts = []
            for i in range(nb):
                m = (proj >= eb[i]) & (proj <= eb[i + 1])
                if m.any():
                    pts.append([ST[sub][m].mean(), Y[sub][m].mean()])
            if len(pts) >= 2:
                lines[t].append(np.array(pts))
                tot[t] += length
    return lines, tot

# ---- s11 full classification ----
P, AGE = cc.load_breaks(11)
mband = (P[:, 1] > 862.0) & (P[:, 1] < 908.0)   # trim 2 m driven-end rings (boundary effect)
P, AGE = P[mband], AGE[mband]
typ, TH, R = cc.classify_breaks(P)
LINES, TOT = build_lines(P, typ, TH, R)
print("s11 lengths: circ=%.0f m  obl=%.0f m  long=%.0f m" % (TOT[0], TOT[1], TOT[2]))

fig = plt.figure(figsize=(30, 10))
gs = fig.add_gridspec(1, 3, width_ratios=[1.65, 0.85, 1.0], wspace=0.2)
axA = fig.add_subplot(gs[0]); axB = fig.add_subplot(gs[1]); axC = fig.add_subplot(gs[2])

# (a) developed line art
H, xe, ye = np.histogram2d(TH, P[:, 1], bins=[np.arange(-6.8, 6.81, 0.1),
                                              np.arange(860, 910.1, 1)])
axA.pcolormesh(xe, ye, np.clip(H.T, 0, np.percentile(H[H > 0], 90)), cmap="Greys",
               alpha=0.35, shading="flat")
for t, lw, z in ((0, 2.4, 5), (1, 3.0, 6), (2, 3.0, 6)):
    for seg in LINES[t]:
        axA.plot(seg[:, 0], seg[:, 1], color=cc.TYPE_COL[t], lw=lw, zorder=z,
                 solid_capstyle="round")
for ylo, yhi in ((862, 865.5), (904.5, 908)):
    axA.axhspan(ylo, yhi, color="0.75", alpha=0.18, zorder=1, hatch="//")
# anchored feet band (v6 grade-following: z <= rim(y)+0.41, rim = 1743.97+0.0372(y-860));
# tracks the grade, so it maps to a constant-width strip on the developed lining
yb = np.linspace(862, 908, 120)
z_top = 1743.97 + 0.0372 * (yb - 860) + 0.41
s_anc = np.clip(tf.QUART + (tf.z0_of(yb) - z_top), None, tf.SFOOT)
for sgn in (1, -1):
    axA.fill_betweenx(yb, sgn * s_anc, sgn * tf.SFOOT, color="0.55", alpha=0.25,
                      hatch="xx", lw=0, zorder=2)
axA.text(6.47, 885.0, "anchored (unbreakable)", fontsize=13, color="0.25",
         rotation=90, va="center", ha="center", style="italic",
         bbox=dict(fc="white", alpha=0.7, lw=0, pad=1.2))
axA.text(-6.6, 906.2, "end-affected", fontsize=15, color="0.35", style="italic",
         bbox=dict(fc="white", alpha=0.7, lw=0, pad=1.2))
axA.text(2.3, 863.2, "end-affected", fontsize=15, color="0.35", style="italic",
         bbox=dict(fc="white", alpha=0.7, lw=0, pad=1.2))
axA.axvline(0, color="0.4", ls="--", lw=1.2)
axA.axvline(tf.QUART, color="0.55", ls=":", lw=1.1)
axA.axvline(-tf.QUART, color="0.55", ls=":", lw=1.1)
axA.set_xlim(-6.9, 6.9); axA.set_ylim(862, 908)
tp_, tl_ = tf.ticks()
axA.set_xticks(tp_)
axA.set_xticklabels(tl_, fontsize=21)
axA.set_ylabel("y (m)")
axA.set_title("(a) Crack traces on the developed lining (s11)", loc="left", fontsize=23)
handles = [Line2D([0], [0], color=cc.TYPE_COL[0], lw=4,
                  label=f"circumferential ({TOT[0]:.0f} m)"),
           Line2D([0], [0], color=cc.TYPE_COL[1], lw=4, label=f"oblique ({TOT[1]:.0f} m)"),
           Line2D([0], [0], color=cc.TYPE_COL[2], lw=4,
                  label=f"longitudinal ({TOT[2]:.0f} m)")]
axA.legend(handles=handles, loc="lower left", fontsize=17, framealpha=0.95)

# (b) cross-section
xs = np.loadtxt(HERE.parent.parent / "04_InitialBalance" / "process" / "couple_solve" /
                "xsec_G4_y885.txt", skiprows=1, ndmin=2)
axB.scatter(xs[:, 0], xs[:, 1], s=4, c="0.82", lw=0)
sl = np.abs(P[:, 1] - 885.0) < 0.5
for t in (0, 2, 1):
    m = sl & (typ == t)
    if m.any():
        axB.scatter(P[m, 0], P[m, 2], s=12, c=cc.TYPE_COL[t], lw=0)
axB.set_aspect("equal")
axB.set_xlabel("x (m)"); axB.set_ylabel("z (m)")
axB.set_title(f"(b) Section y = 885 m\n({int(sl.sum())} breaks)", loc="left", fontsize=23)

# (c) evolution: class lengths per stage
ks = list(range(1, 12))
EV = {0: [], 1: [], 2: []}
for k in ks:
    Pk, _ = cc.load_breaks(k)
    Pk = Pk[(Pk[:, 1] > 862.0) & (Pk[:, 1] < 908.0)]
    if len(Pk) < 10:
        for t in (0, 1, 2):
            EV[t].append(0.0)
        continue
    typk, THk, Rk = cc.classify_breaks(Pk)
    _, totk = build_lines(Pk, typk, THk, Rk)
    for t in (0, 1, 2):
        EV[t].append(totk[t])
    print(f"  s{k}: circ={totk[0]:.0f} obl={totk[1]:.0f} long={totk[2]:.0f}")
for t, nm in ((0, "circumferential"), (1, "oblique"), (2, "longitudinal")):
    axC.plot(ks, EV[t], "-o", color=cc.TYPE_COL[t], lw=3.2, ms=9, label=nm)
axC.axvspan(5.5, 6.5, color="#c0392b", alpha=0.10)
axC.text(6, max(EV[0]) * 0.95, "wet", ha="center", fontsize=17, color="#7a1d12")
axCb = axC.twinx()
wx_, wy_ = TS.water_steps()
axCb.plot(wx_, wy_, "b--", lw=2, alpha=0.65)
axCb.set_ylabel("Water level (m)", color="b", fontsize=19)
axCb.tick_params(axis="y", colors="b", labelsize=15); axCb.grid(False)
axC.set_xticks(ks)
axC.set_xlabel("Stage"); axC.set_ylabel("Total crack trace length (m)")
axC.set_title("(c) Crack length by class vs stage", loc="left", fontsize=23)
axC.legend(fontsize=16, loc="center left")
axC.text(0.985, 0.02, "traces re-classified independently per stage;\n"
         "class totals may fluctuate slightly as traces grow",
         transform=axC.transAxes, ha="right", va="bottom", fontsize=13,
         color="0.4", style="italic",
         bbox=dict(fc="white", alpha=0.8, lw=0, pad=1.5))
fig.suptitle("Lining crack development and classification (water-cycle-induced, s1 baseline "
             "excluded; 2 m driven-end bands trimmed)", y=1.01)
fig.savefig(OUT / "圖5-19_襯砌裂縫發展與分類.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-19")
