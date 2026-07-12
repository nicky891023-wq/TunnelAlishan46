#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_sm_fields.py -- SMALL-model field figures (tunnel zoom, section y=885):
  圖5-11 隧道近場水壓洩降 (s1 dry vs s6 wet + Δ): drawdown funnel from the k x100 annulus
  圖5-12 隧道圍岩塑性區與門檻演化 (5 stages, 3-class IJRMMS colors, tunnel zoom)
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import f3grid_io
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT
TUN = (1297.0, 885.0, 1747.5)
STAGES = [1, 4, 6, 9, 11]
SWATER = {1: "W-110", 4: "W-50", 6: "W-10", 9: "W-50", 11: "W-110"}
SPHASE = {1: "dry (initial)", 4: "rising", 6: "wet (peak)", 9: "falling", 11: "dry (final)"}
XL = (1255, 1345); ZL = (1702, 1792)   # inset 5 m from box faces: exclude driven-boundary skin

grid = f3grid_io.to_unstructured(HERE / "sm_geom.f3grid")
g2 = grid.copy(); g2.cell_data["cid"] = np.arange(g2.n_cells)
sec = g2.slice(normal="y", origin=TUN).triangulate()
pts = sec.points; f = sec.faces.reshape(-1, 4)[:, 1:]
CID = sec.cell_data["cid"]
POLY = pts[f][:, :, [0, 2]]
# keep only zoom-window triangles (fast draw)
cen = POLY.mean(1)
INW = ((cen[:, 0] > XL[0] - 5) & (cen[:, 0] < XL[1] + 5) &
       (cen[:, 1] > ZL[0] - 5) & (cen[:, 1] < ZL[1] + 5))
POLYW = POLY[INW]; CIDW = CID[INW]

def zone_field(stage):
    d = np.loadtxt(HERE / f"sm_zf_s{stage:02d}.txt", skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    return d, id2row

def cellvals(stage):
    d, id2row = zone_field(stage)
    rows = id2row[grid.cell_data["zid"][CIDW]]
    return d[rows]           # [id state pp visc] per zoom triangle

def shell_outline(ax, lw=1.6):
    sh = np.loadtxt(HERE / "sm_shells.txt", skiprows=1)
    tris = sh[:, 1:10].reshape(-1, 3, 3)
    m = np.abs(tris[:, :, 1].mean(1) - TUN[1]) < 0.6
    for t in tris[m]:
        ax.plot(t[[0, 1, 2, 0], 0], t[[0, 1, 2, 0], 2], color="#1a1a1a", lw=lw)

def setax(ax):
    ax.set_xlim(*XL); ax.set_ylim(*ZL); ax.set_aspect("equal")
    ax.set_xlabel("x (m)")

# ================= 圖5-11 near-field pore pressure =================
def fig_pp():
    fig, axs = plt.subplots(1, 3, figsize=(24.5, 8.6), sharey=True)
    fig.subplots_adjust(left=0.055, right=0.99, top=0.90, bottom=0.095, wspace=0.06)
    v1 = cellvals(1); v6 = cellvals(6)
    pp1 = v1[:, 2] / 1e3; pp6 = v6[:, 2] / 1e3      # kPa
    vmax = np.percentile(pp6, 99)
    for ax, s, pp in zip(axs[:2], (1, 6), (pp1, pp6)):
        pc = PolyCollection(POLYW, array=np.clip(pp, 0, None), cmap="Blues",
                            edgecolor="#88888826", linewidth=0.15, clim=(0, vmax))
        ax.add_collection(pc)
        shell_outline(ax)
        setax(ax)
        ax.set_title(f"({'ab'[s==6]}) s{s}  {SWATER[s]}  {SPHASE[s]}", loc="left")
    cb = fig.colorbar(pc, ax=axs[:2], shrink=0.82, fraction=0.035, pad=0.012,
                      extend="max")
    cb.set_label("Pore pressure (kPa)")
    axs[1].annotate("drawdown halo\n(drained wall, pp$\\approx$0)",
                    xy=(TUN[0] + 5.5, TUN[2] + 4.5), xytext=(XL[0] + 4, ZL[1] - 17),
                    fontsize=22, color="#0b3d66",
                    arrowprops=dict(arrowstyle="->", color="#0b3d66", lw=2.2))
    ax = axs[2]
    dpp = (pp6 - pp1)
    pc2 = PolyCollection(POLYW, array=dpp, cmap="Reds", edgecolor="#88888826",
                         linewidth=0.15, clim=(0, max(np.percentile(dpp, 99), 1)))
    ax.add_collection(pc2)
    shell_outline(ax)
    setax(ax)
    ax.set_title(r"(c) $\Delta$pp = s6 $-$ s1", loc="left")
    cb2 = fig.colorbar(pc2, ax=ax, shrink=0.82, fraction=0.06, pad=0.015)
    cb2.set_label(r"$\Delta$ pore pressure (kPa)")
    ax.annotate("wall pinned at 0:\nsteep gradient = seepage force\ntoward tunnel",
                xy=(TUN[0] - 5.5, TUN[2] - 3), xytext=(XL[0] + 3, ZL[0] + 9),
                fontsize=21, color="#5c0f0f",
                arrowprops=dict(arrowstyle="->", color="#5c0f0f", lw=2.2),
                bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.2))
    axs[0].set_ylabel("Elevation z (m)")
    fig.suptitle("Tunnel near-field pore pressure: drawdown toward the drained tunnel "
                 "wall (section y = 885 m)", y=0.995)
    fig.savefig(OUT / "圖5-11_隧道近場水壓洩降.png", dpi=190, bbox_inches="tight")
    plt.close(fig)
    print("saved 圖5-11  pp6 max=%.0f kPa  dpp max=%.0f kPa" % (pp6.max(), dpp.max()))

