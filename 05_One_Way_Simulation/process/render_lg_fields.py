#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
render_lg_fields.py -- LARGE-model field figures from lg_geom.f3grid + lg_zf/gf_s* dumps.
  圖5-06 水壓分布 (s1 dry vs s6 wet, section y=885, Blues + water-table trace)
  圖5-07 變形方向 (s11 cumulative: plan-view terrain quiver + section quiver)
  圖5-08 塑性區與依時變形門檻演化 (5 stages, IJRMMS image20 3-class colors:
         elastic pale-yellow / viscoelastic blue (threshold ON) / yielding red,
         per-stage water line, active-zone count annotation)
All matplotlib-native (real axes, journal grade).
"""
from pathlib import Path
import numpy as np
import pyvista as pv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import f3grid_io
import thesis_style as TS

TS.apply()
pv.OFF_SCREEN = True
HERE = Path(__file__).parent
OUT = TS.RESULT
STL = HERE.parent / "input"
TUN = (1297.0, 885.0, 1747.5)
STAGES = [1, 4, 6, 9, 11]
SWATER = {1: "W-110", 4: "W-50", 6: "W-10", 9: "W-50", 11: "W-110"}
SPHASE = {1: "dry (initial)", 4: "rising", 6: "wet (peak)", 9: "falling", 11: "dry (final)"}

grid = f3grid_io.to_unstructured(HERE / "lg_geom.f3grid")
GIDS = f3grid_io.gid_order_of(HERE / "lg_geom.f3grid")
smb = f3grid_io.to_unstructured(HERE / "sm_geom.f3grid").bounds

# ---- section triangulation (once) with per-triangle parent-cell mapping ----
def make_section():
    g = grid.copy()
    g.cell_data["cid"] = np.arange(g.n_cells)
    sec = g.slice(normal="y", origin=TUN).triangulate()
    pts = sec.points
    f = sec.faces.reshape(-1, 4)[:, 1:]
    cid = sec.cell_data["cid"]
    return pts, f, cid

PTS, F, CID = make_section()
POLY = PTS[F][:, :, [0, 2]]                     # (ntri, 3, 2) in x-z

def zone_field(stage):
    d = np.loadtxt(HERE / f"lg_zf_s{stage:02d}.txt", skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    rows = id2row[grid.cell_data["zid"]]
    return d[rows]                              # per-cell [id state pp visc]

def water_xz(name):
    w = pv.read(str(STL / f"{name}.stl"))
    tr = w.slice(normal="y", origin=TUN)
    p = tr.points; o = np.argsort(p[:, 0])
    x, z = p[o, 0], p[o, 2]
    m = (x >= 0) & (x <= 2000)
    return x[m], z[m]

def draw_frame(ax, zlim=(800, 2250)):
    ax.add_patch(plt.Rectangle((smb[0], smb[4]), smb[1]-smb[0], smb[5]-smb[4],
                 fc="none", ec="#e0231c", lw=2.0, ls="--", zorder=7))
    ax.set_xlim(0, 2000); ax.set_ylim(*zlim); ax.set_aspect("equal")

# ================= 圖5-08 states x 5 stages =================
def fig_states():
    fig, axs = plt.subplots(1, 5, figsize=(34, 5.0), sharey=True,
                            gridspec_kw=dict(left=0.045, right=0.995,
                                             top=0.70, bottom=0.26, wspace=0.08))
    for ax, s in zip(axs, STAGES):
        d = zone_field(s)
        state, visc = d[CID, 1].astype(np.int64), d[CID, 3]
        active = (visc > 0) & (visc < 1e50)
        ynow = (state & 3) > 0
        cls = np.zeros(len(CID), np.int8)       # 0 elastic
        cls[active] = 1                          # viscoelastic (threshold ON)
        cls[ynow] = 2                            # yielding
        cols = np.array([TS.C_ELASTIC, TS.C_VISCO, TS.C_PLASTIC])[cls]
        ax.add_collection(PolyCollection(POLY, facecolor=cols, edgecolor="#88888822",
                                         linewidth=0.15))
        wx, wz = water_xz(SWATER[s])
        ax.plot(wx, wz, color="#1f6fc4", lw=2.6, zorder=6)
        draw_frame(ax, zlim=(1350, 2050))
        # quantitative anchor: threshold-active count over the whole model
        dall = np.loadtxt(HERE / f"lg_zf_s{s:02d}.txt", skiprows=1, usecols=3)
        nact = int(((dall > 0) & (dall < 1e50)).sum())
        ttl = f"s{s}  {SWATER[s]}\n{SPHASE[s]}"
        if s == 1:
            ttl = f"s{s}  {SWATER[s]}\ndry (initial transient)"
        ax.set_title(ttl, fontsize=26)
        ax.text(0.03, 0.05, f"active = {nact:,}", transform=ax.transAxes,
                fontsize=23, bbox=dict(fc="white", ec="0.3", boxstyle="round,pad=0.25"))
        ax.set_xlabel("x (m)", fontsize=24)
        ax.tick_params(labelsize=20)
    axs[0].set_ylabel("Elevation z (m)", fontsize=24)
    handles = [Patch(fc=TS.C_ELASTIC, ec="0.3", label="Elastic (threshold OFF)"),
               Patch(fc=TS.C_VISCO, ec="0.3", label="Viscoelastic (threshold ON)"),
               Patch(fc=TS.C_PLASTIC, ec="0.3", label="Yielding (plastic, now)"),
               Line2D([0], [0], color="#1f6fc4", lw=4, label="Water table (stage)"),
               Line2D([0], [0], color="#e0231c", lw=3, ls="--", label="Tunnel-scale box")]
    fig.legend(handles=handles, loc="lower center", ncol=5, fontsize=25,
               bbox_to_anchor=(0.5, -0.10))
    fig.suptitle("Slope-scale model: time-dependent threshold activation and yielding "
                 "through the water-level cycle (section y = 885 m)", y=0.93)
    fig.savefig(OUT / "圖5-08_邊坡尺度塑性區與門檻演化.png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print("saved 圖5-08")

# ================= 圖5-06 pore pressure s1 vs s6 + Delta =================
def fig_pp():
    fig, axs = plt.subplots(1, 3, figsize=(31, 7.6), sharey=True)
    pp1 = zone_field(1)[CID, 2] / 1e6
    pp6 = zone_field(6)[CID, 2] / 1e6
    vmax = np.percentile(pp6[pp6 > 0], 99)
    for ax, s, pp in zip(axs[:2], (1, 6), (pp1, pp6)):
        pc = PolyCollection(POLY, array=np.clip(pp, 0, None), cmap="Blues",
                            edgecolor="none", clim=(0, vmax))
        ax.add_collection(pc)
        wx, wz = water_xz(SWATER[s])
        ax.plot(wx, wz, color="#0b3d66", lw=3.0, zorder=6,
                label=f"water table {SWATER[s]}")
        draw_frame(ax)
        ax.set_title(f"({'ab'[s==6]}) s{s}  {SWATER[s]}  {SPHASE[s]}", loc="left")
        ax.set_xlabel("x (m)")
        ax.legend(loc="upper left", fontsize=18)
    cb = fig.colorbar(pc, ax=axs[:2], shrink=0.8, pad=0.012, extend="max")
    cb.set_label("Pore pressure (MPa)")
    # ---- (c) Delta pp: the effective-stress unloading band swept by the water swing ----
    ax = axs[2]
    dpp = pp6 - pp1
    pc2 = PolyCollection(POLY, array=dpp, cmap="Reds", edgecolor="none",
                         clim=(0, 1.0))
    ax.add_collection(pc2)
    for nm, c in (("W-110", "#9ecbe8"), ("W-10", "#0b3d66")):
        wx, wz = water_xz(nm)
        ax.plot(wx, wz, color=c, lw=2.6, zorder=6, label=f"water table {nm}")
    draw_frame(ax)
    # white box for visibility on the red field
    ax.add_patch(plt.Rectangle((smb[0], smb[4]), smb[1]-smb[0], smb[5]-smb[4],
                 fc="none", ec="white", lw=2.6, ls="--", zorder=8))
    ax.set_title(r"(c) $\Delta$pp = s6 $-$ s1 (uniform +0.98 MPa below W-110)",
                 loc="left", fontsize=21)
    ax.set_xlabel("x (m)")
    ax.legend(loc="upper left", fontsize=18)
    cb2 = fig.colorbar(pc2, ax=ax, shrink=0.8, pad=0.02)
    cb2.set_label(r"$\Delta$ pore pressure (MPa)")
    axs[0].set_ylabel("Elevation z (m)")
    fig.suptitle("Slope-scale pore pressure: dry vs wet and the swing band at the tunnel "
                 "horizon (section y = 885 m)", y=1.02)
    fig.savefig(OUT / "圖5-06_邊坡尺度水壓分布.png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print("saved 圖5-06  dpp range %.2f..%.2f MPa" % (dpp.min(), dpp.max()))

# ================= 圖5-07 displacement s11 =================
def gp_disp(stage):
    d = np.loadtxt(HERE / f"lg_gf_s{stage:02d}.txt", skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    rows = id2row[GIDS]
    return d[rows, 1:4]

def fig_disp():
    U = gp_disp(11)
    P = grid.points
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(24, 9.5))
    # ---- plan view: terrain gps (max z per xy-bin) ----
    bs = 50.0
    ix = np.floor(P[:, 0] / bs).astype(int); iy = np.floor(P[:, 1] / bs).astype(int)
    key = ix * 10000 + iy
    order = np.argsort(P[:, 2])                  # ascending z; last wins = topmost
    top = {}
    for i in order:
        top[key[i]] = i
    ti = np.array(list(top.values()))
    umag = np.linalg.norm(U[ti, :2], axis=1) * 1000
    q = a1.quiver(P[ti, 0], P[ti, 1], U[ti, 0], U[ti, 1], umag,
                  cmap="YlOrRd", angles="xy", scale_units="xy",
                  scale=np.percentile(umag, 95) / 1000 / 55, width=0.0035,
                  clim=(0, np.percentile(umag, 98)))
    a1.add_patch(plt.Rectangle((smb[0], smb[2]), smb[1]-smb[0], smb[3]-smb[2],
                 fc="none", ec="#e0231c", lw=2.4, ls="--"))
    a1.plot([1297], [885], "o", ms=8, color="#e0231c")
    a1.set_xlim(0, 2000); a1.set_ylim(-100, 2000); a1.set_aspect("equal")
    a1.set_xlabel("x (m)"); a1.set_ylabel("y (m)")
    a1.set_title("(a) Plan view: terrain displacement (s11 cumulative)")
    cb1 = fig.colorbar(q, ax=a1, shrink=0.8, pad=0.02)
    cb1.set_label("|u| horizontal (mm)")
    # ---- section view (decimated: one arrow per 35 m cell to avoid clutter) ----
    m = np.where(np.abs(P[:, 1] - TUN[1]) < 25)[0]
    cell = (np.floor(P[m, 0] / 35).astype(int) * 1000
            + np.floor(P[m, 2] / 35).astype(int))
    _, keep = np.unique(cell, return_index=True)
    m = m[keep]
    umag2 = np.linalg.norm(U[m][:, [0, 2]], axis=1) * 1000
    q2 = a2.quiver(P[m, 0], P[m, 2], U[m, 0], U[m, 2], umag2,
                   cmap="YlOrRd", angles="xy", scale_units="xy",
                   scale=np.percentile(umag2, 95) / 1000 / 55, width=0.0042,
                   clim=(0, np.percentile(umag2, 98)))
    a2.add_patch(plt.Rectangle((smb[0], smb[4]), smb[1]-smb[0], smb[5]-smb[4],
                 fc="none", ec="#e0231c", lw=2.4, ls="--"))
    a2.set_xlim(0, 2000); a2.set_ylim(1300, 2150); a2.set_aspect("equal")
    a2.set_xlabel("x (m)"); a2.set_ylabel("Elevation z (m)")
    a2.set_title("(b) Section y = 885 m: displacement vectors")
    cb2 = fig.colorbar(q2, ax=a2, shrink=0.8, pad=0.02)
    cb2.set_label("|u| in-plane (mm)")
    fig.suptitle("Slope-scale cumulative displacement after the full water cycle (s11)",
                 y=1.0)
    fig.savefig(OUT / "圖5-07_邊坡尺度變形方向.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print("saved 圖5-07  |u|max_plan=%.1fmm section=%.1fmm" % (umag.max(), umag2.max()))

fig_states()
fig_pp()
fig_disp()
