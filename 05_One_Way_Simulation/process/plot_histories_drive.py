#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_histories_drive.py -- 圖5-9 邊坡變形歷線 + 圖5-10 映射驅動場 + 圖5-13 收斂曲線(改號)
5-9(a): full 11-stage |u|,ux history at the anomaly point (lg_disp band, nearest to
        (1298,893,1747)) with water level -- dry-flat / wet-accelerate signature.
5-9(b): east-west transect comparison at tunnel elevation (lg_gf 5 stages, gps nearest
        x=1300/1000/700 at y=885,z~1747): the closer to the east curve, the more westward.
5-10:  coupled-box boundary drive (cpl_resid_s06): dx,dy,dz panels -> push E->W, S->N.
5-13:  copy small_convergence_history_v2.png under thesis number.
"""
import shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT

# ================= 圖5-9 =================
TARGET = np.array([1298.0, 893.0, 1747.0])

def band_hist():
    # seam-closed series (07-11): s1 = NEW T1=1.0 rerun; s2-11 = original run shifted by
    # (new s1 end - old s1 end) so stage INCREMENTS are exactly the original ones and the
    # old-s1 conditioning transient is excluded from the reported window.
    us = []
    for k in range(1, 12):
        d = np.loadtxt(HERE / f"lg_disp_s{k:02d}.txt", skiprows=1, ndmin=2)
        if k == 1:
            i = np.argmin(np.linalg.norm(d[:, :3] - TARGET, axis=1))
            pt = d[i, :3]
        i = np.argmin(np.linalg.norm(d[:, :3] - pt, axis=1))
        us.append(d[i, 3:6])
    us = np.array(us)
    dold = np.loadtxt(HERE / "_backup_T08run" / "lg_disp_s01.txt", skiprows=1, ndmin=2)
    j = np.argmin(np.linalg.norm(dold[:, :3] - pt, axis=1))
    shift = us[0] - dold[j, 3:6]
    us[1:] += shift
    return pt, us

pt, U = band_hist()
fig, (a1, a2) = plt.subplots(1, 2, figsize=(24, 9))
ks = np.arange(1, 12)
wx = -U[:, 0] * 1000
a1.plot(ks, wx, "-o", color="#c0392b", lw=3.5, ms=10, label="westward $-u_x$")
a1.plot(ks, U[:, 2] * 1000, "-s", color="0.45", lw=3, ms=9, label="vertical $u_z$")
a1.axvspan(5.5, 6.5, color="#c0392b", alpha=0.10)
a1.text(6, wx.max()*0.45, "wet", ha="center", fontsize=22, color="#7a1d12")
a1b = a1.twinx()
wx_, wy_ = TS.water_steps()
a1b.plot(wx_, wy_, "b--", lw=2, alpha=0.7)
a1b.set_ylabel("Water level (m)", color="b", fontsize=24)
a1b.tick_params(axis="y", colors="b", labelsize=20); a1b.grid(False)
a1.set_xticks(ks)
a1.set_xlim(0.4, 11.6)
a1.set_xlabel("Stage"); a1.set_ylabel("Displacement (mm)")
a1.set_title(f"(a) Anomaly-section point ({pt[0]:.0f}, {pt[1]:.0f}, {pt[2]:.0f}):\n"
             "flat when dry, accelerates when wet", loc="left", fontsize=26)
a1.legend(fontsize=21, loc="upper left")

# (b) transect from 5-stage gf dumps
import f3grid_io
grid = f3grid_io.to_unstructured(HERE / "lg_geom.f3grid")
GIDS = f3grid_io.gid_order_of(HERE / "lg_geom.f3grid")
P = grid.points
PTS = {"x = 1300 m (anomaly curve)": np.array([1300., 885., 1747.]),
       "x = 1000 m (mid-slope)": np.array([1000., 885., 1747.]),
       "x = 700 m (west section)": np.array([700., 885., 1747.])}
IDX = {nm: np.argmin(np.linalg.norm(P - q, axis=1)) for nm, q in PTS.items()}
SS = [1, 4, 6, 9, 11]
CU = {}
for s in SS:
    d = np.loadtxt(HERE / f"lg_gf_s{s:02d}.txt", skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    rows = id2row[GIDS]
    CU[s] = d[rows, 1:4]
COLS3 = {"x = 1300 m (anomaly curve)": "#c0392b", "x = 1000 m (mid-slope)": "0.35",
         "x = 700 m (west section)": "#7fb3d5"}
for nm, i in IDX.items():
    # re-zeroed at s1 end (old-s1 conditioning excluded); new-s1 increment ~0 by design
    base = CU[1][i, 0]
    wx = [0.0] + [-(CU[s][i, 0] - base) * 1000 for s in SS if s != 1]
    a2.plot(SS, wx, "-o", color=COLS3[nm], lw=3.2, ms=10, label=nm)
a2.axvspan(5.5, 6.5, color="#c0392b", alpha=0.10)
a2.set_xticks(SS)
a2.set_xlim(0.4, 11.6)
a2.set_xlabel("Stage")
a2.set_ylabel("Westward displacement $-u_x$ (mm)")
a2.set_title("(b) East-west transect at tunnel elevation:\ncloser to the east curve, "
             "larger westward creep", loc="left", fontsize=26)
a2.legend(fontsize=20, loc="upper left", handlelength=1.6, borderaxespad=0.4)
fig.subplots_adjust(wspace=0.30)
fig.suptitle("Slope-scale displacement histories through the water cycle", y=1.02)
fig.savefig(OUT / "圖5-09_邊坡變形歷線.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-09  anomaly -ux s11 = %.1f mm" % wx[-1])

# ================= 圖5-10 drive field =================
d = np.loadtxt(HERE / "lg_disp_s06.txt", skiprows=1, ndmin=2)  # FULL disp (with rigid part): push direction
fig, axs = plt.subplots(1, 3, figsize=(28, 8.6), subplot_kw={"projection": "3d"})
labels = [("dx", 3, "east(+)/west(-)"), ("dy", 4, "north(+)/south(-)"),
          ("dz", 5, "up(+)/down(-)")]
for ax, (nm, c, note) in zip(axs, labels):
    v = d[:, c] * 1000
    vmax = np.percentile(np.abs(v), 98)
    sc = ax.scatter(d[:, 0], d[:, 1], d[:, 2], c=v, cmap="RdBu_r", s=7,
                    vmin=-vmax, vmax=vmax)
    ax.set_title(f"({'abc'[c-3]}) {nm}  [{note}]", fontsize=25, pad=2)
    ax.set_xlabel("x", labelpad=10); ax.set_ylabel("y", labelpad=10)
    ax.set_zlabel("z", labelpad=6)
    ax.tick_params(labelsize=16)
    ax.set_box_aspect((1, 1, 1), zoom=1.12)
    ax.view_init(elev=22, azim=-60)
    cb = fig.colorbar(sc, ax=ax, shrink=0.65, pad=0.08)
    cb.set_label(f"{nm} (mm)", fontsize=21)
    cb.ax.tick_params(labelsize=17)
    mv = v.mean()
    ax.text2D(0.03, 0.96, f"mean = {mv:+.2f} mm", transform=ax.transAxes, fontsize=20,
              bbox=dict(fc="white", ec="0.4", boxstyle="round,pad=0.25"))
fig.suptitle("Slope-scale displacement mapped onto the tunnel-scale box boundary "
             "(s6 wet, full field)", y=0.99)
fig.savefig(OUT / "圖5-10_映射驅動場.png", dpi=180, bbox_inches="tight")
plt.close(fig)
print("saved 圖5-10  mean dx=%.2f dy=%.2f dz=%.2f mm"
      % tuple(d[:, 3:6].mean(0) * 1000))

# ================= 圖5-13 =================
shutil.copy(HERE.parent / "result" / "small_convergence_history_v2.png",
            OUT / "圖5-13_隧道收斂曲線.png")
print("saved 圖5-13 (copy)")
