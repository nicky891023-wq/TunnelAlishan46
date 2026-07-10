#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_sm_rays.py -- 圖5-14 隧道周圍徑向有效應力分布 + tau-p 門檻判定.
Data: sm_ray_crown/spring_s01/06.txt (x y z sxx..syz pp per zone in a thin ray corridor).
(a) crown ray (+z):  sigma_r' ~ szz+pp, sigma_theta' ~ sxx+pp  vs height above crown
(b) springline ray (+x): sigma_r' ~ sxx+pp, sigma_theta' ~ szz+pp vs distance from wall
(c) tau-p plot of ray zones vs the reduced MC threshold envelope (lambda=0.6):
    wet stage points migrate LEFT (p' drops at ~constant q) across the threshold line.
Sign: FLAC compression negative -> plot compression positive. Effective = total + pp.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
CX, CZ = 1298.85, 1747.5   # ring centre verified 07-10
R_WALL_C = 2.7    # crown apex z=1750.2 - centre z=1747.5      # approx crown wall radius (m) from ring geometry (z top ~1752.2)
R_WALL_S = 2.35   # right wall x=1301.2 - centre x=1298.85      # approx springline wall radius

def load(ray, s):
    d = np.loadtxt(HERE / f"sm_ray_{ray}2_s{s:02d}.txt", skiprows=1, ndmin=2)
    return d

def profile(ray, s):
    d = load(ray, s)
    x, y, z = d[:, 0], d[:, 1], d[:, 2]
    sxx, syy, szz = d[:, 3], d[:, 4], d[:, 5]
    pp = d[:, 9]
    if ray == "crown":
        r = z - CZ
        sr, st = -(szz + pp) / 1e6, -(sxx + pp) / 1e6      # compression +, MPa, effective
    else:
        r = x - CX
        sr, st = -(sxx + pp) / 1e6, -(szz + pp) / 1e6
    o = np.argsort(r)
    r, sr, st, pp = r[o], sr[o], st[o], pp[o] / 1e6
    # bin-average for a clean curve (0.6 m bins)
    bins = np.arange(r.min(), r.max() + 0.6, 0.6)
    ib = np.digitize(r, bins)
    rb, srb, stb, ppb = [], [], [], []
    for k in np.unique(ib):
        m = ib == k
        if m.sum() >= 2:
            rb.append(r[m].mean()); srb.append(sr[m].mean())
            stb.append(st[m].mean()); ppb.append(pp[m].mean())
    return np.array(rb), np.array(srb), np.array(stb), np.array(ppb)

def taup(ray, s):
    d = load(ray, s)
    sxx, syy, szz = d[:, 3], d[:, 4], d[:, 5]
    sxy, sxz, syz = d[:, 6], d[:, 7], d[:, 8]
    pp = d[:, 9]
    # principal effective stresses (compression +)
    out_p, out_q = [], []
    for i in range(len(d)):
        S = -np.array([[sxx[i], sxy[i], sxz[i]],
                       [sxy[i], syy[i], syz[i]],
                       [sxz[i], syz[i], szz[i]]]) - np.eye(3) * pp[i]
        w = np.linalg.eigvalsh(S)
        s3, s1 = w[0], w[2]           # ascending: s3 min (least compressive)
        out_p.append((s1 + s3) / 2 / 1e6)
        out_q.append((s1 - s3) / 2 / 1e6)
    return np.array(out_p), np.array(out_q)

fig, axs = plt.subplots(1, 3, figsize=(30, 8.6))
COLS = {1: "0.25", 6: "#c0392b"}
LBL = {1: "s1 dry (W-110)", 6: "s6 wet (W-10)"}

for ax, ray, rwall, ttl in ((axs[0], "crown", R_WALL_C,
                             "(a) Crown ray (vertical, above crown)"),
                            (axs[1], "spring", R_WALL_S,
                             "(b) Springline ray (horizontal, right wall)")):
    vis_lo, vis_hi = np.inf, -np.inf
    for s in (1, 6):
        r, sr, st, pp = profile(ray, s)
        dist = r - rwall
        m = dist > 0
        ax.plot(dist[m], st[m], color=COLS[s], lw=3.2,
                label=f"{LBL[s]}  " + r"$\sigma_\theta'$")
        ax.plot(dist[m], sr[m], color=COLS[s], lw=3.2, ls="--",
                label=f"{LBL[s]}  " + r"$\sigma_r'$")
        mv = m & (dist <= 30)          # only what is visible inside xlim
        vis_lo = min(vis_lo, st[mv].min(), sr[mv].min())
        vis_hi = max(vis_hi, st[mv].max(), sr[mv].max())
    ax.set_xlabel("Distance from tunnel wall (m)")
    ax.set_ylabel("Effective stress (MPa, compression +)")
    ax.set_title(ttl, loc="left")
    ax.set_xlim(0, 30)
    rng = vis_hi - vis_lo
    ax.set_ylim(vis_lo - 0.05 * rng, vis_hi + 0.04 * rng)
    loc = "lower left" if ray == "crown" else "lower right"
    ax.legend(fontsize=20, ncol=1, loc=loc, borderaxespad=0.4,
              handlelength=1.6, labelspacing=0.35, borderpad=0.35)

# ---- (c) tau-p vs the REAL layer-4 threshold, with FLAC's own ON flag ----
# layer4 (tunnel host, WET): c=0.10 MPa, phi=30 deg (04/parameter.f3dat L72-73);
# threshold envelope = lambda x MC. Points matched to layer/visc via nearest cell centre.
from scipy.spatial import cKDTree
import f3grid_io
grid = f3grid_io.to_unstructured(HERE / "sm_geom.f3grid")
CEN = grid.cell_centers().points
tree = cKDTree(CEN)

def zone_lookup(stage, xyz):
    d = np.loadtxt(HERE / f"sm_zf_s{stage:02d}.txt", skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    _, ci = tree.query(xyz, k=1)
    rows = id2row[grid.cell_data["zid"][ci]]
    lay = grid.cell_data["layer"][ci]
    visc = d[rows, 3]
    return lay, ((visc > 0) & (visc < 1e50))

ax = axs[2]
lam = 0.6
c0, phi0 = 0.10, np.radians(30.0)            # layer-4 MC (MPa, rad)
means = {}
for s in (1, 6):
    d = load("spring", s)
    lay, _ = zone_lookup(s, d[:, :3])
    m4 = lay == 4
    p1, q1 = taup("spring", s)
    ax.scatter(p1[m4], q1[m4], s=10, c=COLS[s], alpha=0.22, lw=0,
               label=f"{LBL[s]} (layer 4)")
    means[s] = (p1[m4].mean(), q1[m4].mean())
ax.annotate("wet cloud shifts left:\nstates occupy the\nthreshold band",
            xy=(0.55, 0.34), xytext=(1.52, 0.02), fontsize=21, color="#7a1d12",
            arrowprops=dict(arrowstyle="->", color="#7a1d12", lw=2.2))
ax.annotate("cloud capped by\nMC envelope (yield)",
            xy=(1.05, 0.62), xytext=(0.08, 0.74), fontsize=21, color="0.2",
            arrowprops=dict(arrowstyle="->", color="0.2", lw=2.2))
pgrid = np.linspace(0, 2.2, 50)
q_mc = pgrid * np.sin(phi0) + c0 * np.cos(phi0)
ax.plot(pgrid, q_mc, color="0.15", lw=3, label="MC envelope (layer 4)")
ax.plot(pgrid, lam * q_mc, color="#0b5394", lw=3, ls="--",
        label=r"threshold $\lambda\cdot$MC, $\lambda$=0.6")
ax.set_xlabel(r"$p'=(\sigma_1'+\sigma_3')/2$ (MPa)")
ax.set_ylabel(r"$q=(\sigma_1'-\sigma_3')/2$ (MPa)")
ax.set_title("(c) Stress state vs threshold (springline ray, layer 4)", loc="left")
ax.set_xlim(-0.05, 2.28)
ax.set_ylim(-0.04, 1.26)
leg = ax.legend(fontsize=19, loc="upper left", borderaxespad=0.4,
                handlelength=1.6, labelspacing=0.35, borderpad=0.35)
for lh in leg.legend_handles:          # scatter handles inherit alpha=0.22 -> opaque
    lh.set_alpha(1.0)
fig.subplots_adjust(wspace=0.17)
fig.suptitle("Near-field effective-stress profiles and threshold check: "
             "dry vs wet stage (y = 885 m)", y=1.01)
fig.savefig(OUT / "圖5-14_隧道周圍有效應力分布與門檻判定.png", dpi=190,
            bbox_inches="tight")
plt.close(fig)
print("saved 圖5-14")