# ================= 圖5-12 states x 5 stages =================
def fig_states():
    fig, axs = plt.subplots(1, 5, figsize=(36, 8.4), sharey=True)
    fig.subplots_adjust(left=0.045, right=0.995, top=0.87, bottom=0.13, wspace=0.07)
    for ax, s in zip(axs, STAGES):
        v = cellvals(s)
        state = v[:, 1].astype(np.int64); visc = v[:, 3]
        active = (visc > 0) & (visc < 1e50)
        ynow = (state & 3) > 0
        cls = np.zeros(len(v), np.int8)
        cls[active] = 1
        cls[ynow] = 2
        cols = np.array([TS.C_ELASTIC, TS.C_VISCO, TS.C_PLASTIC])[cls]
        ax.add_collection(PolyCollection(POLYW, facecolor=cols,
                                         edgecolor="#88888822", linewidth=0.12))
        shell_outline(ax, lw=1.2)
        setax(ax)
        ttl = f"s{s}  {SWATER[s]}\n{SPHASE[s]}"
        if s == 1:
            ttl = f"s{s}  {SWATER[s]}\ndry (initial)"
        ax.set_title(ttl, fontsize=26)
        # counts within the zoom window
        na = int(active.sum()); ny = int(ynow.sum())
        ax.text(0.03, 0.03, f"ON={na:,}\nyield={ny:,}", transform=ax.transAxes,
                fontsize=21, bbox=dict(fc="white", ec="0.3", boxstyle="round,pad=0.25"))
        ax.tick_params(labelsize=22)
        if s == 6:
            ax.annotate("weak-layer band\n(threshold ON)", xy=(1320, 1755),
                        xytext=(1304, 1780), fontsize=21, color="#0b5394",
                        arrowprops=dict(arrowstyle="->", color="#0b5394", lw=2.0),
                        bbox=dict(fc="white", ec="none", alpha=0.7, pad=0.2))
    axs[0].set_ylabel("Elevation z (m)")
    handles = [Patch(fc=TS.C_ELASTIC, ec="0.3", label="Elastic (threshold OFF)"),
               Patch(fc=TS.C_VISCO, ec="0.3", label="Viscoelastic (threshold ON)"),
               Patch(fc=TS.C_PLASTIC, ec="0.3", label="Yielding (plastic, now)"),
               Line2D([0], [0], color="#1a1a1a", lw=3, label="Lining")]
    fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=26,
               bbox_to_anchor=(0.5, -0.075))
    fig.suptitle("Tunnel-scale model: threshold activation and yielding around the tunnel "
                 "through the water cycle (section y = 885 m)", y=1.005)
    fig.savefig(OUT / "圖5-12_隧道圍岩塑性區與門檻演化.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("saved 圖5-12")

fig_pp()
fig_states()
